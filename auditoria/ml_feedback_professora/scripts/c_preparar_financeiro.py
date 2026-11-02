"""Atributos financeiros para os experimentos da auditoria (mesmo protocolo do treino).

Reproduz ``treinar_lavagem`` até a matriz de atributos: leitura, divisão por
dia, ajuste do preparador no treino, subamostragem de 20% dos negativos do
treino (semente 42, peso 5) e atributos point-in-time de treino amostrado,
validação e teste. Mede tempo e memória de cada etapa e grava os blocos em
parquet na pasta de trabalho (fora do repositório) para os scripts seguintes.

Uso: python scripts/c_preparar_financeiro.py
"""

from __future__ import annotations

import comum  # noqa: F401

import joblib
import numpy as np
import pandas as pd

from src.ml.ingestao import ler_hismall
from src.ml.modelos import ModeloUnificado
from src.ml.preparacao import (PreparadorFinanceiro, amostrar_treino_financeiro, atribuir_split_financeiro,
                               atributos_financeiros)

NW = comum.CAM["nodewatch"]
PASTA = comum.TRABALHO / "financeiro"


def main() -> None:
    cfg = comum.config_nodewatch()
    fin = cfg["financeiro"]
    PASTA.mkdir(parents=True, exist_ok=True)
    reg = {}
    with comum.medir(reg, "leitura_csv_zip"):
        dados = ler_hismall(fin["transacoes"])
    t = dados.trans
    y = t["rotulo"].to_numpy()
    split = atribuir_split_financeiro(t["minuto"].to_numpy(), fin)
    idx = {sp: np.flatnonzero(split == sp) for sp in ("treino", "validacao", "teste")}
    with comum.medir(reg, "ajuste_preparador_treino"):
        prep = PreparadorFinanceiro.ajustar(t.iloc[idx["treino"]])
    salvo: PreparadorFinanceiro = ModeloUnificado.carregar(NW / "artefatos_ml").codificadores["financeiro"]
    assert prep.cambio == salvo.cambio and prep.taxa_formato == salvo.taxa_formato, "preparador difere do salvo"
    rel, pesos = amostrar_treino_financeiro(y[idx["treino"]], fin["fracao_negativos_treino"], comum.SEMENTE)
    idx_tr = idx["treino"][rel]
    consulta = np.concatenate([idx_tr, idx["validacao"], idx["teste"]])
    comum.log(f"atributos de {len(consulta):,} transações")
    with comum.medir(reg, "atributos_point_in_time"):
        X = atributos_financeiros(t, consulta, prep)
    X = X[salvo.colunas]
    cortes = np.cumsum([len(idx_tr), len(idx["validacao"])])
    blocos = {"treino": (0, cortes[0], idx_tr), "validacao": (cortes[0], cortes[1], idx["validacao"]),
              "teste": (cortes[1], len(X), idx["teste"])}
    resumo = {}
    for nome, (ini, fim, ids) in blocos.items():
        b = X.iloc[ini:fim].reset_index(drop=True).copy()
        b["_rotulo"] = y[ids]
        b["_id_transacao"] = t["id_transacao"].to_numpy()[ids]
        b["_minuto"] = t["minuto"].to_numpy()[ids]
        b["_formato"] = t["formato"].astype(str).to_numpy()[ids]
        if nome == "treino":
            b["_peso"] = pesos
        b.to_parquet(PASTA / f"{nome}.parquet", index=False)
        resumo[nome] = {"linhas": int(len(b)), "positivos": int(b["_rotulo"].sum()),
                        "bytes_parquet": (PASTA / f"{nome}.parquet").stat().st_size}
    joblib.dump(salvo, PASTA / "preparador_salvo.joblib")
    comum.salvar("c_preparacao_financeiro", {
        "ambiente": comum.ambiente(),
        "fonte": {"arquivo": comum.CAM["transacoes"].name, "sha256": dados.sha256, "linhas": int(len(t))},
        "protocolo": {k: fin[k] for k in ("inicio", "treino_ate", "validacao_ate", "teste_ate", "inicio_cauda",
                                          "fracao_negativos_treino")} | {"semente": comum.SEMENTE},
        "atributos": len(salvo.colunas),
        "tipo_numerico": "float32",
        "blocos": resumo,
        "tempos_memoria": reg,
        "nota": "A leitura e os atributos são comuns a todos os algoritmos; o custo de treino de cada "
                "algoritmo é medido à parte em e_benchmark.py.",
    })
    comum.log("ok")


if __name__ == "__main__":
    main()
