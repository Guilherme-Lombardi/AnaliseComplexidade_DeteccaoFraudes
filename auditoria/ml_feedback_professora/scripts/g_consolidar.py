"""Consolida os resultados brutos em tabelas comparativas (resultados/TABELAS.md).

Também estima a incerteza das diferenças de qualidade respeitando a
dependência dos dados:
* rede: bootstrap pareado por fluxo (reamostra id_fluxo inteiros, 2.000 vezes),
  porque medições do mesmo fluxo são correlacionadas no tempo;
* lavagem: métricas por dia do teste (2 dias). Não há intervalo de confiança:
  tentativas de lavagem ligam várias contas e transações, e 2 dias não
  sustentam um intervalo honesto.

Uso: python scripts/g_consolidar.py
"""

from __future__ import annotations

import comum  # noqa: F401

import json
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, f1_score

from src.ml.esquemas import CLASSES_REDE
from src.ml.experimentos import _dados_rede
from src.ml.preparacao import MINUTOS_DIA

R = comum.RESULTADOS
FAMILIAS = {"lr": "Regressão logística", "hgb": "HistGradientBoosting", "rf": "Random Forest (grade de produção)",
            "rf_nb": "Random Forest (configuração do notebook da professora)",
            "rf_red": "Random Forest com 50 árvores (mesma folha da produção)",
            "rf_busca": "Random Forest (busca com 4 tentativas)", "xgb": "XGBoost (hist, CPU)"}
SO_LAVAGEM = {"rf_busca"}
SO_REDE = {"rf_nb", "rf_red"}
CLASSES = np.asarray(CLASSES_REDE, dtype=object)


def _ler(nome: str) -> Optional[Dict[str, Any]]:
    p = R / f"{nome}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None


def _ms(x: Optional[float]) -> str:
    return "—" if x is None else f"{x * 1000:.1f}".replace(".", ",")


def _int(x: float) -> str:
    return f"{x:,.0f}".replace(",", ".")


def _num(x: Optional[float], casas: int = 3) -> str:
    return "—" if x is None else f"{x:.{casas}f}".replace(".", ",")


def tabela_rede(regras: Dict[str, Any]) -> List[str]:
    linhas = ["| Candidato | Treino (ajuste) | Macro-F1 val | Macro-F1 teste | Recall RISCO / FALHA (teste) | "
              "Balanced acc. (teste) | Inícios de evento detectados | Falsos alertas por fluxo-hora | "
              "Treino (s, mediana de 3) | Latência 1 linha, ms (mediana / p99) | Vazão lote (linhas/s) | "
              "Memória de pico no ajuste (MB) | Tamanho joblib compress=3 (MB = 10⁶ bytes) | Status |",
              "|" + "---|" * 14]
    for nome, rot in (("R0_majoritaria", "Classe majoritária"), ("R1_persistencia", "Persistência (classe_atual)"),
                      ("R2_regra_limiares", "Regra de limiares da medição atual")):
        v, t = regras["validacao"][nome], regras["teste"][nome]
        pc = t["por_classe"]
        linhas.append(f"| {rot} | sem ajuste | {_num(v['macro_f1'])} | {_num(t['macro_f1'])} | "
                      f"{_num(pc['RISCO']['recall'])} / {_num(pc['FALHA']['recall'])} | {_num(t['balanced_accuracy'])} | "
                      f"{_num(t['inicios_evento_detectados'])} | {_num(t['alerta_nao_ok']['falsos_por_fluxo_hora'], 2)} | "
                      f"0 | ~0 | — | — | — | medido |")
    r3 = next(k for k in regras["teste"] if k.startswith("R3_"))
    v, t = regras["validacao"][r3], regras["teste"][r3]
    pc = t["por_classe"]
    linhas.append(f"| Pior estado das últimas k medições ({r3[3:]}, k no treino) | regra ajustada | {_num(v['macro_f1'])} | "
                  f"{_num(t['macro_f1'])} | {_num(pc['RISCO']['recall'])} / {_num(pc['FALHA']['recall'])} | "
                  f"{_num(t['balanced_accuracy'])} | {_num(t['inicios_evento_detectados'])} | "
                  f"{_num(t['alerta_nao_ok']['falsos_por_fluxo_hora'], 2)} | ~0 | ~0 | — | — | — | medido |")
    for fam, rot in FAMILIAS.items():
        if fam in SO_LAVAGEM:
            continue
        b = _ler(f"e_benchmark_rede_{fam}")
        if b is None:
            linhas.append(f"| {rot} | — | — | — | — | — | — | — | — | — | — | — | — | não medido |")
            continue
        q = b["qualidade_semente_42"]
        v, t = q["validacao"]["multiclasse"], q["teste"]["multiclasse"]
        lat = b["inferencia"][f"latencia_1_linha_threads_{b['ambiente']['threads']}"]
        pico = max(f["ajuste_estimador"]["acrescimo_pico_mb"] for f in b["ajustes_finais"])
        linhas.append(
            f"| {rot} {b['escolhido']['params']} | treino 28/09–03/10 | {_num(v['macro_f1'])} | {_num(t['macro_f1'])} | "
            f"{_num(t['por_classe']['RISCO']['recall'])} / {_num(t['por_classe']['FALHA']['recall'])} | "
            f"{_num(t['balanced_accuracy'])} | {_num(q['teste']['eventos']['inicios_nao_ok']['taxa_deteccao'])} | "
            f"{_num(q['teste']['alertas_no_limiar_da_validacao']['falsos_por_fluxo_hora'], 2)} | "
            f"{_num(b['tempo_ajuste_final']['mediana_s'], 1)} | {_ms(lat['mediana_s'])} / {_ms(lat.get('p99_s'))} | "
            f"{_int(b['inferencia']['vazao_pipeline_linhas_por_s'])} | {_int(pico)} | "
            f"{_num(b['tamanho']['joblib_compress3_bytes'] / 1e6, 2)} | medido |")
    return linhas


def tabela_lavagem(regras: Dict[str, Any]) -> List[str]:
    linhas = ["| Candidato | AP val | AP teste | Precisão / recall / F1 no limiar da validação (teste) | "
              "Falsos positivos por 10 mil (teste) | Recall@1000 por dia (09/09; 10/09) | Treino (s, mediana de 3) | "
              "Latência 1 linha, ms (mediana / p99) | Vazão lote (linhas/s) | Memória de pico no ajuste (MB) | "
              "Tamanho joblib compress=3 (MB = 10⁶ bytes) | Status |", "|" + "---|" * 12]
    t, v = regras["teste"], regras["validacao"]
    linhas.append(f"| Prevalência (constante) | {_num(v['AP']['F0_prevalencia'], 4)} | {_num(t['AP']['F0_prevalencia'], 4)} | "
                  f"— | — | — | 0 | ~0 | — | — | — | medido |")
    for chave, rot in (("F1_taxa_formato", "Taxa de lavagem do formato (treino)"),):
        d = t["decisoes"][chave]
        linhas.append(f"| {rot} | {_num(v['AP']['F1_taxa_formato'], 4)} | {_num(t['AP']['F1_taxa_formato'], 4)} | "
                      f"{_num(d['precisao'])} / {_num(d['recall'])} / {_num(d['f1'])} | {_num(d['falsos_por_10k'], 1)} | — | "
                      f"0 | ~0 | — | — | — | medido |")
    for chave in t["decisoes"]:
        if chave.startswith(("F2_", "F3_")):
            d = t["decisoes"][chave]
            ap = (f"{_num(v['AP']['F2_contagem_motivos'], 4)} | {_num(t['AP']['F2_contagem_motivos'], 4)}"
                  if chave.startswith("F2_") else "— (sem ranking) | — (sem ranking)")
            linhas.append(f"| Regra {chave} | {ap} | {_num(d['precisao'])} / {_num(d['recall'])} / {_num(d['f1'])} | "
                          f"{_num(d['falsos_por_10k'], 1)} | — | ~0 | ~0 | — | — | — | medido |")
    for fam, rot in FAMILIAS.items():
        if fam in SO_REDE:
            continue
        b = _ler(f"e_benchmark_lavagem_{fam}")
        if b is None:
            linhas.append(f"| {rot} | — | — | — | — | — | — | — | — | — | — | não medido |")
            continue
        q = b["qualidade_semente_42"]
        te = q["teste"]
        dias = te["por_dia_topk"]
        lat = b["inferencia"][f"latencia_1_linha_threads_{b['ambiente']['threads']}"]
        pico = max(f["ajuste_estimador"]["acrescimo_pico_mb"] for f in b["ajustes_finais"])
        r1000 = "; ".join(_num(dias[k]["recall@1000"]) for k in sorted(dias))
        linhas.append(
            f"| {rot} {b['escolhido']['params']} | {_num(q['validacao']['average_precision'], 4)} | "
            f"{_num(te['average_precision'], 4)} | {_num(te['precisao'])} / {_num(te['recall'])} / {_num(te['f1'])} | "
            f"{_num(te['falsos_alertas_por_10k'], 1)} | {r1000} | {_num(b['tempo_ajuste_final']['mediana_s'], 1)} | "
            f"{_ms(lat['mediana_s'])} / {_ms(lat.get('p99_s'))} | {b['inferencia']['vazao_pipeline_linhas_por_s']:,.0f} | "
            f"{pico:,.0f} | {b['tamanho']['joblib_compress3_bytes'] / 2**20:,.1f} | medido |")
    return linhas


def bootstrap_rede(B: int = 2000) -> Dict[str, Any]:
    cfg = comum.config_nodewatch()
    s, _ = _dados_rede(cfg)
    sub = s[s["split"] == "teste"].reset_index(drop=True)
    y = sub["alvo"].to_numpy(dtype=object)
    preds = {"persistencia": sub["classe_atual"].to_numpy(dtype=object)}
    for fam in FAMILIAS:
        arq = comum.TRABALHO / "predicoes" / f"rede_{fam}.npz"
        if arq.is_file():
            preds[fam] = CLASSES[np.argmax(np.load(arq)["p_te"], axis=1)]
    fluxos, cod = np.unique(sub["id_fluxo"].to_numpy(), return_inverse=True)
    mapa = {c: i for i, c in enumerate(CLASSES_REDE)}
    yi = np.array([mapa[v] for v in y])
    # matriz de confusão (9 células) de cada fluxo, por modelo: reamostrar fluxos = somar linhas
    por_fluxo = {}
    for k, p in preds.items():
        celula = yi * 3 + np.array([mapa[v] for v in p])
        por_fluxo[k] = np.zeros((len(fluxos), 9))
        np.add.at(por_fluxo[k], (cod, celula), 1)

    def macro_f1(cm9: np.ndarray) -> np.ndarray:
        cm = cm9.reshape(-1, 3, 3)
        tp = np.diagonal(cm, axis1=1, axis2=2)
        prev, real = cm.sum(axis=1), cm.sum(axis=2)
        with np.errstate(invalid="ignore", divide="ignore"):
            f1 = np.where(prev + real > 0, 2 * tp / (prev + real), 0.0)
        return f1.mean(axis=1)

    rng = np.random.default_rng(comum.SEMENTE)
    mult = np.stack([np.bincount(rng.integers(0, len(fluxos), len(fluxos)), minlength=len(fluxos))
                     for _ in range(B)])  # B x fluxos
    f_boot = {k: macro_f1(mult @ c) for k, c in por_fluxo.items()}
    pares = [(a, "rf") for a in preds if a != "rf"]
    saida = {}
    for a, b in pares:
        v = f_boot[a] - f_boot[b]
        ponto = (f1_score(y, preds[a], labels=list(CLASSES_REDE), average="macro")
                 - f1_score(y, preds[b], labels=list(CLASSES_REDE), average="macro"))
        saida[f"{a} - {b}"] = {"diferenca_macro_f1": float(ponto), "ic95": [float(np.quantile(v, 0.025)),
                                                                             float(np.quantile(v, 0.975))],
                               "fracao_bootstrap_maior_que_zero": float((v > 0).mean())}
    return {"metodo": f"bootstrap pareado por id_fluxo ({len(fluxos)} fluxos, B={B})", "pares": saida}


def lavagem_por_dia() -> Dict[str, Any]:
    teste = pd.read_parquet(comum.TRABALHO / "financeiro" / "teste.parquet", columns=["_rotulo", "_minuto"])
    y = teste["_rotulo"].to_numpy()
    dia = pd.to_datetime(teste["_minuto"].to_numpy() // MINUTOS_DIA, unit="D").strftime("%Y-%m-%d").to_numpy()
    saida = {}
    for fam in FAMILIAS:
        arq = comum.TRABALHO / "predicoes" / f"lavagem_{fam}.npz"
        if arq.is_file():
            s = np.load(arq)["p_te"][:, 1]
            saida[fam] = {d: float(average_precision_score(y[dia == d], s[dia == d])) for d in np.unique(dia)}
    return saida


def main() -> None:
    regras = _ler("d_regras")
    linhas = ["# Tabelas da auditoria (geradas por scripts/g_consolidar.py)", ""]
    linhas += ["## Rede — estado da próxima medição (teste 05/10/2026, 46.105 medições)", ""]
    linhas += tabela_rede(regras["rede"]) + [""]
    linhas += ["## Lavagem — IBM AML HI-Small (teste 09–10/09/2022, 862.792 transações, 956 positivas)", ""]
    linhas += tabela_lavagem(regras["lavagem"]) + [""]
    busca = []
    for dom in ("rede", "lavagem"):
        for fam, rot in FAMILIAS.items():
            b = _ler(f"e_benchmark_{dom}_{fam}")
            if b:
                vs = b["variacao_por_semente"]
                busca.append(f"| {dom} | {rot} | {b['busca']['tentativas']} | {_num(b['busca']['segundos_total'], 1)} | "
                             f"{b['escolhido']['params']} | {_num(vs['validacao']['min_s'], 4)}–{_num(vs['validacao']['max_s'], 4)} | "
                             f"{_num(vs['teste']['min_s'], 4)}–{_num(vs['teste']['max_s'], 4)} |")
    linhas += ["## Orçamento de busca e variação por semente", "",
               "| Domínio | Família | Tentativas | Segundos (busca) | Escolhido | Métrica val (sementes 42–44) | "
               "Métrica teste (sementes 42–44) |", "|---|---|---|---|---|---|---|"] + busca + [""]
    boot = bootstrap_rede()
    dias = lavagem_por_dia()
    linhas += ["## Incerteza", "", f"Rede: {boot['metodo']}.", "",
               "| Diferença no teste | Macro-F1 | IC 95% | Fração > 0 |", "|---|---|---|---|"]
    for k, v in boot["pares"].items():
        linhas.append(f"| {k} | {_num(v['diferenca_macro_f1'], 4)} | [{_num(v['ic95'][0], 4)}; {_num(v['ic95'][1], 4)}] | "
                      f"{_num(v['fracao_bootstrap_maior_que_zero'], 3)} |")
    linhas += ["", "Lavagem: AP por dia do teste.", "", "| Família | " + " | ".join(sorted(next(iter(dias.values())))) + " |",
               "|---|---|---|"]
    for fam, v in dias.items():
        linhas.append(f"| {FAMILIAS[fam]} | " + " | ".join(_num(v[d], 4) for d in sorted(v)) + " |")
    (R / "TABELAS.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    comum.salvar("g_consolidado", {"bootstrap_rede": boot, "lavagem_ap_por_dia": dias})
    comum.log("ok: resultados/TABELAS.md")


if __name__ == "__main__":
    main()
