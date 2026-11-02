"""A "regressão" do projeto é uma regressão logística (classificador). Ela convergiu?

Reajusta a regressão logística da grade de produção (mesmo pré-processamento:
imputação pela mediana, log com sinal e padronização, ajustados no treino)
com tolerâncias cada vez menores e compara iterações, valor da função
objetivo, norma do gradiente e qualidade na validação. Se a qualidade mudar
ao apertar a tolerância, o ajuste de produção parou antes do ótimo.

A função objetivo e o gradiente são recalculados aqui à mão (NumPy) a partir
dos coeficientes ajustados, como conferência independente do otimizador:
média ponderada da log-verossimilhança negativa + ||w||² / (2·C·Σpesos),
que é a normalização do scikit-learn >= 1.2 (lbfgs, penalidade L2).

Uso: python scripts/i_regressao_logistica.py
"""

from __future__ import annotations

import comum  # noqa: F401

import time
from typing import Any, Dict

import joblib
import numpy as np
import pandas as pd
from scipy.special import log_softmax, softmax
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score

from src.ml.avaliacao import metricas_multiclasse
from src.ml.esquemas import CLASSES_REDE
from src.ml.experimentos import _dados_rede
from src.ml.preparacao import matriz_rede, montar_pipeline_financeiro, montar_pipeline_rede

CLASSES = np.asarray(CLASSES_REDE, dtype=object)


def objetivo_e_gradiente(est: LogisticRegression, Z: np.ndarray, y: np.ndarray, w: np.ndarray) -> Dict[str, float]:
    """Perda ponderada média + L2, e norma infinito do gradiente, calculadas à mão."""
    classes = list(est.classes_)
    yi = np.array([classes.index(v) for v in y])
    S = w.sum()
    sw = w / S
    W, b = est.coef_, est.intercept_
    binario = len(classes) == 2
    # binário: sigmoide = softmax com logit 0 para a classe negativa
    logits = np.column_stack([np.zeros(len(Z)), Z @ W[0] + b[0]]) if binario else Z @ W.T + b
    perda = -np.sum(sw * log_softmax(logits, axis=1)[np.arange(len(yi)), yi])
    reg = np.sum(W ** 2) / (2 * est.C * S)
    R = softmax(logits, axis=1)
    R[np.arange(len(yi)), yi] -= 1.0
    R *= sw[:, None]
    if binario:
        grad = np.concatenate([R[:, 1] @ Z + W[0] / (est.C * S), [R[:, 1].sum()]])
    else:
        grad = np.concatenate([(R.T @ Z + W / (est.C * S)).ravel(), R.sum(axis=0)])
    return {"objetivo": float(perda + reg), "perda_media": float(perda),
            "norma_inf_gradiente": float(np.abs(grad).max())}


def rodar(nome: str, Xtr, ytr, wtr, Xva, yva, montar, params: Dict[str, Any], metrica) -> Dict[str, Any]:
    linhas = []
    for tol in (1e-4, 1e-6, 1e-8):
        pipe = montar(LogisticRegression(max_iter=20_000, random_state=comum.SEMENTE, tol=tol, **params), True)
        t0 = time.perf_counter()
        pipe.fit(Xtr, ytr, **({"modelo__sample_weight": wtr} if wtr is not None else {}))
        seg = time.perf_counter() - t0
        est = pipe.named_steps["modelo"]
        Ztr = pipe[:-1].transform(Xtr).to_numpy(dtype=np.float64)
        w = wtr if wtr is not None else np.ones(len(ytr))
        og = objetivo_e_gradiente(est, Ztr, np.asarray(ytr), np.asarray(w, dtype=np.float64))
        linhas.append({"tol": tol, "n_iter": np.atleast_1d(est.n_iter_).tolist(), "segundos": seg, **og,
                       "metrica_validacao": metrica(pipe, Xva, yva),
                       "maior_coeficiente_abs": float(np.abs(est.coef_).max())})
        comum.log(f"{nome} tol={tol:g}: n_iter={est.n_iter_} objetivo={og['objetivo']:.8f} "
                  f"|grad|inf={og['norma_inf_gradiente']:.2e} métrica={linhas[-1]['metrica_validacao']:.4f}")
    return {"params": params, "por_tolerancia": linhas}


def main() -> None:
    cfg = comum.config_nodewatch()
    s, _ = _dados_rede(cfg)
    tr, va = s[s["split"] == "treino"], s[s["split"] == "validacao"]

    def m_rede(pipe, X, y):
        ordem = list(pipe.classes_)
        p = pipe.predict_proba(X)[:, [ordem.index(c) for c in CLASSES_REDE]]
        return metricas_multiclasse(y, CLASSES[np.argmax(p, axis=1)])["macro_f1"]

    rede = rodar("rede", matriz_rede(tr), tr["alvo"].to_numpy(dtype=object), None, matriz_rede(va),
                 va["alvo"].to_numpy(dtype=object), montar_pipeline_rede, {"C": 0.1, "class_weight": None}, m_rede)

    pasta = comum.TRABALHO / "financeiro"
    prep = joblib.load(pasta / "preparador_salvo.joblib")
    btr, bva = pd.read_parquet(pasta / "treino.parquet"), pd.read_parquet(pasta / "validacao.parquet")

    def m_lav(pipe, X, y):
        return float(average_precision_score(y, pipe.predict_proba(X)[:, 1]))

    lav = rodar("lavagem", btr[prep.colunas], btr["_rotulo"].to_numpy(), btr["_peso"].to_numpy(),
                bva[prep.colunas], bva["_rotulo"].to_numpy(), montar_pipeline_financeiro, {"C": 0.1}, m_lav)
    comum.salvar("i_regressao_logistica", {
        "ambiente": comum.ambiente(), "rede": rede, "lavagem": lav,
        "nota": "max_iter=20000 para isolar o efeito da tolerância; a produção usa max_iter=3000 e tol=1e-4 "
                "(padrão do scikit-learn). Objetivo e gradiente recalculados à mão a partir dos coeficientes.",
    })


if __name__ == "__main__":
    main()
