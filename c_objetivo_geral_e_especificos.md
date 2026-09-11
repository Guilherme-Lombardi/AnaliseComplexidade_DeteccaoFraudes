# Template de Definição de Objetivos da Pesquisa Científica
### Computabilidade e Complexidade de Algoritmos

> **Como usar este template:** respondam cada pergunta no espaço indicado por `> Resposta:`. Sigam o passo a passo e usem os exemplos apenas como referência de estrutura — o conteúdo deve ser sobre o tema do grupo.

---

## Identificação do Grupo

| Campo | Informação |
|---|---|
| Curso / Disciplina | `[Computabilidade e Complexidade de Algoritmos]` |
| Projeto de Pesquisa / IC | `[Complexidade e Desempenho em Pipeline Híbrida para Detecção de Fraudes Financeiras]` |
| Orientador(a) | `[Andrea Ono Sakai]` |
| Data de entrega desta etapa | `[10/09/2026]` |
| Integrantes do grupo | `[Guilherme Lombardi 1, Ryan dos Santos Veloso 2, Caio Winkler Marangoni 3, Guilherme Liborio Camargo 4, Julia Emily Leonardo Barbosa 5]` |
| Tema (da etapa "a") | `[Análise comparativa de complexidade assintótica entre um pipeline tradicional de grafos (DFS/Kosaraju) e uma arquitetura híbrida com pré-filtragem por Autômatos Finitos, aplicada à detecção de fraudes bancárias em tempo real.]` |

## PARTE 1 — DEFINIR O OBJETIVO GERAL

### 1.1 Tema específico do grupo

**Pergunta:** Qual foi o tema específico que o grupo definiu?

> Resposta: Análise comparativa de desempenho e complexidade assintótica entre um pipeline tradicional de travessia em grafos (DFS/Kosaraju) e uma arquitetura híbrida com pré-filtragem por Autômatos Finitos Determinísticos (DFA/CEP), aplicada à detecção de fraudes em transações bancárias em tempo real.

### 1.2 Passo a passo para chegar ao objetivo geral

**Passo 1 — Delimitação do tema**
Delimitem o tema específico por área, tempo, espaço ou aplicação.

> Resposta: O estudo é delimitado na área de Computabilidade e Complexidade de Algoritmos, focando no processamento de fluxos de dados em tempo real (stream processing). O escopo temporal compreende a literatura recente (2020–2026) e análises com janelas de execução em milissegundos para detecção imediata. A aplicação prática é voltada à detecção de fraudes em sistemas bancários e transações financeiras, utilizando estruturas de multigrafos direcionados ponderados e autômatos finitos para redução de carga e corte de complexidade assintótica.

**Passo 2 — Formulação da problemática**
Transformem o tema em uma pergunta que expresse o problema de pesquisa.

*Exemplo:* "Quais os principais impactos da árvore de decisão em IA para definir estratégias de marketing para segmentação de clientes?"

> Resposta: Em que medida a introdução de uma camada de pré-filtragem baseada em Autômatos Finitos Determinísticos (DFA/CEP) consegue reduzir a complexidade assintótica e o tempo de resposta no pior caso de um pipeline de detecção de fraudes bancárias em tempo real, quando comparada à varredura direta via algoritmos de travessia em grafos (DFS/Kosaraju)?

**Passo 3 — Transformar a pergunta em objetivo geral**
Reescrevam a pergunta como uma afirmação, usando um verbo no infinitivo.

*Exemplo:* "Analisar os principais impactos da árvore de decisão em IA para definir estratégias de marketing para segmentação de clientes."

> Resposta: Avaliar o impacto da inclusão de uma camada de pré-filtragem por Autômatos Finitos Determinísticos (DFA/CEP) na redução da complexidade assintótica e do tempo de latência de um pipeline de detecção de fraudes bancárias em tempo real, em comparação com a abordagem tradicional baseada unicamente em travessia de grafos via DFS e Kosaraju.

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

> Resposta: Em que medida a introdução de uma camada de pré-filtragem baseada em Autômatos Finitos Determinísticos (DFA/CEP) consegue reduzir a complexidade assintótica e o tempo de resposta no pior caso de um pipeline de detecção de fraudes bancárias em tempo real, quando comparada à varredura direta via algoritmos de travessia em grafos (DFS/Kosaraju)?

**2) Qual o objetivo geral?**

> Resposta: Avaliar a aplicação de uma camada de pré-filtragem baseada em Autômatos Finitos Determinísticos (DFA/CEP) em pipelines de detecção de fraudes bancárias em tempo real, com o propósito de reduzir a complexidade assintótica no pior caso e otimizar o tempo de resposta em relação aos algoritmos tradicionais de travessia em grafos (DFS/Kosaraju).

---

## PARTE 2 — DEFININDO OS OBJETIVOS ESPECÍFICOS

### 2.1 Objetivo geral pesquisado

Copiem aqui o objetivo geral definido na Parte 1 (deve conceituar os assuntos abordados no tema).

> Resposta: Avaliar a aplicação de uma camada de pré-filtragem baseada em Autômatos Finitos Determinísticos (DFA/CEP) em pipelines de detecção de fraudes bancárias em tempo real, com o propósito de reduzir a complexidade assintótica no pior caso e otimizar o tempo de resposta em relação aos algoritmos tradicionais de travessia em grafos (DFS/Kosaraju).

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
3. Resposta: Comparar as ordens de complexidade assintótica no pior caso ($O(\vert{}V\vert{} + \vert{}E\vert{})$ vs. custo de travessias profundas) entre a abordagem direta em grafos e a arquitetura híbrida.
4. Resposta: Implementar e benchmarkingar os pipelines em ambiente controlado (usando o dataset PaySim ou similar) para mensurar métricas de latência e Throughput.
5. Resposta: Avaliar o impacto da redução de carga (load shedding e poda) na taxa de falsos positivos e falsos negativos do sistema em tempo real.

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
- Resposta: Apresentação e discussão dos resultados práticos de latência, throughput e consumo de memória (benchmarks no PaySim)
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
  - Resposta: Comparar teoricamente as ordens de complexidade assintótica no pior caso entre o pipeline tradicional de varredura em grafos e a arquitetura híbrida com camada de pré-filtragem por DFA.
  - Resposta: Implementar e benchmarkar ambas as abordagens sob o dataset PaySim para mensurar variações no tempo de resposta (latência) e vazão (throughput).
  - Resposta: Avaliar o impacto da pré-filtragem na taxa de retenção de eventos e no uso de recursos computacionais durante o processamento de transações em tempo real.

---

## CHECKLIST FINAL DO GRUPO

- [x] O tema específico está delimitado (área, tempo, espaço ou aplicação)
- [x] A problemática está formulada como pergunta
- [x] O objetivo geral está no infinitivo, claro e mensurável
- [x] Foram listados de 4 a 5 assuntos do artigo
- [x] A estrutura do artigo foi definida (introdução, desenvolvimento, considerações finais)
- [x] Os objetivos específicos foram classificados em Conceituais e Técnicos


