"""Testes da auditoria: implementação própria (NumPy) contra referências independentes.

Cada teste diz qual risco verifica. Não alteram o NodeWatch: importam ``src.ml``
do clone configurado em ``config_auditoria.local.toml``.
"""

from __future__ import annotations

import math

import joblib
import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import brier_score_loss, f1_score

from referencia_atributos import atributos_referencia, comparar
from src.ml.avaliacao import brier_multiclasse, calibracao_binaria, limiar_max_f1, metricas_eventos, psi, referencia_psi
from src.ml.esquemas import CLASSES_REDE
from src.ml.preparacao import PreparadorFinanceiro, atributos_financeiros

MOEDAS = ["Euro", "US Dollar", "Yen"]
FORMATOS = ["ACH", "Cheque", "Wire"]
CAMBIO = {"US Dollar": 1.0, "Euro": 1.1}  # Yen sem taxa: testa o indicador sem_taxa_cambio


def _prep() -> PreparadorFinanceiro:
    return PreparadorFinanceiro(CAMBIO, {}, FORMATOS, MOEDAS, {}, float("nan"))


def _trans(linhas):
    df = pd.DataFrame(linhas, columns=["minuto", "conta_origem", "conta_destino", "valor_pago", "moeda_pagamento"])
    df["moeda_recebimento"] = df["moeda_pagamento"]
    df["banco_origem"] = df["conta_origem"] % 3
    df["banco_destino"] = df["conta_destino"] % 3
    df["formato"] = "ACH"
    df["minuto"] += 27_000_000  # minutos absolutos plausíveis (2021)
    return df


def test_casos_de_fronteira_resultado_conhecido():
    """Risco: janela [t-w, t) com borda errada ou transação do mesmo minuto visível."""
    t = _trans([
        (100, 1, 2, 10.0, "US Dollar"),
        (100, 1, 3, 20.0, "US Dollar"),   # mesmo minuto da anterior: não se enxergam
        (460, 1, 2, 30.0, "US Dollar"),   # exatamente 6 h depois: minuto 100 entra na janela de 6 h
        (460, 2, 1, 5.0, "Euro"),         # mesmo minuto da anterior
        (461, 1, 1, 7.0, "Yen"),          # auto-transferência, moeda sem taxa
    ])
    X = atributos_financeiros(t, np.arange(len(t)), _prep())
    assert X.loc[1, "n_env_origem_total"] == 0 and X.loc[1, "par_novo"] == 1
    assert X.loc[2, "n_env_origem_6h"] == 2 and X.loc[2, "n_par_previas"] == 1 and X.loc[2, "par_novo"] == 0
    assert X.loc[2, "dest_distintos_origem"] == 2 and X.loc[2, "min_desde_env_origem"] == 360
    assert X.loc[2, "n_rec_origem_24h"] == 0 and X.loc[2, "sem_historico_rec_origem"] == 1
    assert X.loc[4, "n_env_origem_6h"] == 1 and X.loc[4, "n_env_origem_24h"] == 3
    assert X.loc[4, "n_rec_origem_24h"] == 1 and X.loc[4, "min_desde_rec_origem"] == 1
    assert X.loc[4, "auto_transferencia"] == 1 and X.loc[4, "par_novo"] == 1
    assert X.loc[4, "sem_taxa_cambio"] == 1 and math.isnan(X.loc[4, "log_valor_usd"])
    assert X.loc[4, "orig_distintas_destino"] == 1
    assert X.loc[2, "soma_env_origem_usd_24h"] == pytest.approx(30.0)


@pytest.mark.parametrize("semente", [0, 1, 2])
def test_atributos_iguais_a_forca_bruta_em_dados_aleatorios(semente):
    """Risco: erro de índice/ordenação no motor vetorizado (lexsort + searchsorted + cumsum)."""
    rng = np.random.default_rng(semente)
    n = 400
    t = _trans(list(zip(
        np.sort(rng.integers(0, 6000, n)), rng.integers(0, 25, n), rng.integers(0, 25, n),
        np.round(rng.lognormal(6, 2, n), 2), rng.choice(MOEDAS, n),
    )))
    t["formato"] = rng.choice(FORMATOS, n)
    t["moeda_recebimento"] = np.where(rng.random(n) < 0.1, "Euro", t["moeda_pagamento"])
    t = t.sample(frac=1.0, random_state=semente).reset_index(drop=True)  # ordem do arquivo não importa
    obtido = atributos_financeiros(t, np.arange(n), _prep())
    ref = atributos_referencia(t, range(n), CAMBIO, FORMATOS, MOEDAS)
    difs = comparar(obtido, ref)
    assert {c: d for c, d in difs.items() if d["divergentes"]} == {}
    assert set(obtido.columns) == set(ref.columns)  # a ordem é fixada depois por prep.colunas


def test_limiar_max_f1_igual_busca_exaustiva():
    """Risco: limiar escolhido na validação não maximiza o F1 declarado."""
    rng = np.random.default_rng(3)
    y = (rng.random(3000) < 0.05).astype(int)
    score = np.clip(y * 0.3 + rng.random(3000) * 0.8, 0, 1).round(3)  # empates de propósito
    lim = limiar_max_f1(y, score)
    melhor = max(((f1_score(y, score >= s), s) for s in np.unique(score)), key=lambda x: (x[0], -x[1]))
    assert lim["f1"] == pytest.approx(melhor[0], abs=1e-12)
    assert f1_score(y, score >= lim["limiar"]) == pytest.approx(lim["f1"], abs=1e-12)


def test_calibracao_e_brier_iguais_a_formula_independente():
    """Risco: ECE/Brier com caixas ou normalização erradas."""
    rng = np.random.default_rng(4)
    p = rng.random(5000)
    p[:10] = 1.0  # borda superior cai na última caixa
    y = (rng.random(5000) < p).astype(int)
    r = calibracao_binaria(y, p)
    caixa = np.minimum((p * 10).astype(int), 9)
    ece = sum((caixa == b).mean() * abs(p[caixa == b].mean() - y[caixa == b].mean())
              for b in range(10) if (caixa == b).any())
    assert r["ece"] == pytest.approx(ece, abs=1e-12)
    assert r["brier"] == pytest.approx(brier_score_loss(y, p), abs=1e-12)


def test_brier_multiclasse_igual_definicao():
    """Risco: Brier multiclasse com classes fora de ordem."""
    rng = np.random.default_rng(5)
    proba = rng.dirichlet([1, 1, 1], 2000)
    y = np.asarray(CLASSES_REDE, dtype=object)[rng.integers(0, 3, 2000)]
    uma_quente = np.stack([(y == c) for c in CLASSES_REDE], axis=1).astype(float)
    esperado = np.mean(np.sum((proba - uma_quente) ** 2, axis=1))
    assert brier_multiclasse(y, proba, CLASSES_REDE) == pytest.approx(esperado, abs=1e-12)
    # scikit-learn >= 1.7 aceita multiclasse com rótulos em ordem lexicográfica;
    # scale_by_half=False dá a mesma escala da definição acima.
    ordem = [list(CLASSES_REDE).index(c) for c in sorted(CLASSES_REDE)]
    try:
        sk = brier_score_loss(y, proba[:, ordem], labels=sorted(CLASSES_REDE), scale_by_half=False)
    except TypeError:
        pytest.skip("brier_score_loss multiclasse indisponível nesta versão")
    assert brier_multiclasse(y, proba, CLASSES_REDE) == pytest.approx(sk, abs=1e-12)


def test_psi_igual_formula_e_zero_sem_deriva():
    """Risco: alerta de deriva (PSI) calculado com caixas desalinhadas."""
    rng = np.random.default_rng(6)
    v = rng.normal(size=20_000)
    ref = referencia_psi(v)
    assert psi(ref, v) == pytest.approx(0.0, abs=1e-9)
    w = rng.normal(0.5, 1, 20_000)
    bordas = np.asarray(ref["bordas"])
    obs = np.histogram(np.clip(w, bordas[0], bordas[-1]), bins=bordas)[0] / len(w)
    esp = np.asarray(ref["proporcoes"])
    esperado = np.sum((obs - esp) * np.log((obs + 1e-6) / (esp + 1e-6)))
    assert psi(ref, w) == pytest.approx(esperado, rel=1e-3)


def test_inicios_de_evento_iguais_a_laco():
    """Risco: início de evento contado entre medições não consecutivas ou entre fluxos."""
    rng = np.random.default_rng(7)
    linhas = []
    for f in range(6):
        ts = np.cumsum(rng.choice([240, 240, 241, 900], 200))
        alvo = rng.choice(["OK", "OK", "OK", "RISCO", "FALHA"], 200)
        linhas += [(f"f{f}", int(a), b) for a, b in zip(ts, alvo)]
    df = pd.DataFrame(linhas, columns=["id_fluxo", "timestamp", "alvo"]).sample(frac=1, random_state=0)
    pred = rng.choice(list(CLASSES_REDE), len(df))
    r = metricas_eventos(df, pred, 480)
    n = det = 0
    for _, g in df.assign(pred=pred).sort_values(["id_fluxo", "timestamp"]).groupby("id_fluxo"):
        a, ts, p = g["alvo"].to_list(), g["timestamp"].to_list(), g["pred"].to_list()
        for i in range(1, len(a)):
            if ts[i] - ts[i - 1] <= 480 and a[i - 1] == "OK" and a[i] != "OK":
                n += 1
                det += p[i] != "OK"
    assert r["inicios_nao_ok"]["n"] == n and r["inicios_nao_ok"]["detectados_nao_ok"] == det
