"""Regras explícitas e referenciais simples × modelo aprendido.

Rede (alvo = estado da PRÓXIMA medição do fluxo):
  R0  classe majoritária do treino (sempre OK);
  R1  persistência: repete ``classe_atual`` (disponível no instante t);
  R2  regra de limiares da medição atual (``regra_classe_atual``: a mesma
      regra que reproduz o rótulo), sem usar a coluna ``classe_atual``;
  R3  pior estado das últimas k medições do fluxo (k ajustado no TREINO).
Lavagem (alvo = ``Is Laundering`` da transação):
  F0  prevalência (score constante);
  F1  taxa de lavagem do formato de pagamento no treino (ranking);
  F2  número de "motivos verificáveis" (as mesmas condições de
      ``PreparadorFinanceiro.motivos``; limiares p99 do treino);
  F3  conjunções explícitas (formato de risco, par novo, repasse rápido,
      dispersão), escolhidas por F1 na VALIDAÇÃO.
Cada regra é comparada ao modelo salvo no mesmo ponto operacional: o modelo
emite o mesmo número de alertas que a regra (top-N pelo score).

Uso: python scripts/d_regras.py
"""

from __future__ import annotations

import comum  # noqa: F401

from typing import Any, Dict

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score

from src.ml.auditoria import regra_classe_atual
from src.ml.avaliacao import falsos_alertas, limiar_max_f1, metricas_eventos, metricas_multiclasse
from src.ml.esquemas import CLASSES_REDE
from src.ml.experimentos import _dados_rede
from src.ml.modelos import ModeloUnificado
from src.ml.preparacao import matriz_rede

NW = comum.CAM["nodewatch"]
CLASSES = np.asarray(CLASSES_REDE, dtype=object)
SEVERIDADE = {"OK": 0, "RISCO": 1, "FALHA": 2}


def _ponto_operacional_modelo(score: np.ndarray, positivo: np.ndarray, n_alertas: int) -> Dict[str, float]:
    """Precisão e recall do modelo quando emite exatamente ``n_alertas`` (maiores scores)."""
    if n_alertas <= 0:
        return {"alertas": 0, "precisao": None, "recall": 0.0}
    topo = np.argsort(-score, kind="stable")[:n_alertas]
    tp = int(positivo[topo].sum())
    return {"alertas": int(n_alertas), "precisao": tp / n_alertas, "recall": tp / max(int(positivo.sum()), 1)}


def _decisao(positivo: np.ndarray, alerta: np.ndarray) -> Dict[str, float]:
    tp = int((alerta & positivo).sum())
    n = int(alerta.sum())
    prec = tp / n if n else 0.0
    rec = tp / max(int(positivo.sum()), 1)
    return {"alertas": n, "precisao": prec, "recall": rec, "f1": 2 * prec * rec / (prec + rec) if prec + rec else 0.0}


# ---------------------------------------------------------------------------
def regras_rede(modelo: ModeloUnificado, cfg: Dict[str, Any]) -> Dict[str, Any]:
    cab = modelo.cabeca("estado_rede")
    s, _ = _dados_rede(cfg)  # ordenado por id_fluxo, timestamp
    med = cab.metadados["mediana_intervalo_treino_s"]
    limite = cab.metadados["multiplo_intervalo_consecutivo"] * med
    sev = s["classe_atual"].map(SEVERIDADE).to_numpy()
    g = pd.Series(sev).groupby(s["id_fluxo"].to_numpy())
    pior = {k: g.transform(lambda x, k=k: x.rolling(k, min_periods=1).max()).to_numpy().astype(int)
            for k in (1, 2, 3, 4, 6, 12)}
    tr = (s["split"] == "treino").to_numpy()
    y_tr = s.loc[tr, "alvo"].to_numpy(dtype=object)
    ajuste_k = {k: metricas_multiclasse(y_tr, CLASSES[v[tr]])["macro_f1"] for k, v in pior.items()}
    k_best = max(ajuste_k, key=ajuste_k.get)

    saida: Dict[str, Any] = {
        "definicoes": {
            "R0_majoritaria": "sempre OK (classe mais frequente no treino)",
            "R1_persistencia": "previsão(t+1) = classe_atual(t); disponível no instante da decisão",
            "R2_regra_limiares": "FALHA se rtt_ausente=1 ou razao_rtt_p99>1 ou perda_pct>=50; RISCO se "
                                 "razao_rtt_p95>1 ou razao_jitter_p95>1 ou perda_pct>0; senão OK (medição atual)",
            "R3_pior_estado_k": f"pior classe_atual entre as últimas k medições do fluxo; k={k_best} escolhido "
                                f"por macro-F1 no treino entre {list(pior)}",
            "alerta_das_regras": "previsão diferente de OK",
            "horizonte": "próxima medição do fluxo (mediana de 240 s)",
        },
        "ajuste_k_treino_macro_f1": ajuste_k,
    }
    for sp in ("validacao", "teste"):
        m = (s["split"] == sp).to_numpy()
        sub = s[m].reset_index(drop=True)
        y = sub["alvo"].to_numpy(dtype=object)
        nao_ok = y != "OK"
        proba = cab.probabilidades(matriz_rede(sub))
        score = proba[:, 1] + proba[:, 2]
        preds = {
            "R0_majoritaria": np.full(len(y), "OK", dtype=object),
            "R1_persistencia": sub["classe_atual"].to_numpy(dtype=object),
            "R2_regra_limiares": regra_classe_atual(sub).astype(object),
            f"R3_pior_estado_k{k_best}": CLASSES[pior[k_best][m]],
            "modelo_RF_salvo": CLASSES[np.argmax(proba, axis=1)],
        }
        bloco = {}
        for nome, pred in preds.items():
            mm = metricas_multiclasse(y, pred)
            alerta = pred != "OK" if nome != "modelo_RF_salvo" else score >= cab.limiar_alerta
            fa = falsos_alertas(sub, alerta, nao_ok, med)
            ev = metricas_eventos(sub, pred, limite)
            bloco[nome] = {
                "macro_f1": mm["macro_f1"], "balanced_accuracy": mm["balanced_accuracy"], "acuracia": mm["acuracia"],
                "por_classe": mm["por_classe"], "matriz_confusao": mm["matriz_confusao"],
                "alerta_nao_ok": _decisao(nao_ok, alerta) | {"falsos_por_fluxo_hora": fa["falsos_por_fluxo_hora"]},
                "inicios_evento_detectados": ev["inicios_nao_ok"]["taxa_deteccao"],
                "transicoes_acuracia": ev.get("transicoes", {}).get("acuracia"),
                "modelo_no_mesmo_numero_de_alertas": _ponto_operacional_modelo(score, nao_ok, int(alerta.sum()))
                if nome != "modelo_RF_salvo" else None,
            }
        saida[sp] = bloco
    return saida


# ---------------------------------------------------------------------------
def _flags(X: pd.DataFrame, formato: np.ndarray, prep: Any) -> Dict[str, np.ndarray]:
    fator = pd.Series(formato).map(prep.taxa_formato).fillna(0).to_numpy() / prep.taxa_base
    q = prep.quantis
    return {
        "formato_risco_5x": fator >= 5,
        "par_novo": X["par_novo"].to_numpy() == 1,
        "envios_24h_acima_p99": X["n_env_origem_24h"].to_numpy() > q["n_env_origem_24h_p99"],
        "fan_in_acima_p99": X["orig_distintas_destino"].to_numpy() > q["orig_distintas_destino_p99"],
        "fan_out_acima_p99": X["dest_distintos_origem"].to_numpy() > q["dest_distintos_origem_p99"],
        "valor_atipico_z3": np.abs(X["z_valor_origem"].to_numpy()) > 3,
        "repasse_menos_60min": X["min_desde_rec_origem"].to_numpy() < 60,
        "moedas_diferentes": X["moeda_diferente"].to_numpy() == 1,
    }


def regras_lavagem(modelo: ModeloUnificado) -> Dict[str, Any]:
    cab = modelo.cabeca("lavagem")
    pasta = comum.TRABALHO / "financeiro"
    prep = joblib.load(pasta / "preparador_salvo.joblib")
    blocos = {sp: pd.read_parquet(pasta / f"{sp}.parquet") for sp in ("validacao", "teste")}
    dados = {}
    for sp, b in blocos.items():
        X = b[prep.colunas]
        fl = _flags(X, b["_formato"].to_numpy(), prep)
        dados[sp] = {"y": b["_rotulo"].to_numpy().astype(bool), "flags": fl,
                     "taxa_formato": pd.Series(b["_formato"]).map(prep.taxa_formato).fillna(prep.taxa_base).to_numpy(),
                     "motivos": np.sum(np.stack(list(fl.values())), axis=0),
                     "score_modelo": cab.probabilidades(X)[:, 1]}

    def conjuncoes(fl: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        fan = fl["fan_in_acima_p99"] | fl["fan_out_acima_p99"]
        return {
            "formato_risco & par_novo": fl["formato_risco_5x"] & fl["par_novo"],
            "formato_risco & repasse<60min": fl["formato_risco_5x"] & fl["repasse_menos_60min"],
            "formato_risco & (fan>p99 | repasse<60min)": fl["formato_risco_5x"] & (fan | fl["repasse_menos_60min"]),
            "formato_risco & par_novo & (fan>p99 | repasse<60min)":
                fl["formato_risco_5x"] & fl["par_novo"] & (fan | fl["repasse_menos_60min"]),
        }

    va, te = dados["validacao"], dados["teste"]
    lim_fmt = limiar_max_f1(va["y"], va["taxa_formato"])
    f1_k = {k: _decisao(va["y"], va["motivos"] >= k)["f1"] for k in range(1, 9)}
    k_best = max(f1_k, key=f1_k.get)
    conj_va = {n: _decisao(va["y"], a) for n, a in conjuncoes(va["flags"]).items()}
    conj_best = max(conj_va, key=lambda n: conj_va[n]["f1"])
    saida: Dict[str, Any] = {
        "definicoes": {
            "limiares": {k: v for k, v in prep.quantis.items()},
            "taxa_base_treino": prep.taxa_base,
            "formatos_risco_5x": sorted(f for f, v in prep.taxa_formato.items() if v / prep.taxa_base >= 5),
            "nota_quantis": "p99 calculados no treino subamostrado (todos os positivos + 20% dos negativos), "
                            "como em src/ml/preparacao.py:registrar_quantis",
            "nota_valores": "nenhuma regra soma valores de moedas diferentes sem o câmbio estimado no treino; "
                            "não há limite monetário fixo",
        },
        "F1_limiar_taxa_formato_validacao": lim_fmt,
        "F2_f1_por_k_validacao": f1_k, "F2_k_escolhido": k_best,
        "F3_conjuncoes_validacao": conj_va, "F3_escolhida": conj_best,
        "frequencia_flags_positivos_validacao": {n: float(v[va["y"]].mean()) for n, v in va["flags"].items()},
        "frequencia_flags_negativos_validacao": {n: float(v[~va["y"]].mean()) for n, v in va["flags"].items()},
    }
    for sp, d in dados.items():
        y = d["y"]
        regras = {
            "F1_taxa_formato": d["taxa_formato"] >= lim_fmt["limiar"],
            f"F2_motivos>={k_best}": d["motivos"] >= k_best,
            f"F3_{conj_best}": conjuncoes(d["flags"])[conj_best],
        }
        bloco = {
            "positivos": int(y.sum()), "n": int(len(y)), "prevalencia": float(y.mean()),
            "AP": {"F0_prevalencia": float(y.mean()),
                   "F1_taxa_formato": float(average_precision_score(y, d["taxa_formato"])),
                   "F2_contagem_motivos": float(average_precision_score(y, d["motivos"])),
                   "modelo_RF_salvo": float(average_precision_score(y, d["score_modelo"]))},
            "decisoes": {},
        }
        for nome, alerta in regras.items():
            bloco["decisoes"][nome] = _decisao(y, alerta) | {
                "falsos_por_10k": float((alerta & ~y).sum() / len(y) * 1e4),
                "modelo_no_mesmo_numero_de_alertas": _ponto_operacional_modelo(d["score_modelo"], y, int(alerta.sum())),
            }
        alerta_m = d["score_modelo"] >= cab.limiar_alerta
        bloco["decisoes"]["modelo_RF_salvo_no_limiar"] = _decisao(y, alerta_m) | {
            "falsos_por_10k": float((alerta_m & ~y).sum() / len(y) * 1e4)}
        saida[sp] = bloco
    return saida


def main() -> None:
    cfg = comum.config_nodewatch()
    modelo = ModeloUnificado.carregar(NW / "artefatos_ml")
    comum.log("regras da rede")
    rede = regras_rede(modelo, cfg)
    comum.log("regras da lavagem")
    lav = regras_lavagem(modelo)
    comum.salvar("d_regras", {"ambiente": comum.ambiente(), "rede": rede, "lavagem": lav})
    comum.log("ok: resultados/d_regras.json")


if __name__ == "__main__":
    main()
