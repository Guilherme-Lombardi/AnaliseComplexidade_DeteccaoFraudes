"""Benchmark de uma família de modelos num domínio (um processo por execução).

Etapas, sempre com os mesmos registros, alvos e atributos de origem:

1. busca: cada configuração da grade é ajustada só no treino e pontuada na
   validação (rede: macro-F1; lavagem: average precision). O XGBoost usa
   early stopping na validação (dados de desenvolvimento, nunca o teste);
2. ajuste final da configuração escolhida com 3 sementes (tempo, memória e
   variação de qualidade por semente);
3. com o modelo da semente 42: limiar na validação, métricas na validação e
   no teste, inferência em lote (estimador e pipeline), latência de 1 linha
   (4 threads e 1 thread), tamanho serializado e, na Random Forest, qualidade
   na validação em função do número de árvores.

Uso:
  python scripts/e_benchmark.py --dominio rede --familia rf
  python scripts/e_benchmark.py --dominio lavagem --familia xgb
Famílias: rf (grade de produção), hgb, lr (regressão logística), xgb.
"""

from __future__ import annotations

import comum  # noqa: F401  (threads e sys.path antes de numpy)

import argparse
import io
import warnings
from typing import Any, Dict, List, Optional, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import average_precision_score
from sklearn.utils.class_weight import compute_sample_weight
from threadpoolctl import threadpool_limits

from src.ml.avaliacao import (brier_multiclasse, calibracao_binaria, falsos_alertas, limiar_max_f1,
                              metricas_binarias, metricas_eventos, metricas_multiclasse)
from src.ml.esquemas import CLASSES_REDE
from src.ml.experimentos import _dados_rede
from src.ml.modelos import recriar_estimador
from src.ml.preparacao import MINUTOS_DIA, matriz_rede, montar_pipeline_financeiro, montar_pipeline_rede

CLASSES = np.asarray(CLASSES_REDE, dtype=object)
FAMILIA_NODEWATCH = {"rf": "random_forest", "rf_nb": "random_forest", "rf_red": "random_forest",
                     "hgb": "hist_gradient_boosting",
                     "lr": "logistica"}
SEMENTES = (42, 43, 44)
PREDICOES = comum.TRABALHO / "predicoes"


# ---------------------------------------------------------------------------
# Grades (rf, hgb e lr = grades de src/ml/modelos.py; xgb = mesmo número de tentativas)
# ---------------------------------------------------------------------------
def grade(dominio: str, familia: str) -> List[Dict[str, Any]]:
    if dominio == "rede":
        return {
            "rf": [{"n_estimators": 150, "min_samples_leaf": f, "max_samples": 0.5, "class_weight": cw}
                   for f in (20, 100) for cw in (None, "balanced_subsample")],
            "hgb": [{"max_iter": 200, "learning_rate": 0.1, "max_leaf_nodes": f, "class_weight": cw}
                    for f in (31, 63) for cw in (None, "balanced")],
            "lr": [{"C": C, "class_weight": cw} for C in (0.1, 1.0) for cw in (None, "balanced")],
            "xgb": [{"max_depth": d, "pesos": p} for d in (6, 8) for p in (None, "balanced")],
            # Configuração vencedora do notebook didático da professora (100 árvores, folha 5,
            # bootstrap completo), aqui ajustada só no treino para manter o protocolo.
            "rf_nb": [{"n_estimators": 100, "min_samples_leaf": 5, "max_samples": None, "class_weight": None}],
            # RF de produção com 50 árvores: a curva de árvores na VALIDAÇÃO (rede/rf) fica estável
            # de 25 a 150 árvores; testa se o tamanho e a latência caem sem perda de qualidade.
            "rf_red": [{"n_estimators": 50, "min_samples_leaf": 20, "max_samples": 0.5, "class_weight": None}],
        }[familia]
    return {
        "rf": [{"n_estimators": 100, "min_samples_leaf": 50, "max_samples": 0.5}],
        "hgb": [{"max_iter": 300, "learning_rate": 0.1, "max_leaf_nodes": f, "l2_regularization": 1.0} for f in (31, 63)],
        "lr": [{"C": C} for C in (0.1, 1.0)],
        "xgb": [{"max_depth": d, "min_child_weight": m} for d in (6, 8) for m in (1, 10)],
    }[familia]


def criar_xgb(dominio: str, params: Dict[str, Any], semente: int, n_arvores: Optional[int]):
    import xgboost as xgb
    kw: Dict[str, Any] = dict(
        tree_method="hist", device="cpu", n_jobs=comum.THREADS, learning_rate=0.1, max_bin=256,
        subsample=1.0, colsample_bytree=1.0, reg_lambda=1.0, random_state=semente,
        n_estimators=n_arvores or 1000,
    )
    if n_arvores is None:
        kw["early_stopping_rounds"] = 50
    if dominio == "rede":
        kw.update(objective="multi:softprob", eval_metric="mlogloss")
    else:
        kw.update(objective="binary:logistic", eval_metric="aucpr")
    kw.update({k: v for k, v in params.items() if k != "pesos"})
    return xgb.XGBClassifier(**kw)


# ---------------------------------------------------------------------------
# Dados
# ---------------------------------------------------------------------------
def carregar(dominio: str) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, Any], Dict[str, Any]]:
    reg: Dict[str, Any] = {}
    meta: Dict[str, Any] = {}
    d: Dict[str, Dict[str, Any]] = {}
    if dominio == "rede":
        cfg = comum.config_nodewatch()
        with comum.medir(reg, "leitura_csv_e_matriz"):
            s, _ = _dados_rede(cfg)
            for sp in ("treino", "validacao", "teste"):
                sub = s[s["split"] == sp].reset_index(drop=True)
                d[sp] = {"X": matriz_rede(sub), "y": sub["alvo"].to_numpy(dtype=object),
                         "df": sub[["id_fluxo", "anchor_id", "timestamp", "alvo", "classe_atual"]]}
        med = float(s[s["split"] == "treino"].groupby("id_fluxo")["timestamp"].diff().median())
        meta = {"mediana_intervalo_s": med, "limite_consecutivo_s": cfg["rede"]["multiplo_intervalo_consecutivo"] * med}
    else:
        pasta = comum.TRABALHO / "financeiro"
        with comum.medir(reg, "leitura_parquet_atributos"):
            prep = joblib.load(pasta / "preparador_salvo.joblib")
            for sp in ("treino", "validacao", "teste"):
                b = pd.read_parquet(pasta / f"{sp}.parquet")
                d[sp] = {"X": b[prep.colunas], "y": b["_rotulo"].to_numpy(),
                         "peso": b["_peso"].to_numpy() if "_peso" in b else None,
                         "dia": pd.to_datetime(b["_minuto"].to_numpy() // MINUTOS_DIA, unit="D").strftime("%Y-%m-%d").to_numpy()}
    for sp, v in d.items():
        meta[f"linhas_{sp}"] = int(len(v["X"]))
    meta["atributos_entrada"] = int(d["treino"]["X"].shape[1])
    meta["tipo_numerico_entrada"] = str(d["treino"]["X"].dtypes.iloc[0])
    return d, meta, reg


# ---------------------------------------------------------------------------
# Ajuste
# ---------------------------------------------------------------------------
def ajustar(dominio: str, familia: str, params: Dict[str, Any], semente: int, d: Dict[str, Any],
            n_arvores_xgb: Optional[int] = None) -> Tuple[Any, Dict[str, Any]]:
    montar = montar_pipeline_rede if dominio == "rede" else montar_pipeline_financeiro
    pipe = montar(None, familia == "lr")
    pre = pipe[:-1]
    info: Dict[str, Any] = {"params": params, "semente": semente}
    y = d["treino"]["y"]
    peso = d["treino"].get("peso")
    with warnings.catch_warnings(record=True) as avisos:
        warnings.simplefilter("always", ConvergenceWarning)
        with comum.medir(info, "ajuste_transformadores"):
            Ztr = pre.fit_transform(d["treino"]["X"])
        if familia == "xgb":
            if dominio == "rede":
                mapa = {c: i for i, c in enumerate(CLASSES_REDE)}
                ycod = np.array([mapa[v] for v in y])
                yva = np.array([mapa[v] for v in d["validacao"]["y"]])
                if params.get("pesos") == "balanced":
                    peso = compute_sample_weight("balanced", ycod)
            else:
                ycod, yva = y, d["validacao"]["y"]
            est = criar_xgb(dominio, params, semente, n_arvores_xgb)
            kw: Dict[str, Any] = {"sample_weight": peso, "verbose": False}
            if n_arvores_xgb is None:
                kw["eval_set"] = [(pre.transform(d["validacao"]["X"]), yva)]
            with comum.medir(info, "ajuste_estimador"):
                est.fit(Ztr, ycod, **kw)
            info["arvores_usadas"] = int(est.best_iteration + 1) if n_arvores_xgb is None else int(n_arvores_xgb)
            modelo = comum.ClassificadorRotulado(est, list(CLASSES_REDE)) if dominio == "rede" else est
        else:
            est = recriar_estimador(FAMILIA_NODEWATCH[familia], params, semente, comum.THREADS)
            with comum.medir(info, "ajuste_estimador"):
                est.fit(Ztr, y, **({"sample_weight": peso} if peso is not None else {}))
            modelo = est
    info["avisos_convergencia"] = [str(a.message)[:300] for a in avisos if issubclass(a.category, ConvergenceWarning)]
    if familia == "lr":
        info["n_iter"] = np.atleast_1d(est.n_iter_).tolist()
        info["max_iter"] = est.max_iter
        info["norma_coeficientes"] = float(np.linalg.norm(est.coef_))
    info["ajuste_total_s"] = info["ajuste_transformadores"]["segundos"] + info["ajuste_estimador"]["segundos"]
    pipe.steps[-1] = ("modelo", modelo)
    return pipe, info


def probabilidades(pipe: Any, X: pd.DataFrame, classes: List[Any], lote: int = 250_000) -> np.ndarray:
    ordem = list(pipe.classes_)
    idx = [ordem.index(c) for c in classes]
    return np.vstack([pipe.predict_proba(X.iloc[i:i + lote])[:, idx] for i in range(0, len(X), lote)])


def classes_dominio(dominio: str) -> List[Any]:
    return list(CLASSES_REDE) if dominio == "rede" else [0, 1]


def metrica_selecao(dominio: str, y: np.ndarray, p: np.ndarray) -> float:
    if dominio == "rede":
        return metricas_multiclasse(y, CLASSES[np.argmax(p, axis=1)])["macro_f1"]
    return float(average_precision_score(y, p[:, 1]))


# ---------------------------------------------------------------------------
# Avaliação
# ---------------------------------------------------------------------------
def avaliar(dominio: str, d: Dict[str, Any], meta: Dict[str, Any], p_va: np.ndarray, p_te: np.ndarray) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    if dominio == "rede":
        s_va = p_va[:, 1] + p_va[:, 2]
        lim = limiar_max_f1(d["validacao"]["y"] != "OK", s_va)
        out["limiar_nao_ok_validacao"] = lim
        for sp, p in (("validacao", p_va), ("teste", p_te)):
            y, df = d[sp]["y"], d[sp]["df"]
            pred = CLASSES[np.argmax(p, axis=1)]
            score = p[:, 1] + p[:, 2]
            out[sp] = {
                "multiclasse": metricas_multiclasse(y, pred),
                "eventos": metricas_eventos(df, pred, meta["limite_consecutivo_s"]),
                "alertas_no_limiar_da_validacao": falsos_alertas(df, score >= lim["limiar"], y != "OK",
                                                                 meta["mediana_intervalo_s"]),
                "calibracao_nao_ok": {k: v for k, v in calibracao_binaria(y != "OK", score).items() if k != "caixas"},
                "brier_multiclasse": brier_multiclasse(y, p, CLASSES_REDE),
            }
    else:
        lim = limiar_max_f1(d["validacao"]["y"], p_va[:, 1])
        out["limiar_validacao"] = lim
        for sp, p in (("validacao", p_va), ("teste", p_te)):
            m = metricas_binarias(d[sp]["y"], p[:, 1], lim["limiar"], d[sp]["dia"])
            m.pop("curva_pr_resumida", None)
            out[sp] = m
    return out


def medir_inferencia(familia: str, pipe: Any, X: pd.DataFrame) -> Dict[str, Any]:
    r: Dict[str, Any] = {"linhas_lote": int(len(X))}
    est = pipe.named_steps["modelo"]
    Z = pipe[:-1].transform(X)
    r["lote_estimador"] = comum.cronometrar(lambda: est.predict_proba(Z), repeticoes=5)
    r["lote_pipeline"] = comum.cronometrar(lambda: pipe.predict_proba(X), repeticoes=5)
    r["vazao_pipeline_linhas_por_s"] = len(X) / r["lote_pipeline"]["mediana_s"]
    with comum.medir(r, "memoria_lote_pipeline"):
        pipe.predict_proba(X)
    rng = np.random.default_rng(0)
    linhas = [X.iloc[[i]] for i in rng.choice(len(X), 1000, replace=False)]

    def latencia() -> Dict[str, Any]:
        for x in linhas[:20]:
            pipe.predict_proba(x)
        tempos = []
        for x in linhas:
            t0 = comum.time.perf_counter()
            pipe.predict_proba(x)
            tempos.append(comum.time.perf_counter() - t0)
        return comum.resumo_tempos(tempos)

    r[f"latencia_1_linha_threads_{comum.THREADS}"] = latencia()
    alvo = est.modelo if isinstance(est, comum.ClassificadorRotulado) else est
    antes = alvo.get_params().get("n_jobs")
    if antes is not None:
        alvo.set_params(n_jobs=1)
    with threadpool_limits(limits=1):
        r["latencia_1_linha_threads_1"] = latencia()
    if antes is not None:
        alvo.set_params(n_jobs=antes)
    return r


def tamanho(pipe: Any) -> Dict[str, Any]:
    saida = {}
    for nome, nivel in (("joblib_compress3_bytes", 3), ("joblib_sem_compressao_bytes", 0)):
        buf = io.BytesIO()
        joblib.dump(pipe, buf, compress=nivel)
        saida[nome] = len(buf.getvalue())
    return saida


def curva_arvores(dominio: str, pipe: Any, d: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Qualidade na validação usando só as k primeiras árvores da floresta (sem reajuste)."""
    est = pipe.named_steps["modelo"]
    Z = pipe[:-1].transform(d["validacao"]["X"]).to_numpy(dtype=np.float32)
    ordem = list(est.classes_)
    idx = [ordem.index(c) for c in classes_dominio(dominio)]
    soma = np.zeros((len(Z), len(ordem)))
    ks = [k for k in (5, 10, 25, 50, 75, 100, 150) if k <= len(est.estimators_)]
    saida = []
    for i, arv in enumerate(est.estimators_, 1):
        soma += arv.predict_proba(Z)
        if i in ks:
            p = (soma / i)[:, idx]
            saida.append({"arvores": i, "metrica_validacao": metrica_selecao(dominio, d["validacao"]["y"], p)})
    return saida


# ---------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dominio", choices=("rede", "lavagem"), required=True)
    ap.add_argument("--familia", choices=("rf", "rf_nb", "rf_red", "hgb", "lr", "xgb"), required=True)
    args = ap.parse_args()
    dom, fam = args.dominio, args.familia
    classes = classes_dominio(dom)
    comum.log(f"{dom}/{fam}: carregando dados")
    d, meta, reg_dados = carregar(dom)

    busca = []
    t_busca = 0.0
    melhor = None
    for params in grade(dom, fam):
        pipe, info = ajustar(dom, fam, params, comum.SEMENTE, d)
        with comum.medir(info, "previsao_validacao"):
            p_va = probabilidades(pipe, d["validacao"]["X"], classes)
        info["metrica_validacao"] = metrica_selecao(dom, d["validacao"]["y"], p_va)
        if dom == "rede":
            info["recall_falha_validacao"] = metricas_multiclasse(
                d["validacao"]["y"], CLASSES[np.argmax(p_va, axis=1)])["por_classe"]["FALHA"]["recall"]
        t_busca += info["ajuste_total_s"] + info["previsao_validacao"]["segundos"]
        busca.append(info)
        comum.log(f"  {params} -> {info['metrica_validacao']:.4f} ({info['ajuste_total_s']:.1f} s)")
        chave = (round(info["metrica_validacao"], 6), info.get("recall_falha_validacao", 0.0))
        if melhor is None or chave > melhor[0]:
            melhor = (chave, params, info.get("arvores_usadas"))
    _, escolhido, n_arv = melhor
    comum.log(f"{dom}/{fam}: escolhido {escolhido}; ajustes finais com sementes {SEMENTES}")

    finais = []
    modelo42 = None
    for s in SEMENTES:
        pipe, info = ajustar(dom, fam, escolhido, s, d, n_arvores_xgb=n_arv)
        p_va = probabilidades(pipe, d["validacao"]["X"], classes)
        p_te = probabilidades(pipe, d["teste"]["X"], classes)
        info["metrica_validacao"] = metrica_selecao(dom, d["validacao"]["y"], p_va)
        info["metrica_teste"] = metrica_selecao(dom, d["teste"]["y"], p_te)
        finais.append(info)
        if s == comum.SEMENTE:
            modelo42 = (pipe, p_va, p_te)
    pipe, p_va, p_te = modelo42
    comum.log(f"{dom}/{fam}: avaliação, inferência e tamanho")
    qualidade = avaliar(dom, d, meta, p_va, p_te)
    inferencia = medir_inferencia(fam, pipe, d["teste"]["X"])
    PREDICOES.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(PREDICOES / f"{dom}_{fam}.npz", p_va=p_va, p_te=p_te)
    resultado = {
        "ambiente": comum.ambiente(),
        "dominio": dom, "familia": fam,
        "dados": meta, "custo_dados": reg_dados,
        "busca": {"tentativas": len(busca), "segundos_total": t_busca, "configuracoes": busca,
                  "criterio": "macro-F1 na validação (desempate: recall de FALHA)" if dom == "rede"
                  else "average precision na validação"},
        "escolhido": {"params": escolhido, "arvores_xgb": n_arv},
        "ajustes_finais": finais,
        "tempo_ajuste_final": comum.resumo_tempos([f["ajuste_total_s"] for f in finais]),
        "qualidade_semente_42": qualidade,
        "variacao_por_semente": {
            "validacao": comum.resumo_tempos([f["metrica_validacao"] for f in finais]),
            "teste": comum.resumo_tempos([f["metrica_teste"] for f in finais]),
            "nota": "campos *_s aqui são valores da métrica, não segundos",
        },
        "inferencia": inferencia,
        "tamanho": tamanho(pipe),
    }
    if fam.startswith("rf"):
        resultado["curva_arvores_validacao"] = curva_arvores(dom, pipe, d)
    if fam == "xgb":
        import xgboost
        resultado["xgboost_config"] = pipe.named_steps["modelo"].get_params() if dom == "lavagem" else \
            pipe.named_steps["modelo"].modelo.get_params()
        resultado["xgboost_versao"] = xgboost.__version__
    comum.salvar(f"e_benchmark_{dom}_{fam}", resultado)
    comum.log(f"{dom}/{fam}: ok")


if __name__ == "__main__":
    main()
