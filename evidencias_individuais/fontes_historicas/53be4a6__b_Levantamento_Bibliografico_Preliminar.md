# Etapa (b) — Levantamento Bibliográfico

> **Como preencher:** este documento deve ser preenchido **em conjunto pelo grupo**, mas com registro individualizado da contribuição de cada integrante em cada passo. Substitua os campos entre `[ ]` pelas informações do seu grupo. Não apague as instruções em itálico — elas ajudam na avaliação do orientador.

---

## 1. Identificação do Grupo

| Campo | Informação |
|---|---|
| Curso / Disciplina | `[Computabilidade e Complexidade de Algoritmos]` |
| Projeto de Pesquisa / IC | `[Complexidade e Desempenho em Pipeline Híbrida para Detecção de Fraudes Financeiras]` |
| Orientador(a) | `[Andrea Ono Sakai]` |
| Data de entrega desta etapa | `[10/09/2026]` |
| Integrantes do grupo | `[Guilherme Lombardi 1, Ryan dos Santos Veloso 2, Caio Winkler Marangoni 3, Guilherme Liborio Camargo 4, Julia Emily Leonardo Barbosa 5]` |
| Tema (da etapa "a") | `[Análise comparativa de complexidade assintótica entre um pipeline tradicional de grafos (DFS/Kosaraju) e uma arquitetura híbrida com pré-filtragem por Autômatos Finitos, aplicada à detecção de fraudes bancárias em tempo real.]` |

---

## FASE 1 — Planejamento da Busca

### Passo 1 — Pergunta de pesquisa e palavras-chave

**1.1 Problema/pergunta de pesquisa (versão de trabalho)**
*Ainda não precisa ser a versão final (isso vem na etapa "c"), mas deve orientar a busca desta fase.*

> `[Em que medida a introdução de uma camada de pré-filtragem baseada em Autômatos Finitos reduz a complexidade assintótica e o tempo de resposta de um pipeline de detecção de fraudes bancárias em tempo real, quando comparada à varredura direta via DFS/Kosaraju?]`

**1.2 Conceitos-chave e sinônimos**
*Liste os conceitos centrais da pergunta e seus sinônimos, em português e inglês.*

| Conceito-chave | Sinônimos / termos relacionados (PT) | Sinônimos / termos relacionados (EN) |
|---|---|---|
| `[ex.: Segurança]` | `[proteção, vulnerabilidade]` | `[security, vulnerability]` |
| `[ex.: IoT]` | `[Internet das Coisas]` | `[Internet of Things, smart devices]` |
| `[Complexidade Assintótica ]` | `[Análise de algoritmos, Notação Big-O, Custo computacional, Limite assintótico, Escalonamento de desempenho ]` | `[Asymptotic complexity, Big-O notation, Computational cost, Algorithm scalability, Time-space complexity ]` |
| `[Pré-filtragem por Autômatos Finitos ]` | `[Autômato Finito Determinístico (DFA), Processamento de Eventos Complexos (CEP), Filtro de entrada, Validação em tempo linear ]` | `[Deterministic Finite Automaton (DFA), Complex Event Processing (CEP), Stream filtering, Pattern matching automata, Edge filtering ]` |
| `[Algoritmos de Travessia em Grafos ]` | `[Busca em Profundidade (DFS), Componentes Fortemente Conectados (Kosaraju), Detecção de ciclos, Centralidade de rede ]` | `[Depth-First Search (DFS), Kosaraju's algorithm, Strongly Connected Components (SCC), Graph traversal, Sub-graph detection ]` |
| `[Processamento de Fluxos de Dados ]` | `[Processamento em tempo real, Processamento de streams, Análise contínua de dados, Baixa latência ]` | `[Stream processing, Data stream mining, Real-time event processing, Low-latency processing, In-memory streaming ]` |
| `[Detecção de Fraudes Bancárias ]` | `[Detecção de anomalias financeiras, Transações suspeitas, Análise de risco em tempo real, Prevenção à fraude ]` | `[Financial fraud detection, Real-time anomaly detection, Credit card fraud detection, Transaction monitoring, Anti-fraud pipeline ]` |

*Responsável por este passo: `[Guilherme Lombardi]`*

---

### Passo 2 — Strings de busca

*Combine os termos do passo 1 com operadores booleanos (`AND`, `OR`, `NOT`). Use aspas para termos compostos e truncamento (`*`) quando a base permitir.*

*Coluna extra "Conceito-chave / eixo coberto" adicionada para rastrear cada string ate os conceitos do Passo 1.2, ate a pergunta de pesquisa do item 1.1 e ate os modulos do sistema atual (`cycle_detection.py`, `scc.py`, `centralidade.py`).*

| No | String de busca | Conceito-chave / eixo coberto (Passo 1) | Base(s) em que sera usada | Elaborada por |
|---|---|---|---|---|
| 1 | `["cycle enumeration" OR "simple cycles" OR "cycle detection") AND ("directed graph" OR "transaction graph" OR "transaction network") AND ("time complexity" OR "exponential" OR "pruning" OR "scalability")]` | `[Complexidade Assintotica — gargalo do modulo cycle_detection.py]` | `[ACM DL; IEEE Xplore; Springer Link]` | `[Caio Winkler Marangoni]` |
| 2 | `[("cycle" OR "circular flow" OR "temporal cycle") AND ("money laundering" OR "layering" OR "smurfing" OR "anti-money laundering") AND ("graph" OR "network")]` | `[Deteccao de Fraudes Bancarias — layering, o padrao que o sistema procura]` | `[ACM DL; Springer Link; ScienceDirect]` | `[Caio Winkler Marangoni]` |
| 3 | `[("strongly connected components" OR "Kosaraju" OR "Tarjan" OR "SCC") AND ("large-scale" OR "parallel" OR "distributed" OR "scalability") AND ("directed graph" OR "graph processing")]` | `[Algoritmos de Travessia em Grafos — custo do modulo scc.py em escala]` | `[IEEE Xplore; ACM DL; Springer Link]` | `[Caio Winkler Marangoni]` |
| 4 | `[("finite automaton" OR "deterministic finite automaton" OR "DFA" OR "complex event processing") AND ("event stream" OR "stream processing") AND ("pattern matching" OR "filtering" OR "candidate reduction")]` | `[Pre-filtragem por Automatos Finitos — foco central da pesquisa]` | `[ACM DL; IEEE Xplore]` | `[Caio Winkler Marangoni]` |
| 5 | `[("pre-filter*" OR "candidate reduction" OR "pruning" OR "filtering layer") AND ("graph search" OR "graph traversal" OR "subgraph matching") AND ("real-time" OR "streaming" OR "low latency")]` | `[Processamento de Fluxos de Dados — a hipotese: reduzir o volume antes da travessia]` | `[ACM DL; ScienceDirect; arXiv]` | `[Caio Winkler Marangoni]` |
| 6 | `[("PaySim" OR "synthetic financial dataset" OR "mobile money simulator") AND ("fraud" OR "money laundering")]` | `[Base experimental — origem e limites do dataset usado no sistema]` | `[Springer Link; IEEE Xplore; arXiv]` | `[Caio Winkler Marangoni]` |
| 7 | `[("automat*" OR "complex event processing") AND ("pre-filter*" OR "filtering layer") AND ("cycle detection" OR "strongly connected components" OR "graph traversal") AND ("fraud" OR "money laundering")]` | `[String-sintese: reproduz a pergunta de pesquisa do item 1.1 (pipeline hibrido)]` | `[ACM DL; Springer Link; arXiv]` | `[Caio Winkler Marangoni]` |
| 8 | `[("Graph Neural Network*" OR "GNN") AND ("Financial Fraud" OR "Fraud Detection" OR "Transaction Fraud")]` | `[Detecção de fraudes em grafos financeiros / Análise de transações atípicas (cycle_detection.py)]` | `[Springer / IEEE / ACM]` | `[Guilherme Libório Camargo]` |
| 9 | `[("Complex Event Processing" OR "CEP") AND ("Graph Processing" OR "Stream Analytics") AND ("Real-time" OR "Parallel")]` | `[Processamento de eventos complexos e análise de grafos em tempo real (centralidade.py)]` | `[ACM Digital Library / IEEE]` | `[Guilherme Libório Camargo]` |
| 10 | `[("Graph Anomaly Detection" OR "GAD") AND ("Supervised Learning" OR "Benchmark*" OR "Graph Mining")]` | `[Análise e benchmark de detecção de anomalias em estruturas de grafos (scc.py)]` | `[NeurIPS / Google Scholar / ScienceDirect]` | `[Guilherme Libório Camargo]` |
| 11 | `[("data engineering" OR "feature engineering" OR "data preprocessing") AND ("fraud detection" OR "financial fraud") AND ("computational complexity" OR "scalability")`] | `[Engenharia de dados, pré-processamento de transações e complexidade computacional para pipelines em larga escala (Relação: (cycle_detection.py.)]` | `[ScienceDirect (Elsevier)]` | `[Ryan dos Santos Veloso]`|
| 12 | `[("machine learning" OR "classification algorithms") AND ("financial fraud detection" OR "banking fraud") AND ("performance evaluation" OR "benchmark")]` | `[Avaliação de desempenho de algoritmos em fraudes financeiras e métricas de relevância (Relação: (centralidade.py).]` | `[MDPI]` | `[Ryan dos Santos Veloso]` |
| 13 | `[("graph analysis" OR "graph algorithms" OR "path detection") AND ("fraudulent accounts" OR "money laundering") AND ("parallel paths" OR "cycle detection" OR "strongly connected components")]` | `[Algoritmos em grafos, detecção de caminhos paralelos e subestruturas fortemente conectadas/cíclicas em redes bancárias (Relação: (scc.py) e (cycle_detection.py).]` | `[PubMed Central / IEEE Xplore / ScienceDirect]` | `[Ryan dos Santos Veloso]` |
| 14 | `[("Finite Automata" OR "DFA" OR "Complex Event Processing") AND ("fraud detection" OR "stream filtering") AND ("graph reduction" OR "latency")]` | `[IEEE Xplore, ACM Digital Library, ScienceDirect, Google Scholar ]` | `[Guilherme Lombardi]` |
| 15 | `[("financial fraud" OR "anti-money laundering") AND ("strongly connected components" OR "Kosaraju" OR "DFS") AND ("graph complexity" OR "time complexity")]` | `[IEEE Xplore, ACM Digital Library, Google Scholar ]` | `[Guilherme Lombardi]` |
| 16 | `[("graph stream" OR "real-time graph") AND ("pre-filtering" OR "subgraph extraction") AND ("asymptotic complexity" OR "worst-case bound") AND "fraud"]` | `[ACM Digital Library, IEEE Xplore, ScienceDirect, Google Scholar ]` | `[Guilherme Lombardi]` |
| 17 | `[("subgraph reduction" OR "graph pruning" OR "stream filtering") AND ("graph traversal" OR "strongly connected components") AND ("financial fraud" OR "transaction network") ]` | `[ACM Digital Library, IEEE Xplore, Google Scholar ]` | `[Guilherme Lombardi]` |
| 18 | `[("real-time graph" OR "streaming graph") AND ("pre-filter" OR "early discard") AND ("computational complexity" OR "execution time") AND "fraud" ]` | `[ACM Digital Library, IEEE Xplore, Google Scholar ]` | `[Guilherme Lombardi]` |
| 19 | `[("rule-based filter" OR "automata") AND ("graph analytics" OR "network analysis") AND ("performance evaluation" OR "latency reduction") AND "fraud" ]` | `[ACM Digital Library, IEEE Xplore, Google Scholar ]` | `[Guilherme Lombardi]` |



**Observacoes sobre a construcao das strings**

- As strings foram reescritas a partir do vocabulario do sistema que o grupo ja implementou, e nao do vocabulario generico de "fraude com machine learning". O sistema modela transacoes como multigrafo direcionado ponderado e procura **estrutura** (ciclos, componentes fortemente conectados, centralidade) — nao classifica transacao individual. Buscar por `"credit card fraud detection" AND "machine learning"` devolve outra literatura.
- A **string 1** e a mais importante: o proprio README do sistema registra que "a enumeracao de todos os ciclos simples tem pior caso teorico exponencial em |V|". Esse expoente e o que a camada de pre-filtragem existe para atacar, e e o que a pergunta do item 1.1 pergunta.
- As **strings 1 e 3** cobrem o baseline da comparacao (DFS/Kosaraju ja implementados); as **strings 4 e 5** cobrem a camada proposta (automato / pre-filtro); a **string 2** ancora tudo no dominio de aplicacao (lavagem de dinheiro, layering).
- A **string 6** existe para a secao de metodologia: o sistema le CSV no formato PaySim (`step, type, amount, nameOrig, nameDest, isFraud`), e sera preciso citar a origem e as limitacoes desse dataset.
- A **string 7** e a mais restritiva e serve de teste de originalidade: se retornar poucos resultados, isso e evidencia a favor da nao-redundancia argumentada no item 3.3 da etapa (a).
- Truncamento com `*` so nas bases que aceitam (ACM DL e ScienceDirect aceitam; conferir no Passo 5). Onde nao aceitar, expandir para `("pre-filter" OR "pre-filtering" OR "pre-filtered")` e `("automaton" OR "automata" OR "automata-based")`.

---

### Passo 3 — Bases de dados escolhidas

*Selecione de 2 a 4 bases relevantes ao tema. Registre a justificativa — isso vai para a seção de metodologia do artigo/relatório de IC.*

| Base de dados | Por que foi escolhida | Responsável pela busca nesta base |
|---|---|---|
| `[IEEE Xplore]` | `[Referência internacional em engenharia e computação; essencial para mapear artigos sobre Complex Event Processing (CEP), arquiteturas de altíssimo desempenho e processamento de fluxos em tempo real. ]` | `[Guilherme Lombardi]` |
| `[ACM Digital Library]` | `[Principal repositório de Ciência da Computação teórica e aplicada; fundamental para resgatar estudos sobre Teoria dos Autômatos, Regular Path Queries (RPQ) e algoritmos de grafos. ]` | `[Guilherme Lombardi]` |
| `[Google Scholar ]` | `[Permite ampla cobertura da literatura cinzenta, pré-prints e conferências emergentes (2020–2026), garantindo a recuperação de artigos recentes sobre grafos temporais e detecção de fraudes financeiras. ]` | `[Guilherme Lombardi]` |
| `[Springer Link ]` | `[Altíssima relevância em Ciência da Computação (incluindo as coleções LNCS); apresentou maior volume de artigos aderentes sobre algoritmos em grafos, otimização de complexidade e autômatos. ]` | `[Guilherme Lombardi]` |

---

### Passo 4 — Critérios de inclusão e exclusão

**Critérios de inclusão:**
- `[Artigos publicados no recorte temporal recente (entre 2020 e 2026)]`
- `[Artigos científicos revisados por pares (peer-reviewed) publicados em periódicos ou anais de conferências relevantes.]`
- `[Trabalhos publicados no idioma inglês ou português.]`
- `[Textos disponíveis na íntegra para leitura e análise qualitativa.]`
- `[Estudos focados em detecção de fraudes financeiras/bancárias, processamento de fluxos em tempo real (stream processing/CEP), algoritmos em grafos temporais/dinâmicos ou consultas via autômatos (Regular Path Queries - RPQ). ]`
- `[Trabalhos que apresentem análise de complexidade computacional, otimização de latência/vazão ou mecanismos de pré-filtragem/redução de carga (load shedding/pruning). ]`

**Critérios de exclusão:**
- `[Artigos publicados antes de 2020 (exceto os livros texto clássicos para fundamentação teórica de base).]`
- `[Publicações sem texto completo acessível (paywall sem acesso via repositório/convênio).]`
- `[Artigos duplicados entre as diferentes bases de dados consultadas.]`
- `[Trabalhos fora do escopo do tema (ex.: detecção de fraudes sem abordagem algorítmica/computacional ou focados exclusivamente em aspectos jurídicos/financeiros não-técnicos).]`
- `[Trabalhos que utilizem apenas técnicas de Aprendizado de Máquina/IA "caixa-preta" sem abordagem estrutural em grafos, autômatos ou análise formal de complexidade assintótica. ]`
- `[Artigos de opinião, editoriais, resumos expandidos de eventos sem avaliação cega ou literatura não-científica. ]`

*Definidos em conjunto por: `[Guilherme Lombardi]`*

---

## FASE 2 — Execução da Busca e Triagem

### Passo 5 — Execução das buscas e registro dos resultados

*Anote quantos resultados cada string trouxe em cada base (útil para o fluxograma tipo PRISMA, se o projeto exigir). Exporte as referências (BibTeX, RIS, CSV) para um gerenciador de referências.*

| Base | String usada (nº) | Data da busca | Nº de resultados | Executada por |
|---|---|---|---|---|
| `[ACM Digital Library ]` | `[String 1 ]` | `[06/09/2026 ]` | `[18 ]` | `[Caio Winkler Marangoni ]` |
| `[IEEE Xplore ]` | `[String 1 ]` | `[06/09/2026 ]` | `[12 ]` | `[Caio Winkler Marangoni ]` |
| `[Springer Link ]` | `[String 1 ]` | `[06/09/2026 ]` | `[15 ]` | `[Caio Winkler Marangoni ]` |
| `[ACM Digital Library ]` | `[String 2 ]` | `[06/09/2026 ]` | `[14 ]` | `[Caio Winkler Marangoni ]` |
| `[Springer Link ]` | `[String 2 ]` | `[06/09/2026 ]` | `[22 ]` | `[Caio Winkler Marangoni ]` |
| `[ScienceDirect ]` | `[String 2 ]` | `[06/09/2026 ]` | `[19 ]` | `[Caio Winkler Marangoni ]` |
| `[IEEE Xplore ]` | `[String 3 ]` | `[06/09/2026 ]` | `[25 ]` | `[Caio Winkler Marangoni ]` |
| `[ACM Digital Library ]` | `[String 3 ]` | `[06/09/2026 ]` | `[16 ]` | `[Caio Winkler Marangoni ]` |
| `[Springer Link ]` | `[String 3 ]` | `[06/09/2026 ]` | `[20 ]` | `[Caio Winkler Marangoni ]` |
| `[ACM Digital Library ]` | `[String 4 ]` | `[06/09/2026 ]` | `[11 ]` | `[Caio Winkler Marangoni ]` |
| `[IEEE Xplore ]` | `[String 4 ]` | `[06/09/2026 ]` | `[9 ]` | `[Caio Winkler Marangoni ]` |
| `[ACM Digital Library ]` | `[String 5 ]` | `[06/09/2026 ]` | `[13 ]` | `[Caio Winkler Marangoni ]` |
| `[ScienceDirect ]` | `[String 5 ]` | `[06/09/2026 ]` | `[17 ]` | `[Caio Winkler Marangoni  ]` |
| `[arXiv ]` | `[String 5 ]` | `[06/09/2026 ]` | `[8 ]` | `[Caio Winkler Marangoni ]` |
| `[Springer Link ]` | `[String 6 ]` | `[06/09/2026 ]` | `[10 ]` | `[Caio Winkler Marangoni ]` |
| `[IEEE Xplore ]` | `[String 6 ]` | `[06/09/2026 ]` | `[6 ]` | `[Caio Winkler Marangoni ]` |
| `[arXiv ]` | `[String 6 ]` | `[06/09/2026 ]` | `[5 ]` | `[Caio Winkler Marangoni ]` |
| `[ACM Digital Library ]` | `[String 7 ]` | `[06/09/2026 ]` | `[4 ]` | `[Caio Winkler Marangoni ]` |
| `[Springer Link ]` | `[String 7 ]` | `[06/09/2026 ]` | `[7 ]` | `[Caio Winkler Marangoni ]` |
| `[arXiv ]` | `[String 7 ]` | `[06/09/2026 ]` | `[3 ]` | `[Caio Winkler Marangoni ]` |
| `[Springer Link ]` | `[String 8 ]` | `[05/09/2026 ]` | `[21 ]` | `[Guilherme Libório Camargo ]` |
| `[IEEE Xplore ]` | `[String 8 ]` | `[05/09/2026 ]` | `[18 ]` | `[Guilherme Libório Camargo ]` |
| `[ACM Digital Library ]` | `[String 8 ]` | `[05/09/2026 ]` | `[15 ]` | `[Guilherme Libório Camargo ]` |
| `[ACM Digital Library ]` | `[String 9 ]` | `[05/09/2026 ]` | `[14 ]` | `[Guilherme Libório Camargo ]` |
| `[IEEE Xplore ]` | `[String 9 ]` | `[05/09/2026 ]` | `[19 ]` | `[Guilherme Libório Camargo ]` |
| `[Google Scholar ]` | `[String 10 ]` | `[05/09/2026 ]` | `[28 ]` | `[Guilherme Libório Camargo ]` |
| `[ScienceDirect ]` | `[String 10 ]` | `[05/09/2026 ]` | `[16 ]` | `[Guilherme Libório Camargo ]` |
| `[ScienceDirect ]` | `[String 11 ]` | `[08/09/2026 ]` | `[23 ]` | `[Ryan dos Santos Veloso ]` |
| `[MDPI ]` | `[String 12 ]` | `[08/09/2026 ]` | `[31 ]` | `[Ryan dos Santos Veloso ]` |
| `[PubMed Central ]` | `[String 13 ]` | `[08/09/2026 ]` | `[12 ]` | `[Ryan dos Santos Veloso ]` |
| `[IEEE Xplore ]` | `[String 13 ]` | `[08/09/2026 ]` | `[17 ]` | `[Ryan dos Santos Veloso ]` |
| `[ScienceDirect ]` | `[String 13 ]` | `[08/09/2026 ]` | `[20 ]` | `[Ryan dos Santos Veloso ]` |
| `[IEEE Xplore]` | `[Strings 14, 15 e 18 ]` | `[09/09/2026]` | `[42]` | `[Guilherme Lombardi]` |
| `[ACM Digital Library]` | `[Strings 14, 16 e 19 ]` | `[09/09/2026]` | `[38]` | `[Guilherme Lombardi]` |
| `[Springer Link ]` | `[Strings 15, 17 e 19 ]` | `[09/09/2026]` | `[55]` | `[Guilherme Lombardi]` |
| `[Google Scholar ]` | `[Strings 3 e 4 ]` | `[09/09/2026]` | `[61]` | `[Guilherme Lombardi]` |

**Total de resultados brutos (soma de todas as buscas):** `[721]`

**Gerenciador de referências utilizado:** `[Repositório local de artigos (Armazenamento em diretório do projeto)]`
**Formato de exportação:** `[Documentos na íntegra (PDF) e citações diretas das bases.]`

---

### Passo 6 — Triagem por título e resumo (1ª filtragem)

*Leia apenas título e resumo de cada resultado. Classifique: incluir / excluir / dúvida. Remova duplicatas entre bases.*

| Item de controle | Quantidade |
|---|---|
| Total de resultados antes da triagem | `[721 ]` |
| Duplicatas removidas | `[525 ]` |
| Classificados como "Incluir" | `[54 ]` |
| Classificados como "Excluir" | `[142 ]` |
| Classificados como "Dúvida" | `[0]` |

*A triagem detalhada, artigo por artigo, deve ser registrada na planilha de controle do projeto (aba "Triagem de Artigos"). Aqui, registre apenas o resumo quantitativo.*

**Como as dúvidas foram resolvidas?** *(ex.: discussão em grupo, consulta ao orientador)*
`[As dúvidas foram alinhadas por meio de conversas informais presenciais durante os horários vagos das aulas e trocas frequentes de mensagens no grupo virtual dos integrantes. Para analisar trechos mais complexos, foram realizadas pesquisas complementares na internet e utilizado o auxílio de inteligências artificiais para triagem inicial de conceitos, alinhando o direcionamento final das escolhas com as orientações da professora Andrea Ono Sakai.]`

*Responsável(is) por esta triagem: `[Guilherme Lombardi, Caio Winkler Marangoni, Guilherme Libório Camargo, Ryan dos Santos Veloso, Julia Emily Leonardo Barbosa]`*

---

### Passo 7 — Triagem por leitura completa (2ª filtragem)

*Para os artigos que passaram na primeira filtragem, leia introdução e conclusão. Aplique os critérios de inclusão/exclusão (passo 4) de forma mais rigorosa.*

| Item de controle | Quantidade |
|---|---|
| Total de artigos que entraram nesta filtragem | `[54 ]` |
| Aprovados (conjunto definitivo para fichamento) | `[16 ]` |
| Excluídos nesta etapa | `[38 ]` |

**Principais motivos de exclusão nesta filtragem:**
- `[Ausência de análise formal de complexidade assintótica ou de métricas quantitativas de tempo de execução/latência no processamento do fluxo. ]`
- `[Foco exclusivo em modelos de Aprendizado de Máquina/IA "caixa-preta" para classificação individual de transações, sem abordagem de pré-filtragem estrutural ou análise em grafos. ]`

*Responsável(is) por esta triagem: `[Guilherme Lombardi, Caio Winkler Marangoni, Guilherme Libório Camargo, Ryan dos Santos Veloso, Julia Emily Leonardo Barbosa]`*

---

## 3. Lista Final de Artigos Selecionados (Conjunto Definitivo)

*Liste aqui os artigos que passaram por todas as filtragens e seguirão para o fichamento (etapa "j"). Referência completa no formato ABNT/APA definido pelo projeto.*

1. `[ZHANG, Ruirui et al. DARLING: Data-Aware Load Shedding in Complex Event Processing. Proceedings of the VLDB Endowment, v. 14, n. 11, p. 2270-2282, 2021. Disponível em: https://dl.acm.org/doi/abs/10.14778/3494124.3494137. Acesso em: 10 set. 2026.]`
2. `[HYSON, Luke et al. hSPICE: State-Aware Event Shedding in Complex Event Processing. In: ACM INTERNATIONAL CONFERENCE ON DISTRIBUTED AND EVENT-BASED SYSTEMS (DEBS '20), 14., 2020, Montreal. Proceedings... New York: ACM, 2020. p. 49-60. Disponível em: https://dl.acm.org/doi/abs/10.1145/3401025.3401742. Acesso em: 10 set. 2026.]`
3. `[KOLCHINSKY, Ilya et al. HYPERSONIC: A Hybrid Parallelization Approach for Scalable Complex Event Processing. In: ACM INTERNATIONAL CONFERENCE ON MANAGEMENT OF DATA (SIGMOD '22), 2022, Philadelphia. Proceedings... New York: ACM, 2022. p. 892-905. Disponível em: https://dl.acm.org/doi/abs/10.1145/3514221.3517829. Acesso em: 10 set. 2026.]`
4. `[PFANDZELTER, Tobias; BERMBACH, David. Operator as a Service: Stateful Serverless Complex Event Processing. In: IEEE INTERNATIONAL CONFERENCE ON BIG DATA (BIG DATA '20), 2020, Atlanta. Proceedings... Piscataway: IEEE, 2020. p. 2875-2884. Disponível em: https://ieeexplore.ieee.org/abstract/document/9378142. Acesso em: 10 set. 2026.]`
5. `[LI, Xueli et al. Efficient Densest Flow Queries in Transaction Flow Networks. IEEE Transactions on Knowledge and Data Engineering, v. 38, n. 7, p. 1147-1160, 2026. Disponível em: https://ieeexplore.ieee.org/abstract/document/11471253. Acesso em: 10 set. 2026.]`
6. `[CAPOZZI, Arthur et al. FlowSeries: Anomaly Detection in Financial Transaction Flows. In: INTERNATIONAL CONFERENCE ON COMPLEX NETWORKS AND THEIR APPLICATIONS (COMPLEX NETWORKS '24), 13., 2024, Lisboa. Complex Networks & Their Applications XIII. Cham: Springer, 2025. p. 28-40. (Studies in Computational Intelligence, v. 1189). Disponível em: https://link.springer.com/chapter/10.1007/978-3-031-82435-7_3. Acesso em: 10 set. 2026.]`
7. `[CAPOZZI, Arthur et al. FlowSeries: Flow Analysis on Financial Networks. Applied Network Science, v. 10, n. 1, art. 28, p. 1-24, 2025. Disponível em: https://link.springer.com/article/10.1007/s41109-025-00711-0. Acesso em: 10 set. 2026.]`
8. `[LI, Zhiyong et al. Internet Financial Fraud Detection Based on a Distributed Big Data Approach With Node2vec. IEEE Access, v. 9, p. 23145-23156, 2021. Disponível em: https://ieeexplore.ieee.org/document/9363921. Acesso em: 10 set. 2026.]`
9. `[WANG, Yong et al. TempASD: Temporal Anomalous Subgraph Discovery in Large-Scale Dynamic Financial Networks. In: ACM SIGKDD CONFERENCE ON KNOWLEDGE DISCOVERY AND DATA MINING (KDD '25), 31., 2025, Toronto. Proceedings... New York: ACM, 2025. p. 1420-1431. Disponível em: https://dl.acm.org/doi/abs/10.1145/3711896.3737149. Acesso em: 10 set. 2026.]`
10. `[ZHENG, Lixiao; XIAO, Jipeng. Temporal Cycle Enumeration for Detecting Financial Fraud. Data and Information Management, v. 9, n. 2, art. 100058, p. 1-12, 2024. Disponível em: https://www.sciengine.com/DI/doi/10.3724/2096-7004.di.2024.0058. Acesso em: 10 set. 2026.]`
11. `[WU, Zhiying et al. TRacer: Scalable Graph-Based Transaction Tracing for Account-Based Blockchain Trading Systems. IEEE Transactions on Information Forensics and Security, v. 18, p. 2541-2555, 2023. Disponível em: https://dl.acm.org/doi/abs/10.1109/TIFS.2023.3266162. Acesso em: 10 set. 2026.]`
12. `[DARWISH, Saad M. et al. An Intelligent Memetic Approach to Detect Online Fraud for Distributed FinTech Environments. Electronic Commerce Research, v. 25, n. 2, p. 415-438, 2025. Disponível em: https://link.springer.com/article/10.1007/s10660-025-10050-y. Acesso em: 10 set. 2026.]`
13. `[IYER, Anand P. et al. ASAP: Fast, Approximate Graph Pattern Mining at Scale. In: USENIX SYMPOSIUM ON OPERATING SYSTEMS DESIGN AND IMPLEMENTATION (OSDI '18), 13., 2018, Carlsbad. Proceedings... Berkeley: USENIX Association, 2018. p. 745-761. Disponível em: https://dl.acm.org/doi/abs/10.5555/3291168.3291224. Acesso em: 10 set. 2026.]`
14. `[CHEN, Xining et al. cuRPQ: A High-Performance GPU-Based Framework for Processing Regular and Conjunctive Regular Path Queries. In: ACM SIGMOD INTERNATIONAL CONFERENCE ON MANAGEMENT OF DATA (SIGMOD '26), 2026, Santiago. Proceedings... New York: ACM, 2026. p. 1-15. Disponível em: https://dl.acm.org/doi/abs/10.1145/3802033. Acesso em: 10 set. 2026.]`
15. `[AHMAD, Shahbaz. Scalable Analytics on Multi-Streams Dynamic Graphs. 2025. Tese (Doutorado em Ciência da Computação) — Université Grenoble Alpes, Grenoble, 2025. Disponível em: https://theses.hal.science/tel-05351773/. Acesso em: 10 set. 2026.]`
16. `[JEYARAMAN, Brindha Priyadarshini. Temporal Relational Graph Convolutional Networks for Financial Applications. 2025. Tese (Doutorado em Engenharia) — Singapore Management University, Singapura, 2025. Disponível em: https://ink.library.smu.edu.sg/etd_coll/703. Acesso em: 10 set. 2026.]`

*(Adicione quantas linhas forem necessárias.)*

---

## 4. Contribuição Individual dos Integrantes

> **Importante:** cada integrante deve descrever, com suas próprias palavras, o que efetivamente fez em cada passo desta etapa. Contribuições genéricas como "ajudei em tudo" não serão aceitas. Use verbos de ação e seja específico (ex.: "executei a busca no IEEE Xplore com a string 2 e obtive 84 resultados; fiz a triagem por título/resumo de 40 desses").

### Integrante 1 — `[Guilherme Lombardi]`
- **Passo(s) em que atuou:** `[Passos 1, 2, 3, 4, 5, 6 e 7]`
- **O que fez em cada passo:** 
- `[Passo 1: Elaborei a pergunta de pesquisa central sobre o uso de Autômatos Finitos para redução de complexidade assintótica e fiz o mapeamento dos conceitos-chave e seus sinônimos (PT/EN).]` 
- `[Passo 2: Formulei e validei as strings de busca 14 a 19 focadas nos conceitos de pré-filtragem, latência e complexidade em grafos.]` 
- `[Passo 3: Selecionei e redigi a justificativa metodológica para o uso das quatro bases principais (IEEE Xplore, ACM Digital Library, Springer Link e Google Scholar).]` 
- `[Passo 4: Redigi os critérios de inclusão e exclusão técnicos para direcionar o escopo do projeto de 2020 a 2026.]` 
- `[Passo 5: Consolidei os registros de buscas de todo o grupo, executei as varreduras com as strings 14 a 19 e organizei os metadados dos artigos em diretório local.]` 
- `[Passos 6 e 7: Participei ativamente da triagem por título/resumo dos 721 resultados brutos, remoção de duplicatas e conduzi a leitura completa dos artigos para fechamento do conjunto definitivo de 16 publicações.]` 
- **Tempo dedicado (aprox.):** `[18h]`
- **Evidência da contribuição** *(print de busca, planilha de triagem, exportação BibTeX, etc.)*: `[acervo digital dos PDFs organizados e postagens dos artigos no github]`

### Integrante 2 — `[Caio Winkler Marangoni]`
- **Passo(s) em que atuou:** `[Passos 2, 5, 6 e 7 ]`
- **O que fez em cada passo:** 
- `[Passo 2: Criei as strings de busca de 1 a 7, conectando os eixos do projeto ao vocabulário técnico do sistema implementado pelo grupo (enumeração de ciclos, componentes fortemente conectados no scc.py e padrões do PaySim).]`
- `[Passo 5: Executei as varreduras de teste e coleta das strings 1 a 7 nas bases ACM DL, IEEE Xplore, Springer Link, ScienceDirect e arXiv, registrando o volume de resultados de cada consulta.]`
- `[Passos 6 e 7: Colaborei no processo de desduplicação e triagem por título/resumo e participei da leitura dos textos integrais dos artigos do eixo de algoritmos em grafos.]`
- **Tempo dedicado (aprox.):** `[10h]`
- **Evidência da contribuição:** `[Definição das strings 1 a 7 na documentação e histórico de registros da primeira e segunda filtragem.]`

### Integrante 3 — `[Guilherme Libório Camargo]`
- **Passo(s) em que atuou:** `[Passos 2, 5, 6 e 7 ]`
- **O que fez em cada passo:** 
- `[Passo 2: Formulei as strings de busca de 8 a 10 focadas em redes neurais em grafos (GNNs), processamento de eventos complexos e detecção de anomalias estruturais.]`
- `[Passo 5: Realizei as buscas com as strings 8 a 10 nas bases Springer Link, IEEE Xplore, ACM DL, NeurIPS, Google Scholar e ScienceDirect, contabilizando o retorno de cada uma.]`
- `[Passos 6 e 7: Atuei na filtragem de títulos e resumos para eliminação de trabalhos focados unicamente em IA caixa-preta e auxilei na seleção dos artigos do conjunto definitivo]`
- **Tempo dedicado (aprox.):** `[ex.: 9h]`
- **Evidência da contribuição:** `[Mapeamento das strings 8 a 10 e registros de participação na planilha de triagem do grupo.]`

### Integrante 4 — `[Ryan dos Santos Veloso]`
- **Passo(s) em que atuou:** `[Passos 2, 5, 6 e 7 ]`
- **O que fez em cada passo:**
- `[Passo 2: Desenvolvi as strings de busca de 11 a 13 direcionadas à engenharia de dados, pré-processamento de transações e busca por caminhos paralelos/ciclos em redes bancárias.]`
- `[Passo 5: Executei a busca das strings 11 a 13 nas bases ScienceDirect, MDPI, PubMed Central e IEEE Xplore, registrando a contagem de resultados retornados.]`
- `[Passos 6 e 7: Participei das reuniões presenciais e remotas do grupo para discussão sobre a exclusão de artigos fora do escopo e leitura de introdução/conclusão dos artigos pré-selecionados.]`
- **Tempo dedicado (aprox.):** `[9h]`
- **Evidência da contribuição:** `[Estruturação das strings 11 a 13 e participação nos registros das etapas de filtragem do PRISMA.]`

### Integrante 5 — `[Julia Emily Leonardo Barbosa]`
- **Passo(s) em que atuou:** `[Passos 6 e 7 ]`
- **O que fez em cada passo:**
- `[Passo 6: Participou ativamente das conversas do grupo nas aulas vagas e no ambiente virtual para análise de títulos e resumos, auxiliando na identificação e remoção de duplicatas entre as bases.]`
- `[Passo 7: Colaborou na leitura analítica de introdução e conclusão dos artigos pré-selecionados, ajudando no desempate de dúvidas com suporte de buscas complementares e no alinhamento às orientações da professora Andrea Ono Sakai.]`
- **Tempo dedicado (aprox.):** `[6h]`
- **Evidência da contribuição:** `[Registro de participação na planilha de triagem do projeto e validação dos critérios de exclusão do conjunto final.]`

*(Copie o bloco acima para cada integrante adicional do grupo.)*

### 4.1 Quadro-resumo de participação por passo

| Passo | Responsável(is) | % estimado de participação de cada um |
|---|---|---|
| 1. Pergunta e palavras-chave | `[Guilherme Lombardi]` | `[Guilherme Lombardi (100%) ]` |
| 2. Strings de busca | `[Caio, Guilherme Libório, Ryan e Guilherme Lombardi]` | `[Caio (30%), Guilherme Libório (25%), Ryan (25%), Guilherme Lombardi (20%) ]` |
| 3. Bases de dados | `[Guilherme Lombardi]` | `[Guilherme Lombardi (100%) ]` |
| 4. Critérios de inclusão/exclusão | `[Guilherme Lombardi]` | `[Guilherme Lombardi (100%) ]` |
| 5. Execução das buscas | `[Guilherme Lombardi, Caio, Guilherme Libório e Ryan]` | `[Guilherme Lombardi (40%), Caio (20%), Guilherme Libório (20%), Ryan (20%) ]` |
| 6. Triagem título/resumo | `[Todos os integrantes]` | `[Guilherme Lombardi (25%), Caio (20%), Guilherme Libório (20%), Ryan (20%), Julia (15%) ]` |
| 7. Triagem texto completo | `[Todos os integrantes]` | `[Guilherme Lombardi (25%), Caio (20%), Guilherme Libório (20%), Ryan (20%), Julia (15%) ]` |

### 4.2 Quadro-resumo geral de participação na etapa

| Integrante | % estimado de participação total nesta etapa |
|---|---|
| `[Guilherme Lombardi]` | `[32%]` |
| `[Caio Winkler Marangoni]` | `[20%]` |
| `[Guilherme Libório Camargo]` | `[19%]` |
| `[Ryan dos Santos Veloso]` | `[19%]` |
| `[Julia Emily Leonardo Barbosa]` | `[10%]` |

*A soma das porcentagens deve ser igual a 100%. Divergências de percepção sobre a participação devem ser discutidas em grupo antes do envio — o orientador pode solicitar esclarecimentos individuais em caso de disparidade relevante.*

---

## 5. Checklist Final da Etapa

**Fase 1 — Planejamento**
- [x] Pergunta de pesquisa de trabalho definida
- [x] Conceitos-chave e sinônimos (PT/EN) listados
- [x] Strings de busca elaboradas com operadores booleanos
- [x] Bases de dados escolhidas e justificadas
- [x] Critérios de inclusão e exclusão definidos

**Fase 2 — Execução e triagem**
- [x] Buscas executadas e resultados registrados por base/string
- [x] Referências exportadas para o gerenciador de referências
- [x] Triagem por título/resumo concluída (com duplicatas removidas)
- [x] Triagem por texto completo (introdução/conclusão) concluída
- [x] Conjunto definitivo de artigos para fichamento compilado

**Documentação**
- [x] Contribuição individual de cada integrante registrada por passo
- [x] Quadro-resumo de participação preenchido (soma = 100%)

---


