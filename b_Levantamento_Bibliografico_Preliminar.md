# Etapa (b) — Levantamento Bibliográfico

> Documento de revisão bibliográfica com registros declarados de busca e triagem. O escopo atual é a análise teórica e documental da complexidade de DFS/Kosaraju e da pré-filtragem DFA/CEP; as métricas discutidas serão extraídas das publicações revisadas.

---

## 1. Identificação do Grupo

| Campo | Informação |
|---|---|
| Curso / Disciplina | Computabilidade e Complexidade de Algoritmos |
| Projeto de Pesquisa / IC | Complexidade e Desempenho em Pipeline Híbrida para Detecção de Fraudes Financeiras |
| Orientador(a) | Andrea Ono Sakai |
| Data de entrega desta etapa | 10/09/2026 |
| Integrantes atuais do grupo | Guilherme Lombardi; Ryan dos Santos Veloso; Caio Winkler Marangoni; Guilherme Liborio Camargo |
| Tema (da etapa "a") | Análise comparativa de complexidade assintótica entre um pipeline tradicional de grafos (DFS/Kosaraju) e uma arquitetura híbrida com pré-filtragem por Autômatos Finitos, aplicada à detecção de fraudes bancárias em tempo real. |

---

> **Atualização da equipe:** Quando Julia Emily Leonardo Barbosa saiu do grupo, eu, Caio Winkler Marangoni, dei continuidade às partes que ficaram em aberto e assumi as respectivas pendências. Mantenho as contribuições, horas e porcentagens antigas como histórico declarado, sem redistribuição automática nem comprovação presumida.

## FASE 1 — Planejamento da Busca

### Passo 1 — Pergunta de pesquisa e palavras-chave

**1.1 Problema/pergunta de pesquisa (versão de trabalho)**
*Ainda não precisa ser a versão final (isso vem na etapa "c"), mas deve orientar a busca desta fase.*

> Em que medida a introdução de uma camada de pré-filtragem baseada em Autômatos Finitos reduz a complexidade assintótica e o tempo de resposta de um pipeline de detecção de fraudes bancárias em tempo real, quando comparada à varredura direta via DFS/Kosaraju?

**1.2 Conceitos-chave e sinônimos**
*Liste os conceitos centrais da pergunta e seus sinônimos, em português e inglês.*

| Conceito-chave | Sinônimos / termos relacionados (PT) | Sinônimos / termos relacionados (EN) |
|---|---|---|
| Segurança | proteção, vulnerabilidade | security, vulnerability |
| IoT | Internet das Coisas | Internet of Things, smart devices |
| Complexidade Assintótica | Análise de algoritmos, Notação Big-O, Custo computacional, Limite assintótico, Escalonamento de desempenho | Asymptotic complexity, Big-O notation, Computational cost, Algorithm scalability, Time-space complexity |
| Pré-filtragem por Autômatos Finitos | Autômato Finito Determinístico (DFA), Processamento de Eventos Complexos (CEP), Filtro de entrada, Validação em tempo linear | Deterministic Finite Automaton (DFA), Complex Event Processing (CEP), Stream filtering, Pattern matching automata, Edge filtering |
| Algoritmos de Travessia em Grafos | Busca em Profundidade (DFS), Componentes Fortemente Conectados (Kosaraju), Detecção de ciclos, Centralidade de rede | Depth-First Search (DFS), Kosaraju's algorithm, Strongly Connected Components (SCC), Graph traversal, Sub-graph detection |
| Processamento de Fluxos de Dados | Processamento em tempo real, Processamento de streams, Análise contínua de dados, Baixa latência | Stream processing, Data stream mining, Real-time event processing, Low-latency processing, In-memory streaming |
| Detecção de Fraudes Bancárias | Detecção de anomalias financeiras, Transações suspeitas, Análise de risco em tempo real, Prevenção à fraude | Financial fraud detection, Real-time anomaly detection, Credit card fraud detection, Transaction monitoring, Anti-fraud pipeline |

*Responsável por este passo: Guilherme Lombardi*

---

### Passo 2 — Strings de busca

*Combine os termos do passo 1 com operadores booleanos (`AND`, `OR`, `NOT`). Use aspas para termos compostos e truncamento (`*`) quando a base permitir.*

*Preservei nas strings abaixo a numeração do levantamento declarado na versão `5b61858`. As consultas históricas 6, 10 e 12 são acessíveis na versão original pelos links da tabela; não recalculei suas contagens nem as atribuí a novas consultas. Elas não estabelecem atividades experimentais nesta etapa. A comprovação das buscas e decisões continua pendente no [registro de evidências individuais](evidencias_individuais/README.md).*

| No | String de busca | Conceito-chave / eixo coberto (Passo 1) | Base(s) declarada(s) | Elaborada por |
|---|---|---|---|---|
| 1 | `"cycle enumeration" OR "simple cycles" OR "cycle detection") AND ("directed graph" OR "transaction graph" OR "transaction network") AND ("time complexity" OR "exponential" OR "pruning" OR "scalability")` | Complexidade Assintotica — gargalo do modulo cycle_detection.py | ACM DL; IEEE Xplore; Springer Link | Caio Winkler Marangoni |
| 2 | `("cycle" OR "circular flow" OR "temporal cycle") AND ("money laundering" OR "layering" OR "smurfing" OR "anti-money laundering") AND ("graph" OR "network")` | Deteccao de Fraudes Bancarias — layering, o padrao que o sistema procura | ACM DL; Springer Link; ScienceDirect | Caio Winkler Marangoni |
| 3 | `("strongly connected components" OR "Kosaraju" OR "Tarjan" OR "SCC") AND ("large-scale" OR "parallel" OR "distributed" OR "scalability") AND ("directed graph" OR "graph processing")` | Algoritmos de Travessia em Grafos — custo do modulo scc.py em escala | IEEE Xplore; ACM DL; Springer Link | Caio Winkler Marangoni |
| 4 | `("finite automaton" OR "deterministic finite automaton" OR "DFA" OR "complex event processing") AND ("event stream" OR "stream processing") AND ("pattern matching" OR "filtering" OR "candidate reduction")` | Pre-filtragem por Automatos Finitos — foco central da pesquisa | ACM DL; IEEE Xplore | Caio Winkler Marangoni |
| 5 | `("pre-filter*" OR "candidate reduction" OR "pruning" OR "filtering layer") AND ("graph search" OR "graph traversal" OR "subgraph matching") AND ("real-time" OR "streaming" OR "low latency")` | Processamento de Fluxos de Dados — a hipotese: reduzir o volume antes da travessia | ACM DL; ScienceDirect; arXiv | Caio Winkler Marangoni |
| 6 | [Consulta histórica nº 6](https://github.com/Guilherme-Lombardi/AnaliseComplexidade_DeteccaoFraudes/blob/5b618580e0eb84657a83106c2d15433b872f717f/b_Levantamento_Bibliografico_Preliminar.md#L59) | Consulta histórica sobre dados sintéticos; fora do escopo atual de análise teórica | Springer Link; IEEE Xplore; arXiv | Caio Winkler Marangoni |
| 7 | `("automat*" OR "complex event processing") AND ("pre-filter*" OR "filtering layer") AND ("cycle detection" OR "strongly connected components" OR "graph traversal") AND ("fraud" OR "money laundering")` | String-sintese: reproduz a pergunta de pesquisa do item 1.1 (pipeline hibrido) | ACM DL; Springer Link; arXiv | Caio Winkler Marangoni |
| 8 | `("Graph Neural Network*" OR "GNN") AND ("Financial Fraud" OR "Fraud Detection" OR "Transaction Fraud")` | Detecção de fraudes em grafos financeiros / Análise de transações atípicas (cycle_detection.py) | Springer / IEEE / ACM | Guilherme Libório Camargo |
| 9 | `("Complex Event Processing" OR "CEP") AND ("Graph Processing" OR "Stream Analytics") AND ("Real-time" OR "Parallel")` | Processamento de eventos complexos e análise de grafos em tempo real (centralidade.py) | ACM Digital Library / IEEE | Guilherme Libório Camargo |
| 10 | [Consulta histórica nº 10](https://github.com/Guilherme-Lombardi/AnaliseComplexidade_DeteccaoFraudes/blob/5b618580e0eb84657a83106c2d15433b872f717f/b_Levantamento_Bibliografico_Preliminar.md#L63) | Desempenho reportado em detecção de anomalias em grafos; sujeito aos critérios de inclusão | NeurIPS / Google Scholar / ScienceDirect | Guilherme Libório Camargo |
| 11 | `("data engineering" OR "feature engineering" OR "data preprocessing") AND ("fraud detection" OR "financial fraud") AND ("computational complexity" OR "scalability")` | Engenharia de dados, pré-processamento de transações e complexidade computacional para pipelines em larga escala (relação com `cycle_detection.py`) | ScienceDirect (Elsevier) | Ryan dos Santos Veloso |
| 12 | [Consulta histórica nº 12](https://github.com/Guilherme-Lombardi/AnaliseComplexidade_DeteccaoFraudes/blob/5b618580e0eb84657a83106c2d15433b872f717f/b_Levantamento_Bibliografico_Preliminar.md#L65) | Avaliação de desempenho reportada na literatura; sujeita aos critérios de inclusão | MDPI | Ryan dos Santos Veloso |
| 13 | `("graph analysis" OR "graph algorithms" OR "path detection") AND ("fraudulent accounts" OR "money laundering") AND ("parallel paths" OR "cycle detection" OR "strongly connected components")` | Algoritmos em grafos, detecção de caminhos paralelos e subestruturas fortemente conectadas/cíclicas em redes bancárias (Relação: (scc.py) e (cycle_detection.py). | PubMed Central / IEEE Xplore / ScienceDirect | Ryan dos Santos Veloso |
| 14 | `("Finite Automata" OR "DFA" OR "Complex Event Processing") AND ("fraud detection" OR "stream filtering") AND ("graph reduction" OR "latency")` | Pré-filtragem, grafos e complexidade: relação com a pergunta de pesquisa | IEEE Xplore, ACM Digital Library, ScienceDirect, Google Scholar | Guilherme Lombardi |
| 15 | `("financial fraud" OR "anti-money laundering") AND ("strongly connected components" OR "Kosaraju" OR "DFS") AND ("graph complexity" OR "time complexity")` | Pré-filtragem, grafos e complexidade: relação com a pergunta de pesquisa | IEEE Xplore, ACM Digital Library, Google Scholar | Guilherme Lombardi |
| 16 | `("graph stream" OR "real-time graph") AND ("pre-filtering" OR "subgraph extraction") AND ("asymptotic complexity" OR "worst-case bound") AND "fraud"` | Pré-filtragem, grafos e complexidade: relação com a pergunta de pesquisa | ACM Digital Library, IEEE Xplore, ScienceDirect, Google Scholar | Guilherme Lombardi |
| 17 | `("subgraph reduction" OR "graph pruning" OR "stream filtering") AND ("graph traversal" OR "strongly connected components") AND ("financial fraud" OR "transaction network")` | Pré-filtragem, grafos e complexidade: relação com a pergunta de pesquisa | ACM Digital Library, IEEE Xplore, Google Scholar | Guilherme Lombardi |
| 18 | `("real-time graph" OR "streaming graph") AND ("pre-filter" OR "early discard") AND ("computational complexity" OR "execution time") AND "fraud"` | Pré-filtragem, grafos e complexidade: relação com a pergunta de pesquisa | ACM Digital Library, IEEE Xplore, Google Scholar | Guilherme Lombardi |
| 19 | `("rule-based filter" OR "automata") AND ("graph analytics" OR "network analysis") AND ("performance evaluation" OR "latency reduction") AND "fraud"` | Pré-filtragem, grafos e complexidade: relação com a pergunta de pesquisa | ACM Digital Library, IEEE Xplore, Google Scholar | Guilherme Lombardi |



**Observações sobre as strings e o recorte atual**

- As strings 1 e 3 cobrem algoritmos e problemas em grafos; as strings 4 e 5 cobrem autômatos, processamento de eventos e pré-filtragem; a string 2 situa a aplicação em fraudes financeiras.
- A análise distinguirá o custo da travessia DFS e do cálculo de componentes por Kosaraju do custo de enumerar ciclos. Redução de volume ou de latência reportada não será tomada, por si só, como demonstração de mudança da classe assintótica no pior caso.
- A string 6 integra somente o histórico de busca, sem previsão de execução própria. As strings 8, 10 e 12 exigem triagem de aderência ao recorte: estudos exclusivamente de classificação sem análise estrutural ou de complexidade não integram a comparação central.
- A string 7 aproxima a busca da pergunta de pesquisa. Uma contagem pequena de resultados, isoladamente, não demonstra originalidade.
- A sintaxe e o suporte a operadores de cada base devem ser registrados junto das evidências reais. Preservei as consultas originais e seus números; qualquer nova busca deverá receber data, consulta e contagem próprias.

---

### Passo 3 — Bases de dados escolhidas

*Selecione de 2 a 4 bases relevantes ao tema. Registre a justificativa — isso vai para a seção de metodologia do artigo/relatório de IC.*

| Base de dados | Por que foi escolhida | Responsável pela busca nesta base |
|---|---|---|
| IEEE Xplore | Referência internacional em engenharia e computação; essencial para mapear artigos sobre Complex Event Processing (CEP), arquiteturas de altíssimo desempenho e processamento de fluxos em tempo real. | Guilherme Lombardi |
| ACM Digital Library | Principal repositório de Ciência da Computação teórica e aplicada; fundamental para resgatar estudos sobre Teoria dos Autômatos, Regular Path Queries (RPQ) e algoritmos de grafos. | Guilherme Lombardi |
| Google Scholar | Permite ampla cobertura da literatura cinzenta, pré-prints e conferências emergentes (2020–2026), garantindo a recuperação de artigos recentes sobre grafos temporais e detecção de fraudes financeiras. | Guilherme Lombardi |
| Springer Link | Altíssima relevância em Ciência da Computação (incluindo as coleções LNCS); apresentou maior volume de artigos aderentes sobre algoritmos em grafos, otimização de complexidade e autômatos. | Guilherme Lombardi |

---

### Passo 4 — Critérios de inclusão e exclusão

**Critérios de inclusão:**
- Artigos publicados no recorte temporal recente (entre 2020 e 2026)
- Artigos científicos revisados por pares (peer-reviewed) publicados em periódicos ou anais de conferências relevantes.
- Trabalhos publicados no idioma inglês ou português.
- Textos disponíveis na íntegra para leitura e análise qualitativa.
- Estudos focados em detecção de fraudes financeiras/bancárias, processamento de fluxos em tempo real (stream processing/CEP), algoritmos em grafos temporais/dinâmicos ou consultas via autômatos (Regular Path Queries - RPQ).
- Trabalhos que apresentem análise de complexidade computacional, otimização de latência/vazão ou mecanismos de pré-filtragem/redução de carga (load shedding/pruning).

**Critérios de exclusão:**
- Artigos publicados antes de 2020 (exceto os livros texto clássicos para fundamentação teórica de base).
- Publicações sem texto completo acessível (paywall sem acesso via repositório/convênio).
- Artigos duplicados entre as diferentes bases de dados consultadas.
- Trabalhos fora do escopo do tema (ex.: detecção de fraudes sem abordagem algorítmica/computacional ou focados exclusivamente em aspectos jurídicos/financeiros não-técnicos).
- Trabalhos que utilizem apenas técnicas de Aprendizado de Máquina/IA "caixa-preta" sem abordagem estrutural em grafos, autômatos ou análise formal de complexidade assintótica.
- Artigos de opinião, editoriais, resumos expandidos de eventos sem avaliação cega ou literatura não-científica.

*Definidos em conjunto por: Guilherme Lombardi*

---

## FASE 2 — Execução da Busca e Triagem

### Passo 5 — Execução das buscas e registro dos resultados

*Histórico declarado no levantamento original, ainda dependente de prints ou exportações das bases. Os números das consultas remetem ao Passo 2, inclusive aos links das consultas históricas. Preservei as contagens abaixo; apenas organizei os registros existentes, sem realizar novas buscas.*

| Base | String usada (nº) | Data da busca | Nº de resultados | Executada por |
|---|---|---|---|---|
| ACM Digital Library | String 1 | 06/09/2026 | 18 | Caio Winkler Marangoni |
| IEEE Xplore | String 1 | 06/09/2026 | 12 | Caio Winkler Marangoni |
| Springer Link | String 1 | 06/09/2026 | 15 | Caio Winkler Marangoni |
| ACM Digital Library | String 2 | 06/09/2026 | 14 | Caio Winkler Marangoni |
| Springer Link | String 2 | 06/09/2026 | 22 | Caio Winkler Marangoni |
| ScienceDirect | String 2 | 06/09/2026 | 19 | Caio Winkler Marangoni |
| IEEE Xplore | String 3 | 06/09/2026 | 25 | Caio Winkler Marangoni |
| ACM Digital Library | String 3 | 06/09/2026 | 16 | Caio Winkler Marangoni |
| Springer Link | String 3 | 06/09/2026 | 20 | Caio Winkler Marangoni |
| ACM Digital Library | String 4 | 06/09/2026 | 11 | Caio Winkler Marangoni |
| IEEE Xplore | String 4 | 06/09/2026 | 9 | Caio Winkler Marangoni |
| ACM Digital Library | String 5 | 06/09/2026 | 13 | Caio Winkler Marangoni |
| ScienceDirect | String 5 | 06/09/2026 | 17 | Caio Winkler Marangoni |
| arXiv | String 5 | 06/09/2026 | 8 | Caio Winkler Marangoni |
| Springer Link | String 6 | 06/09/2026 | 10 | Caio Winkler Marangoni |
| IEEE Xplore | String 6 | 06/09/2026 | 6 | Caio Winkler Marangoni |
| arXiv | String 6 | 06/09/2026 | 5 | Caio Winkler Marangoni |
| ACM Digital Library | String 7 | 06/09/2026 | 4 | Caio Winkler Marangoni |
| Springer Link | String 7 | 06/09/2026 | 7 | Caio Winkler Marangoni |
| arXiv | String 7 | 06/09/2026 | 3 | Caio Winkler Marangoni |
| Springer Link | String 8 | 05/09/2026 | 21 | Guilherme Libório Camargo |
| IEEE Xplore | String 8 | 05/09/2026 | 18 | Guilherme Libório Camargo |
| ACM Digital Library | String 8 | 05/09/2026 | 15 | Guilherme Libório Camargo |
| ACM Digital Library | String 9 | 05/09/2026 | 14 | Guilherme Libório Camargo |
| IEEE Xplore | String 9 | 05/09/2026 | 19 | Guilherme Libório Camargo |
| Google Scholar | String 10 | 05/09/2026 | 28 | Guilherme Libório Camargo |
| ScienceDirect | String 10 | 05/09/2026 | 16 | Guilherme Libório Camargo |
| ScienceDirect | String 11 | 08/09/2026 | 23 | Ryan dos Santos Veloso |
| MDPI | String 12 | 08/09/2026 | 31 | Ryan dos Santos Veloso |
| PubMed Central | String 13 | 08/09/2026 | 12 | Ryan dos Santos Veloso |
| IEEE Xplore | String 13 | 08/09/2026 | 17 | Ryan dos Santos Veloso |
| ScienceDirect | String 13 | 08/09/2026 | 20 | Ryan dos Santos Veloso |
| IEEE Xplore | Strings 14, 15 e 18 | 09/09/2026 | 42 | Guilherme Lombardi |
| ACM Digital Library | Strings 14, 16 e 19 | 09/09/2026 | 38 | Guilherme Lombardi |
| Springer Link | Strings 15, 17 e 19 | 09/09/2026 | 55 | Guilherme Lombardi |
| Google Scholar | Strings 3 e 4 | 09/09/2026 | 61 | Guilherme Lombardi |

**Total de resultados brutos declarado no levantamento original:** 721

**Divergência pendente de conferência:** as 36 linhas de buscas da tabela acima somam 684 resultados, 37 a menos que o total declarado de 721. Preservei os registros e o fluxo original de triagem até a conferência com os prints ou exportações e a planilha reais. Não criei consultas ou contagens para compensar essa diferença; após a conferência, o grupo deverá atualizar o total e os números da triagem que dele dependem.

**Gerenciador de referências utilizado:** Repositório local de artigos (Armazenamento em diretório do projeto)
**Formato de exportação:** Documentos na íntegra (PDF) e citações diretas das bases.

---

### Passo 6 — Triagem por título e resumo (1ª filtragem)

*Leia apenas título e resumo de cada resultado. Classifique: incluir / excluir / dúvida. Remova duplicatas entre bases.*

| Item de controle | Quantidade |
|---|---|
| Total de resultados antes da triagem | 721 |
| Duplicatas removidas | 525 |
| Classificados como "Incluir" | 54 |
| Classificados como "Excluir" | 142 |
| Classificados como "Dúvida" | 0 |

*A triagem detalhada, artigo por artigo, deve ser registrada na planilha de controle do projeto (aba "Triagem de Artigos"). Aqui, registre apenas o resumo quantitativo.*

**Como as dúvidas foram resolvidas?** *(ex.: discussão em grupo, consulta ao orientador)*
As dúvidas foram alinhadas por meio de conversas informais presenciais durante os horários vagos das aulas e trocas frequentes de mensagens no grupo virtual dos integrantes. Para analisar trechos mais complexos, foram realizadas pesquisas complementares na internet e utilizado o auxílio de inteligências artificiais para triagem inicial de conceitos, alinhando o direcionamento final das escolhas com as orientações da professora Andrea Ono Sakai.

*Responsável(is) declarados à época por esta triagem: Guilherme Lombardi, Caio Winkler Marangoni, Guilherme Libório Camargo, Ryan dos Santos Veloso, Julia Emily Leonardo Barbosa*

---

### Passo 7 — Triagem por leitura completa (2ª filtragem)

*Para os artigos que passaram na primeira filtragem, leia introdução e conclusão. Aplique os critérios de inclusão/exclusão (passo 4) de forma mais rigorosa.*

| Item de controle | Quantidade |
|---|---|
| Total de textos que entraram nesta filtragem | 54 |
| Artigos aprovados no conjunto definitivo para fichamento | 14 |
| Teses encaminhadas à fundamentação teórica complementar | 2 |
| Excluídos de ambas as listas nesta etapa | 38 |

As categorias são disjuntas: 54 = 14 + 2 + 38. O conjunto definitivo contém 14 artigos; as 2 teses são mantidas separadamente como contexto e não contam como artigos aprovados. Em relação ao conjunto definitivo, são 40 textos não incluídos (2 complementares + 38 excluídos).

**Principais motivos de exclusão nesta filtragem:**
- Ausência de análise formal de complexidade assintótica ou de métricas quantitativas de tempo de execução/latência no processamento do fluxo.
- Foco exclusivo em modelos de Aprendizado de Máquina/IA "caixa-preta" para classificação individual de transações, sem abordagem de pré-filtragem estrutural ou análise em grafos.

*Responsável(is) declarados à época por esta triagem: Guilherme Lombardi, Caio Winkler Marangoni, Guilherme Libório Camargo, Ryan dos Santos Veloso, Julia Emily Leonardo Barbosa*

---

## 3. Lista Final de Artigos Selecionados (Conjunto Definitivo)

*Liste aqui os artigos que passaram por todas as filtragens e seguirão para o fichamento (etapa "j"). Referência completa no formato ABNT/APA definido pelo projeto.*

1. CHAPNIK, Koral; KOLCHINSKY, Ilya; SCHUSTER, Assaf. DARLING: Data-Aware Load Shedding in Complex Event Processing. PVLDB, 15(3), 541–554, 2022. Disponível em: https://dl.acm.org/doi/abs/10.14778/3494124.3494137. Acesso em: 10 set. 2026.
2. SLO, Ahmad; BHOWMIK, Sukanya; ROTHERMEL, Kurt. hSPICE: State-Aware Event Shedding in Complex Event Processing. In: ACM INTERNATIONAL CONFERENCE ON DISTRIBUTED AND EVENT-BASED SYSTEMS (DEBS '20), 14., 2020, Montreal. Proceedings... New York: ACM, 2020. p. 109–120. Disponível em: https://dl.acm.org/doi/abs/10.1145/3401025.3401742. Acesso em: 10 set. 2026.
3. YANKOVITCH, Maor; KOLCHINSKY, Ilya; SCHUSTER, Assaf. HYPERSONIC: A Hybrid Parallelization Approach for Scalable Complex Event Processing. In: ACM INTERNATIONAL CONFERENCE ON MANAGEMENT OF DATA (SIGMOD '22), 2022, Philadelphia. Proceedings... New York: ACM, 2022. p. 1093–1107. Disponível em: https://dl.acm.org/doi/abs/10.1145/3514221.3517829. Acesso em: 10 set. 2026.
4. PFANDZELTER, Tobias; BERMBACH, David. Operator as a Service: Stateful Serverless Complex Event Processing. In: IEEE INTERNATIONAL CONFERENCE ON BIG DATA (BIG DATA '20), 2020, Atlanta. Proceedings... Piscataway: IEEE, 2020. p. 2875-2884. Disponível em: https://ieeexplore.ieee.org/abstract/document/9378142. Acesso em: 10 set. 2026.
5. LI, Xueli et al. Efficient Densest Flow Queries in Transaction Flow Networks. IEEE Transactions on Knowledge and Data Engineering, v. 38, n. 7, p. 1147-1160, 2026. Disponível em: https://ieeexplore.ieee.org/abstract/document/11471253. Acesso em: 10 set. 2026.
6. CAPOZZI, Arthur et al. FlowSeries: Anomaly Detection in Financial Transaction Flows. In: INTERNATIONAL CONFERENCE ON COMPLEX NETWORKS AND THEIR APPLICATIONS (COMPLEX NETWORKS '24), 13., 2024, Lisboa. Complex Networks & Their Applications XIII. Cham: Springer, 2025. p. 28-40. (Studies in Computational Intelligence, v. 1189). Disponível em: https://link.springer.com/chapter/10.1007/978-3-031-82435-7_3. Acesso em: 10 set. 2026.
7. CAPOZZI, Arthur et al. FlowSeries: Flow Analysis on Financial Networks. Applied Network Science, v. 10, n. 1, art. 28, p. 1-24, 2025. Disponível em: https://link.springer.com/article/10.1007/s41109-025-00711-0. Acesso em: 10 set. 2026.
8. LI, Zhiyong et al. Internet Financial Fraud Detection Based on a Distributed Big Data Approach With Node2vec. IEEE Access, v. 9, p. 23145-23156, 2021. Disponível em: https://ieeexplore.ieee.org/document/9363921. Acesso em: 10 set. 2026.
9. WANG, Yong et al. TempASD: Temporal Anomalous Subgraph Discovery in Large-Scale Dynamic Financial Networks. In: ACM SIGKDD CONFERENCE ON KNOWLEDGE DISCOVERY AND DATA MINING (KDD '25), 31., 2025, Toronto. Proceedings... New York: ACM, 2025. p. 1420-1431. Disponível em: https://dl.acm.org/doi/abs/10.1145/3711896.3737149. Acesso em: 10 set. 2026.
10. ZHENG, Lixiao; XIAO, Jipeng. Temporal Cycle Enumeration for Detecting Financial Fraud. Data and Information Management, v. 9, n. 2, art. 100058, p. 1-12, 2024. Disponível em: https://www.sciengine.com/DI/doi/10.3724/2096-7004.di.2024.0058. Acesso em: 10 set. 2026.
11. WU, Zhiying et al. TRacer: Scalable Graph-Based Transaction Tracing for Account-Based Blockchain Trading Systems. IEEE Transactions on Information Forensics and Security, v. 18, p. 2541-2555, 2023. Disponível em: https://dl.acm.org/doi/abs/10.1109/TIFS.2023.3266162. Acesso em: 10 set. 2026.
12. DARWISH, Saad M. et al. An Intelligent Memetic Approach to Detect Online Fraud for Distributed FinTech Environments. Electronic Commerce Research, v. 25, n. 2, p. 415-438, 2025. Disponível em: https://link.springer.com/article/10.1007/s10660-025-10050-y. Acesso em: 10 set. 2026.
13. IYER, Anand P. et al. ASAP: Fast, Approximate Graph Pattern Mining at Scale. In: USENIX SYMPOSIUM ON OPERATING SYSTEMS DESIGN AND IMPLEMENTATION (OSDI '18), 13., 2018, Carlsbad. Proceedings... Berkeley: USENIX Association, 2018. p. 745-761. Disponível em: https://dl.acm.org/doi/abs/10.5555/3291168.3291224. Acesso em: 10 set. 2026.
14. CHEN, Xining et al. cuRPQ: A High-Performance GPU-Based Framework for Processing Regular and Conjunctive Regular Path Queries. In: ACM SIGMOD INTERNATIONAL CONFERENCE ON MANAGEMENT OF DATA (SIGMOD '26), 2026, Santiago. Proceedings... New York: ACM, 2026. p. 1-15. Disponível em: https://dl.acm.org/doi/abs/10.1145/3802033. Acesso em: 10 set. 2026.

### 3.1 Fundamentação Teórica Complementar

As duas teses abaixo ficam fora do conjunto definitivo de 14 artigos e da comparação central. São utilizadas somente como pano de fundo, com sua natureza documental explicitada.

1. AHMAD, Shahbaz. Scalable Analytics on Multi-Streams Dynamic Graphs. 2025. Tese (Doutorado em Ciência da Computação) — Université Grenoble Alpes, Grenoble, 2025. Disponível em: https://theses.hal.science/tel-05351773/. Acesso em: 10 set. 2026.

   - **Justificativa de uso:** contexto de processamento de fluxos e análise de grafos dinâmicos; material complementar para situar o problema, sem contabilização como artigo revisado por pares.

2. JEYARAMAN, Brindha Priyadarshini. Temporal Relational Graph Convolutional Networks for Financial Applications. 2025. Tese (Doutorado em Engenharia) — Singapore Management University, Singapura, 2025. Disponível em: https://ink.library.smu.edu.sg/etd_coll/703. Acesso em: 10 set. 2026.

   - **Justificativa de uso:** contexto de redes neurais em grafos temporais (GNN) em aplicações financeiras; abordagem fora do escopo central DFS/Kosaraju versus DFA/CEP, mantida apenas para contextualização.

---

## 4. Contribuição Individual dos Integrantes

> **Importante:** cada integrante deve descrever, com suas próprias palavras, o que efetivamente fez em cada passo desta etapa. Contribuições genéricas como "ajudei em tudo" não serão aceitas. Use verbos de ação e seja específico (ex.: "executei a busca no IEEE Xplore com a string 2 e obtive 84 resultados; fiz a triagem por título/resumo de 40 desses").

### Integrante 1 — Guilherme Lombardi
- **Passo(s) em que atuou:** Passos 1, 2, 3, 4, 5, 6 e 7
- **O que fez em cada passo:** 
- Passo 1: Elaborei a pergunta de pesquisa central sobre o uso de Autômatos Finitos para redução de complexidade assintótica e fiz o mapeamento dos conceitos-chave e seus sinônimos (PT/EN).
- Passo 2: Formulei e validei as strings de busca 14 a 19 focadas nos conceitos de pré-filtragem, latência e complexidade em grafos.
- Passo 3: Selecionei e redigi a justificativa metodológica para o uso das quatro bases principais (IEEE Xplore, ACM Digital Library, Springer Link e Google Scholar).
- Passo 4: Redigi os critérios de inclusão e exclusão técnicos para direcionar o escopo do projeto de 2020 a 2026.
- Passo 5: Consolidei os registros de buscas de todo o grupo, executei as varreduras com as strings 14 a 19 e organizei os metadados dos artigos em diretório local.
- Passos 6 e 7: Participei ativamente da triagem por título/resumo dos 721 resultados brutos, remoção de duplicatas e conduzi a leitura completa dos textos para seleção original de 16 publicações. Após a revisão do recorte, a seleção foi organizada em 14 artigos definitivos e 2 teses de fundamentação complementar.
- **Tempo dedicado:** 18h

<a id="evidencia-lombardi"></a>

- **Evidência declarada da contribuição** *(print de busca, planilha de triagem, exportação BibTeX, etc.)*: acervo digital dos PDFs organizados e postagens dos artigos no github
- **Comprovação pendente:** [registro individual e anexos necessários](evidencias_individuais/README.md#lombardi). O texto acima registra uma declaração; os prints ou exportações e a planilha de triagem artigo a artigo ainda precisam ser anexados.

### Integrante 2 — Caio Winkler Marangoni
- **Passo(s) em que atuou:** Passos 2, 5, 6 e 7
- **O que fez em cada passo:** 
- Passo 2: Criei as strings de busca de 1 a 7, conectando os eixos do projeto à enumeração de ciclos, componentes fortemente conectados e dados de transações. A consulta histórica nº 6 permanece vinculada ao registro original no Passo 2.
- Passo 5: Executei as varreduras de teste e coleta das strings 1 a 7 nas bases ACM DL, IEEE Xplore, Springer Link, ScienceDirect e arXiv, registrando o volume de resultados de cada consulta.
- Passos 6 e 7: Colaborei no processo de desduplicação e triagem por título/resumo e participei da leitura dos textos integrais dos artigos do eixo de algoritmos em grafos.
- **Tempo dedicado:** 10h

<a id="evidencia-caio"></a>

- **Evidência declarada da contribuição:** Definição das strings 1 a 7 na documentação e histórico de registros da primeira e segunda filtragem.
- **Comprovação pendente:** [registro individual e anexos necessários](evidencias_individuais/README.md#caio). O texto acima registra uma declaração; os prints ou exportações e a planilha de triagem artigo a artigo ainda precisam ser anexados.

### Integrante 3 — Guilherme Libório Camargo
- **Passo(s) em que atuou:** Passos 2, 5, 6 e 7
- **O que fez em cada passo:** 
- Passo 2: Formulei as strings de busca de 8 a 10 focadas em redes neurais em grafos (GNNs), processamento de eventos complexos e detecção de anomalias estruturais.
- Passo 5: Realizei as buscas com as strings 8 a 10 nas bases Springer Link, IEEE Xplore, ACM DL, NeurIPS, Google Scholar e ScienceDirect, contabilizando o retorno de cada uma.
- Passos 6 e 7: Atuei na filtragem de títulos e resumos para eliminação de trabalhos focados unicamente em IA caixa-preta e auxilei na seleção dos artigos do conjunto definitivo
- **Tempo dedicado:** 9h

<a id="evidencia-liborio"></a>

- **Evidência declarada da contribuição:** Mapeamento das strings 8 a 10 e registros de participação na planilha de triagem do grupo.
- **Comprovação pendente:** [registro individual e anexos necessários](evidencias_individuais/README.md#liborio). O texto acima registra uma declaração; os prints ou exportações e a planilha de triagem artigo a artigo ainda precisam ser anexados.

### Integrante 4 — Ryan dos Santos Veloso
- **Passo(s) em que atuou:** Passos 2, 5, 6 e 7
- **O que fez em cada passo:**
- Passo 2: Desenvolvi as strings de busca de 11 a 13 direcionadas à engenharia de dados, pré-processamento de transações e busca por caminhos paralelos/ciclos em redes bancárias.
- Passo 5: Executei a busca das strings 11 a 13 nas bases ScienceDirect, MDPI, PubMed Central e IEEE Xplore, registrando a contagem de resultados retornados.
- Passos 6 e 7: Participei das reuniões presenciais e remotas do grupo para discussão sobre a exclusão de artigos fora do escopo e leitura de introdução/conclusão dos artigos pré-selecionados.
- **Tempo dedicado:** 9h

<a id="evidencia-ryan"></a>

- **Evidência declarada da contribuição:** Estruturação das strings 11 a 13 e participação nos registros das etapas de filtragem do PRISMA.
- **Comprovação pendente:** [registro individual e anexos necessários](evidencias_individuais/README.md#ryan). O texto acima registra uma declaração; os prints ou exportações e a planilha de triagem artigo a artigo ainda precisam ser anexados.

### Registro histórico — Julia Emily Leonardo Barbosa; minha continuidade (Caio Winkler Marangoni)

> Quando Julia saiu do grupo, dei continuidade às partes que ficaram em aberto e assumi a organização das evidências dessa continuidade. As declarações abaixo continuam pertencendo ao histórico dela; não as reatribuo a mim.

- **Passo(s) em que atuou:** Passos 6 e 7
- **O que fez em cada passo:**
- Passo 6: Participou ativamente das conversas do grupo nas aulas vagas e no ambiente virtual para análise de títulos e resumos, auxiliando na identificação e remoção de duplicatas entre as bases.
- Passo 7: Colaborou na leitura analítica de introdução e conclusão dos artigos pré-selecionados, ajudando no desempate de dúvidas com suporte de buscas complementares e no alinhamento às orientações da professora Andrea Ono Sakai.
- **Tempo dedicado:** 6h

<a id="evidencia-julia-caio"></a>

- **Evidência declarada da contribuição:** Registro de participação na planilha de triagem do projeto e validação dos critérios de exclusão do conjunto final.
- **Comprovação pendente:** [registro individual e anexos necessários](evidencias_individuais/README.md#julia-caio). O texto acima registra uma declaração; os prints ou exportações e a planilha de triagem artigo a artigo ainda precisam ser anexados.

### 4.1 Quadro-resumo histórico de participação por passo

Preservei os percentuais e as horas declarados na etapa original, anteriores à saída de Julia. Minha continuidade não significa somar a mim as horas ou porcentagens históricas dela.

| Passo | Responsável(is) | % estimado de participação de cada um |
|---|---|---|
| 1. Pergunta e palavras-chave | Guilherme Lombardi | Guilherme Lombardi (100%) |
| 2. Strings de busca | Caio, Guilherme Libório, Ryan e Guilherme Lombardi | Caio (30%), Guilherme Libório (25%), Ryan (25%), Guilherme Lombardi (20%) |
| 3. Bases de dados | Guilherme Lombardi | Guilherme Lombardi (100%) |
| 4. Critérios de inclusão/exclusão | Guilherme Lombardi | Guilherme Lombardi (100%) |
| 5. Execução das buscas | Guilherme Lombardi, Caio, Guilherme Libório e Ryan | Guilherme Lombardi (40%), Caio (20%), Guilherme Libório (20%), Ryan (20%) |
| 6. Triagem título/resumo | Integrantes da composição original | Guilherme Lombardi (25%), Caio (20%), Guilherme Libório (20%), Ryan (20%), Julia (15%) |
| 7. Triagem texto completo | Integrantes da composição original | Guilherme Lombardi (25%), Caio (20%), Guilherme Libório (20%), Ryan (20%), Julia (15%) |

### 4.2 Quadro-resumo histórico geral de participação na etapa

| Integrante | % estimado de participação total nesta etapa |
|---|---|
| Guilherme Lombardi | 32% |
| Caio Winkler Marangoni | 20% |
| Guilherme Libório Camargo | 19% |
| Ryan dos Santos Veloso | 19% |
| Julia Emily Leonardo Barbosa | 10% |

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
- [ ] Exportações bibliográficas anexadas e vinculadas aos registros individuais
- [x] Triagem por título/resumo concluída (com duplicatas removidas)
- [x] Triagem por texto completo (introdução/conclusão) concluída
- [x] Conjunto definitivo de artigos para fichamento compilado

**Documentação**
- [x] Contribuição individual de cada integrante registrada por passo
- [x] Quadro-resumo histórico de participação preservado (soma = 100%)
- [ ] Prints ou exportações reais de busca anexados
- [ ] Planilha real de triagem artigo a artigo anexada, com identificação de responsáveis
- [ ] Evidências da minha continuidade das partes de Julia anexadas

---
