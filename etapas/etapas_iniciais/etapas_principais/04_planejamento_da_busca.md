# Etapa 4 Planejamento da busca bibliográfica

## Solicitação

Planeje como os artigos serão localizados e selecionados antes de iniciar a busca definitiva.

## Conceitos e termos

| Conceito principal | Sinônimos em português | Termos em inglês |
|---|---|---|
| Complexidade assintótica | Análise de algoritmos, notação Big-O, custo computacional, limite assintótico, escalonamento de desempenho | Asymptotic complexity, Big-O notation, computational cost, algorithm scalability, time-space complexity |
| Pré-filtragem por autômatos finitos | Autômato Finito Determinístico (DFA), Processamento de Eventos Complexos (CEP), filtro de entrada, validação em tempo linear | Deterministic Finite Automaton (DFA), Complex Event Processing (CEP), stream filtering, pattern matching automata, edge filtering |
| Algoritmos de travessia em grafos | Busca em Profundidade (DFS), Componentes Fortemente Conectados (Kosaraju), detecção de ciclos, centralidade de rede | Depth-First Search (DFS), Kosaraju's algorithm, Strongly Connected Components (SCC), graph traversal, sub-graph detection |
| Processamento de fluxos de dados | Processamento em tempo real, processamento de streams, análise contínua de dados, baixa latência | Stream processing, data stream mining, real-time event processing, low-latency processing, in-memory streaming |
| Detecção de fraudes bancárias | Detecção de anomalias financeiras, transações suspeitas, análise de risco em tempo real, prevenção à fraude | Financial fraud detection, real-time anomaly detection, credit card fraud detection, transaction monitoring, anti-fraud pipeline |

> ⚠️ **REVISAR:** (b), Passo 1.2, também lista "Segurança / vulnerabilidade" e "IoT / Internet das Coisas". Não têm relação com o tema (parecem resto do exemplo do template) e as strings não os usam, então retirei. Confirmem.

## Strings de busca

| Nº | String completa | Base em que será usada |
|---|---|---|
| 1 | `"cycle enumeration" OR "simple cycles" OR "cycle detection") AND ("directed graph" OR "transaction graph" OR "transaction network") AND ("time complexity" OR "exponential" OR "pruning" OR "scalability")` | ACM DL; IEEE Xplore; Springer Link |
| 2 | `("cycle" OR "circular flow" OR "temporal cycle") AND ("money laundering" OR "layering" OR "smurfing" OR "anti-money laundering") AND ("graph" OR "network")` | ACM DL; Springer Link; ScienceDirect |
| 3 | `("strongly connected components" OR "Kosaraju" OR "Tarjan" OR "SCC") AND ("large-scale" OR "parallel" OR "distributed" OR "scalability") AND ("directed graph" OR "graph processing")` | IEEE Xplore; ACM DL; Springer Link |
| 4 | `("finite automaton" OR "deterministic finite automaton" OR "DFA" OR "complex event processing") AND ("event stream" OR "stream processing") AND ("pattern matching" OR "filtering" OR "candidate reduction")` | ACM DL; IEEE Xplore |
| 5 | `("pre-filter*" OR "candidate reduction" OR "pruning" OR "filtering layer") AND ("graph search" OR "graph traversal" OR "subgraph matching") AND ("real-time" OR "streaming" OR "low latency")` | ACM DL; ScienceDirect; arXiv |
| 6 | `("PaySim" OR "synthetic financial dataset" OR "mobile money simulator") AND ("fraud" OR "money laundering")` ⚠️ (consulta histórica; texto recuperado da versão 53be4a6) | Springer Link; IEEE Xplore; arXiv |
| 7 | `("automat*" OR "complex event processing") AND ("pre-filter*" OR "filtering layer") AND ("cycle detection" OR "strongly connected components" OR "graph traversal") AND ("fraud" OR "money laundering")` | ACM DL; Springer Link; arXiv |
| 8 | `("Graph Neural Network*" OR "GNN") AND ("Financial Fraud" OR "Fraud Detection" OR "Transaction Fraud")` | Springer / IEEE / ACM |
| 9 | `("Complex Event Processing" OR "CEP") AND ("Graph Processing" OR "Stream Analytics") AND ("Real-time" OR "Parallel")` | ACM Digital Library / IEEE |
| 10 | `("Graph Anomaly Detection" OR "GAD") AND ("Supervised Learning" OR "Benchmark*" OR "Graph Mining")` ⚠️ (consulta histórica; texto recuperado da versão 53be4a6) | NeurIPS / Google Scholar / ScienceDirect |
| 11 | `("data engineering" OR "feature engineering" OR "data preprocessing") AND ("fraud detection" OR "financial fraud") AND ("computational complexity" OR "scalability")` | ScienceDirect (Elsevier) |
| 12 | `("machine learning" OR "classification algorithms") AND ("financial fraud detection" OR "banking fraud") AND ("performance evaluation" OR "benchmark")` ⚠️ (consulta histórica; texto recuperado da versão 53be4a6) | MDPI |
| 13 | `("graph analysis" OR "graph algorithms" OR "path detection") AND ("fraudulent accounts" OR "money laundering") AND ("parallel paths" OR "cycle detection" OR "strongly connected components")` | PubMed Central / IEEE Xplore / ScienceDirect |
| 14 | `("Finite Automata" OR "DFA" OR "Complex Event Processing") AND ("fraud detection" OR "stream filtering") AND ("graph reduction" OR "latency")` | IEEE Xplore, ACM Digital Library, ScienceDirect, Google Scholar |
| 15 | `("financial fraud" OR "anti-money laundering") AND ("strongly connected components" OR "Kosaraju" OR "DFS") AND ("graph complexity" OR "time complexity")` | IEEE Xplore, ACM Digital Library, Google Scholar |
| 16 | `("graph stream" OR "real-time graph") AND ("pre-filtering" OR "subgraph extraction") AND ("asymptotic complexity" OR "worst-case bound") AND "fraud"` | ACM Digital Library, IEEE Xplore, ScienceDirect, Google Scholar |
| 17 | `("subgraph reduction" OR "graph pruning" OR "stream filtering") AND ("graph traversal" OR "strongly connected components") AND ("financial fraud" OR "transaction network")` | ACM Digital Library, IEEE Xplore, Google Scholar |
| 18 | `("real-time graph" OR "streaming graph") AND ("pre-filter" OR "early discard") AND ("computational complexity" OR "execution time") AND "fraud"` | ACM Digital Library, IEEE Xplore, Google Scholar |
| 19 | `("rule-based filter" OR "automata") AND ("graph analytics" OR "network analysis") AND ("performance evaluation" OR "latency reduction") AND "fraud"` | ACM Digital Library, IEEE Xplore, Google Scholar |

> ⚠️ **REVISAR:** **String 1 tem parênteses desbalanceados**: falta o "(" no início (`"cycle enumeration" OR … "cycle detection") AND (…`). Mantive como está em (b). Correção sugerida: `("cycle enumeration" OR "simple cycles" OR "cycle detection") AND ("directed graph" OR "transaction graph" OR "transaction network") AND ("time complexity" OR "exponential" OR "pruning" OR "scalability")`. Confirmem se foi essa a string executada.
> ⚠️ **REVISAR:** as strings 6, 10 e 12 não têm o texto em (b) atual (só links para o histórico). Recuperei o texto na cópia 53be4a6, que tem essas consultas nas linhas 59, 63 e 65, as mesmas apontadas pelos links, mas o commit citado é 5b61858, que não está entre as cópias. Elas estão fora do recorte atual: a 6 trata de dados sintéticos (base experimental), e a 10 e a 12 são de aprendizado de máquina/benchmark, que os critérios de exclusão descartariam. Decidam se entram neste plano.
> ⚠️ **PENDENTE:** (b) pede registrar a sintaxe e o suporte a operadores de cada base junto das evidências, e isso não consta.

## Bases de dados

| Base | Justificativa da escolha |
|---|---|
| IEEE Xplore | Referência internacional em engenharia e computação; essencial para artigos sobre Complex Event Processing (CEP), arquiteturas de alto desempenho e processamento de fluxos em tempo real. |
| ACM Digital Library | Principal repositório de Ciência da Computação teórica e aplicada; fundamental para estudos sobre Teoria dos Autômatos, Regular Path Queries (RPQ) e algoritmos de grafos. |
| Google Scholar | Ampla cobertura de literatura cinzenta, pré-prints e conferências emergentes (2020–2026), com recuperação de artigos recentes sobre grafos temporais e detecção de fraudes financeiras. |
| Springer Link | Alta relevância em Ciência da Computação (inclui as coleções LNCS); teve o maior volume de artigos aderentes sobre algoritmos em grafos, otimização de complexidade e autômatos. |

> ⚠️ **REVISAR:** (b) justifica 4 bases, mas as buscas registradas usaram **8**: também ScienceDirect, arXiv, MDPI e PubMed Central, sem justificativa. NeurIPS aparece como base da string 10 e na contribuição de um integrante, mas não há busca registrada nela. Justifiquem as bases extras ou expliquem por que foram usadas.

## Critérios de inclusão

- Período: publicados entre 2020 e 2026.
- Idioma: inglês ou português.
- Tipo de publicação: artigos científicos revisados por pares (peer-reviewed) em periódicos ou anais de conferências relevantes, com texto disponível na íntegra.
- Aderência ao tema: estudos sobre detecção de fraudes financeiras/bancárias, processamento de fluxos em tempo real (stream processing/CEP), algoritmos em grafos temporais/dinâmicos ou consultas via autômatos (Regular Path Queries, RPQ).
- Outro critério: trabalhos com análise de complexidade computacional, otimização de latência/vazão ou mecanismos de pré-filtragem/redução de carga (load shedding/pruning).

## Critérios de exclusão

- Duplicatas entre as bases consultadas.
- Fora do tema: detecção de fraudes sem abordagem algorítmica/computacional, ou focada só em aspectos jurídicos/financeiros não técnicos.
- Sem texto completo acessível (paywall sem acesso via repositório ou convênio).
- Outro: publicados antes de 2020 (exceto livros-texto clássicos de fundamentação); apenas técnicas de aprendizado de máquina/IA "caixa-preta" sem abordagem estrutural em grafos, autômatos ou análise formal de complexidade; artigos de opinião, editoriais, resumos expandidos sem avaliação cega e literatura não científica.

> ⚠️ **REVISAR:** o artigo nº 13 do conjunto final (ASAP, **2018**) fere o critério de período, e a única exceção prevista é para livros-texto clássicos. Ajustem o critério (por exemplo, abrindo uma exceção para trabalhos seminais) ou justifiquem a inclusão.
> ⚠️ **PENDENTE:** os filtros efetivamente aplicados nas bases (período, idioma, tipo) não estão registrados em (b).

## Produto da etapa

Plano de busca com termos, strings, bases e critérios.

## Checklist

- [x] Há termos em português e inglês.
- [ ] As strings usam AND e OR corretamente.
> ⚠️ **REVISAR:** desmarquei por causa da string 1 (parênteses). Marquem depois de corrigir.
- [ ] As bases são adequadas ao tema.
> ⚠️ **REVISAR:** as 4 bases justificadas são adequadas, mas 4 usadas não têm justificativa (ver acima).
- [x] Os critérios foram definidos antes da triagem.
