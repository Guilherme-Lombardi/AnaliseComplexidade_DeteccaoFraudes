"""Confere a implementação própria (NumPy) contra referências, em dados reais.

1. Atributos financeiros: ``atributos_financeiros`` (vetorizado) × força bruta
   (``referencia_atributos``) numa amostra de transações do HI-Small.
2. Reprodutibilidade do cache: recalcula os atributos de todo o teste com o
   codificador salvo e compara, bit a bit, com o parquet usado na avaliação.
3. Métricas próprias da rede (matriz, eventos, falsos alertas, limiar, ECE)
   recalculadas por fórmulas independentes sobre as previsões do artefato.
4. ``regra_classe_atual``: quanto a regra de limiares reproduz ``classe_atual``.

Uso: python scripts/b_verificar_implementacao.py [--amostra 2000]
"""

from __future__ import annotations

import comum  # noqa: F401

import argparse
import json
from typing import Any, Dict

import numpy as np
import pandas as pd

from referencia_atributos import atributos_referencia, comparar
from src.ml.auditoria import regra_classe_atual
from src.ml.avaliacao import (calibracao_binaria, falsos_alertas, limiar_max_f1, metricas_eventos,
                              metricas_multiclasse)
from src.ml.esquemas import CLASSES_REDE
from src.ml.experimentos import _dados_rede
from src.ml.ingestao import ler_hismall
from src.ml.modelos import ModeloUnificado
from src.ml.preparacao import PreparadorFinanceiro, atribuir_split_financeiro, atributos_financeiros, matriz_rede

NW = comum.CAM["nodewatch"]


def verificar_atributos(modelo: ModeloUnificado, cfg: Dict[str, Any], n_amostra: int) -> Dict[str, Any]:
    reg: Dict[str, Any] = {}
    with comum.medir(reg, "leitura_hismall"):
        dados = ler_hismall(cfg["financeiro"]["transacoes"])
    t = dados.trans
    split = atribuir_split_financeiro(t["minuto"].to_numpy(), cfg["financeiro"])
    prep_salvo: PreparadorFinanceiro = modelo.codificadores["financeiro"]
    with comum.medir(reg, "ajuste_preparador"):
        prep_novo = PreparadorFinanceiro.ajustar(t.iloc[np.flatnonzero(split == "treino")])
    preparador_igual = (prep_novo.cambio == prep_salvo.cambio and prep_novo.formatos == prep_salvo.formatos
                        and prep_novo.moedas == prep_salvo.moedas and prep_novo.taxa_formato == prep_salvo.taxa_formato)

    # 1. amostra: transações comuns e de lavagem, dos três períodos
    rng = np.random.default_rng(comum.SEMENTE)
    y = t["rotulo"].to_numpy()
    elegiveis = np.flatnonzero(np.isin(split, ["treino", "validacao", "teste"]))
    pos = elegiveis[y[elegiveis] == 1]
    neg = elegiveis[y[elegiveis] == 0]
    consulta = np.sort(np.concatenate([rng.choice(pos, n_amostra // 4, replace=False),
                                       rng.choice(neg, n_amostra - n_amostra // 4, replace=False)]))
    contas = np.unique(np.concatenate([t["conta_origem"].to_numpy()[consulta], t["conta_destino"].to_numpy()[consulta]]))
    envolve = np.isin(t["conta_origem"].to_numpy(), contas) | np.isin(t["conta_destino"].to_numpy(), contas)
    sub_idx = np.flatnonzero(envolve)
    sub = t.iloc[sub_idx].reset_index(drop=True)
    pos_sub = np.searchsorted(sub_idx, consulta)
    with comum.medir(reg, "vetorizado_amostra"):
        obtido = atributos_financeiros(t, consulta, prep_salvo)
    comum.log(f"força bruta: {len(consulta)} consultas sobre {len(sub):,} transações das contas envolvidas")
    with comum.medir(reg, "forca_bruta_amostra"):
        ref = atributos_referencia(sub, pos_sub, prep_salvo.cambio, prep_salvo.formatos, prep_salvo.moedas)
    difs = comparar(obtido, ref[obtido.columns])
    divergentes = {c: d for c, d in difs.items() if d["divergentes"]}

    # 2. cache do teste
    comum.log("recalculando os atributos de todo o teste")
    idx_te = np.flatnonzero(split == "teste")
    with comum.medir(reg, "vetorizado_teste_completo"):
        X_te = atributos_financeiros(t, idx_te, prep_salvo)
    cache = pd.read_parquet(NW / "artefatos_ml/cache/financeiro_teste.parquet")
    mesma_ordem = bool((cache["_id_transacao"].to_numpy() == t["id_transacao"].to_numpy()[idx_te]).all())
    a = X_te[prep_salvo.colunas].to_numpy()
    b = cache[prep_salvo.colunas].to_numpy()
    iguais = (a == b) | (np.isnan(a) & np.isnan(b))
    return {
        "tempos_memoria": reg,
        "preparador_reajustado_igual_ao_salvo": preparador_igual,
        "moedas_sem_taxa": prep_salvo.info_cambio.get("moedas_sem_taxa"),
        "amostra": {"consultas": int(len(consulta)), "positivas": int(y[consulta].sum()),
                    "por_split": pd.Series(split[consulta]).value_counts().to_dict(),
                    "transacoes_de_historico_consideradas": int(len(sub)),
                    "colunas_comparadas": int(len(difs)), "colunas_divergentes": divergentes,
                    "max_rel_por_coluna": {c: d["max_rel"] for c, d in difs.items() if d["max_rel"] > 0}},
        "cache_teste": {"linhas": int(len(cache)), "mesma_ordem_de_transacoes": mesma_ordem,
                        "celulas": int(iguais.size), "celulas_identicas": int(iguais.sum())},
    }


def _metricas_independentes(y: np.ndarray, pred: np.ndarray) -> Dict[str, Any]:
    k = list(CLASSES_REDE)
    m = np.zeros((3, 3), dtype=int)
    for a, b in zip(y, pred):
        m[k.index(a), k.index(b)] += 1
    prec = np.diag(m) / np.maximum(m.sum(axis=0), 1)
    rec = np.diag(m) / np.maximum(m.sum(axis=1), 1)
    f1 = np.where(prec + rec > 0, 2 * prec * rec / np.maximum(prec + rec, 1e-300), 0)
    return {"matriz": m.tolist(), "macro_f1": float(f1.mean()), "balanced_accuracy": float(rec.mean())}


def verificar_metricas_rede(modelo: ModeloUnificado, cfg: Dict[str, Any]) -> Dict[str, Any]:
    cab = modelo.cabeca("estado_rede")
    s, _ = _dados_rede(cfg)
    classes = np.asarray(CLASSES_REDE, dtype=object)
    saida: Dict[str, Any] = {}
    # regra de limiares × classe_atual (todas as linhas)
    regra = regra_classe_atual(s)
    por_split = {sp: float((regra[(s["split"] == sp).to_numpy()] == s.loc[s["split"] == sp, "classe_atual"]).mean())
                 for sp in ("treino", "validacao", "teste")}
    saida["regra_classe_atual"] = {
        "concordancia_total": float((regra == s["classe_atual"].to_numpy()).mean()),
        "concordancia_por_split": por_split,
        "linhas_divergentes": int((regra != s["classe_atual"].to_numpy()).sum()),
        "matriz_regra_x_classe_atual": pd.crosstab(pd.Series(regra, name="regra"),
                                                   s["classe_atual"].rename("classe_atual")).to_dict(),
        "alvo_igual_classe_atual_seguinte": None,
    }
    prox = s.groupby("id_fluxo")["classe_atual"].shift(-1)
    tem = prox.notna().to_numpy()
    saida["regra_classe_atual"]["alvo_igual_classe_atual_seguinte"] = float(
        (s["alvo"].to_numpy()[tem] == prox.to_numpy()[tem]).mean())

    for sp in ("validacao", "teste"):
        sub = s[s["split"] == sp].reset_index(drop=True)
        y = sub["alvo"].to_numpy(dtype=object)
        proba = cab.probabilidades(matriz_rede(sub))
        pred = classes[np.argmax(proba, axis=1)]
        oficial = metricas_multiclasse(y, pred)
        indep = _metricas_independentes(y, pred)
        score = proba[:, 1] + proba[:, 2]
        nao_ok = y != "OK"
        # eventos por laço explícito
        n = det = 0
        ordenado = sub.assign(pred=pred).sort_values(["id_fluxo", "timestamp"], kind="stable")
        limite = cab.metadados["multiplo_intervalo_consecutivo"] * cab.metadados["mediana_intervalo_treino_s"]
        for _, g in ordenado.groupby("id_fluxo", sort=False):
            a, ts, p = g["alvo"].to_list(), g["timestamp"].to_list(), g["pred"].to_list()
            for i in range(1, len(a)):
                if ts[i] - ts[i - 1] <= limite and a[i - 1] == "OK" and a[i] != "OK":
                    n += 1
                    det += p[i] != "OK"
        ev = metricas_eventos(sub, pred, limite)
        alerta = score >= cab.limiar_alerta
        fa = falsos_alertas(sub, alerta, nao_ok, cab.metadados["mediana_intervalo_treino_s"])
        horas = len(sub) * cab.metadados["mediana_intervalo_treino_s"] / 3600
        bloco = {
            "matriz_igual": oficial["matriz_confusao"] == indep["matriz"],
            "macro_f1": [oficial["macro_f1"], indep["macro_f1"]],
            "balanced_accuracy": [oficial["balanced_accuracy"], indep["balanced_accuracy"]],
            "inicios_evento": [[ev["inicios_nao_ok"]["n"], ev["inicios_nao_ok"]["detectados_nao_ok"]], [n, det]],
            "falsos_por_fluxo_hora": [fa["falsos_por_fluxo_hora"], float((alerta & ~nao_ok).sum() / horas)],
        }
        if sp == "validacao":
            lim = limiar_max_f1(nao_ok, score)
            # busca exaustiva vetorizada: F1 para cada limiar candidato (valores únicos do score)
            ordem = np.argsort(-score, kind="stable")
            ss, yy = score[ordem], nao_ok[ordem].astype(int)
            fim = np.r_[np.flatnonzero(np.diff(ss) != 0), len(ss) - 1]
            tp = np.cumsum(yy)[fim]
            k = fim + 1
            f1 = 2 * tp / (k + yy.sum())
            bloco["limiar_max_f1"] = {"funcao": [lim["limiar"], lim["f1"]],
                                      "exaustivo": [float(ss[fim][np.argmax(f1)]), float(f1.max())]}
        cal = calibracao_binaria(nao_ok, score)
        caixa = np.minimum((np.clip(score, 0, 1) * 10).astype(int), 9)
        ece = sum((caixa == b).mean() * abs(score[caixa == b].mean() - nao_ok[caixa == b].mean())
                  for b in range(10) if (caixa == b).any())
        bloco["ece"] = [cal["ece"], float(ece)]
        saida[sp] = bloco
    return saida


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--amostra", type=int, default=2000)
    args = ap.parse_args()
    cfg = comum.config_nodewatch()
    modelo = ModeloUnificado.carregar(NW / "artefatos_ml")
    comum.log("métricas da rede e regra de classe_atual")
    rede = verificar_metricas_rede(modelo, cfg)
    comum.log("atributos financeiros: vetorizado × força bruta")
    fin = verificar_atributos(modelo, cfg, args.amostra)
    comum.salvar("b_verificacao_implementacao", {"ambiente": comum.ambiente(), "rede": rede, "financeiro": fin})
    comum.log("ok: resultados/b_verificacao_implementacao.json")


if __name__ == "__main__":
    main()
