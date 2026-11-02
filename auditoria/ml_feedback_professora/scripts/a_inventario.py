"""Inventário e rastreabilidade do ML do NodeWatch.

* varre ``src/`` (análise estática) e lista as bibliotecas de ML importadas e
  as funções de NumPy usadas, com arquivo e linha;
* descreve o artefato salvo: algoritmo efetivo de cada cabeça, parâmetros,
  etapas do pipeline e tamanho das árvores;
* refaz as métricas documentadas a partir do artefato salvo e compara com
  ``docs/ml/resultados`` (verifica se modelo, código e relatório batem).

Uso: python scripts/a_inventario.py
"""

from __future__ import annotations

import comum  # noqa: F401  (threads e sys.path antes de numpy)

import ast
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pandas as pd

from src.ml.avaliacao import metricas_binarias, metricas_multiclasse
from src.ml.esquemas import CLASSES_REDE
from src.ml.experimentos import _dados_rede
from src.ml.modelos import CabecaClassificacao, ModeloUnificado
from src.ml.preparacao import MINUTOS_DIA, matriz_rede

NW = comum.CAM["nodewatch"]
BIBLIOTECAS_ML = ("sklearn", "xgboost", "lightgbm", "catboost", "torch", "tensorflow", "statsmodels", "scipy")
_ABSOLUTO = re.compile(r"^[A-Za-z]:[\\/]")


def varrer_codigo() -> Dict[str, Any]:
    importacoes: List[Dict[str, Any]] = []
    numpy_por_arquivo: Dict[str, Counter] = defaultdict(Counter)
    for arq in sorted((NW / "src").rglob("*.py")):
        rel = arq.relative_to(NW).as_posix()
        arvore = ast.parse(arq.read_text(encoding="utf-8"))
        for no in ast.walk(arvore):
            if isinstance(no, ast.ImportFrom) and no.module and no.module.split(".")[0] in BIBLIOTECAS_ML:
                for a in no.names:
                    importacoes.append({"arquivo": rel, "linha": no.lineno, "modulo": no.module, "nome": a.name})
            elif isinstance(no, ast.Import):
                for a in no.names:
                    if a.name.split(".")[0] in BIBLIOTECAS_ML:
                        importacoes.append({"arquivo": rel, "linha": no.lineno, "modulo": a.name, "nome": None})
            elif (isinstance(no, ast.Attribute) and isinstance(no.value, ast.Name) and no.value.id == "np"):
                numpy_por_arquivo[rel][no.attr] += 1
    estimadores = sorted({i["nome"] for i in importacoes if i["nome"] and re.search(
        r"Classifier|Regress|Regressor|Forest|Boost|SVC|SVR|KMeans|Isolation|Linear", i["nome"])})
    return {
        "importacoes_ml": importacoes,
        "estimadores_importados": estimadores,
        "regressores_para_alvo_continuo": [e for e in estimadores if e.endswith("Regressor") or e in (
            "LinearRegression", "Ridge", "Lasso", "SVR")],
        "numpy_funcoes_por_arquivo": {k: dict(v.most_common()) for k, v in numpy_por_arquivo.items()},
    }


def _complexidade_floresta(est: Any) -> Dict[str, Any]:
    if not hasattr(est, "estimators_"):
        return {}
    nos = np.array([e.tree_.node_count for e in est.estimators_])
    prof = np.array([e.tree_.max_depth for e in est.estimators_])
    folhas = np.array([e.tree_.n_leaves for e in est.estimators_])
    return {"arvores": int(len(nos)), "nos_total": int(nos.sum()), "nos_medio": float(nos.mean()),
            "profundidade_media": float(prof.mean()), "profundidade_max": int(prof.max()),
            "folhas_total": int(folhas.sum())}


def descrever_cabeca(nome: str, cab: Any) -> Dict[str, Any]:
    if not isinstance(cab, CabecaClassificacao):
        return {"tarefa": nome, "status": cab.status, "motivo": cab.motivo, "requisitos": cab.requisitos}
    est = cab.pipeline.named_steps["modelo"]
    chaves = ("n_estimators", "min_samples_leaf", "max_samples", "max_features", "max_depth", "class_weight",
              "criterion", "bootstrap", "random_state", "n_jobs", "C", "penalty", "solver", "max_iter",
              "learning_rate", "max_leaf_nodes", "max_iter")
    params = {k: v for k, v in est.get_params().items() if k in chaves}
    return {
        "tarefa": nome,
        "algoritmo_efetivo": f"{type(est).__module__}.{type(est).__qualname__}",
        "familia_declarada": cab.familia,
        "params_declarados": cab.params,
        "params_efetivos": params,
        "etapas_pipeline": [(n, f"{type(p).__module__}.{type(p).__qualname__}") for n, p in cab.pipeline.steps],
        "colunas_entrada": len(cab.colunas_entrada),
        "atributos_no_estimador": int(getattr(est, "n_features_in_", -1)),
        "classes": [str(c) for c in cab.classes],
        "classes_estimador": [str(c) for c in est.classes_],
        "limiar_alerta": cab.limiar_alerta,
        "usa_classe_atual": cab.usa_classe_atual,
        "versao": cab.metadados.get("versao"),
        "complexidade": _complexidade_floresta(est),
    }


def _sem_caminhos(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: _sem_caminhos(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sem_caminhos(v) for v in obj]
    if isinstance(obj, str) and _ABSOLUTO.match(obj):
        return Path(obj.replace("\\", "/")).name
    return obj


def reproduzir_rede(modelo: ModeloUnificado, cfg: Dict[str, Any]) -> Dict[str, Any]:
    cab = modelo.cabeca("estado_rede")
    s, rel = _dados_rede(cfg)
    hash_treino = [a["sha256"] for a in cab.metadados["arquivos"]]
    hash_agora = [a["sha256"] for a in rel["arquivos"]]
    doc = json.loads((NW / "docs/ml/resultados/avaliacao_estado_rede.json").read_text(encoding="utf-8"))
    saida: Dict[str, Any] = {"sha256_dados_treino": hash_treino, "sha256_dados_agora": hash_agora,
                             "mesmos_dados": hash_treino == hash_agora}
    classes = np.asarray(CLASSES_REDE, dtype=object)
    for sp in ("validacao", "teste"):
        sub = s[s["split"] == sp].reset_index(drop=True)
        proba = cab.probabilidades(matriz_rede(sub))
        m = metricas_multiclasse(sub["alvo"].to_numpy(dtype=object), classes[np.argmax(proba, axis=1)])
        ref = doc[sp]["modelo"]
        saida[sp] = {"macro_f1_recalculado": m["macro_f1"], "macro_f1_documentado": ref["macro_f1"],
                     "matriz_igual": m["matriz_confusao"] == ref["matriz_confusao"],
                     "proba_soma_1_max_desvio": float(np.abs(proba.sum(axis=1) - 1).max()),
                     "proba_fora_0_1": int(((proba < 0) | (proba > 1)).sum())}
    return saida


def reproduzir_lavagem(modelo: ModeloUnificado) -> Dict[str, Any]:
    cab = modelo.cabeca("lavagem")
    prep = modelo.codificadores["financeiro"]
    pasta_cache = NW / "artefatos_ml" / "cache"
    info = json.loads((pasta_cache / "financeiro_cache.json").read_text(encoding="utf-8"))
    doc = json.loads((NW / "docs/ml/resultados/avaliacao_lavagem.json").read_text(encoding="utf-8"))
    bloco = pd.read_parquet(pasta_cache / "financeiro_teste.parquet")
    y = bloco["_rotulo"].to_numpy()
    dia = pd.to_datetime(bloco["_minuto"].to_numpy() // MINUTOS_DIA, unit="D").strftime("%Y-%m-%d").to_numpy()
    score = cab.probabilidades(bloco[prep.colunas])[:, 1]
    m = metricas_binarias(y, score, cab.limiar_alerta, dia)
    ref = doc["teste"]["modelo"]
    return {
        "sha256_transacoes_treino": cab.metadados["sha256"],
        "sha256_cache_atributos": info["sha256"],
        "sha256_transacoes_agora": comum.sha256(comum.CAM["transacoes"]),
        "teste": {k: {"recalculado": m[k], "documentado": ref[k]} for k in
                  ("average_precision", "precisao", "recall", "f1", "falsos_positivos", "verdadeiros_positivos")},
    }


def linha_do_tempo() -> Dict[str, Any]:
    pasta = NW / "artefatos_ml"
    saida = {}
    for nome in ("log_treino_rede.txt", "log_treino_lavagem.txt", "log_avaliacao.txt"):
        linhas = (pasta / nome).read_text(encoding="utf-8", errors="replace").splitlines()
        horas = [l[1:9] for l in linhas if l.startswith("[")]
        saida[nome] = {"primeira": horas[0] if horas else None, "ultima": horas[-1] if horas else None,
                       "linhas": len(linhas)}
    meta = json.loads((pasta / "metadados_modelo.json").read_text(encoding="utf-8"))
    saida["artefato_salvo_em_utc"] = meta["metadados"].get("salvo_em")
    return saida


def main() -> None:
    cfg = comum.config_nodewatch()
    comum.log("varrendo src/")
    codigo = varrer_codigo()
    comum.log("carregando artefato salvo (somente leitura)")
    arq_modelo = NW / "artefatos_ml" / "modelo_unificado.joblib"
    modelo = ModeloUnificado.carregar(NW / "artefatos_ml")
    cabecas = [descrever_cabeca(n, c) for n, c in modelo.cabecas.items()]
    meta_art = json.loads((NW / "artefatos_ml/metadados_modelo.json").read_text(encoding="utf-8"))
    meta_doc = json.loads((NW / "docs/ml/resultados/metadados_modelo.json").read_text(encoding="utf-8"))
    comum.log("refazendo métricas da rede com o artefato")
    rede = reproduzir_rede(modelo, cfg)
    comum.log("refazendo métricas da lavagem com o artefato")
    lav = reproduzir_lavagem(modelo)
    dados = {}
    for chave in ("rede", "transacoes", "contas", "padroes"):
        p = comum.CAM.get(chave)
        if p and p.is_file():
            dados[chave] = {"arquivo": p.name, "bytes": p.stat().st_size, "sha256": comum.sha256(p)}
    comum.salvar("a_inventario", {
        "ambiente": comum.ambiente(),
        "dados": dados,
        "artefato": {"arquivo": arq_modelo.name, "bytes": arq_modelo.stat().st_size,
                     "sha256": comum.sha256(arq_modelo), "versoes_no_artefato": modelo.metadados.get("versoes"),
                     "salvo_em": modelo.metadados.get("salvo_em"), "tarefas": modelo.tarefas_disponiveis()},
        "metadados_docs_igual_artefato_sem_caminhos": _sem_caminhos(meta_art) == _sem_caminhos(meta_doc),
        "cabecas": cabecas,
        "codigo": codigo,
        "reproducao_rede": rede,
        "reproducao_lavagem": lav,
        "linha_do_tempo": linha_do_tempo(),
    })
    comum.log("ok: resultados/a_inventario.json")


if __name__ == "__main__":
    main()
