"""Auditoria de contas e padrões do HI-Small (pendente no treino de 26/10).

* ``HI-Small_accounts.csv``: atributos de entidade revelam a resposta? (mesmo
  critério de ``src/ml/auditoria.py:_auditar_contas``, medido no treino);
* ``HI-Small_Patterns.txt``: casamento com as transações, tentativas que
  atravessam períodos (dependência entre eventos de um episódio);
* recall por tipo de padrão e por tentativa nova × iniciada antes do teste,
  para o modelo salvo e para os candidatos do benchmark (se houver previsões);
* contas conhecidas × inéditas: recall conforme a conta de origem já ter
  aparecido no treino.
Padrões e contas nunca viram atributo: só servem para auditar e estratificar.

Uso: python scripts/f_contas_padroes.py
"""

from __future__ import annotations

import comum  # noqa: F401

from typing import Any, Dict

import numpy as np
import pandas as pd

from src.ml.auditoria import auditar_financeiro
from src.ml.ingestao import casar_padroes, ler_contas, ler_hismall, ler_padroes
from src.ml.modelos import ModeloUnificado
from src.ml.preparacao import atribuir_split_financeiro, minuto_de

NW = comum.CAM["nodewatch"]


def _recall(grupo: pd.Series, alerta: np.ndarray) -> Dict[str, Any]:
    q = pd.DataFrame({"g": grupo.astype(str).to_numpy(), "a": alerta})
    r = q.groupby("g")["a"].agg(["size", "sum"])
    return {g: {"n": int(v["size"]), "detectados": int(v["sum"]), "recall": float(v["sum"] / v["size"])}
            for g, v in r.iterrows()}


def main() -> None:
    cfg = comum.config_nodewatch()
    fin = cfg["financeiro"]
    reg: Dict[str, Any] = {}
    with comum.medir(reg, "leitura"):
        dados = ler_hismall(fin["transacoes"])
        contas = ler_contas(comum.CAM["contas"])
        padroes = ler_padroes(comum.CAM["padroes"])
    with comum.medir(reg, "casamento_padroes"):
        casados = casar_padroes(dados, padroes)
    comum.log("auditoria de contas e padrões")
    aud = auditar_financeiro(dados, fin, contas, casados)
    t = dados.trans
    split = atribuir_split_financeiro(t["minuto"].to_numpy(), fin)

    # Estratificação do teste
    teste = pd.read_parquet(comum.TRABALHO / "financeiro" / "teste.parquet",
                            columns=["_id_transacao", "_rotulo"])
    modelo = ModeloUnificado.carregar(NW / "artefatos_ml")
    cab = modelo.cabeca("lavagem")
    prep = modelo.codificadores["financeiro"]
    X_te = pd.read_parquet(comum.TRABALHO / "financeiro" / "teste.parquet", columns=prep.colunas)
    scores = {"modelo_RF_salvo": (cab.probabilidades(X_te)[:, 1], cab.limiar_alerta)}
    del X_te
    pasta_pred = comum.TRABALHO / "predicoes"
    for fam in ("rf", "xgb", "hgb", "lr"):
        arq = pasta_pred / f"lavagem_{fam}.npz"
        bench = comum.RESULTADOS / f"e_benchmark_lavagem_{fam}.json"
        if arq.is_file() and bench.is_file():
            import json
            lim = json.loads(bench.read_text(encoding="utf-8"))["qualidade_semente_42"]["limiar_validacao"]["limiar"]
            scores[f"benchmark_{fam}"] = (np.load(arq)["p_te"][:, 1], lim)

    ok = casados["id_transacao"].notna()
    cs = casados[ok].copy()
    cs["id_transacao"] = cs["id_transacao"].astype(np.int64)
    inicio = cs.groupby("tentativa")["minuto"].transform("min")
    cs["inicio_tentativa"] = np.where(inicio < minuto_de(fin["validacao_ate"]), "iniciada_antes_do_teste", "nova_no_teste")
    info = cs.drop_duplicates("id_transacao").set_index("id_transacao")[["tipo_padrao", "inicio_tentativa"]]
    pos = teste[teste["_rotulo"] == 1].copy()
    pos["tipo_padrao"] = pos["_id_transacao"].map(info["tipo_padrao"]).fillna("sem_padrao")
    pos["inicio_tentativa"] = pos["_id_transacao"].map(info["inicio_tentativa"]).fillna("sem_padrao")
    # conta de origem já vista no treino (como origem ou destino)?
    tr = split == "treino"
    vistas = np.zeros(len(dados.nomes_contas), dtype=bool)
    vistas[t["conta_origem"].to_numpy()[tr]] = True
    vistas[t["conta_destino"].to_numpy()[tr]] = True
    origem_te = t["conta_origem"].to_numpy()[teste["_id_transacao"].to_numpy()]
    destino_te = t["conta_destino"].to_numpy()[teste["_id_transacao"].to_numpy()]
    conhecida = np.where(vistas[origem_te], "origem_vista_no_treino", "origem_inedita")
    mask_pos = (teste["_rotulo"] == 1).to_numpy()

    estrat: Dict[str, Any] = {}
    for nome, (score, lim) in scores.items():
        alerta = score >= lim
        estrat[nome] = {
            "limiar": float(lim),
            "recall_por_tipo_padrao": _recall(pos["tipo_padrao"], alerta[mask_pos]),
            "recall_por_inicio_da_tentativa": _recall(pos["inicio_tentativa"], alerta[mask_pos]),
            "recall_por_conta_origem": _recall(pd.Series(conhecida[mask_pos]), alerta[mask_pos]),
            "falsos_por_conta_origem": {g: float((alerta & ~mask_pos & (conhecida == g)).sum())
                                        for g in np.unique(conhecida)},
        }
    cobertura = {
        "transacoes_teste_com_origem_vista_no_treino": float(vistas[origem_te].mean()),
        "transacoes_teste_com_destino_visto_no_treino": float(vistas[destino_te].mean()),
        "positivos_teste_com_origem_vista_no_treino": float(vistas[origem_te[mask_pos]].mean()),
    }
    # tentativas: quantas linhas de padrão casam; em quantos períodos cada tentativa aparece
    sp_ids = pd.Series(split[cs["id_transacao"].to_numpy()], index=cs.index)
    periodos = cs.assign(sp=sp_ids).groupby("tentativa")["sp"].agg(lambda x: "+".join(sorted(set(x))))
    comum.salvar("f_contas_padroes", {
        "ambiente": comum.ambiente(),
        "arquivos": {k: {"arquivo": comum.CAM[k].name, "sha256": comum.sha256(comum.CAM[k])}
                     for k in ("contas", "padroes", "transacoes")},
        "auditoria_contas": aud.get("contas"),
        "auditoria_padroes": aud.get("padroes"),
        "padroes_lidos": {"linhas": int(len(padroes)), "casadas": int(ok.sum()),
                          "tentativas": int(padroes["tentativa"].nunique())},
        "tentativas_por_combinacao_de_periodos": periodos.value_counts().to_dict(),
        "cobertura_contas": cobertura,
        "estratificacao_teste": estrat,
        "tempos_memoria": reg,
    })
    comum.log("ok: resultados/f_contas_padroes.json")


if __name__ == "__main__":
    main()
