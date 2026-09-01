# Etapa (a) — Escolha do Tema

> **Como preencher:** este documento deve ser preenchido **em conjunto pelo grupo**, mas com registro individualizado da contribuição de cada integrante. Substitua os campos entre `[ ]` pelas informações do seu grupo. Não apague as instruções em itálico — elas ajudam na avaliação do orientador.

---

## 1. Identificação do Grupo

| Campo | Informação |
|---|---|
| Curso / Disciplina | `[Computabilidade e Complexidade de Algoritmos]` |
| Projeto de Pesquisa / IC | `[Complexidade e Desempenho em Pipeline Híbrida para Detecção de Fraudes Financeiras]` |
| Orientador(a) | `[Andrea Ono Sakai]` |
| Data de entrega desta etapa | `[18/08/2026]` |
| Integrantes do grupo | `[Guilherme Lombardi 1, Ryan dos Santos Veloso 2, Caio Winkler Marangoni 3, Guilherme Liborio Camargo 4, Julia Emily Leonardo Barbosa 5]` |

---

## 2. Tema Escolhido

### 2.1 Área geral de interesse
*Qual grande área do conhecimento/disciplina motivou a escolha (ex.: complexidade dos algoritmos, classes de problemas P, NP, Algoritmos Gulosos, Programação Dinâmica, Divisão e conquista)?*

`[Sistema de Detecção de fraude, Algoritmos de Otimização de Busca, Modelo Aprendizagem e Complexidade dos Algoritmos]`

### 2.2 Tema delimitado (versão final)
*Escreva o tema já delimitado, de forma específica — não o tema amplo. Lembre-se: o tema deve ser enunciado em 1 a 2 frases, como um assunto (ainda não é uma pergunta de pesquisa, isso vem na etapa "c").*

> **Tema:** `[Análise comparativa de complexidade assintótica entre um pipeline tradicional de grafos (DFS/Kosaraju) e uma arquitetura híbrida com pré-filtragem por Autômatos Finitos, aplicada à detecção de fraudes bancárias em tempo real.]`

### 2.3 Do amplo ao específico
*Mostre o raciocínio de delimitação — como vocês chegaram do tema amplo ao tema específico.*

| Tema amplo (ponto de partida) | Tema delimitado (ponto de chegada) |
|---|---|
| `[Análise de complexidade e desempenho em algoritmos de busca e grafos.]` | `[Comparação entre o gargalo computacional dos algoritmos DFS/Kosaraju em grandes volumes e a eficiência do uso de Autômatos Finitos com Machine Learning para detecção de fraudes em tempo real.]` |

---

## 3. Justificativa da Escolha

### 3.1 Relevância
*Por que esse tema é importante ou atual? Para quem ele importa (academia, mercado, sociedade)?*

`[Sistemas bancários reais lidam com volumes massivos de transações por segundo e exigem respostas em milissegundos. No mercado e na pesquisa acadêmica, o uso direto de algoritmos estáticos de grafos gera gargalos computacionais conforme a base de dados cresce. Analisar teoricamente a complexidade e avaliar uma arquitetura baseada em autômatos para pré-filtragem traz alto valor prático para o setor financeiro e fundamentação teórica sólida para a Ciência da Computação, demonstrando como a otimização algorítmica viabiliza a escalabilidade de sistemas reais.]`

### 3.2 Viabilidade
*O grupo avaliou se tem tempo, recursos, acesso a dados/fontes e domínio mínimo do assunto para desenvolver esse tema até o fim do projeto?*

| Critério | Avaliação (Sim/Parcial/Não) | Observação |
|---|---|---|
| Tempo disponível é suficiente | `[Sim]` | `[O escopo está delimitado para testes de desempenho e análise assintótica sobre dados simulados.]` |
| Há acesso a fontes/dados necessários | `[Sim]` | `[Referências bibliográficas consolidadas (ACM, Springer, IEEE) e dados sintéticos em JSON/CSV disponíveis.]` |
| O grupo já tem domínio mínimo do tema | `[Sim]` | `[Conhecimento prévio em algoritmos de grafos (DFS, Kosaraju) e protótipo base já estruturado..]` |
| Recursos técnicos necessários estão disponíveis | `[Sim]` | `[Uso de ambiente Python, bibliotecas de grafos, automação de testes e modelos de aprendizado de máquina.]` |

### 3.3 Originalidade / Não-redundância
*O grupo verificou rapidamente (via um levantamento preliminar) se o tema já é excessivamente explorado ou se existe um ângulo próprio a ser explorado?*

`[Diferente de trabalhos convencionais que focam apenas na acurácia do Machine Learning para detectar fraudes, esta pesquisa direciona o foco para a Complexidade de Algoritmos. O diferencial está em demonstrar matematicamente e na prática como a introdução de um Autômato Finito na camada de borda altera a ordem de grandeza do tempo de execução, reduzindo o volume processado pelo motor de grafos e viabilizando a análise em tempo real.]`

---

## 4. Validação com o Orientador

| Campo | Informação |
|---|---|
| Data da conversa/validação | `[28/08/2026]` |
| Tema aprovado pelo orientador? | `[Sim com ajustes]` |
| Observações ou ajustes solicitados pelo orientador | `[Falta registrar formalmente a validação do tema com a orientadora (campo e checklistem branco); recomenda-se também já planejar como a comparação dedesempenho será medida experimentalmente (dataset sintético,métricas, ambiente de teste)]` |

---

## 5. Contribuição Individual dos Integrantes

> **Importante:** cada integrante deve descrever, com suas próprias palavras, o que efetivamente fez nesta etapa. Contribuições genéricas como "ajudei em tudo" não serão aceitas. Use verbos de ação e seja específico (ex.: "pesquisei 5 temas candidatos e apresentei prós/contras ao grupo").

### Integrante 1 — `[Guilherme Lombardi]`
- **O que fez nesta etapa:** `[Busquei artigos sobre algoritmos de busca em grafos (como DFS), pesquisei sobre os limites de desempenho no processamento de grandes bases de dados e ajudei a selecionar os dois primeiros links, auxiliei no direcionamento do tema e das pesquisas e defini suas palavras-chave]`
- **Tempo dedicado (aprox.):** `[ex.: 3h30]`
- **Evidência da contribuição** *(print de conversa, rascunho, e-mail, documento compartilhado etc.)*: 
`[https://www.semanticscholar.org/paper/Benchmarking-Algorithms-for-Detecting-Anomalies-in-Carrasquilla/60d9e710304b9223c4206c0b29c192f7a0ed6f30]` 
`[https://dl.acm.org/doi/abs/10.1145/3677052.3698648]`


### Integrante 2 — `[Ryan dos Santos Veloso]`
- **O que fez nesta etapa:** `[Pesquisei artigos científicos que mostram como transações bancárias e suspeitas de fraude são representadas em forma de grafos e ajudei a preencher a tabela de delimitação do tema. E ajudei nas pesquisas de filtragem contínua por autômatos]`
- **Tempo dedicado (aprox.):** `[ex.: 3h]`
- **Evidência da contribuição:**
`[https://dl.acm.org/doi/abs/10.1145/3690624.3709170]`
`[https://dl.acm.org/doi/abs/10.1145/2675743.2771877]`

### Integrante 3 — `[Caio Winkler Marangoni]`
- **O que fez nesta etapa:** `[Pesquisei artigos sobre o uso de inteligência artificial e Machine Learning para detecção de fraudes em tempo real e colaborei na redação do texto de justificativa.]`
- **Tempo dedicado (aprox.):** `[ex.: 2h30]`
- **Evidência da contribuição:**
`[https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4895921]`
`[https://dl.acm.org/doi/abs/10.1145/3289402.3289530]`

### Integrante 4 — `[Guilherme Liborio Camargo]`
- **O que fez nesta etapa:** `[Realizei o levantamento bibliográfico sobre processamento de dados em fluxo (streaming) e filtragem contínua por autômatos, selecionando as fontes de pesquisa deste assunto.]`
- **Tempo dedicado (aprox.):** `[ex.: 3h]`
- **Evidência da contribuição:** 
`[https://hal.science/hal-04687320/]`
`[https://dl.acm.org/doi/10.1145/2187671.2187677]`


### Integrante 5 — `[Julia Emily Leonardo Barbosa]`
- **O que fez nesta etapa:** `[Procurei pesquisas sobre detecção de fraude em pagamentos digitais, organizei a tabela de avaliação de viabilidade do projeto e revisei a formatação geral do documento.]`
- **Tempo dedicado (aprox.):** `[ex.: 2h45]`
- **Evidência da contribuição:** 
`[https://link.springer.com/article/10.1007/s10791-025-09549-7]`
`[https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5076783]`

*(Copie o bloco acima para cada integrante adicional do grupo.)*

### 5.1 Quadro-resumo de participação

| Integrante | Contribuição principal | % estimado de participação nesta etapa |
|---|---|---|
| `[Guilherme Lombardi 1]` | `[Pesquisa de artigos sobre grafos e travessia]` | `[ex.: 20%]` |
| `[Ryan dos Santos Veloso 2]` | `[Pesquisa de grafos em fraudes e delimitação do tema]` | `[ex.: 20%]` |
| `[Caio Winkler Marangoni 3]` | `[Pesquisa de Machine Learning em tempo real e justificativa]` | `[ex.: 20%]` |
| `[Guilherme Liborio Camargo 4]` | `[Pesquisa de artigos sobre streams e autômatos]` | `[ex.: 20%]` |
| `[Julia Emily Leonardo Barbosa 5]` | `[Pesquisa de IA em pagamentos e tabela de viabilidade]` | `[ex.: 20%]` |

*A soma das porcentagens deve ser igual a 100%. Divergências de percepção sobre a participação devem ser discutidas em grupo antes do envio — o orientador pode solicitar esclarecimentos individuais em caso de disparidade relevante.*

---

## 6. Checklist Final da Etapa

- [x] Tema delimitado e redigido em 1-2 frases
- [x] Justificativa de relevância escrita
- [x] Viabilidade avaliada pelo grupo
- [x] Verificação preliminar de originalidade realizada
- [X] Tema validado com o orientador
- [x] Contribuição individual de cada integrante registrada
- [x] Quadro-resumo de participação preenchido (soma = 100%)

---


