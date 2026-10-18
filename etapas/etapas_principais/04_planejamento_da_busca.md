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

## Strings de busca

| Nº | String completa | Base em que será usada |
|---|---|---|
| 1 | `("cycle enumeration" OR "simple cycles" OR "cycle detection") AND ("directed graph" OR "transaction graph" OR "transaction network") AND ("time complexity" OR "exponential" OR "pruning" OR "scalability")` | ACM DL; IEEE Xplore; Springer Link |
| 2 | `("cycle" OR "circular flow" OR "temporal cycle") AND ("money laundering" OR "layering" OR "smurfing" OR "anti-money laundering") AND ("graph" OR "network")` | ACM DL; Springer Link; ScienceDirect |
| 3 | `("strongly connected components" OR "Kosaraju" OR "Tarjan" OR "SCC") AND ("large-scale" OR "parallel" OR "distributed" OR "scalability") AND ("directed graph" OR "graph processing")` | IEEE Xplore; ACM DL; Springer Link |
| 4 | `("finite automaton" OR "deterministic finite automaton" OR "DFA" OR "complex event processing") AND ("event stream" OR "stream processing") AND ("pattern matching" OR "filtering" OR "candidate reduction")` | ACM DL; IEEE Xplore |
| 5 | `("pre-filter*" OR "candidate reduction" OR "pruning" OR "filtering layer") AND ("graph search" OR "graph traversal" OR "subgraph matching") AND ("real-time" OR "streaming" OR "low latency")` | ACM DL; ScienceDirect; arXiv |
| 6 | `("PaySim" OR "synthetic financial dataset" OR "mobile money simulator") AND ("fraud" OR "money laundering")` | Springer Link; IEEE Xplore; arXiv |
| 7 | `("automat*" OR "complex event processing") AND ("pre-filter*" OR "filtering layer") AND ("cycle detection" OR "strongly connected components" OR "graph traversal") AND ("fraud" OR "money laundering")` | ACM DL; Springer Link; arXiv |
| 8 | `("Graph Neural Network*" OR "GNN") AND ("Financial Fraud" OR "Fraud Detection" OR "Transaction Fraud")` | Springer / IEEE / ACM |
| 9 | `("Complex Event Processing" OR "CEP") AND ("Graph Processing" OR "Stream Analytics") AND ("Real-time" OR "Parallel")` | ACM Digital Library / IEEE |
| 10 | `("Graph Anomaly Detection" OR "GAD") AND ("Supervised Learning" OR "Benchmark*" OR "Graph Mining")` | NeurIPS / Google Scholar / ScienceDirect |
| 11 | `("data engineering" OR "feature engineering" OR "data preprocessing") AND ("fraud detection" OR "financial fraud") AND ("computational complexity" OR "scalability")` | ScienceDirect (Elsevier) |
| 12 | `("machine learning" OR "classification algorithms") AND ("financial fraud detection" OR "banking fraud") AND ("performance evaluation" OR "benchmark")` | MDPI |
| 13 | `("graph analysis" OR "graph algorithms" OR "path detection") AND ("fraudulent accounts" OR "money laundering") AND ("parallel paths" OR "cycle detection" OR "strongly connected components")` | PubMed Central / IEEE Xplore / ScienceDirect |
| 14 | `("Finite Automata" OR "DFA" OR "Complex Event Processing") AND ("fraud detection" OR "stream filtering") AND ("graph reduction" OR "latency")` | IEEE Xplore, ACM Digital Library, ScienceDirect, Google Scholar |
| 15 | `("financial fraud" OR "anti-money laundering") AND ("strongly connected components" OR "Kosaraju" OR "DFS") AND ("graph complexity" OR "time complexity")` | IEEE Xplore, ACM Digital Library, Google Scholar |
| 16 | `("graph stream" OR "real-time graph") AND ("pre-filtering" OR "subgraph extraction") AND ("asymptotic complexity" OR "worst-case bound") AND "fraud"` | ACM Digital Library, IEEE Xplore, ScienceDirect, Google Scholar |
| 17 | `("subgraph reduction" OR "graph pruning" OR "stream filtering") AND ("graph traversal" OR "strongly connected components") AND ("financial fraud" OR "transaction network")` | ACM Digital Library, IEEE Xplore, Google Scholar |
| 18 | `("real-time graph" OR "streaming graph") AND ("pre-filter" OR "early discard") AND ("computational complexity" OR "execution time") AND "fraud"` | ACM Digital Library, IEEE Xplore, Google Scholar |
| 19 | `("rule-based filter" OR "automata") AND ("graph analytics" OR "network analysis") AND ("performance evaluation" OR "latency reduction") AND "fraud"` | ACM Digital Library, IEEE Xplore, Google Scholar |

**Observações sobre as strings**

- **String 1:** o parêntese de abertura que faltava foi restaurado. As demais strings foram conferidas e têm os parênteses balanceados.
- **Strings 6, 10 e 12:** são consultas exploratórias, registradas por transparência, e estão fora do recorte principal da revisão. A 6 trata de dados sintéticos (base experimental), e a 10 e a 12 tratam de aprendizado de máquina e benchmark, temas que os critérios de exclusão descartam. Os resultados delas não entram no conjunto final, a menos que passem pelos critérios de inclusão.
- **Curingas entre aspas:** termos como `"pre-filter*"` e `"automat*"` só expandem em bases que aceitam curinga dentro de aspas. Nas demais, o termo é buscado literalmente (ver tabela de sintaxe abaixo).

### Sintaxe e suporte a operadores por base

| Base | Operadores e sintaxe | Pontos de atenção na execução |
|---|---|---|
| IEEE Xplore | AND, OR, NOT em maiúsculas; frase entre aspas; parênteses para agrupar; curinga `*` | Curinga exige alguns caracteres antes do `*` e tende a não funcionar dentro de aspas. |
| ACM Digital Library | AND, OR, NOT; frase entre aspas; parênteses; busca por campo (título, resumo, palavras-chave) | Strings longas funcionam melhor na busca avançada, aplicadas a título, resumo e palavras-chave. |
| Springer Link | AND, OR, NOT; frase entre aspas; parênteses; curingas `*` e `?` | A ordenação por relevância pode priorizar capítulos de livro, então é preciso filtrar por tipo de conteúdo. |
| ScienceDirect | AND, OR, NOT; frase entre aspas; parênteses | Há limite de operadores booleanos por campo (8, segundo a ajuda da base). Strings longas devem ser divididas em duas buscas ou distribuídas entre "Title, abstract, keywords" e outros campos. |
| Google Scholar | AND implícito; OR em maiúsculas; frase entre aspas | Não há operadores avançados nem curingas confiáveis, e o tamanho da consulta é limitado. As strings precisam ser simplificadas, e a ordenação é opaca. |
| arXiv | AND, OR, ANDNOT na busca avançada; frase entre aspas; busca por campo | Só indexa pré-prints. Serve para localizar a versão publicada, já que o critério exige revisão por pares. |
| MDPI | Busca simples com aspas; operadores booleanos limitados | Usado apenas na string exploratória 12. |
| PubMed Central | AND, OR, NOT em maiúsculas; frase entre aspas; parênteses | Base de foco biomédico. A cobertura de Ciência da Computação é restrita. |

Esta tabela descreve o comportamento geral de cada base. A sintaxe efetivamente aceita deve ser conferida no dia da execução e registrada junto com os prints/exports de cada busca.

## Bases de dados

| Base | Justificativa da escolha |
|---|---|
| IEEE Xplore | Referência internacional em engenharia e computação; essencial para artigos sobre Complex Event Processing (CEP), arquiteturas de alto desempenho e processamento de fluxos em tempo real. |
| ACM Digital Library | Principal repositório de Ciência da Computação teórica e aplicada; fundamental para estudos sobre Teoria dos Autômatos, Regular Path Queries (RPQ) e algoritmos de grafos. |
| Google Scholar | Ampla cobertura de literatura cinzenta, pré-prints e conferências emergentes (2020–2026), com recuperação de artigos recentes sobre grafos temporais e detecção de fraudes financeiras. |
| Springer Link | Alta relevância em Ciência da Computação (inclui as coleções LNCS); teve o maior volume de artigos aderentes sobre algoritmos em grafos, otimização de complexidade e autômatos. |
| ScienceDirect (Elsevier) | Complementa IEEE e ACM com periódicos aplicados (sistemas especialistas, redes e segurança financeira) que publicam estudos de detecção de fraude com análise de custo computacional e engenharia de dados. Usada nas strings 2, 5, 10, 11, 13, 14 e 16. |
| arXiv | Concentra pré-prints recentes de algoritmos de grafos e bancos de dados (cs.DS, cs.DB), áreas em que a versão revisada por pares muitas vezes sai com atraso. Usada para localizar preprints. Quando o trabalho tem versão publicada revisada por pares, a versão publicada é a referenciada; uma versão somente arXiv só entra no conjunto final se a venue com revisão por pares for comprovada. Usada nas strings 5, 6 e 7. |
| MDPI | Editora de acesso aberto, o que atende ao critério de texto completo acessível. Usada apenas na string exploratória 12, fora do recorte principal. |
| PubMed Central | Arquivo de acesso aberto de foco biomédico, usado na string 13 para capturar artigos de métodos de análise de grafos e caminhos aplicados a redes de contas. Tem aderência temática limitada e é fonte complementar; nenhum artigo do conjunto final provém dela. |
| NeurIPS (anais) | Não é uma base de dados, e sim um repositório de anais de conferência. Constou na string exploratória 10 (detecção de anomalias em grafos), fora do recorte principal. Na prática, a consulta é feita pelo Google Scholar ou pelo ScienceDirect. |

## Critérios de inclusão

- Período: publicados entre 2020 e 2026.
- Idioma: inglês ou português.
- Tipo de publicação: artigos científicos revisados por pares (peer-reviewed) em periódicos ou anais de conferências relevantes, com texto disponível na íntegra.
- Aderência ao tema: estudos sobre detecção de fraudes financeiras/bancárias, processamento de fluxos em tempo real (stream processing/CEP), algoritmos em grafos temporais/dinâmicos ou consultas via autômatos (Regular Path Queries, RPQ).
- Outro critério: trabalhos com análise de complexidade computacional, otimização de latência/vazão ou mecanismos de pré-filtragem/redução de carga (load shedding/pruning).

## Critérios de exclusão

- Duplicatas entre as bases consultadas e versões do mesmo trabalho (preliminar e estendida): mantém-se a versão publicada mais completa.
- Fora do tema: detecção de fraudes sem abordagem algorítmica/computacional, ou focada só em aspectos jurídicos/financeiros não técnicos.
- Sem texto completo acessível (paywall sem acesso via repositório ou convênio).
- Outro: publicados antes de 2020 (exceto livros-texto clássicos e trabalhos usados apenas na fundamentação teórica complementar, que ficam fora da contagem do conjunto final analisado); apenas técnicas de aprendizado de máquina/IA "caixa-preta" sem abordagem estrutural em grafos, autômatos ou análise formal de complexidade; artigos de opinião, editoriais, resumos expandidos sem avaliação cega e literatura não científica.

## Filtros aplicados nas bases

| Filtro | Valor aplicado | Observação |
|---|---|---|
| Período | 2020–2026 | Aplicado pelo filtro de data de publicação de cada base. |
| Idioma | Inglês e português | Onde a base não oferece filtro de idioma, a checagem é feita na triagem. |
| Tipo de publicação | Artigos de periódico e anais de conferência | Excluir capítulos de livro, editoriais e resumos expandidos, onde a base permitir. |
| Campos de busca | Título, resumo e palavras-chave | Texto completo apenas quando a base não permitir restringir por campo. |


## Produto da etapa

Plano de busca com termos, strings, bases e critérios.

## Checklist

- [x] Há termos em português e inglês.
- [x] As strings usam AND e OR corretamente.
- [x] As bases são adequadas ao tema.
- [x] Os critérios foram definidos antes da triagem.
