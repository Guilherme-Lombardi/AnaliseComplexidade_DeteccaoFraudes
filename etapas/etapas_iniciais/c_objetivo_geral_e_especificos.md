# Template de Definição de Objetivos da Pesquisa Científica
### Computabilidade e Complexidade de Algoritmos

> **Como usar este template:** respondam cada pergunta no espaço indicado por `> Resposta:`. Sigam o passo a passo e usem os exemplos apenas como referência de estrutura — o conteúdo deve ser sobre o tema do grupo.

---

## Identificação do Grupo

| Campo | Informação |
|---|---|
| Curso / Disciplina | Computabilidade e Complexidade de Algoritmos |
| Projeto de Pesquisa / IC | Complexidade e Desempenho em Pipeline Híbrida para Detecção de Fraudes Financeiras |
| Orientador(a) | Andrea Ono Sakai |
| Data de entrega desta etapa | 10/09/2026 |
| Integrantes do grupo | Guilherme Lombardi 1, Ryan dos Santos Veloso 2, Caio Winkler Marangoni 3, Guilherme Liborio Camargo 4 |
| Tema (da etapa "a") | Análise comparativa de complexidade assintótica entre um pipeline tradicional de grafos (DFS/Kosaraju) e uma arquitetura híbrida com pré-filtragem por Autômatos Finitos, aplicada à detecção de fraudes bancárias em tempo real. |

**Atualização da composição do grupo:** Quando Julia Emily Leonardo Barbosa saiu do grupo, eu, Caio Winkler Marangoni, dei continuidade às partes que ficaram em aberto, mantendo a autoria histórica dela.

## PARTE 1 — DEFINIR O OBJETIVO GERAL

### 1.1 Tema específico do grupo

**Pergunta:** Qual foi o tema específico que o grupo definiu?

> Resposta: Análise comparativa de desempenho e complexidade assintótica entre um pipeline tradicional de travessia em grafos (DFS/Kosaraju) e uma arquitetura híbrida com pré-filtragem por Autômatos Finitos Determinísticos (DFA/CEP), aplicada à detecção de fraudes em transações bancárias em tempo real.

### 1.2 Passo a passo para chegar ao objetivo geral

**Passo 1 — Delimitação do tema**
Delimitem o tema específico por área, tempo, espaço ou aplicação.

> Resposta: O estudo é delimitado na área de Computabilidade e Complexidade de Algoritmos, focando no processamento de fluxos de dados em tempo real (stream processing) para detecção de fraudes em sistemas bancários e transações financeiras. A pesquisa se restringe à análise teórica e documental da literatura selecionada na etapa (b), com foco na produção recente (2020–2026) e apoio de fundamentos clássicos. Serão comparados os custos assintóticos de DFS/Kosaraju e de uma arquitetura com pré-filtragem DFA/CEP, incluindo o custo do pré-filtro e o tamanho dos grafos processados. Os dados de latência, vazão e uso de recursos serão extraídos dos artigos revisados, observadas as condições e limitações de comparação entre os estudos.

**Passo 2 — Formulação da problemática**
Transformem o tema em uma pergunta que expresse o problema de pesquisa.

*Exemplo:* "Quais os principais impactos da árvore de decisão em IA para definir estratégias de marketing para segmentação de clientes?"

> Resposta: Segundo a literatura revisada, como se comparam a complexidade assintótica no pior caso e os tempos de resposta reportados para a abordagem direta em grafos (DFS/Kosaraju) e para uma arquitetura com pré-filtragem por DFA/CEP no contexto da detecção de fraudes financeiras em tempo real, e sob quais hipóteses a redução de carga pode afetar esses custos?

**Passo 3 — Transformar a pergunta em objetivo geral**
Reescrevam a pergunta como uma afirmação, usando um verbo no infinitivo.

*Exemplo:* "Analisar os principais impactos da árvore de decisão em IA para definir estratégias de marketing para segmentação de clientes."

> Resposta: Analisar, com base na literatura selecionada na etapa (b), a complexidade assintótica e as métricas de desempenho reportadas para a abordagem direta em grafos (DFS/Kosaraju) e para uma arquitetura com pré-filtragem por DFA/CEP na detecção de fraudes financeiras em tempo real, identificando as hipóteses, os custos e as limitações de cada abordagem.

**Passo 4 — Ajustes finais**
Revisem o objetivo geral seguindo os critérios abaixo:

- [x] É claro, direto e mensurável?
- [x] Evitei verbos fracos como "estudar" ou "conhecer"?
- [x] Usei um verbo forte (explorar, analisar, investigar, compreender, avaliar, propor, desenvolver, aplicar, identificar)?

**Modelo genérico de referência:**
> "[Verbo no infinitivo] a aplicação de [conceito ou técnica] em [contexto específico], com o propósito de [finalidade principal]."

**Outros exemplos de objetivos gerais (referência):**
- Investigar o uso de árvores de decisão para prever exportações de vinho no Brasil, com base em dados da Embrapa entre 2000 e 2025.
- Analisar o impacto da classificação automática de vinhos finos e de mesa por meio de algoritmos de inteligência artificial, a fim de apoiar estratégias de exportação.
- Desenvolver um modelo computacional baseado em árvore binária de busca para otimizar a recomendação de rotas de ambulância em cenários urbanos.

### 1.3 Respostas finais da Parte 1

**1) Qual a problemática?**

> Resposta: Segundo a literatura revisada, como se comparam a complexidade assintótica no pior caso e os tempos de resposta reportados para a abordagem direta em grafos (DFS/Kosaraju) e para uma arquitetura com pré-filtragem por DFA/CEP no contexto da detecção de fraudes financeiras em tempo real, e sob quais hipóteses a redução de carga pode afetar esses custos?

**2) Qual o objetivo geral?**

> Resposta: Analisar, com base na literatura selecionada na etapa (b), a complexidade assintótica e as métricas de desempenho reportadas para a abordagem direta em grafos (DFS/Kosaraju) e para uma arquitetura com pré-filtragem por DFA/CEP na detecção de fraudes financeiras em tempo real, identificando as hipóteses, os custos e as limitações de cada abordagem.

---

## PARTE 2 — DEFININDO OS OBJETIVOS ESPECÍFICOS

### 2.1 Objetivo geral pesquisado

Copiem aqui o objetivo geral definido na Parte 1 (deve conceituar os assuntos abordados no tema).

> Resposta: Analisar, com base na literatura selecionada na etapa (b), a complexidade assintótica e as métricas de desempenho reportadas para a abordagem direta em grafos (DFS/Kosaraju) e para uma arquitetura com pré-filtragem por DFA/CEP na detecção de fraudes financeiras em tempo real, identificando as hipóteses, os custos e as limitações de cada abordagem.

### 2.2 Assuntos da pesquisa

Escrevam de 4 a 5 assuntos que serão abordados na pesquisa.

*Exemplo (para o tema de árvore de decisão em IA e marketing):*
- Conceituar árvore de decisão
- Conceituar inteligência artificial
- Quais são as estratégias de marketing para segmentação de clientes?
- Analisar a relação existente entre árvore de decisão e inteligência artificial
- Apresentar quais são os resultados das estratégias de marketing para segmentação de clientes sem e com IA

**Assuntos do grupo:**
1. Resposta: Mapear a arquitetura de detecção de fraudes baseada em detecção de ciclos e Componentes Fortemente Conectados (SCC) em grafos de transações financeiras.
2. Resposta: Conceituar a modelagem de pré-filtragem por Autômatos Finitos Determinísticos (DFA) e Processamento de Eventos Complexos (CEP) para fluxos de dados contínuos.
3. Resposta: Comparar, a partir das análises teóricas publicadas, as ordens de complexidade assintótica no pior caso entre a abordagem direta em grafos e a arquitetura híbrida, considerando o custo da pré-filtragem e o tamanho dos grafos processados.
4. Resposta: Analisar, com base na literatura revisada, o comportamento assintótico e os tempos de resposta e vazão reportados para DFS/Kosaraju e para a pré-filtragem DFA/CEP, registrando as condições e limitações de comparação entre os estudos.
5. Resposta: Avaliar, a partir dos resultados disponíveis nos artigos revisados, o impacto da redução de carga (load shedding e poda) nas taxas de falsos positivos e falsos negativos, explicitando a origem bibliográfica dos dados e eventuais lacunas de evidência.

### 2.3 Estrutura básica do artigo

Definam a estrutura do artigo, incluindo introdução e considerações finais.

*Exemplo de estrutura:*
- Introdução
- Conceituar árvore de decisão
- Conceituar inteligência artificial
- Quais são as estratégias de marketing para segmentação de clientes
- Analisar a relação existente entre árvore de decisão e inteligência artificial
- Apresentar quais são os resultados das estratégias de marketing para segmentação de clientes sem e com IA
- Considerações finais

**Estrutura do grupo:**
- Introdução
- Resposta: Mapeamento do estado da arte em algoritmos de grafos (DFS/Kosaraju) para detecção de anomalias e ciclos em transações bancárias
- Resposta: Fundamentação teórica de Autômatos Finitos Determinísticos (DFA/CEP) aplicados à pré-filtragem e redução de carga em fluxos contínuos
- Resposta: Análise comparativa de complexidade assintótica no pior caso entre a abordagem direta em grafos e a arquitetura híbrida com pré-filtro
- Resposta: Apresentação e discussão dos resultados comparativos de latência, vazão e consumo de memória extraídos dos artigos revisados, com suas condições de avaliação e limitações
- Considerações finais

### 2.4 Objetivos específicos classificados

Classifiquem os objetivos específicos em **Conceituais** e **Técnicos**.

*Exemplo:*
- **Objetivos Conceituais**
  - Conceituar árvore de decisão
  - Conceituar inteligência artificial
- **Objetivos Técnicos**
  - Quais são as estratégias de marketing para segmentação de clientes
  - Analisar a relação existente entre árvore de decisão e inteligência artificial
  - Apresentar quais são os resultados das estratégias de marketing para segmentação de clientes sem e com IA

**Objetivos específicos do grupo:**

- **Objetivos Conceituais**
  - Resposta: Mapear os fundamentos teóricos de algoritmos de travessia em grafos (DFS e Kosaraju) aplicados à identificação de ciclos e Componentes Fortemente Conectados (SCC) em redes de transações financeiras.
  - Resposta: Conceituar a modelagem de Autômatos Finitos Determinísticos (DFA) e Processamento de Eventos Complexos (CEP) para reconhecimento de padrões e pré-filtragem em fluxos de dados contínuos.

- **Objetivos Técnicos**
  - Resposta: Comparar teoricamente, a partir das fontes da etapa (b), as ordens de complexidade assintótica no pior caso entre o pipeline tradicional de varredura em grafos e a arquitetura híbrida com pré-filtragem por DFA/CEP, incluindo o custo do pré-filtro e as hipóteses sobre o tamanho dos grafos processados.
  - Comparar e avaliar, exclusivamente a partir dos resultados publicados na literatura revisada na etapa (b), os tempos de resposta (latência), a vazão (throughput) e o uso de recursos computacionais das duas abordagens, bem como o impacto da redução de carga (load shedding e poda) proporcionada pela pré-filtragem DFA/CEP na taxa de retenção de eventos e nas taxas de falsos positivos e falsos negativos, identificando as fontes, as condições de avaliação, as limitações de comparação entre os estudos e eventuais lacunas de evidência.a.

---

## CHECKLIST FINAL DO GRUPO

- [x] O tema específico está delimitado (área, tempo, espaço ou aplicação)
- [x] A problemática está formulada como pergunta
- [x] O objetivo geral está no infinitivo, claro e mensurável
- [x] Foram listados de 4 a 5 assuntos do artigo
- [x] A estrutura do artigo foi definida (introdução, desenvolvimento, considerações finais)
- [x] Os objetivos específicos foram classificados em Conceituais e Técnicos

