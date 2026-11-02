"""Onde está o custo da inferência de lavagem: atributos ou classificador?

``atributos_financeiros`` reconstrói os índices ordenados (lexsort sobre todo o
histórico) a cada chamada. Este script mede o tempo para pontuar lotes de 1,
1.000, 100.000 e 862.792 transações do teste contra o histórico completo
(5,08 milhões de transações) e separa atributos e classificador (modelo salvo).

Uso: python scripts/h_custo_atributos.py
"""

from __future__ import annotations

import comum  # noqa: F401

import time

import numpy as np

from src.ml.ingestao import ler_hismall
from src.ml.modelos import ModeloUnificado
from src.ml.preparacao import atribuir_split_financeiro, atributos_financeiros

NW = comum.CAM["nodewatch"]


def main() -> None:
    cfg = comum.config_nodewatch()
    modelo = ModeloUnificado.carregar(NW / "artefatos_ml")
    cab = modelo.cabeca("lavagem")
    prep = modelo.codificadores["financeiro"]
    t = ler_hismall(cfg["financeiro"]["transacoes"]).trans
    idx_te = np.flatnonzero(atribuir_split_financeiro(t["minuto"].to_numpy(), cfg["financeiro"]) == "teste")
    rng = np.random.default_rng(comum.SEMENTE)
    linhas = []
    for n, reps in ((1, 5), (1000, 3), (100_000, 3), (len(idx_te), 2)):
        tempos_attr, tempos_mod = [], []
        for _ in range(reps):
            q = np.sort(rng.choice(idx_te, n, replace=False)) if n < len(idx_te) else idx_te
            t0 = time.perf_counter()
            X = atributos_financeiros(t, q, prep)
            t1 = time.perf_counter()
            cab.probabilidades(X)
            t2 = time.perf_counter()
            tempos_attr.append(t1 - t0)
            tempos_mod.append(t2 - t1)
        linhas.append({"transacoes_pontuadas": int(n), "historico": int(len(t)),
                       "atributos": comum.resumo_tempos(tempos_attr), "classificador_rf": comum.resumo_tempos(tempos_mod)})
        comum.log(f"{n:>7} transações: atributos {np.median(tempos_attr):.3f} s; RF {np.median(tempos_mod):.3f} s")
    comum.salvar("h_custo_atributos", {
        "ambiente": comum.ambiente(), "medicoes": linhas,
        "nota": "Sem aquecimento separado: cada chamada reconstrói os índices, então a 1ª e as demais custam igual. "
                "O classificador é a RF salva (n_jobs=4).",
    })


if __name__ == "__main__":
    main()
