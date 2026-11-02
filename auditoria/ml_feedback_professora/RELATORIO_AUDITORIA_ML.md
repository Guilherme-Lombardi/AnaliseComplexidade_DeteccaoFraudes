# Auditoria do ML do NodeWatch após o feedback da professora

**Data:** 02/11/2026.
**Objeto:** o código de `src/ml` no branch `ml/arquitetura-unificada` (commit `893ceea`) e o artefato salvo `artefatos_ml/modelo_unificado.joblib`. A auditoria também examinou:
- `dataset_final.csv` e o IBM AML HI-Small (transações, contas e padrões);
- o notebook didático da professora;
- o documento "Como funciona o ML do NodeWatch".

**Escopo:** nenhum modelo de produção foi substituído e nenhum componente foi removido. Os experimentos rodaram com scripts isolados nesta pasta, que só leem o NodeWatch. O XGBoost foi instalado fora do `.venv` do projeto. O `git status` do NodeWatch continua limpo.

**Como reproduzir:** os comandos estão no [README](README.md). Os números deste relatório vêm de `resultados/*.json` e de [`resultados/TABELAS.md`](resultados/TABELAS.md).

**Atualização de 02/11/2026: correções aplicadas.** Depois deste relatório, as correções de baixo risco foram aplicadas no NodeWatch (branch `ml/arquitetura-unificada`):

| Correção | Resultado |
|---|---|
| `z_valor_origem` com piso de variância e somas deslocadas | 0 divergências contra a força bruta nas mesmas 2.000 transações reais (`resultados/b_verificacao_implementacao_pos_correcao.json`) |
| `tol=1e-6` na regressão logística | AP de validação na lavagem: 0,19 |
| Previsões de menos de 1.000 linhas com 1 thread | Mesmo resultado, sem o custo de threads |
| Testes de força bruta em `testes/ml` | 88 testes passando |
| Recall por tipologia e por tentativa nova | Gerado automaticamente pela avaliação |

O modelo foi retreinado e reavaliado com a mesma configuração:
- **Rede:** sem mudança.
- **Lavagem:** AP de validação 0,499 e de teste 0,464, com precisão 0,627, recall 0,407, F1 0,494 e 231 falsos positivos.

O restante deste relatório descreve o estado auditado (commit `893ceea`).

---

## Resumo para a professora

**1. Qual algoritmo o código com NumPy implementa, e ele está correto?**

Nenhum modelo de aprendizado foi implementado à mão com NumPy. Os modelos treinados vêm todos do scikit-learn 1.9.1: regressão logística, Random Forest, HistGradientBoosting e `DummyClassifier`. O NumPy entra em três peças próprias que não são modelos:

| Peça própria | O que faz | Onde está |
|---|---|---|
| Motor de atributos "point-in-time" das transações | Índice ordenado por conta e minuto (`lexsort`), limites da janela `[t−w, t)` por busca binária (`searchsorted`) e somas por prefixo (`cumsum`) | `src/ml/preparacao.py:193-394` |
| Métricas próprias | Início de evento, falsos alertas por fluxo-hora, limiar de máximo F1, ECE, Brier e PSI | `src/ml/avaliacao.py:58-239` |
| Regra de limiares | Reproduz `classe_atual` | `src/ml/auditoria.py:34` |

As três peças foram comparadas com referências escritas de forma independente:

- **Motor de atributos:**
  - Em dados sintéticos, inclusive casos de borda com resultado conhecido, bate com a força bruta nas 49 colunas.
  - No HI-Small real, numa amostra de 2.000 transações, 47 colunas batem dentro da tolerância de float32.
  - `z_valor_origem` diverge em 4 linhas. Isso acontece quando o histórico da conta tem variância ≈ 0: a fórmula E[x²]−E[x]² sobre somas acumuladas, com ε = 10⁻⁶, gera |z| de até 1.939 nas duas implementações.
  - `razao_saida_entrada_24h` diverge em 8 linhas, até 0,7%, por arredondamento quando as entradas em 24 h somam centavos.
  - Recalculados para todo o teste, os atributos ficam idênticos, célula por célula, ao cache usado na avaliação (42.276.808 de 42.276.808).
- **Métricas próprias:** coincidem com as fórmulas independentes nas previsões reais do modelo.
- **Regra de limiares:** reproduz `classe_atual` em 99,944% das linhas.

**2. O aprendizado traz ganho útil sobre regras e referências simples?**

*Na rede*, os rótulos são uma regra de limiares aplicada à medição seguinte. A tarefa é prever essa regra uma medição à frente.

| Comparação no teste | Persistência (repete o estado atual) | Random Forest |
|---|---|---|
| Macro-F1 | 0,711 | 0,750 |
| Falsos alertas por fluxo-hora | 0,73 | 0,31 |
| Recall de RISCO | 0,507 | 0,418 |
| Inícios de evento antecipados | 0% | 4,5% |
| Macro-F1 em fluxos inéditos | 0,674 | 0,681 |

O ganho vem quase todo de emitir menos falsos alertas; o modelo quase não antecipa eventos, e em fluxos inéditos a vantagem quase some. Duas regras explícitas dão praticamente a persistência: a regra que gera o rótulo, aplicada à medição atual (macro-F1 0,712), e a melhor janela de "pior estado recente" escolhida no treino (k = 1). Com o mesmo número de alertas da persistência (5.861 no teste), o modelo acerta mais: precisão e recall de 0,674 para "próxima medição não-OK", contra 0,618.

*Na lavagem*, o modelo tem AP de 0,461, contra 0,0064 do baseline que usa só o formato de pagamento e 0,011 da contagem de regras explícitas. A melhor regra explícita escolhida na validação, "formato ACH e primeira transação do par", encontra 78% da lavagem, mas emite 20.575 alertas em dois dias, com precisão de 0,036. Com o mesmo número de alertas, o modelo chega a 82,5%. A diferença decisiva está nos orçamentos pequenos: no limiar da validação, o modelo emite 817 alertas com precisão de 0,52, o que nenhuma regra testada alcança. Sim, há ganho útil, mas com três limites:
- vale para dados **sintéticos** e não é evidência de desempenho em transações reais;
- concentra-se nas tipologias de `HI-Small_Patterns.txt`: o modelo pega cerca de 72% delas, mas só 3,5% dos 39% de positivos do teste que não pertencem a padrão nenhum;
- é otimista para tentativas novas: recall de 0,59, contra 0,77 nas tentativas iniciadas antes do teste.

**3. O XGBoost melhora o compromisso entre qualidade, tempo e memória em relação à Random Forest?**

*Na rede*, não melhora a qualidade:

| Modelo no teste | Macro-F1 | Treino | Tamanho |
|---|---|---|---|
| XGBoost | 0,7515 | 4,1 s | 0,86 MB |
| Random Forest de produção | 0,7499 | 12,2 s | 17,6 MB |
| HistGradientBoosting (já no projeto) | 0,750 | 4,5 s | 0,97 MB |
| Random Forest com 50 árvores | 0,751 | 5,8 s | 5,9 MB |

No bootstrap pareado por fluxo, a diferença XGBoost − RF é +0,0016, com IC 95% de [−0,003; 0,006]. O XGBoost treina mais rápido e é menor, mas o HistGradientBoosting, que já está no projeto, e a própria RF com menos árvores entregam o mesmo ganho.

*Na lavagem*, o XGBoost foi melhor que a RF de produção:

| Modelo no teste | AP | Falsos positivos | Treino |
|---|---|---|---|
| XGBoost | 0,509 | 196 | 6,6 s |
| Random Forest de produção | 0,461 | 391 | 42–48 s |

O recall dos dois é parecido (0,447 contra 0,446). Com o mesmo orçamento de busca (4 tentativas), a melhor RF (200 árvores, folha 10) chega a AP de 0,478 no teste e 0,525 na validação. A vantagem do XGBoost cai para cerca de +0,03 e continua com custo muito menor: treino de 6,6 s contra 85 s e modelo de 0,13 MB contra 9,4 MB. Há três ressalvas:

- O XGBoost é sensível a hiperparâmetros: a AP de validação vai de 0,27 a 0,55 entre as 4 tentativas.
- O early stopping e a escolha usaram a validação.
- O teste agora já foi consultado para comparar modelos.

O "custo de processamento da Random Forest" não é um gargalo absoluto: o treino leva 12 s na rede e cerca de 45 s na lavagem, com 4 threads de CPU, e não precisa de GPU. Os custos que pesam de fato são estes:

- **Latência de uma linha com `n_jobs=4`:** 27 ms, contra 9 ms com uma thread. É uma questão de configuração.
- **Atributos da lavagem:** a cada chamada, os índices são reconstruídos sobre todo o histórico. Pontuar uma única transação contra o histórico de 5,08 milhões leva 12,0 s só nos atributos, contra 0,03 s da RF. Pontuar as 862.792 transações do teste leva 15,2 s de atributos e 1,2 s de RF.

**4. O modelo chamado de regressão é adequado e tem utilidade?**

É uma **regressão logística**, ou seja, um classificador supervisionado, não uma regressão para alvo contínuo. Na rede é multinomial com 3 classes; na lavagem, binária. Nenhum regressor existe no código. Ela nunca foi escolhida:

| Tarefa | Regressão logística | Persistência | Árvores |
|---|---|---|---|
| Rede, macro-F1 no teste | 0,642 | 0,711 | — |
| Lavagem, AP no teste | 0,169 | — | 0,46–0,51 |

Na rede, converge em 44 a 63 iterações sem aviso. Na lavagem, para em 17 iterações pela tolerância padrão e a AP variou entre execuções (0,1647 e 0,1690). Com a tolerância apertada para 10⁻⁶, ela faz 87 iterações, o objetivo cai de 0,004084 para 0,004005 e a AP de validação sobe de 0,169 para 0,190. Ou seja, **a regressão logística da lavagem parava cedo demais**. Na rede nada muda: 0,5900 contra 0,5899. Recomendação: **manter como referência linear** (baseline didático e diagnóstico de não linearidade), não como modelo operacional.

**5. O que melhorar primeiro, e com qual evidência?**

Validade antes de desempenho:

1. Declarar que o teste foi reutilizado nesta comparação e reservar um período intocado antes de trocar qualquer modelo.
2. Corrigir o documento dos modelos: papel do NumPy, a regressão logística como classificador, XGBoost ausente do código.
3. Na lavagem, reportar o recall separado por tipologia e por tentativa nova. O número global esconde que os positivos sem padrão quase não são detectados.
4. Incluir no NodeWatch os testes de força bruta e corrigir o condicionamento de `z_valor_origem` e a tolerância da regressão logística.
5. Usar `n_jobs=1` na inferência de poucas linhas.
6. Tornar incremental o índice de atributos da lavagem antes de qualquer uso on-line.
7. Só então decidir a troca de modelo:
   - **Rede:** com qualidade empatada, vale o mais simples e leve que atenda aos requisitos, que ainda não foram definidos.
   - **Lavagem:** confirmar o XGBoost, ou uma RF ajustada, no período intocado.

Detalhes, critérios de aceite e evidências estão nas seções 8 a 10.

---

## 1. O que foi inspecionado e o que foi executado

| Item | Inspecionado | Executado |
|---|---|---|
| Código `src/ml` (13 módulos) | Leitura e varredura estática dos imports de ML e das funções NumPy (`a_inventario.py`) | — |
| Artefato salvo | Algoritmo efetivo e parâmetros de cada cabeça | Métricas refeitas a partir dele |
| Notebook `Arvore_e_random_forest_didatico.ipynb` | Leitura das células e saídas | Configuração vencedora reajustada no protocolo do NodeWatch (`rf_nb`) |
| Documento "Como funciona o ML do NodeWatch" (doc e PDF exportado em 30/10) | Leitura | — |
| Atributos financeiros (NumPy) | — | Comparados com força bruta em dados sintéticos e reais |
| Métricas próprias | — | Comparadas com fórmulas independentes |
| Regras explícitas e referências | — | Medidas na validação e no teste (`d_regras.py`) |
| RF, HGB, regressão logística e XGBoost | — | Busca, 3 sementes, teste, tempo, memória, latência, vazão e tamanho (`e_benchmark.py`) |
| Contas e padrões do HI-Small | — | Auditoria de vazamento e de episódios, recall por padrão (`f_contas_padroes.py`) |
| Convergência da regressão logística | — | 3 tolerâncias, com objetivo e gradiente recalculados à mão (`i_regressao_logistica.py`) |
| Custo da inferência de lavagem | — | Atributos × classificador por tamanho de lote (`h_custo_atributos.py`) |

**O documento que a professora leu não foi identificado com certeza.** Há dois candidatos:

- *Como funciona o ML do NodeWatch*: cita regressão logística, Random Forest e HistGradientBoosting, mas não menciona NumPy nem bibliotecas.
- *O notebook da professora*: lista `numpy` como biblioteca, usada para criar o vetor `test_fold` e fixar a semente, e usa só árvore de decisão e Random Forest do scikit-learn.

Nenhum dos dois descreve um modelo implementado em NumPy. Por isso as respostas sobre "NumPy" se referem ao que o código realmente faz com a biblioteca.

## 2. Inventário e rastreabilidade

### 2.1 Componentes

| Componente | Algoritmo efetivo | Biblioteca | Onde | Tarefa e alvo | Uso dos rótulos | Configuração | Resultado disponível | Status |
|---|---|---|---|---|---|---|---|---|
| Classe majoritária | `DummyClassifier(most_frequent)` | scikit-learn 1.9.1 | `src/ml/modelos.py:322` | Rede: `alvo` | Só a contagem no treino | — | Macro-F1 de teste 0,311 | Existente (referência) |
| Persistência | Repete `classe_atual(t)` | — | `src/ml/modelos.py:326`, `src/ml/experimentos.py:126` | Rede | Nenhum | — | Macro-F1 de teste 0,711 | Existente (referência) |
| Regra de limiares | Limiares fixos de perda e RTT/jitter | pandas/NumPy | `src/ml/auditoria.py:34` | Reproduz `classe_atual` (auditoria) | Nenhum | Limiares 1 e 50% | Reproduz 99,944% | Existente (regra, não ML) |
| Regressão logística | `LogisticRegression` (lbfgs, L2, multinomial na rede e binária na lavagem) | scikit-learn 1.9.1 | `src/ml/modelos.py:50-51` (grades 89-91 e 113-114); pré-processamento em `src/ml/preparacao.py:114-119` e `400-404` | Rede e lavagem | Supervisionado no treino | C ∈ {0,1; 1}; `class_weight` ∈ {None, balanced} na rede; `max_iter` 3000; `tol` 1e-4 | Rede: 0,590 (val) e 0,642 (teste). Lavagem: AP 0,165–0,169 | Existente; candidata nunca escolhida |
| Random Forest | `RandomForestClassifier` (gini, `max_features=sqrt`, `max_samples=0.5`) | scikit-learn 1.9.1 | `src/ml/modelos.py:54-55` (grades 92-96 e 115-117) | Rede e lavagem | Supervisionado no treino; escolha na validação | Rede: 150 árvores, folha 20. Lavagem: 100 árvores, folha 50, `n_jobs=4` | Rede: 0,750. Lavagem: AP 0,461 | **Em produção, nas duas tarefas** |
| HistGradientBoosting | `HistGradientBoostingClassifier` (log-loss) | scikit-learn 1.9.1 | `src/ml/modelos.py:58-59` (grades 97-101 e 118-121) | Rede e lavagem | Supervisionado no treino | 200 ou 300 iterações; lr 0,1; 31 ou 63 folhas | Rede: 0,750. Lavagem: AP 0,414 | Existente; candidata |
| Taxa do formato | Taxa de lavagem por formato de pagamento no treino | pandas | `src/ml/experimentos.py:378-383` | Lavagem | Taxas do treino | — | AP de teste 0,0064 | Existente (referência) |
| Atributos point-in-time | Índice ordenado, `searchsorted` e `cumsum` | NumPy 2.5.4 | `src/ml/preparacao.py:193-394` | Lavagem (49 atributos) | Nunca; câmbio e categorias vêm do treino | Janelas de 6, 24 e 72 h | Seção 3A | Implementação própria (não é modelo) |
| Métricas próprias | Eventos, alertas, ECE, Brier, PSI, limiar | NumPy/pandas | `src/ml/avaliacao.py:58-239` | Avaliação | Avaliação; o limiar é escolhido na validação | — | Seção 3A | Implementação própria |
| Fusão rede ↔ transação | — | — | `src/ml/modelos.py:165-216` | — | — | Bloqueada (falta vínculo) | — | Apenas descrito |
| Árvore e RF do notebook | `DecisionTreeClassifier` e `RandomForestClassifier` com `GridSearchCV` + `PredefinedSplit`, reajuste em treino+validação | scikit-learn | Notebook da professora | Rede | Supervisionado | RF: 100 árvores, folha 5, sem limite de profundidade | Teste 0,755 (notebook) | Referência didática, fora do NodeWatch |
| XGBoost | `XGBClassifier` (`hist`, CPU) | xgboost 3.4.1 (só na auditoria) | `scripts/e_benchmark.py` | Rede e lavagem | Supervisionado no treino; early stopping na validação | Seção 6 | Seção 6 | **Alternativa proposta, ausente do código** |

A varredura estática (`resultados/a_inventario.json`) só encontrou em `src/` os estimadores `DummyClassifier`, `HistGradientBoostingClassifier`, `LogisticRegression` e `RandomForestClassifier`. Não há nenhum `*Regressor`, `LinearRegression`, otimização com gradiente própria ou modelo escrito em NumPy. Importar NumPy não prova que um modelo foi treinado.

### 2.2 Rastreabilidade

| Item | Valor |
|---|---|
| Código | NodeWatch `ml/arquitetura-unificada`, commit `893ceeae79a5f86294e6c69c40b34a041217c781`, sem alterações rastreadas |
| Rede | `dataset_final.csv`, SHA-256 `125453f1…d9b997`, 333.954 linhas |
| HI-Small | `HI-Small_Trans.zip`, SHA-256 `93c9d651…5179`, 5.078.345 transações |
| Contas e padrões | `HI-Small_accounts.csv`: SHA-256 `78680852…b014`, 518.581 linhas. `HI-Small_Patterns.txt`: SHA-256 `2c546b5c…f39b`, 370 tentativas e 3.209 linhas. Ambos extraídos de uma cópia do `.rar` da professora no diretório temporário da auditoria. |
| Divisão da rede (coluna `split`) | Treino 28/09–03/10 (241.359), validação 04/10 (46.490), teste 05/10 (46.105) |
| Divisão da lavagem (por dia) | Treino 01–06/09, validação 07–08/09, teste 09–10/09; cauda de 11/09 em diante fora das métricas |
| Semente | 42 em todo o projeto; o benchmark acrescenta 43 e 44 |
| Artefato | `modelo_unificado.joblib`, SHA-256 `d7ed398f…078a`, 38,6 MB, salvo em 26/10/2026 12:36 UTC. Versões gravadas nele: Python 3.14.0, NumPy 2.5.4, pandas 3.1.0, scikit-learn 1.9.1 (iguais às atuais) |
| Ambiente | Windows 11 (10.0.26200), i7-13650HX (14 núcleos e 20 threads), 15,7 GB de RAM com 0,4–0,5 GB livres (carga de 96%), 4 threads nos experimentos |

O **artefato corresponde ao código e aos resultados documentados**:

- Com ele, o macro-F1 da rede sai igual ao documentado em `docs/ml/resultados`: 0,7628197569 na validação e 0,7499003080 no teste, com as mesmas matrizes de confusão.
- A AP da lavagem no teste também sai igual (0,4610030807), com os mesmos 426 verdadeiros positivos e 391 falsos positivos.
- As probabilidades somam 1, com desvio de até 1,1·10⁻¹⁵, e nenhuma fica fora de [0, 1].
- Ao refazer a busca com o código atual, as Random Forests reproduzem exatamente as métricas de validação do treino de 26/10 (0,7628 e 0,4950).
- `docs/ml/resultados/metadados_modelo.json` só difere da cópia em `artefatos_ml/` pelos caminhos absolutos, que foram trocados por nomes de arquivo.

### 2.3 Correções necessárias no documento dos modelos

1. **Papel de cada biblioteca.**
   - O NumPy é suporte numérico: constrói os atributos e calcula as métricas. Não é um modelo.
   - Os modelos vêm do scikit-learn.
   - O XGBoost não é usado no NodeWatch.
2. **"Regressão" → "regressão logística (classificador linear)".** Ela foi uma candidata derrotada nas duas tarefas e serve de referência linear.
3. **Modelos efetivamente em produção.** Random Forest nas duas tarefas: na rede, 150 árvores com folha 20; na lavagem, 100 árvores com folha 50. A grade da rede tem 12 configurações; a da lavagem, 5.
4. **Reuso do teste.** Os números de teste dos candidatos desta auditoria (seção 6) não são uma avaliação inédita.
5. **Custos medidos.** Incluir o tempo de treino e a latência medidos, e a separação entre o custo dos atributos e o do classificador.
6. **Notebook.** Em `classe_atual`, o notebook fala em "potencial vazamento". Nesta tarefa, `classe_atual` está disponível no instante da previsão e não acrescenta nada (0,752 contra 0,750); o risco real é medir reprodução de regra, não vazamento. O guia que acompanha o `.rar` descreve o teste como "dados sem rótulo": o teste tem rótulo, só não pode orientar escolhas.

## 3. NumPy, implementação própria e regras

### 3A. Correção da implementação própria

**Atributos point-in-time** (`src/ml/preparacao.py:197-394`).

*Método:*
- Para cada conta, os eventos (envios ou recebimentos) ficam num índice composto `chave·2²⁶ + minuto`, ordenado com `lexsort`.
- Para uma transação no minuto *t*, os limites da janela `[t−w, t)` saem de `searchsorted`. Contagens são diferenças de posição; somas são diferenças de prefixos acumulados (`cumsum`).
- Contrapartes distintas usam o primeiro minuto de cada par origem→destino.
- O desvio-padrão do valor usa E[x²]−E[x]² sobre prefixos.
- Transações do mesmo minuto não se enxergam.

*Referência:* `scripts/referencia_atributos.py` reescreve as mesmas definições com filtros diretos, sem índices nem somas acumuladas.

| Verificação | Resultado |
|---|---|
| Casos de borda com resultado conhecido: mesmo minuto, borda exata de 6 h, auto-transferência, moeda sem câmbio, primeira transação do par (`testes/`) | Passa |
| 3 conjuntos aleatórios de 400 transações, com a ordem do arquivo embaralhada | 0 divergências nas 49 colunas |
| HI-Small real: 2.000 consultas (500 de lavagem; 1.245 do treino, 387 da validação e 368 do teste) contra 588.638 transações de histórico | 47 de 49 colunas idênticas (rtol 10⁻⁵, atol 10⁻³) |
| `z_valor_origem` | 4 linhas divergentes, todas com 2 a 10 envios anteriores e variância de 0 a 1,7·10⁻⁷ (por exemplo, o mesmo valor enviado duas vezes). O z é mal condicionado nesse regime: com ε = 10⁻⁶, um valor 0,5 log-unidade acima da média vira z ≈ 500 nas duas implementações, e a diferença vem do cancelamento numérico em E[x²]−E[x]² |
| `razao_saida_entrada_24h` | 8 linhas com diferença relativa ≤ 0,7%, quando as entradas em 24 h somam centavos (por exemplo, US$ 0,08). As somas em USD têm erro absoluto da ordem de 10⁻³ dólar, porque o prefixo acumulado global chega a 1,8·10¹² |
| Cache de atributos do teste × recálculo com o codificador salvo | 42.276.808 de 42.276.808 células idênticas, na mesma ordem de transações |
| Câmbio, formatos e taxas reajustados no treino × salvos | Iguais. Nenhuma moeda ficou sem câmbio |

*Conclusão:* a implementação vetorizada está correta. Há uma limitação numérica confirmada, de baixo impacto: `z_valor_origem` fica extremo e instável quando a variância do histórico é quase nula. Para árvores, valores como 496 e 498 caem do mesmo lado de qualquer corte, então o efeito é desprezível. Na regressão logística, o log com sinal comprime esses valores. A seção 8 traz a correção sugerida.

**Métricas próprias** (`src/ml/avaliacao.py`), conferidas sobre as previsões do artefato:

| Métrica | Função do projeto | Referência independente |
|---|---|---|
| Matriz de confusão e macro-F1 de teste | 0,7499003080 | 0,7499003080 (contagem por laço) |
| Balanced accuracy | 0,70225 | 0,70225 |
| Inícios de evento (teste) | 2.229, dos quais 100 detectados | 2.229 e 100 (laço por fluxo) |
| Falsos alertas por fluxo-hora | 0,30810 | 0,30810 |
| Limiar de máximo F1 (validação) | 0,31735 (F1 0,67299) | 0,31735 e 0,67299 (busca exaustiva) |
| ECE | 0,00811 (val) e 0,00972 (teste) | Iguais |
| Brier multiclasse e PSI (dados sintéticos, `testes/`) | — | Iguais à definição; o Brier também bate com o `brier_score_loss` do scikit-learn |

Não há otimização diferenciável própria no projeto: todo ajuste é feito pelo scikit-learn. Por isso a verificação numérica de gradiente foi aplicada à conferência de convergência da regressão logística (seção 4). Nenhuma das execuções gerou overflow, probabilidade inválida ou classe invertida. As classes do scikit-learn ficam em ordem alfabética (FALHA, OK, RISCO), e `CabecaClassificacao.probabilidades` (`src/ml/modelos.py:144-151`) as reordena por nome. O teste de contrato confirma isso com outro estimador.

### 3B. Utilidade do aprendizado: regras × modelos

**Rede.**

*Origem dos rótulos:* `classe_atual` é a regra de limiares aplicada à medição atual (99,944% de concordância), e `alvo` é a `classe_atual` da medição seguinte (99,983%). Logo, a avaliação mede **quão bem se prevê a saída da regra uma medição à frente** (mediana de 240 s). Não mede degradação "real" independente da regra.

*Referências avaliadas,* todas disponíveis no instante t e ajustadas só no treino:

| Referência | Definição |
|---|---|
| R0 | Classe majoritária: sempre OK |
| R1 | Persistência: repete `classe_atual(t)` |
| R2 | A regra de limiares aplicada à medição atual. Dispensa a coluna `classe_atual`, mas é quase idêntica a R1 |
| R3 | Pior estado entre as últimas k medições do fluxo, com k escolhido por macro-F1 no treino |

| Referência ou modelo | Macro-F1 val | Macro-F1 teste | Recall RISCO / FALHA (teste) | Alertas não-OK (teste) | Precisão / recall do alerta (teste) | Falsos alertas por fluxo-hora | Inícios antecipados | Modelo com o mesmo nº de alertas: precisão / recall |
|---|---|---|---|---|---|---|---|---|
| R0 classe majoritária | 0,312 | 0,311 | 0 / 0 | 0 | — | 0 | 0% | — |
| R1 persistência | 0,711 | 0,711 | 0,507 / 0,681 | 5.861 | 0,618 / 0,619 | 0,73 | 0% | 0,674 / 0,675 |
| R2 regra de limiares (medição atual) | 0,710 | 0,712 | 0,506 / 0,687 | 5.858 | 0,618 / 0,618 | 0,73 | 0% | 0,674 / 0,675 |
| R3 pior estado das últimas k (k = 1 escolhido no treino) | 0,711 | 0,711 | 0,507 / 0,681 | 5.861 | 0,618 / 0,619 | 0,73 | 0% | 0,674 / 0,675 |
| RF de produção (limiar da validação) | 0,763 | 0,750 | 0,418 / 0,697 | 4.621 | 0,795 / 0,627 | 0,31 | 4,5% | — |

*Leitura:*
- Aumentar k piora já no treino (k = 2: 0,672; k = 12: 0,477). Estados mais antigos não ajudam como regra.
- O aprendizado ganha em precisão no mesmo orçamento de alertas (+5,6 pontos) e no equilíbrio entre alertas e acertos.
- Não ganha em antecipação: 95% dos inícios de evento continuam sem alerta.
- Também não há regra que preveja a próxima medição sem aprender: a regra de limiares só descreve o instante atual.

**Lavagem.**

*Regras:* nenhuma usa limite monetário fixo nem soma moedas diferentes sem o câmbio estimado no treino.

| Regra | Definição | Gera ranking? |
|---|---|---|
| F1 | Taxa de lavagem do formato no treino | Sim |
| F2 | Número de "motivos verificáveis": as 8 condições de `PreparadorFinanceiro.motivos`, com limiares p99 do treino | Sim (ordinal) |
| F3 | Conjunções explícitas (formato de risco, par novo, repasse em menos de 60 min, dispersão acima do p99), escolhidas por F1 na validação | Não |

Como F3 não gera ranking, ela não tem curva precisão-recall. A comparação é feita no mesmo ponto operacional: o modelo emite o mesmo número de alertas que a regra.

| Referência, regra ou modelo | AP val | AP teste | Alertas no teste (2 dias) | Precisão / recall (teste) | Falsos positivos por 10 mil | RF de produção com o mesmo nº de alertas: precisão / recall |
|---|---|---|---|---|---|---|
| F0 prevalência | 0,0011 | 0,0011 | — | — | — | — |
| F1 taxa do formato (limiar na validação) | 0,0068 | 0,0064 | 119.195 | 0,007 / 0,872 | 1.371,8 | 0,008 / 0,951 |
| F2 motivos ≥ 2 (k escolhido na validação) | 0,0145 | 0,0112 | 57.871 | 0,014 / 0,820 | 661,7 | 0,015 / 0,879 |
| F3 ACH ∧ par novo (melhor conjunção na validação) | sem ranking | sem ranking | 20.575 | 0,036 / 0,780 | 229,8 | 0,038 / 0,825 |
| RF de produção (limiar da validação) | 0,495 | 0,461 | 817 | 0,521 / 0,446 | 4,5 | — |

*Leitura:*
- **As regras capturam o sinal grosso:** na validação, 86% da lavagem é ACH, contra 12% das transações normais; 79% é a primeira transação do par, contra 4%.
- **Mas não ordenam:** o melhor ponto delas custa 20 mil alertas em dois dias. O modelo concentra o sinal: os 50 alertas de maior score por dia têm precisão de 0,96 a 1,00.
- **Três das oito condições de "motivos verificáveis" nunca disparam para positivos na validação:** envios em 24 h acima do p99 (19.667), dispersão de saída acima do p99 (14.230) e moedas diferentes. Os p99 são dominados por contas-hub e não servem como motivo (seção 8, achado 12).

## 4. O modelo "de regressão"

- **Identidade.** É `sklearn.linear_model.LogisticRegression` (`src/ml/modelos.py:50-51`): lbfgs, penalidade L2, `max_iter=3000`, `tol=1e-4` (padrão).
  - Na rede, é multinomial com 3 classes; na lavagem, binária, com pesos amostrais 5 nos negativos subamostrados.
  - O pré-processamento é ajustado só no treino: sentinelas → NaN com indicador, imputação pela mediana, `sign(x)·log1p(|x|)` e padronização (`src/ml/preparacao.py:109-121` e `397-406`).
- **Classificador, não regressor.** O modelo é supervisionado e os rótulos entram como classes, não como códigos numéricos contínuos. Nenhum regressor trata OK/RISCO/FALHA como 0/1/2. Não existe tarefa de regressão no projeto, e criar uma só para justificar o nome não faz sentido.
- **Convergência na rede:** 44 a 63 iterações, sem `ConvergenceWarning`, norma dos coeficientes ≈ 1.
- **Convergência na lavagem:** só 17 iterações, também sem aviso. A AP de validação mudou entre o treino de 26/10 (0,1647) e esta auditoria (0,1690), com os mesmos dados e a mesma semente. As Random Forests repetiram exatamente. Isso indica uma solução sensível à ordem das operações numéricas, provavelmente pela quantidade de threads do BLAS.
- **Teste de tolerância** (`i_regressao_logistica.py`), com objetivo e gradiente recalculados à mão: 

| Tarefa | Tolerância | Iterações | Objetivo | ‖∇‖∞ | Validação |
|---|---|---|---|---|---|
| Rede | 10⁻⁴ (produção) | 47 | 0,30662518 | 5,4·10⁻⁵ | macro-F1 0,5900 |
| Rede | 10⁻⁶ | 96 | 0,30662396 | 8,8·10⁻⁷ | 0,5899 |
| Rede | 10⁻⁸ | 145 | 0,30662396 | 1,7·10⁻⁸ | 0,5899 |
| Lavagem | 10⁻⁴ (produção) | 17 | 0,00408406 | 6,5·10⁻⁵ | AP 0,1690 |
| Lavagem | 10⁻⁶ | 87 | 0,00400532 | 6,2·10⁻⁷ | AP 0,1899 |
| Lavagem | 10⁻⁸ | 112 | 0,00400529 | 2,2·10⁻⁷ | AP 0,1900 |

  Na lavagem, a perda média ponderada é pequena (≈ 0,004) porque a prevalência é de 0,1%. Para essa escala, a tolerância padrão de 10⁻⁴ no gradiente é grande, e o lbfgs para antes do ótimo. É um **erro de configuração confirmado**, que o scikit-learn não acusa com aviso. O impacto é limitado: mesmo corrigida, a regressão logística fica muito abaixo das árvores (0,19 contra 0,46–0,51). A fórmula manual foi validada nos `testes/`: no ótimo de um ajuste com tolerância 10⁻¹², o gradiente fica abaixo de 10⁻⁶ e perturbar os coeficientes aumenta o objetivo.
- **Utilidade:**
  - Na rede, fica abaixo da persistência. Com alertas no limiar da validação, emite 0,29 falso alerta por fluxo-hora, perto das árvores, mas acerta menos.
  - Na lavagem, a AP de 0,17 está bem acima da taxa do formato (0,0064) e bem abaixo das árvores (0,41–0,51). A interação entre histórico de contas e formato pesa.
- **Recomendação:** **manter como referência linear**, para mostrar quanto da tarefa é linear e como exemplo didático de classificador probabilístico. Não manter para operação. Corrigir `tol` para 10⁻⁶ na grade da lavagem (`src/ml/modelos.py:51`), para que a referência seja a regressão logística de fato ajustada.

## 5. Validade dos dados e da avaliação

**Rede**

| Verificação | Resultado | Fonte |
|---|---|---|
| Horizonte do alvo | Próxima medição do fluxo: mediana de 240 s, p99,9 de 484 s. As lacunas entre períodos (≥ 3.605 s) são muito maiores que o horizonte, então nenhum rótulo cruza a fronteira e não há expurgo a fazer | `docs/ml/resultados/auditoria_rede.json` |
| Divergências entre `alvo` e a classe seguinte | 6 dentro dos períodos, todas logo antes de lacunas na série; mantidas | idem |
| Janelas w3, w6 e w12 | Batem com o cálculo para trás em ≥ 99,4% das linhas e com o cálculo para frente em só 20%: não usam observações futuras | idem |
| `classe_atual` | Disponível em t (sai da medição atual). Não é vazamento para prever t+1, mas também não acrescenta nada (0,752 × 0,750) | idem e `avaliacao_estado_rede.json` |
| Sentinelas | O −1 das razões coincide com `rtt_ausente`. O −1 das janelas marca janela sem RTT. `delta_ttl_clip` negativo é legítimo | idem |
| Constantes e duplicatas | `ttl_reset` é constante e foi removido no pipeline. Nenhuma duplicata por fluxo e timestamp, nenhum NaN ou inf | idem |
| Referências p95/p99 | O período de cálculo é desconhecido (o código que gerou o CSV não foi fornecido). No treino, 7,5% das medições ficam acima do "p95" | idem |
| Fluxos conhecidos × inéditos | Os mesmos 135 fluxos aparecem nos três períodos. Em fluxos inéditos (GroupKFold), o macro-F1 é 0,681 ± 0,073, contra 0,674 da persistência | `avaliacao_estado_rede.json` |

**Lavagem (HI-Small)**

| Verificação | Resultado |
|---|---|
| Rótulo | `Is Laundering` é o único alvo. É sintético e vem sem data de confirmação |
| Cauda do gerador | Do dia 11/09 em diante há 1.108 transações, 59% de lavagem; ficam fora das métricas |
| Atributos | Usam só minutos estritamente anteriores (conferido pela força bruta). Rótulos passados nunca viram atributo |
| Padrões e contas | Não entram nos atributos (`src/ml/preparacao.py` não lê nenhum dos dois) |
| Contas: vazamento | Nenhum atributo de conta revela a resposta pelo critério de `src/ml/auditoria.py:_auditar_contas`. O tipo de entidade (origem e destino) e o número de contas da entidade têm AP de validação de 0,0011 a 0,0017, contra prevalência de 0,0011, e lift máximo de 1,1 a 3,3 (o limite é 50). Todas as contas das transações têm cadastro, e nenhum nome de entidade contém termo suspeito. |
| Padrões e episódios | 370 tentativas em 8 tipologias, com 3.209 linhas, todas casadas com transações de rótulo 1. **Porém 1.968 dos 5.177 positivos não pertencem a nenhum padrão.** No teste, são 371 de 956 (39%). **206 das 370 tentativas atravessam períodos**, e 64% das linhas de padrão do teste vêm de tentativas iniciadas no treino ou na validação. |
| Contas conhecidas × inéditas | 99,9% das transações de teste têm conta de origem já vista no treino; entre os positivos, 98%. Só 19 positivos têm origem inédita, com recall de 0,37 na RF contra 0,45 nas contas conhecidas. A amostra é pequena demais para concluir. |
| Recall por tipo de padrão (RF de produção) | Nas tipologias, o recall no limiar vai de 0,58 a 0,77 (FAN-OUT 0,77; GATHER-SCATTER 0,74; BIPARTITE 0,59; RANDOM 0,58). **Nos positivos sem padrão, é de 0,035.** Nas tentativas já iniciadas antes do teste, 0,773; nas novas, 0,586. O XGBoost chega a 0,671 nas novas e a 0,030 nos positivos sem padrão. O recall global de 0,446 mistura, portanto, cerca de 72% das tipologias com quase nada dos demais positivos, e é otimista para episódios novos. |

**Reuso do teste.** No treino de 26/10:

- O código de treino nunca lê rótulos do teste (`src/ml/experimentos.py:108-214` e `333-434`).
- O treino terminou e o artefato foi salvo às 09:36:07. A avaliação começou às 09:36:48 (`artefatos_ml/log_*.txt`).
- O registro da sessão de desenvolvimento mostra uma única avaliação de teste com dados reais (AP 0,4610).
- **Limitação:** o protocolo foi desenhado depois de olhar as distribuições de rótulos de todos os dias, inclusive os do teste. Essa leitura definiu o fim da janela de modelagem em 10/09 e a cauda a partir de 11/09.

**Nesta auditoria, o teste foi consultado para 9 candidatos.** Portanto:

- Os números de teste da seção 6 **não são avaliação inédita**.
- Escolher entre RF e XGBoost por eles seria selecionar pelo teste.
- A escolha usa a validação; o teste aparece só como descrição.

Para confirmar qualquer troca é preciso um **período intocado**:

- **Rede:** telemetria posterior a 05/10/2026, coletada com o mesmo pipeline. `ler_rede` já aceita vários CSVs.
- **Lavagem:** o HI-Small não tem outro período limpo (o que vem depois do teste é a cauda artificial). A alternativa é uma replicação externa, por exemplo o HI-Medium, declarada como outra distribuição, e não como o mesmo período.

**Variação.**

- *Rede:* bootstrap pareado por fluxo (os 135 fluxos reamostrados inteiros, B = 2.000), porque medições do mesmo fluxo são dependentes no tempo. 

| Diferença no teste (em relação à RF de produção) | Macro-F1 | IC 95% | Fração das reamostras > 0 |
|---|---|---|---|
| Persistência − RF | −0,0391 | [−0,0535; −0,0171] | 0,002 |
| Regressão logística − RF | −0,1074 | [−0,1876; −0,0435] | 0,000 |
| HGB − RF | +0,0001 | [−0,0076; 0,0070] | 0,524 |
| RF com 50 árvores − RF | +0,0007 | [−0,0004; 0,0021] | 0,886 |
| RF do notebook − RF | +0,0055 | [+0,0007; +0,0110] | 0,983 |
| XGBoost − RF | +0,0016 | [−0,0030; 0,0057] | 0,765 |

  Esses intervalos usam o teste já consultado e não corrigem para múltiplas comparações.
- *Lavagem:* não há intervalo de confiança. As tentativas de lavagem ligam várias contas e transações, e o teste tem só 2 dias. A variação aparece por dia e por semente.

## 6. Random Forest × XGBoost (e as demais candidatas)

### 6.1 Desenho

*O que é igual para todos:*
- registros elegíveis, alvos e atributos de origem;
- transformadores ajustados no treino;
- 4 threads;
- escolha na validação: na rede por macro-F1, com desempate pelo recall de FALHA; na lavagem por AP;
- limiar de alerta pelo máximo F1 na validação;
- teste só no fim.

*Representação:* a RF e o XGBoost recebem a mesma matriz: sentinelas viram NaN com indicador e constantes saem. Os dois tratam NaN nativamente. A regressão logística acrescenta imputação, log e padronização.

*Configuração do XGBoost:*

| Parâmetro | Valor |
|---|---|
| Objetivo | `multi:softprob` na rede; `binary:logistic` na lavagem |
| Construção das árvores | `tree_method="hist"`, `device="cpu"`, `max_bin=256` |
| Taxa de aprendizado | 0,1 |
| Regularização | `reg_lambda=1` |
| Amostragem | `subsample=1` e `colsample_bytree=1` |
| Número de árvores | Até 1.000, com early stopping de 50 rodadas na **validação** (mlogloss na rede, aucpr na lavagem) |
| Ajustes finais | Número de árvores fixado no valor escolhido |

*Desbalanceamento:* na rede não se transferiu nenhum ajuste binário. A grade testa pesos "balanced" multiclasse, como o `class_weight` da produção. Na lavagem, os pesos 5 dos negativos subamostrados são os mesmos da RF.

*Orçamento de busca (4 tentativas por família):*

| Domínio | Família | Grade |
|---|---|---|
| Rede | RF de produção | Folha {20, 100} × `class_weight` |
| Rede | XGBoost | Profundidade {6, 8} × pesos |
| Lavagem | XGBoost | Profundidade {6, 8} × `min_child_weight` {1, 10} |
| Lavagem | RF | Grade de produção (1 tentativa); `rf_busca` iguala o orçamento com {100, 200} árvores × folha {10, 50} |

Também foram medidas a configuração do notebook da professora (`rf_nb`) e a RF de produção com 50 árvores (`rf_red`). A curva de árvores na validação mostrava qualidade estável de 25 a 150 árvores, então 50 árvores testam se tamanho e latência caem sem perda.

*Limitação:* o early stopping usa a validação, que também escolhe a configuração. A métrica de validação do XGBoost (0,766 na rede e 0,555 na lavagem) é otimista; a da RF não tem esse ajuste extra.

### 6.2 Resultados

**Rede.** Teste em 05/10/2026, com 46.105 medições. Os tempos são medianas de 3 ajustes com 4 threads. A latência é de uma linha no pipeline completo.

| Candidato | Tentativas / s de busca | Macro-F1 val | Macro-F1 teste (sementes 42–44) | Recall RISCO / FALHA | Inícios antecipados | Falsos alertas por fluxo-hora | Treino (s) | Latência com 4 threads, ms (mediana / p99) | Latência com 1 thread, ms | Vazão do lote (linhas/s) | Pico no ajuste (MB) | Tamanho (MB) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Regressão logística (C = 0,1) | 4 / 7,9 | 0,590 | 0,642 | 0,397 / 0,395 | 4,4% | 0,29 | 1,7 | 5,4 / 7,5 | 5,3 | 1.336.834 | 57 | 0,003 |
| HGB (31 folhas, 200 iterações) | 4 / 20,4 | 0,762 | 0,746–0,750 | 0,438 / 0,686 | 6,6% | 0,27 | 4,5 | 8,1 / 14,6 | 6,7 | 283.869 | 126 | 0,97 |
| **RF de produção** (150 árvores, folha 20) | 4 / 44,6 | 0,763 | 0,750–0,751 | 0,418 / 0,697 | 4,5% | 0,31 | 12,2 | 27,7 / 29,5 | 8,8 | 289.027 | 133 | 17,59 |
| RF com 50 árvores (folha 20) | 1 / 6,3 | 0,764 | 0,750–0,751 | 0,420 / 0,695 | 4,5% | 0,25 | 5,8 | 23,2 / 39,9 | 11,7 | 550.605 | 94 | 5,87 |
| RF do notebook (100 árvores, folha 5, bootstrap completo) | 1 / 20,7 | 0,767 | 0,754–0,756 | 0,438 / 0,696 | 5,9% | 0,29 | 24,4 | 35,8 / 51,2 | 15,7 | 239.840 | 230 | 39,21 |
| XGBoost (profundidade 6, 203 árvores) | 4 / 71,9 | 0,766* | 0,752 | 0,430 / 0,698 | 6,0% | 0,29 | 4,1 | 5,3 / 8,1 | 4,6 | 451.591 | 58 | 0,86 |

**Lavagem.** Teste em 09 e 10/09/2022, com 862.792 transações, 956 delas positivas (0,111%).

| Candidato | Tentativas / s de busca | AP val | AP teste (sementes 42–44) | Precisão / recall / F1 no limiar da validação | Falsos positivos por 10 mil | Recall@1000 por dia (09/09; 10/09) | Treino (s) | Latência com 4 threads, ms (mediana / p99) | Latência com 1 thread, ms | Vazão do lote (linhas/s) | Pico no ajuste (MB) | Tamanho (MB) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Regressão logística (C = 0,1) | 2 / 8,3 | 0,169 | 0,169 | 0,176 / 0,411 / 0,247 | 21,3 | 0,35; 0,45 | 4,0 | 4,4 / 8,6 | 4,4 | 802.234 | 132 | 0,004 |
| HGB (31 folhas, 300 iterações) | 2 / 51,7 | 0,450 | 0,414–0,444 | 0,616 / 0,394 / 0,481 | 2,7 | 0,49; 0,59 | 19,3 | 4,5 / 8,4 | 3,0 | 240.653 | 565 | 0,46 |
| **RF de produção** (100 árvores, folha 50) | 1 / 53,8 | 0,495 | 0,461–0,463 | 0,521 / 0,446 / 0,481 | 4,5 | 0,54; 0,61 | 42,7 | 26,3 / 29,2 | 5,4 | 622.377 | 175 | 2,86 |
| RF com busca (200 árvores, folha 10) | 4 / 269,8 | 0,525 | 0,470–0,478 | 0,651 / 0,412 / 0,505 | 2,4 | 0,56; 0,63 | 85,4 | 39,5 / 56,0 | 15,3 | 287.802 | 199 | 9,43 |
| XGBoost (profundidade 6, `min_child_weight` 10, 147 árvores) | 4 / 251,9 | 0,555* | 0,509 | 0,685 / 0,447 / 0,541 | 2,3 | 0,54; 0,66 | 6,6 | 4,3 / 7,8 | 4,3 | 1.188.339 | 99 | 0,13 |

\* A validação escolheu a configuração e também o número de árvores, por early stopping; por isso o valor de validação é otimista.

*Notas sobre as colunas:*
- "Pico no ajuste" é o acréscimo de bytes privados durante o ajuste, sem contar os dados já carregados (rede: 0,5 GB no processo; lavagem: cerca de 1,1 GB).
- "Tamanho" é o `joblib` com `compress=3`. Sem compressão: RF da rede 57,3 MB, RF do notebook 153,1 MB, XGBoost da rede 2,4 MB, RF da lavagem 13,0 MB, XGBoost da lavagem 0,4 MB.
- O XGBoost não tem subamostragem (`subsample=1`), então as sementes não mudam seu resultado; a variação por semente só informa sobre RF e HGB.
- Status: todos os valores foram **medidos** nesta auditoria, num único processo por família.
- Não foi medido: GPU (não usada), latência dos atributos de rede (já vêm prontos no CSV) e treino em treino+validação.

### 6.3 Leitura

- **Rede.**
  - Todos os modelos de árvore empatam em qualidade: macro-F1 de teste entre 0,750 e 0,755, com variação por semente de ±0,001 a 0,004. No bootstrap pareado por fluxo, só a RF do notebook tem diferença acima de zero em relação à RF de produção (+0,0055; IC 95% de [+0,0007; +0,011]); o XGBoost (+0,0016) e o HGB (+0,0001) não se distinguem dela.
  - Comparados à RF de produção, o XGBoost e o HGB treinam cerca de 3× mais rápido, são cerca de 20× menores e têm latência 2 a 5× menor.
  - A RF de 50 árvores já reduz o tamanho em 3× e o treino em 2×, sem perda.
  - A configuração do notebook (folha 5, bootstrap completo) teve o melhor macro-F1 de validação entre as RFs (0,767), mas é a mais pesada: 24 s de treino, 39 MB e latência de 36 ms.
  - A grade de produção não testou folhas abaixo de 20. Isso é uma oportunidade de ajuste, não um erro, e pede confirmação fora do teste atual.
- **Lavagem.**
  - Com a configuração de produção, o XGBoost é melhor que a RF em AP (0,509 × 0,461 no teste), em precisão no limiar (0,685 × 0,521, com recall igual) e em falsos positivos por 10 mil (2,3 × 4,5).
  - Com o mesmo orçamento de 4 tentativas, a RF melhora para AP de 0,525 na validação e 0,478 no teste, e o XGBoost continua à frente: +0,030 na validação e +0,031 no teste. O XGBoost também custa muito menos: 6,6 s de treino contra 85 s, 4,3 ms contra 15 a 40 ms por linha e 0,13 MB contra 9,4 MB. A vantagem aparece nos dois dias do teste (AP por dia: XGBoost 0,466 e 0,561; RF com busca 0,458 e 0,505) e nas tentativas novas (recall de 0,671 contra 0,586 da RF de produção).
  - O XGBoost é sensível a `min_child_weight`: com 1, o early stopping parou na 1ª árvore (AP 0,27). A RF variou pouco entre configurações.
- **Custo da RF.** Treinar não é o gargalo:

  | Tarefa | Treino da RF |
  |---|---|
  | Rede | 12 s de parede (47 s de CPU) |
  | Lavagem | cerca de 45 s de parede (160 a 200 s de CPU) |

  O pico de memória do ajuste fica entre +130 e +175 MB sobre os dados. Os gargalos medidos estão em outros pontos:
  1. **Latência de 1 linha com `n_jobs=4`:** 26 a 28 ms, contra 5 a 9 ms com uma thread. É o custo de criar threads por chamada.
  2. **Tamanho do artefato:** 17,6 MB comprimidos (57 MB em memória) para a RF da rede.
  3. **Atributos da lavagem:** a cada chamada, `atributos_financeiros` reordena o histórico inteiro. Isso custa cerca de 12 s fixos, seja para 1 ou para 862.792 transações: 12,0 s para uma, 11,7 s para 1.000, 12,3 s para 100.000 e 15,2 s para o teste inteiro. O classificador custa de 0,03 a 1,2 s. Em lote, o custo é aceitável; para pontuar uma transação por vez, é inviável, qualquer que seja o algoritmo.

  A percepção de lentidão no notebook vem da grade de 24 combinações com árvores sem limite e folha 5, ajustadas uma vez cada e reajustadas em treino+validação. Não vem do algoritmo em si. A configuração vencedora do notebook levou 24 s por ajuste com 4 threads. Que a grade inteira leve minutos em CPU é estimativa, não medição. GPU não é necessária para esse volume.

## 7. Desempenho: protocolo e limites da medição

- **Medições:** o protocolo completo está no [README](README.md#protocolo-de-medição): um processo por família, sem concorrência, 4 threads, tempo de parede e de CPU, bytes privados amostrados a 10 ms, 1.000 latências de uma linha, lotes com aquecimento e tamanho serializado com joblib.
- **Etapas separadas:**
  - leitura e preparação (CSV da rede; zip do HI-Small: 6,1 s e +2,0 GB);
  - ajuste dos transformadores e ajuste do estimador;
  - busca;
  - inferência do estimador e do pipeline completo.

  Na rede, as transformações em pandas do pipeline (sentinelas, constantes) custam cerca de 5 ms por chamada de uma linha. Isso pesa mais que o modelo na regressão logística, que leva 5,4 ms por linha no pipeline e 4,6 ms para o lote inteiro de 46 mil linhas no estimador. Esse é o piso de latência de qualquer candidato com o pipeline atual.
- **Máquina sob pressão de memória:** 0,4–0,5 GB livres. Os tempos de treino da RF da lavagem variaram entre sessões: 28,6 s em 26/10 e 42–52 s hoje. Comparações entre candidatos na mesma sessão são válidas; comparações com números antigos, não. As latências têm cauda longa (máximos de 30 a 50 ms), por isso foram usados mediana e p99.
- **Tipo numérico:** float64 na entrada da rede; float32 nos atributos da lavagem.
- **Requisitos:** **não há requisitos documentados** de qualidade mínima, latência, memória ou capacidade de investigação. Sem eles não existe um "vencedor". Para operação, faltam:
  - latência máxima por medição ou transação;
  - orçamento de alertas por dia (para a lavagem, a capacidade de investigação; os números de recall@1000 por dia são uma referência);
  - memória e espaço disponíveis no servidor;
  - recall mínimo de FALHA e de lavagem.

## 8. Achados priorizados

Tipos: **E** = erro confirmado; **L** = limitação metodológica; **O** = oportunidade de melhoria; **H** = hipótese ainda não testada.

| # | Tipo | Problema | Evidência | Impacto | Prioridade | Esforço | Alteração sugerida | Critério de verificação |
|---|---|---|---|---|---|---|---|---|
| 1 | L | O teste foi reutilizado para comparar 9 candidatos, e o protocolo foi desenhado vendo rótulos do período de teste | Seção 5; `resultados/e_benchmark_*.json` | Os números de teste dos candidatos ficam otimistas para escolha | Alta | Baixo | Declarar no relatório do NodeWatch; congelar o candidato escolhido na validação; confirmar em período novo | Métricas do candidato congelado num período posterior a 05/10/2026 (rede) e numa replicação declarada (lavagem) |
| 2 | L | O documento dos modelos é impreciso sobre NumPy, "regressão" e XGBoost | Seção 2.3 | A professora fica com uma leitura errada do que foi implementado | Alta | Baixo | Aplicar as correções da seção 2.3 | O documento lista os 4 estimadores efetivos e o papel de cada biblioteca |
| 3 | E (numérico, baixo impacto) | `z_valor_origem` instável com variância do histórico ≈ 0 | Seção 3A: 4/2.000 linhas reais, \|z\| até 1.939 | Pequeno nas árvores; atributo pouco interpretável | Média | Baixo | Piso para o desvio-padrão (por exemplo, 0,1 em log) ou n ≥ 3; variância por soma deslocada | O teste de força bruta (`testes/`) passa sem tolerância especial; AP de validação não piora |
| 4 | O | Latência de uma linha da RF com `n_jobs=4` | 27,7 ms contra 8,8 ms (rede); 26,3 contra 5,4 ms (lavagem) | Latência 3 a 5× maior em inferência unitária | Média | Baixo | `n_jobs=1` quando o lote é pequeno (por exemplo, menos de 1.000 linhas), mantendo 4 no treino | Mediana e p99 de uma linha ≤ resultado com 1 thread; vazão em lote inalterada |
| 5 | O | Os atributos da lavagem reconstroem os índices sobre todo o histórico a cada chamada | `h_custo_atributos.json`: 12,0 s por transação isolada, contra 0,03 s da RF | Inviabiliza pontuação on-line de uma transação | Média (alta se houver uso on-line) | Médio | Índice incremental por conta (estado mantido entre chamadas) ou pré-computação por janela | Tempo por transação independe do tamanho do histórico; força bruta continua igual |
| 6 | O | A RF da rede tem 150 árvores e 17,6 MB, mas 50 árvores dão a mesma validação | Curva de árvores; `rf_red`: 0,7637 val, 5,9 MB, 5,8 s | Artefato 3× menor e treino 2× mais rápido | Baixa | Baixo | Considerar 50 árvores, ou trocar para HGB/XGB se os requisitos pedirem latência menor | Macro-F1 de validação dentro de ±0,002 da produção; tamanho e latência medidos |
| 7 | O | A grade de produção da rede não testa folhas < 20; a da lavagem testa uma só RF | `rf_nb` (folha 5): 0,767 val; `rf_busca`: AP de validação 0,525 com folha 10 e 200 árvores, contra 0,495 | Possível ganho de qualidade | Média | Baixo | Ampliar as grades (folha {5, 10, 20}; árvores {100, 200}) mantendo a escolha na validação | Escolha feita só pela validação e confirmada em período novo |
| 8 | O | XGBoost na lavagem | Val 0,555 (com early stopping na validação); teste 0,509 contra 0,461 da RF de produção | Mais precisão com o mesmo recall; metade dos falsos positivos | Média | Médio (dependência nova; o contrato da cabeça já aceita, como mostra o teste) | Acrescentar como candidato na grade; escolher na validação | Vencer a RF ajustada na validação e no período de confirmação, com a mesma busca |
| 9 | E | A regressão logística da lavagem para antes do ótimo (17 iterações com `tol=1e-4`) | Seção 4: objetivo 0,004084 contra 0,004005; AP de validação 0,169 contra 0,190 com `tol=1e-6`; variou entre execuções | Referência linear subestimada e pouco reprodutível; as conclusões não mudam | Baixa | Baixo | `tol=1e-6` na grade da lavagem (`src/ml/modelos.py:51`) | Mesma AP de validação (±0,001) em duas execuções com threads diferentes; ‖∇‖∞ < 10⁻⁶ |
| 10 | L | Origem das referências p95/p99 desconhecida; HI-Small sintético | Seção 5 | Limita a generalização | — | — | Obter o código que gerou o `dataset_final.csv`; não apresentar o HI-Small como evidência em dados reais | — |
| 11 | H | O ganho da rede depende de fluxos conhecidos | Fluxos inéditos: 0,681 contra 0,674 | Modelo pouco útil para fluxos novos | Média | — | Testar atributos relativos ao próprio fluxo ou mais histórico | GroupKFold por fluxo acima da persistência com IC |
| 12 | O | Três dos oito "motivos verificáveis" nunca disparam para positivos | Seção 3B: os p99 de envios (19.667) e de dispersão de saída (14.230) são dominados por contas-hub; nenhum positivo tem moedas diferentes | Explicações operacionais pobres | Baixa | Baixo | Limiares por perfil de conta (por exemplo, quantis por conta ou excluindo hubs) e validação dos motivos pela frequência em positivos e negativos | Cada motivo mantido aparece em ≥ 5% dos positivos da validação, com razão positivos/negativos > 1 |
| 13 | L | O recall da lavagem é concentrado nas tipologias de `Patterns` | Seção 5: 39% dos positivos do teste não têm padrão, e a RF detecta 3,5% deles, contra cerca de 72% nas tipologias | O recall global de 0,446 superestima a cobertura dos demais mecanismos do gerador | Alta (para a leitura dos resultados) | Baixo | Reportar recall por tipologia, "sem padrão" e tentativa nova (já calculado em `f_contas_padroes.py`); investigar o que distingue os positivos sem padrão | Relatório do NodeWatch com a estratificação; nenhuma afirmação de recall global sem ela |
| 14 | L | Episódios de lavagem atravessam a fronteira treino/teste | 206 de 370 tentativas em mais de um período; 64% das linhas de padrão do teste vêm de tentativas já iniciadas; recall 0,773 nelas contra 0,586 nas novas | O teste mistura continuação de episódios já vistos com episódios novos (otimismo) | Média | Médio | Reportar à parte as tentativas novas; considerar avaliação por tentativa (agrupar por episódio) | Métrica principal recalculada só em tentativas iniciadas no período de avaliação |

Nada aqui justifica redes neurais nem refatorações extensas. Nenhum problema medido seria resolvido por elas.

## 9. Plano de testes (teste ↔ risco)

Os testes em `testes/test_implementacao_propria.py` foram executados: **12 aprovados**. A suíte do NodeWatch também passa, com 80 testes, e o `git status` do NodeWatch continua limpo.

| Teste | Risco verificado | Situação |
|---|---|---|
| `test_casos_de_fronteira_resultado_conhecido` | Borda da janela `[t−w, t)` errada; transação do mesmo minuto visível (vazamento temporal) | Passa |
| `test_atributos_iguais_a_forca_bruta_em_dados_aleatorios` (3 sementes) | Erro de índice ou ordenação no motor vetorizado; dependência da ordem do arquivo | Passa |
| `test_limiar_max_f1_igual_busca_exaustiva` | Limiar escolhido na validação não maximizar o F1 declarado | Passa |
| `test_calibracao_e_brier_iguais_a_formula_independente` | ECE ou Brier com caixas ou normalização erradas | Passa |
| `test_brier_multiclasse_igual_definicao` | Classes fora de ordem no Brier multiclasse | Passa |
| `test_psi_igual_formula_e_zero_sem_deriva` | Alerta de deriva calculado com caixas desalinhadas | Passa |
| `test_inicios_de_evento_iguais_a_laco` | Início de evento contado entre medições não consecutivas ou entre fluxos | Passa |
| `test_objetivo_da_logistica_confere_com_otimo_do_sklearn` (2 e 3 classes) | Conferência de convergência com normalização errada | Passa |
| `test_contrato_da_cabeca_aceita_outro_estimador` | Trocar o modelo (XGBoost) quebrar a ordem das classes, a persistência em joblib ou a checagem de colunas | Passa |

Já cobertos no NodeWatch (80 testes):
- `alvo`, `split` e identificadores fora dos preditores;
- esquema inválido;
- ordem e identidade das linhas na inferência;
- inferência sem rótulos;
- salvar e carregar com previsões idênticas;
- prefixo × arquivo inteiro nos atributos;
- fusão bloqueada;
- asof sem sinal posterior;
- `Patterns` fora dos atributos.

A acrescentar ao NodeWatch:
1. O teste de força bruta (risco: regressões no motor de atributos).
2. Um teste de que o artefato reproduz as métricas documentadas, dados os hashes (risco: artefato e relatório divergirem).
3. Um teste de latência de uma linha com `n_jobs=1` (risco: regressão de desempenho).

## 10. Plano de melhorias com critérios de aceite

| Ordem | Melhoria | Critério de aceite |
|---|---|---|
| 1 | Declarar o reuso do teste e definir o período de confirmação | Nota em `docs/ml/notas_relatorio.md`. Período novo coletado e guardado sem consulta até o modelo ser congelado |
| 2 | Corrigir o documento dos modelos (seção 2.3) | Revisão do grupo; a professora consegue localizar cada modelo no código pela tabela 2.1 |
| 3 | Avaliação da lavagem estratificada por tipologia, por "sem padrão" e por tentativa nova; `Patterns` e contas no `ml_config.local.toml` | `avaliar` gera essas tabelas (hoje ficam "pendentes" sem os arquivos) |
| 4 | Testes de força bruta e de reprodução do artefato no NodeWatch | `pytest` verde; o teste falha se uma janela for alterada para incluir o mesmo minuto |
| 5 | Condicionamento de `z_valor_origem` e `tol=1e-6` na regressão logística da lavagem | 0 divergências em relação à referência; AP de validação da RF ≥ a atual − 0,005; regressão logística com ‖∇‖∞ < 10⁻⁶ |
| 6 | `n_jobs=1` na inferência de poucas linhas | Mediana de uma linha ≤ 10 ms (RF da rede) na mesma máquina; vazão em lote sem queda > 5% |
| 7 | Índice incremental para a lavagem (só se houver uso on-line) | Tempo por transação constante com histórico de 1 a 5 milhões; força bruta igual |
| 8 | Ampliar as grades (RF e, opcionalmente, XGBoost como candidato) com a mesma escolha na validação | Registro de tentativas e tempo; vencedor confirmado no período novo; sem isso, manter a RF atual |
| 9 | Definir os requisitos operacionais (seção 7) | Documento com latência, memória, orçamento de alertas e recall mínimo; a escolha final do modelo cita esses números |

## 11. Conclusões explícitas

- **Manter a Random Forest?**
  - *Rede:* sim, por ora. Não há evidência de que XGBoost, HGB ou outra RF sejam melhores em qualidade: as diferenças de teste ficam dentro da variação (XGBoost − RF: +0,0016, IC 95% de [−0,003; 0,006]). Se os requisitos pedirem um artefato menor ou latência menor, HGB, XGBoost ou a RF com 50 árvores entregam a mesma qualidade com 3 a 20× menos espaço. A escolha entre eles depende de requisitos ainda não definidos.
  - *Lavagem:* a RF de produção é dominada pelo XGBoost nesta comparação. Com o mesmo orçamento de busca, o XGBoost continua melhor (+0,03 de AP) e bem mais barato. Mesmo assim, a RF não deve ser trocada antes da confirmação, pelos motivos abaixo. Se for mantida até lá, a configuração ajustada na validação (200 árvores, folha 10) é preferível à atual.
- **Adotar o XGBoost?** Ainda não como substituto direto:
  - *Rede:* não há ganho de qualidade.
  - *Lavagem:* há ganho, mas foi medido num teste já consultado, com escolha e early stopping na mesma validação, em dados sintéticos. O experimento que falta é congelar o XGBoost e a RF ajustada pela validação e compará-los uma única vez num período ou numa base de confirmação.
  - *Integração:* o contrato da cabeça já aceita o XGBoost (teste de contrato). A troca não exige mudar a arquitetura.
- **Manter ou retirar a regressão logística?** Manter como referência linear, didática e diagnóstica; não usar para operação. A tolerância da lavagem deve ser corrigida para 10⁻⁶, porque hoje ela para antes do ótimo (AP de validação 0,169 → 0,190).
- **Implementação própria em NumPy: operacional ou didática?** O que existe de próprio são os atributos point-in-time e as métricas. Os atributos estão corretos, confirmados contra a força bruta, e **são operacionais para lotes**: o pipeline de lavagem depende deles. Precisam de duas correções: o condicionamento de `z_valor_origem` e, se houver uso on-line, um índice incremental. A referência de força bruta (`scripts/referencia_atributos.py`) serve de material didático e de teste: ela mostra a definição de forma legível, mas é O(n) por consulta e lenta demais para produção (25 s para 2.000 consultas, contra 12 s para 2,48 milhões na versão vetorizada). Não há um modelo de aprendizado próprio em NumPy para avaliar. Se a disciplina pedir um, ele seria uma peça didática nova, sem problema demonstrado que o justifique na operação.
