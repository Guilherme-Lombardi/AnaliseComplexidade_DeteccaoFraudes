# Etapa 1 Tema e delimitação

## Solicitação

Defina um tema específico, relevante e viável para o artigo de revisão bibliográfica.

## Identificação

- Grupo: Grupo 1 = Complexidade e Desempenho em Pipeline Híbrida para Detecção de Fraudes Financeiras (Computabilidade e Complexidade de Algoritmos; orientadora: Andrea Ono Sakai)
> ⚠️ **PENDENTE:** o nome ou número do grupo não consta em (a), (b) ou (c). Usei o título do projeto.
- Integrantes: Guilherme Lombardi, Ryan dos Santos Veloso, Caio Winkler Marangoni e Guilherme Liborio Camargo. Ex-integrante (registro histórico): Julia Emily Leonardo Barbosa.
> ⚠️ **REVISAR:** a grafia do sobrenome varia entre "Liborio" (README, a, c) e "Libório" (b). Definam uma só.
- Data: {dd/mm/aaaa}
> ⚠️ **PENDENTE:** a etapa (a) foi entregue em 18/08/2026, mas a data de entrega deste template não consta.

## Preenchimento

### Área geral

Sistema de detecção de fraude, algoritmos de otimização de busca, modelo de aprendizagem e complexidade dos algoritmos.
> ⚠️ **REVISAR:** é o texto original de (a), seção 2.1. "Modelo de aprendizagem" destoa do recorte final, que exclui estudos de aprendizado de máquina "caixa-preta" sem abordagem estrutural (critérios de exclusão em b). Sugestão: enfatizar "Computabilidade e Complexidade de Algoritmos".

### Tema delimitado

Análise comparativa, a partir da literatura, da complexidade assintótica de um pipeline tradicional de grafos (DFS/Kosaraju) e de uma arquitetura híbrida com pré-filtragem DFA/CEP, no contexto da detecção de fraudes bancárias em tempo real.

> ⚠️ **REVISAR:** a tabela 2.3 de (a) fala em "Autômatos Finitos com Machine Learning", enquanto 2.2 de (a) e (c) tratam só de DFA/CEP. Usei a versão de 2.2 e (c). Alinhem a 2.3 a essa versão.

### Do tema amplo ao específico

- Tema amplo: Análise de complexidade e desempenho em algoritmos de busca e grafos.
- Objeto estudado: o pipeline tradicional de travessia em grafos (DFS/Kosaraju, para ciclos e componentes fortemente conectados) comparado a uma arquitetura híbrida com pré-filtragem por Autômatos Finitos Determinísticos / Processamento de Eventos Complexos (DFA/CEP).
- Contexto ou aplicação: detecção de fraudes bancárias e em transações financeiras em tempo real (processamento de fluxos).
- Aspecto que será analisado: a complexidade assintótica no pior caso (incluindo o custo do pré-filtro e o tamanho dos grafos processados) e os tempos de resposta, a vazão e o consumo de memória reportados nas fontes, distinguindo redução do volume processado de mudança da ordem assintótica.
- O que ficará fora do estudo: execução própria de experimentos ou medição experimental; estudos exclusivamente de aprendizado de máquina "caixa-preta" sem análise estrutural ou de complexidade; aspectos jurídicos ou financeiros não técnicos; publicações anteriores a 2020 (exceto livros-texto clássicos de fundamentação); qualquer pressuposto de ganho no pior caso.

### Justificativa

Sistemas bancários reais processam volumes massivos de transações por segundo e exigem respostas em milissegundos. O uso direto de algoritmos estáticos de grafos (DFS/Kosaraju) gera gargalos computacionais à medida que a base de dados cresce. Analisar, na literatura, a complexidade e o desempenho de uma arquitetura com pré-filtragem por autômatos (DFA/CEP) tem valor prático para o setor financeiro e dá fundamentação teórica à Ciência da Computação, ao mostrar como a otimização algorítmica viabiliza a escalabilidade de sistemas reais.

### Viabilidade

- Há artigos científicos disponíveis? Sim. O conjunto final da etapa (b) tem 14 artigos e 2 teses de fundamentação complementar, em acervo local de PDFs.
- O tema pode ser estudado no prazo? Sim. O escopo foi limitado à revisão bibliográfica e à análise teórica de DFS/Kosaraju versus pré-filtragem DFA/CEP.
- O grupo possui acesso às fontes necessárias? Sim. Há acesso ao acervo bibliográfico registrado em (b).

## Produto da etapa

Tema delimitado e justificativa.

## Checklist

- [x] O tema é específico.
- [x] O tema é relevante.
- [x] O tema é viável.
- [x] O recorte está claro.
- [x] O tema foi validado pelo professor.
> ⚠️ **PENDENTE:** (a) registra "Sim com ajustes" em 28/08/2026, mas o próprio documento diz que falta registrar formalmente a validação (o campo e o checklist estavam em branco). Marquei conforme o checklist de (a). Confirmem e anexem o registro da validação.

## Contribuições

| Integrante | Atividade realizada |
|---|---|
| Guilherme Lombardi | Busquei artigos sobre algoritmos de busca em grafos (como DFS) e sobre limites de desempenho no processamento de grandes bases; ajudei a selecionar os dois primeiros links, auxiliei no direcionamento do tema e das pesquisas e defini suas palavras-chave. |
| Ryan dos Santos Veloso | Pesquisei artigos sobre como transações bancárias e suspeitas de fraude são representadas em grafos, ajudei a preencher a tabela de delimitação do tema e a pesquisar filtragem contínua por autômatos. |
| Caio Winkler Marangoni | Pesquisei artigos sobre IA e Machine Learning para detecção de fraudes em tempo real e colaborei na redação da justificativa. |
| Guilherme Liborio Camargo | Fiz o levantamento bibliográfico sobre processamento de dados em fluxo (streaming) e filtragem contínua por autômatos, selecionando as fontes desse assunto. |
| Julia Emily Leonardo Barbosa (ex-integrante, registro histórico) | Procurei pesquisas sobre detecção de fraude em pagamentos digitais, organizei a tabela de viabilidade e revisei a formatação geral do documento. |

> ⚠️ **REVISAR:** as contribuições vêm de (a), seção 5, e são históricas. Decidam se Julia continua na tabela. Se esta etapa nova exigir contribuições atuais, será preciso reescrevê-las.
