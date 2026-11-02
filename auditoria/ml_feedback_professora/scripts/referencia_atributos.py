"""Implementação de referência, por força bruta, dos atributos financeiros.

Reescreve a definição documentada em ``src/ml/preparacao.py`` (janela
``[t - w, t)``, só minutos estritamente anteriores) com laços e filtros
explícitos, sem índices ordenados nem somas acumuladas. Serve para conferir
``atributos_financeiros`` (lexsort + searchsorted + cumsum) linha a linha.

É lenta de propósito: O(n) por consulta.
"""

from __future__ import annotations

import math
from typing import Dict, Iterable, List

import numpy as np
import pandas as pd

TETO_MIN = 14_400.0  # mesmo teto de src/ml/preparacao.py (_SEM_HISTORICO_MIN)
try:  # piso da variância do z: 0,01 depois da correção de 02/11/2026; 1e-6 no commit 893ceea
    from src.ml.preparacao import _VAR_MIN_Z as VAR_MIN_Z
except ImportError:
    VAR_MIN_Z = 1e-6


def _min_desde(minutos: np.ndarray, t: int) -> float:
    return float(t - minutos.max()) if len(minutos) else math.nan


def atributos_referencia(trans: pd.DataFrame, consulta: Iterable[int], cambio: Dict[str, float],
                         formatos: List[str], moedas: List[str]) -> pd.DataFrame:
    """Mesmas colunas de ``atributos_financeiros``, calculadas por filtragem direta."""
    minuto = trans["minuto"].to_numpy(dtype=np.int64)
    o_all = trans["conta_origem"].to_numpy(dtype=np.int64)
    d_all = trans["conta_destino"].to_numpy(dtype=np.int64)
    moeda_pag = trans["moeda_pagamento"].astype(str).to_numpy()
    moeda_rec = trans["moeda_recebimento"].astype(str).to_numpy()
    taxa = np.array([cambio.get(m, np.nan) for m in moeda_pag], dtype=np.float64)
    usd = trans["valor_pago"].to_numpy(dtype=np.float64) * taxa
    usd0 = np.where(np.isfinite(usd), usd, 0.0)
    logv = np.log1p(usd0)
    banco_o = trans["banco_origem"].to_numpy()
    banco_d = trans["banco_destino"].to_numpy()
    formato = trans["formato"].astype(str).to_numpy()

    linhas = []
    for i in consulta:
        t, o, d = int(minuto[i]), int(o_all[i]), int(d_all[i])
        antes = minuto < t
        env_o = antes & (o_all == o)
        rec_o = antes & (d_all == o)
        env_d = antes & (o_all == d)
        rec_d = antes & (d_all == d)
        r: Dict[str, float] = {}
        r["log_valor_usd"] = float(np.log1p(usd[i])) if np.isfinite(usd[i]) else math.nan
        r["sem_taxa_cambio"] = float(not np.isfinite(usd[i]))
        r["moeda_diferente"] = float(moeda_pag[i] != moeda_rec[i])
        r["mesmo_banco"] = float(banco_o[i] == banco_d[i])
        r["auto_transferencia"] = float(o == d)
        for h in (6, 24, 72):
            r[f"n_env_origem_{h}h"] = float((env_o & (minuto >= t - h * 60)).sum())
        r["soma_env_origem_usd_24h"] = float(usd0[env_o & (minuto >= t - 1440)].sum())
        n = int(env_o.sum())
        r["n_env_origem_total"] = float(n)
        if n >= 2:
            hist = logv[env_o]
            r["z_valor_origem"] = float((logv[i] - hist.mean()) / math.sqrt(hist.var() + VAR_MIN_Z))
        else:
            r["z_valor_origem"] = 0.0
        r["min_desde_env_origem"] = _min_desde(minuto[env_o], t)
        r["n_env_destino_24h"] = float((env_d & (minuto >= t - 1440)).sum())
        r["n_rec_origem_24h"] = float((rec_o & (minuto >= t - 1440)).sum())
        soma_rec = float(usd0[rec_o & (minuto >= t - 1440)].sum())
        r["soma_rec_origem_usd_24h"] = soma_rec
        r["razao_saida_entrada_24h"] = r["soma_env_origem_usd_24h"] / (soma_rec + 1.0)
        r["min_desde_rec_origem"] = _min_desde(minuto[rec_o], t)
        for h in (24, 72):
            r[f"n_rec_destino_{h}h"] = float((rec_d & (minuto >= t - h * 60)).sum())
        r["min_desde_rec_destino"] = _min_desde(minuto[rec_d], t)
        par_antes = env_o & (d_all == d)
        r["par_novo"] = float(not par_antes.any())
        r["n_par_previas"] = float(par_antes.sum())
        r["dest_distintos_origem"] = float(len(np.unique(d_all[env_o])))
        r["orig_distintas_destino"] = float(len(np.unique(o_all[rec_d])))
        for col in ("min_desde_env_origem", "min_desde_rec_origem", "min_desde_rec_destino"):
            v = r[col]
            r[f"sem_historico_{col[10:]}"] = float(math.isnan(v))
            r[col] = TETO_MIN if math.isnan(v) else min(v, TETO_MIN)
        for f in formatos:
            r[f"formato_{f}"] = float(formato[i] == f)
        for m in moedas:
            r[f"moeda_{m}"] = float(moeda_pag[i] == m)
        linhas.append(r)
    return pd.DataFrame(linhas)


def comparar(obtido: pd.DataFrame, referencia: pd.DataFrame, rtol: float = 1e-5,
             atol: float = 1e-3) -> Dict[str, Dict[str, float]]:
    """Diferença por coluna (obtido em float32, referência em float64)."""
    saida = {}
    for col in referencia.columns:
        a = obtido[col].to_numpy(dtype=np.float64)
        b = referencia[col].to_numpy(dtype=np.float64)
        ambos_nan = np.isnan(a) & np.isnan(b)
        dif = np.where(ambos_nan, 0.0, np.abs(a - b))
        ok = ambos_nan | np.isclose(a, b, rtol=rtol, atol=atol)
        rel = dif / np.maximum(np.abs(b), 1e-12)
        saida[col] = {"divergentes": int((~ok).sum()), "max_abs": float(np.nanmax(dif)) if len(dif) else 0.0,
                      "max_rel": float(np.nanmax(np.where(ambos_nan, 0.0, rel))) if len(rel) else 0.0}
    return saida
