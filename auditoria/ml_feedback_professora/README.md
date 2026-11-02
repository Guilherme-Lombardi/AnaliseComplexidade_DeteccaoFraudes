# Auditoria do ML do NodeWatch após o feedback da professora

Scripts, testes e resultados brutos da auditoria de novembro de 2026. O relatório está em [RELATORIO_AUDITORIA_ML.md](RELATORIO_AUDITORIA_ML.md).

Nada aqui altera o NodeWatch. Os scripts leem o código de `src/ml`, os dados e o artefato salvo em `artefatos_ml/`. Eles gravam só em `resultados/` e numa pasta de trabalho fora do repositório.

## Preparar

1. Ter um clone do NodeWatch no commit auditado (`ml/arquitetura-unificada`, `893ceea`), com o `.venv` criado a partir de `requirements-ml.txt` e o artefato `artefatos_ml/modelo_unificado.joblib` gerado por `python -m src.ml.cli treinar --tarefa todas`.
2. Instalar o XGBoost **fora** do `.venv` do NodeWatch:

   ```bash
   python -m pip install --no-deps --target C:/caminho/temporario/bench_pkgs xgboost==3.4.1
   ```

3. Copiar `config_auditoria.exemplo.toml` para `config_auditoria.local.toml` e preencher os caminhos:
   - NodeWatch;
   - `dataset_final.csv`;
   - `HI-Small_Trans` (`.csv` ou `.zip`);
   - `HI-Small_accounts.csv` e `HI-Small_Patterns.txt`;
   - pasta de trabalho e pasta do XGBoost.

   Os dados não estão no repositório e os JSONs de resultado guardam só nome e SHA-256 dos arquivos.

## Executar (nesta ordem, um processo por vez)

Use o Python do `.venv` do NodeWatch. Rode a partir desta pasta.

```bash
python scripts/a_inventario.py
python scripts/b_verificar_implementacao.py
python scripts/c_preparar_financeiro.py
python scripts/e_benchmark.py --dominio rede --familia lr
python scripts/e_benchmark.py --dominio rede --familia rf
python scripts/e_benchmark.py --dominio rede --familia rf_nb
python scripts/e_benchmark.py --dominio rede --familia rf_red
python scripts/e_benchmark.py --dominio rede --familia hgb
python scripts/e_benchmark.py --dominio rede --familia xgb
python scripts/e_benchmark.py --dominio lavagem --familia lr
python scripts/e_benchmark.py --dominio lavagem --familia rf
python scripts/e_benchmark.py --dominio lavagem --familia rf_busca
python scripts/e_benchmark.py --dominio lavagem --familia hgb
python scripts/e_benchmark.py --dominio lavagem --familia xgb
python scripts/d_regras.py
python scripts/f_contas_padroes.py
python scripts/h_custo_atributos.py
python scripts/i_regressao_logistica.py
python scripts/g_consolidar.py
python -m pytest testes -q -p no:cacheprovider
```

| Script | O que verifica | Saída |
|---|---|---|
| `a_inventario.py` | Algoritmos importados em `src/` (análise estática); algoritmo efetivo de cada cabeça do artefato; o artefato salvo refaz as métricas documentadas | `resultados/a_inventario.json` |
| `b_verificar_implementacao.py` | Atributos financeiros vetorizados (NumPy) × força bruta em dados reais; cache do teste idêntico ao recalculado; métricas próprias × fórmulas independentes; regra que reproduz `classe_atual` | `resultados/b_verificacao_implementacao.json` |
| `c_preparar_financeiro.py` | Refaz a matriz de atributos do treino de lavagem (mesmo protocolo) e mede leitura e atributos | parquet na pasta de trabalho; `resultados/c_preparacao_financeiro.json` |
| `e_benchmark.py` | Busca na validação, ajuste com 3 sementes, qualidade no teste, tempo, memória, latência, vazão e tamanho por família | `resultados/e_benchmark_<domínio>_<família>.json` |

As famílias do benchmark são estas:

| Família | O que é |
|---|---|
| `lr`, `rf`, `hgb` | Grades de `src/ml/modelos.py`. |
| `xgb` | XGBoost `hist` em CPU, com 4 tentativas e early stopping na validação. |
| `rf_nb` | Configuração do notebook da professora. |
| `rf_red` | RF de produção com 50 árvores. |
| `rf_busca` | RF da lavagem com 4 tentativas, para igualar o orçamento do XGBoost. |
| `d_regras.py` | Regras explícitas × modelo no mesmo número de alertas | `resultados/d_regras.json` |
| `f_contas_padroes.py` | Vazamento em contas; padrões e episódios; recall por tipo de padrão e por conta conhecida × inédita | `resultados/f_contas_padroes.json` |
| `h_custo_atributos.py` | Separa o custo de atributos e de classificador na inferência de lavagem (lotes de 1 a 862.792 transações) | `resultados/h_custo_atributos.json` |
| `i_regressao_logistica.py` | Convergência da regressão logística: tolerâncias 1e-4, 1e-6 e 1e-8; objetivo e gradiente recalculados à mão | `resultados/i_regressao_logistica.json` |
| `g_consolidar.py` | Tabelas comparativas e bootstrap pareado por fluxo | `resultados/TABELAS.md`, `resultados/g_consolidado.json` |
| `testes/` | Implementação própria × referência; contrato da cabeça com outro estimador | saída do pytest |

## Protocolo de medição

| Item | Como foi medido |
|---|---|
| Threads | 4 (`n_jobs=4`, igual ao treino documentado). `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS` e `MKL_NUM_THREADS` também ficam em 4. |
| Isolamento | Um processo por família e nenhum benchmark rodando ao mesmo tempo. |
| Tempo | `time.perf_counter` (parede) e `time.process_time` (CPU de todas as threads). |
| Tempo de treino | Mediana de 3 ajustes, com sementes 42, 43 e 44. |
| Lote | 1 aquecimento e 5 repetições. |
| Latência de 1 linha | 20 aquecimentos e 1.000 linhas sorteadas do teste, com 4 threads e com 1 thread. O p95 só é calculado a partir de 100 medições e o p99 a partir de 1.000. |
| Memória | Bytes privados do processo (`GetProcessMemoryInfo`), amostrados a cada 10 ms. Picos mais curtos que isso podem escapar. |
| Tamanho | `joblib.dump` do pipeline, com `compress=3` (como no NodeWatch) e sem compressão. |

A RAM livre da máquina estava entre 0,4 e 0,5 GB no início das medições (16 GB no total, carga de 96%). Por isso os tempos podem incluir paginação. Os números servem para comparar candidatos nas mesmas condições, não como capacidade absoluta.
