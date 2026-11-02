"""Utilidades dos scripts da auditoria de ML (externos ao NodeWatch).

Importe este módulo ANTES de numpy/pandas/sklearn: ele fixa o número de
threads das bibliotecas numéricas e põe no ``sys.path`` o NodeWatch e a pasta
do XGBoost instalado à parte. Nada aqui altera o NodeWatch: os scripts leem o
código, os dados e o artefato salvo, e gravam só em ``resultados/`` e na pasta
de trabalho configurada.
"""

from __future__ import annotations

import ctypes
import ctypes.wintypes as wt
import hashlib
import json
import os
import platform
import statistics
import subprocess
import sys
import threading
import time
import tomllib
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
RESULTADOS = RAIZ / "resultados"


def _ler_config() -> tuple[Dict[str, Any], Path]:
    for nome in ("config_auditoria.local.toml", "config_auditoria.exemplo.toml"):
        p = RAIZ / nome
        if p.is_file():
            with p.open("rb") as fh:
                return tomllib.load(fh), p
    raise FileNotFoundError("Crie config_auditoria.local.toml a partir do exemplo.")


CFG, ARQ_CFG = _ler_config()
CAM: Dict[str, Path] = {k: Path(v) for k, v in CFG["caminhos"].items() if v}
THREADS = int(os.environ.get("AUD_THREADS", CFG["execucao"]["threads"]))
SEMENTE = int(CFG["execucao"]["semente"])
for _var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_var, str(THREADS))
sys.path.insert(0, str(CAM["nodewatch"]))
if "pacotes_extras" in CAM and CAM["pacotes_extras"].is_dir():
    sys.path.append(str(CAM["pacotes_extras"]))
TRABALHO = CAM["trabalho"]
TRABALHO.mkdir(parents=True, exist_ok=True)
RESULTADOS.mkdir(parents=True, exist_ok=True)


def config_nodewatch() -> Dict[str, Any]:
    """Configuração do NodeWatch com os caminhos de dados desta auditoria."""
    from src.ml.config import carregar_config
    cfg = carregar_config()
    cfg["rede"]["arquivos"] = [str(CAM["rede"])]
    cfg["financeiro"]["transacoes"] = str(CAM["transacoes"])
    cfg["financeiro"]["contas"] = str(CAM.get("contas", ""))
    cfg["financeiro"]["padroes"] = str(CAM.get("padroes", ""))
    cfg["geral"]["n_jobs"] = THREADS
    cfg["geral"]["semente"] = SEMENTE
    return cfg


# ---------------------------------------------------------------------------
# Memória (Windows): bytes privados do processo, amostrados numa thread
# ---------------------------------------------------------------------------
class _PMC(ctypes.Structure):
    _fields_ = [("cb", wt.DWORD), ("PageFaultCount", wt.DWORD),
                ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t), ("QuotaPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t), ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                ("PagefileUsage", ctypes.c_size_t), ("PeakPagefileUsage", ctypes.c_size_t),
                ("PrivateUsage", ctypes.c_size_t)]


class _MEMSTATUS(ctypes.Structure):
    _fields_ = [("dwLength", wt.DWORD), ("dwMemoryLoad", wt.DWORD),
                ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]


_K32 = ctypes.WinDLL("kernel32")
_PSAPI = ctypes.WinDLL("psapi")
_K32.GetCurrentProcess.restype = wt.HANDLE
_PSAPI.GetProcessMemoryInfo.argtypes = [wt.HANDLE, ctypes.POINTER(_PMC), wt.DWORD]
_MB = 2 ** 20


def memoria_processo() -> Dict[str, float]:
    c = _PMC()
    c.cb = ctypes.sizeof(_PMC)
    _PSAPI.GetProcessMemoryInfo(_K32.GetCurrentProcess(), ctypes.byref(c), c.cb)
    return {"privada_mb": c.PrivateUsage / _MB, "working_set_mb": c.WorkingSetSize / _MB,
            "pico_privada_processo_mb": c.PeakPagefileUsage / _MB,
            "pico_working_set_processo_mb": c.PeakWorkingSetSize / _MB}


def memoria_sistema() -> Dict[str, float]:
    m = _MEMSTATUS()
    m.dwLength = ctypes.sizeof(_MEMSTATUS)
    _K32.GlobalMemoryStatusEx(ctypes.byref(m))
    return {"ram_total_gb": m.ullTotalPhys / 2 ** 30, "ram_livre_gb": m.ullAvailPhys / 2 ** 30,
            "carga_memoria_pct": m.dwMemoryLoad}


@contextmanager
def medir(registro: Dict[str, Any], nome: str, intervalo_s: float = 0.01):
    """Tempo de parede, tempo de CPU (todas as threads) e pico de bytes privados.

    O pico é amostrado a cada ``intervalo_s``; alocações mais curtas que isso
    podem escapar. Bytes privados não dependem de a página estar em RAM ou no
    arquivo de paginação, por isso são usados no lugar do working set.
    """
    antes = memoria_processo()["privada_mb"]
    pico = [antes]
    parar = threading.Event()

    def amostrar() -> None:
        while not parar.is_set():
            v = memoria_processo()["privada_mb"]
            if v > pico[0]:
                pico[0] = v
            parar.wait(intervalo_s)

    th = threading.Thread(target=amostrar, daemon=True)
    th.start()
    t0, c0 = time.perf_counter(), time.process_time()
    try:
        yield
    finally:
        seg, cpu = time.perf_counter() - t0, time.process_time() - c0
        parar.set()
        th.join()
        depois = memoria_processo()["privada_mb"]
        registro[nome] = {
            "segundos": seg, "cpu_segundos": cpu,
            "privada_antes_mb": antes, "privada_pico_mb": max(pico[0], depois),
            "acrescimo_pico_mb": max(pico[0], depois) - antes, "privada_depois_mb": depois,
        }


def resumo_tempos(tempos: List[float]) -> Dict[str, Any]:
    import numpy as np
    a = np.asarray(tempos, dtype=float)
    out: Dict[str, Any] = {"n": int(len(a)), "mediana_s": float(np.median(a)), "min_s": float(a.min()),
                           "max_s": float(a.max())}
    if len(a) >= 4:
        q1, q3 = np.quantile(a, [0.25, 0.75])
        out["iqr_s"] = float(q3 - q1)
    if len(a) >= 100:
        out["p95_s"] = float(np.quantile(a, 0.95))
    if len(a) >= 1000:
        out["p99_s"] = float(np.quantile(a, 0.99))
    return out


def cronometrar(funcao: Callable[[], Any], repeticoes: int, aquecimento: int = 1) -> Dict[str, Any]:
    for _ in range(aquecimento):
        funcao()
    tempos = []
    for _ in range(repeticoes):
        t0 = time.perf_counter()
        funcao()
        tempos.append(time.perf_counter() - t0)
    return {**resumo_tempos(tempos), "aquecimento": aquecimento}


# ---------------------------------------------------------------------------
# Rastreabilidade
# ---------------------------------------------------------------------------
def sha256(caminho: Path, bloco: int = 1 << 22) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as fh:
        for parte in iter(lambda: fh.read(bloco), b""):
            h.update(parte)
    return h.hexdigest()


def _nome_cpu() -> str:
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0") as k:
            return str(winreg.QueryValueEx(k, "ProcessorNameString")[0]).strip()
    except OSError:
        return platform.processor()


def git_nodewatch() -> Dict[str, Any]:
    def git(*args: str) -> str:
        return subprocess.run(["git", "-C", str(CAM["nodewatch"]), *args], capture_output=True,
                              text=True, encoding="utf-8").stdout.strip()
    alterados = [l for l in git("status", "--porcelain").splitlines() if l.strip()]
    return {"commit": git("rev-parse", "HEAD"), "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
            "alteracoes_nao_commitadas_rastreadas": [l for l in alterados if not l.startswith("??")]}


def ambiente() -> Dict[str, Any]:
    import joblib
    import numpy
    import pandas
    import scipy
    import sklearn
    try:
        import xgboost
        xgb = xgboost.__version__
    except ImportError:
        xgb = None
    return {
        "sistema": platform.platform(), "processador": _nome_cpu(), "nucleos_logicos": os.cpu_count(),
        **{k: round(v, 2) for k, v in memoria_sistema().items()},
        "python": platform.python_version(),
        "versoes": {"numpy": numpy.__version__, "pandas": pandas.__version__, "scikit-learn": sklearn.__version__,
                    "scipy": scipy.__version__, "joblib": joblib.__version__, "xgboost": xgb},
        "threads": THREADS,
        "variaveis_threads": {v: os.environ.get(v) for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")},
        "nodewatch": git_nodewatch(),
    }


def _normalizar(obj: Any) -> Any:
    """Converte tipos numpy e caminhos para JSON; caminhos viram só o nome."""
    import numpy as np
    if isinstance(obj, dict):
        return {str(k): _normalizar(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_normalizar(v) for v in obj]
    if isinstance(obj, Path):
        return obj.name
    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, np.ndarray):
        return _normalizar(obj.tolist())
    if isinstance(obj, float) and obj != obj:
        return None
    return obj


def salvar(nome: str, obj: Dict[str, Any]) -> Path:
    destino = RESULTADOS / f"{nome}.json"
    corpo = {"gerado_em_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
             "script": Path(sys.argv[0]).name, **obj}
    destino.write_text(json.dumps(_normalizar(corpo), ensure_ascii=False, indent=2, default=str),
                       encoding="utf-8")
    return destino


def log(msg: str) -> None:
    print(f"[{datetime.now():%H:%M:%S}] {msg}", flush=True)


# ---------------------------------------------------------------------------
# Adaptador para classificadores que exigem rótulos 0..K-1 (XGBoost)
# ---------------------------------------------------------------------------
from sklearn.base import BaseEstimator, ClassifierMixin  # noqa: E402  (depois de fixar as threads)


class ClassificadorRotulado(ClassifierMixin, BaseEstimator):
    """Expõe ``classes_`` com os rótulos originais (``OK``/``RISCO``/``FALHA``).

    ``CabecaClassificacao.probabilidades`` reordena colunas por ``classes_``;
    o XGBoost só aceita rótulos inteiros. Este invólucro mantém o contrato da
    cabeça sem alterar o NodeWatch.
    """

    def __init__(self, modelo: Any = None, classes: Optional[List[Any]] = None):
        import numpy as np
        self.modelo = modelo
        self.classes = classes
        self.classes_ = np.asarray(classes, dtype=object)

    def fit(self, X, y, **kwargs):
        raise NotImplementedError("O ajuste é feito fora do pipeline (com eval_set da validação).")

    def predict_proba(self, X):
        return self.modelo.predict_proba(X)

    def predict(self, X):
        import numpy as np
        return self.classes_[np.argmax(self.predict_proba(X), axis=1)]

    def __sklearn_is_fitted__(self) -> bool:
        return True
