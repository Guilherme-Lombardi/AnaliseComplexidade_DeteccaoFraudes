# Etapa 6 Leitura e fichamento

## Solicitação

Preencha uma cópia deste template para cada artigo selecionado.

Este arquivo reúne as **14 cópias** (uma por artigo do conjunto definitivo de (b), seção 3), na mesma ordem da lista final. A identificação veio de (b). O fichamento exige a leitura dos artigos, que não consta em (a), (b) ou (c).

| Nº | Artigo | Acervo | Leitor | Fichamento |
|---|---|---|---|---|
| 01 | CHAPNIK et al. (2022), DARLING | Bloco 1 | Guilherme Libório| Data da leitura: 17/10/2026, Problema investigado, Objetivo do estudo, Método utilizado, Contexto, amostra ou dados, Principais resultados, Limitações, Contribuição para o nosso artigo, Comentário crítico |
| 02 | SLO et al. (2020), hSPICE | Bloco 1 | Guilherme Libório| Data da leitura: 17/10/2026, Problema investigado, Objetivo do estudo, Método utilizado, Contexto, amostra ou dados, Principais resultados, Limitações, Contribuição para o nosso artigo, Comentário crítico |
| 03 | YANKOVITCH et al. (2022), HYPERSONIC | Bloco 1 | Guilherme Libório | Data da leitura: 17/10/2026, Problema investigado, Objetivo do estudo, Método utilizado, Contexto, amostra ou dados, Principais resultados, Limitações, Contribuição para o nosso artigo, Comentário crítico |
| 04 | PFANDZELTER; BERMBACH (2020), Operator as a Service | Bloco 1 | Guilherme Libório | Data da leitura: 17/10/2026, Problema investigado, Objetivo do estudo, Método utilizado, Contexto, amostra ou dados, Principais resultados, Limitações, Contribuição para o nosso artigo, Comentário crítico|
| 05 | LI et al. (2026), Efficient Densest Flow Queries | Bloco 2 | Guilherme Libório | Data da leitura: 17/10/2026, Problema investigado, Objetivo do estudo, Método utilizado, Contexto, amostra ou dados, Principais resultados, Limitações, Contribuição para o nosso artigo, Comentário crítico |
| 06 | CAPOZZI et al. (2025), FlowSeries: Anomaly Detection | Bloco 2 | Guilherme Libório | Data da leitura: 17/10/2026, Problema investigado, Objetivo do estudo, Método utilizado, Contexto, amostra ou dados, Principais resultados, Limitações, Contribuição para o nosso artigo, Comentário crítico |
| 07 | CAPOZZI et al. (2025), FlowSeries: Flow Analysis | Bloco 2 | Guilherme Libório | Data da leitura: 17/10/2026, Problema investigado, Objetivo do estudo, Método utilizado, Contexto, amostra ou dados, Principais resultados, Limitações, Contribuição para o nosso artigo, Comentário crítico|
| 08 | LI et al. (2021), Node2vec fraud detection | Bloco 2 | Ryan Santos | Data da leitura: 17/10/2026, Problema investigado, Objetivo do estudo, Método utilizado, Contexto, amostra ou dados, Principais resultados, Limitações, Contribuição para o nosso artigo, Comentário crítico |
| 09 | WANG et al. (2025), TempASD | Bloco 2 | Ryan Santos | Data da leitura: 17/10/2026, Problema investigado, Objetivo do estudo, Método utilizado, Contexto, amostra ou dados, Principais resultados, Limitações, Contribuição para o nosso artigo, Comentário crítico |
| 10 | ZHENG; XIAO (2024), Temporal Cycle Enumeration | Bloco 2 | Ryan Santos | Data da leitura: 17/10/2026, Problema investigado, Objetivo do estudo, Método utilizado, Contexto, amostra ou dados, Principais resultados, Limitações, Contribuição para o nosso artigo, Comentário crítico |
| 11 | WU et al. (2023), TRacer | Bloco 2 | Ryan Santos| Data da leitura: 17/10/2026, Problema investigado, Objetivo do estudo, Método utilizado, Contexto, amostra ou dados, Principais resultados, Limitações, Contribuição para o nosso artigo, Comentário crítico|
| 12 | DARWISH et al. (2025), Memetic approach | Bloco 3 | Ryan Santos | Data da leitura: 17/10/2026, Problema investigado, Objetivo do estudo, Método utilizado, Contexto, amostra ou dados, Principais resultados, Limitações, Contribuição para o nosso artigo, Comentário crítico|
| 13 | IYER et al. (2018), ASAP | Bloco 3 | Ryan Santos | Data da leitura: 17/10/2026, Problema investigado, Objetivo do estudo, Método utilizado, Contexto, amostra ou dados, Principais resultados, Limitações, Contribuição para o nosso artigo, Comentário crítico |
| 14 | CHEN et al. (2026), cuRPQ | Bloco 3 | Ryan Santos | Data da leitura: 17/10/2026, Problema investigado, Objetivo do estudo, Método utilizado, Contexto, amostra ou dados, Principais resultados, Limitações, Contribuição para o nosso artigo, Comentário crítico |


## Ficha 01/14 — CHAPNIK et al. — DARLING (2022)

### Identificação do artigo

- Referência completa: CHAPNIK, Koral; KOLCHINSKY, Ilya; SCHUSTER, Assaf. “DARLING: Data-Aware Load Shedding in Complex Event Processing Systems”. *Proceedings of the VLDB Endowment*, v. 15, n. 3, p. 541–554. 2022.
- DOI ou URL: https://doi.org/10.14778/3494124.3494137
- Base de origem: PVLDB / VLDB Endowment; também indexado pela ACM Digital Library.
- Leitor responsável: Guilherme Libório
- Data da leitura: 17/10/2026.

### Fichamento

#### Problema investigado

Sistemas de processamento de eventos complexos (CEP) precisam reconhecer padrões em fluxos contínuos dentro de limites de latência. Durante picos inesperados, a capacidade disponível pode ser insuficiente; descartar eventos alivia a carga, mas pode degradar a qualidade dos padrões detectados. Estratégias anteriores nem sempre consideram de modo adequado a importância dos dados para os resultados.

#### Objetivo do estudo

Apresentar DARLING, uma estratégia de descarte de carga orientada por dados que respeite um limite de latência e minimize a perda de qualidade dos resultados.

#### Método utilizado

O mecanismo coleta estatísticas sobre a execução e a carga do sistema, estima a utilidade dos eventos para os padrões que podem ser detectados e escolhe quais eventos descartar. O desenho considera a estrutura de avaliação dos padrões e restrições globais/locais de latência e processamento. Os autores comparam a abordagem com técnicas anteriores por meio de avaliação experimental.

#### Contexto, amostra ou dados

Avaliação experimental em um conjunto amplo de padrões e conjuntos de dados descritos como representativos de aplicações reais. O artigo usa exemplos de detecção de fraude com sequências de eventos financeiros, mas não se limita a esse domínio.

#### Principais resultados

Os experimentos reportados indicam que DARLING supera as técnicas de referência avaliadas, mantendo a latência dentro do limite definido e reduzindo a degradação da qualidade dos resultados. O artigo disponibiliza artefatos de código e dados no repositório indicado pelos autores.

#### Limitações

A eficácia depende das estatísticas, da estimativa de utilidade e da estrutura de avaliação usada pelo mecanismo. O descarte continua sendo uma aproximação: em situações de sobrecarga, alguns eventos e possíveis correspondências deixam de ser processados. Os resultados experimentais não significam que toda aplicação financeira terá o mesmo ganho.

#### Contribuição para o nosso artigo

É relevante para sistemas que monitoram transações em tempo real, pois evidencia que a resposta à sobrecarga deve considerar não só throughput e latência, mas também a importância de cada evento para o alerta de fraude. Pode fundamentar requisitos de desempenho de um sistema de monitoramento.

#### Comentário crítico

A abordagem aproxima a gestão de recursos do impacto semântico dos dados, uma vantagem em comparação com descartar eventos apenas por volume ou ordem de chegada. Para aplicar a ideia a fraude financeira, seria necessário definir quais padrões e eventos são mais críticos e validar a função de utilidade com especialistas do domínio.

#### Citação literal opcional

Não utilizada.

### Checklist

- [x] O problema, objetivo, método e resultados foram identificados.
- [x] As limitações foram registradas.
- [x] A conexão com o tema foi explicada.
- [x] A referência foi revisada.
- [x] Não foram incluídas citações literais sem página.

---

## Ficha 02/14 — SLO et al. — hSPICE (2020)

### Identificação do artigo

- Referência completa: SLO, Ahmad; BHOWMIK, Sukanya; ROTHERMEL, Kurt. “hSPICE: State-Aware Event Shedding in Complex Event Processing”. Referência bibliográfica conforme os dados presentes no PDF enviado.
- DOI ou URL: https://doi.org/10.1145/3401025.3401742
- Base de origem: ACM.
- Leitor responsável: Guilherme Libório
- Data da leitura: 17/10/2026.

### Fichamento

#### Problema investigado

Em sobrecarga, sistemas CEP precisam descartar eventos para cumprir limites de latência, mas isso reduz a qualidade dos resultados. Técnicas anteriores tendem a atribuir utilidade aos eventos ou às correspondências parciais (partial matches), sem combinar adequadamente a importância do evento, sua posição e o estado da correspondência em andamento.

#### Objetivo do estudo

Propor hSPICE, uma técnica leve de descarte que combina informação sobre os eventos de entrada com o estado das correspondências parciais, reduzindo o impacto sobre a qualidade dos resultados.

#### Método utilizado

O método estima a utilidade de um evento a partir de três elementos: tipo do evento, posição na janela e estado atual da correspondência parcial. Um modelo probabilístico prevê o valor do evento para a detecção de padrões; sob sobrecarga, o sistema descarta eventos com menor utilidade, em vez de aplicar uma regra indiferenciada.

#### Contexto, amostra ou dados

Os autores avaliam hSPICE com consultas representativas e dois conjuntos de dados reais, comparando a qualidade dos resultados com estratégias anteriores de descarte.

#### Principais resultados

Segundo o artigo, para a maioria das consultas avaliadas, hSPICE obtém melhor qualidade de resultado do que as abordagens de referência, mantendo o objetivo de latência em cenários de sobrecarga.

#### Limitações

O ganho varia por consulta; o texto não afirma superioridade em todos os cenários. A previsão de utilidade depende do modelo probabilístico e das características observadas durante a avaliação. O método também não elimina a perda de informação causada pelo descarte.

#### Contribuição para o nosso artigo

Ajuda a fundamentar a priorização de eventos financeiros em fluxos de alta frequência. Em detecção de fraude, perder um evento aparentemente comum pode quebrar uma sequência temporal relevante, então a importância do evento precisa ser avaliada no contexto da sequência.

#### Comentário crítico

A noção de estado parcial é pertinente a fraudes que se manifestam como sequências de operações. Para uso real, seria importante testar o método com padrões financeiros específicos e avaliar separadamente falsos negativos, além da latência e da qualidade agregada.

#### Citação literal opcional

Não utilizada.

### Checklist

- [x] O problema, objetivo, método e resultados foram identificados.
- [x] As limitações foram registradas.
- [x] A conexão com o tema foi explicada.
- [x] A referência foi revisada.
- [x] Não foram incluídas citações literais sem página.

---

## Ficha 03/14 — YANKOVITCH et al. — HYPERSONIC (2022)

### Identificação do artigo

- Referência completa: YANKOVITCH, Maor; KOLCHINSKY, Ilya; SCHUSTER, Assaf. “HYPERSONIC: A Hybrid Parallelization Approach for Scalable Complex Event Processing”. In: *Proceedings of the ACM SIGMOD International Conference on Management of Data* (SIGMOD ’22), 2022, pp. 1093–1107.
- DOI ou URL: https://doi.org/10.1145/3514221.3517829
- Base de origem: ACM Digital Library.
- Leitor responsável: Guilherme Libório
- Data da leitura: 17/10/2026.

### Fichamento

#### Problema investigado

O processamento de eventos complexos precisa detectar padrões arbitrários em fluxos volumosos e com baixa latência. A paralelização tradicional é limitada pelo acoplamento entre eventos e pelo estado compartilhado necessário à detecção, o que dificulta escalar o sistema com mais núcleos ou máquinas.

#### Objetivo do estudo

Desenvolver uma abordagem híbrida de paralelização que combine diferentes formas de paralelismo para melhorar a escalabilidade do CEP sem comprometer a semântica dos padrões.

#### Método utilizado

HYPERSONIC explora paralelização em diferentes níveis do processamento de padrões, combinando particionamento/execução paralela e coordenação do estado de avaliação. O artigo apresenta o desenho do sistema e compara experimentalmente sua execução com alternativas de referência em consultas de CEP.

#### Contexto, amostra ou dados

Avaliação experimental de padrões e fluxos de eventos, com foco em throughput, escalabilidade e latência. Os domínios motivadores incluem finanças on-line, fraude de cartão, sensores, saúde e IoT.

#### Principais resultados

Os autores reportam ganhos de escalabilidade e desempenho frente às alternativas comparadas, demonstrando que a estratégia híbrida aproveita paralelismo que não é capturado por uma única forma de particionamento.

#### Limitações

O desempenho depende da forma dos padrões, da distribuição dos eventos e do custo de coordenação/estado. Os resultados de benchmarks não asseguram o mesmo ganho para qualquer consulta ou infraestrutura operacional.

#### Contribuição para o nosso artigo

Oferece fundamentos arquiteturais para monitoramento financeiro em tempo real, especialmente quando muitas transações precisam ser correlacionadas por sequência e janela temporal.

#### Comentário crítico

O artigo trata principalmente de desempenho do mecanismo CEP, não da precisão de um classificador de fraude. É complementar a métodos de detecção: pode acelerar a análise de regras e sequências, mas precisa ser combinado com padrões financeiros bem definidos e validação operacional.

#### Citação literal opcional

Não utilizada.

### Checklist

- [x] O problema, objetivo, método e resultados foram identificados.
- [x] As limitações foram registradas.
- [x] A conexão com o tema foi explicada.
- [x] A referência foi revisada.
- [x] Não foram incluídas citações literais sem página.

---

## Ficha 04/14 — LUTHRA et al. — Operator as a Service / CEP LESS (2020)

### Identificação do artigo

- Referência completa: LUTHRA, Manisha; HENNIG, Sebastian; RAZAVI, Kamran; WANG, Lin; KOLDEHOFE, Boris. “Operator as a Service: Stateful Serverless Complex Event Processing”. In: *2020 IEEE International Conference on Big Data* (Big Data 2020), 2020, pp. 1964–1973.
- DOI ou URL: https://ieeexplore.ieee.org/abstract/document/9378142
- Base de origem: IEEE Xplore; preprint também disponibilizado no arXiv.
- Leitor responsável: Guilherme Libório
- Data da leitura: 17/10/2026.

### Fichamento

#### Problema investigado

Sistemas CEP tradicionais acoplam a linguagem de especificação de eventos ao runtime e às implementações de operadores. Isso exige conhecimento especializado, dificulta a portabilidade e limita a evolução dinâmica da lógica de processamento. Funções definidas pelo usuário nem sempre resolvem a questão de estado e integração.

#### Objetivo do estudo

Propor CEP LESS e a abstração “Operator as a Service”, permitindo disponibilizar operadores com estado como serviços serverless e integrá-los à execução de CEP.

#### Método utilizado

O sistema encapsula a lógica do operador em um contêiner/serviço com interface definida, desacoplando a lógica da aplicação do motor CEP. O artigo descreve arquitetura, ciclo de vida e interação com operadores, e avalia custos de execução, atualização dinâmica e processamento.

#### Contexto, amostra ou dados

A avaliação usa uma consulta CEP relacionada a transações de cartão de crédito para detecção de fraude e mede o comportamento dos operadores em diferentes configurações.

#### Principais resultados

A avaliação mostra que é possível integrar operadores stateful serverless ao processamento CEP e atualizar a lógica de operadores dinamicamente, mantendo o sistema utilizável para fluxos de eventos. Os custos dependem da configuração e do modo de execução.

#### Limitações

A separação entre operador e runtime introduz custos de comunicação, empacotamento e gerenciamento de estado. O experimento apresentado não cobre todos os tipos de operadores ou todos os ambientes serverless, portanto a generalização deve ser cautelosa.

#### Contribuição para o nosso artigo

É útil para arquiteturas modulares de detecção de fraude, nas quais regras e análises podem ser atualizadas sem reimplementar todo o pipeline. Também destaca a importância do gerenciamento de estado em sequências de transações.

#### Comentário crítico

A modularidade favorece manutenção e evolução de regras, mas um sistema de fraude deve medir o custo total do caminho crítico e garantir que atualizações não percam eventos nem corrompam o estado de uma sequência em andamento.

#### Citação literal opcional

Não utilizada.

### Checklist

- [x] O problema, objetivo, método e resultados foram identificados.
- [x] As limitações foram registradas.
- [x] A conexão com o tema foi explicada.
- [x] A referência foi revisada.
- [x] Não foram incluídas citações literais sem página.

---

## Ficha 05/14 — JIANG et al. — Efficient Densest Flow Queries (2026)

### Identificação do artigo

- Referência completa: JIANG, Jiaxin; ZHAO, Yunxiang; XU, Lyu; CHOI, Byron; HE, Bingsheng; SUN, Shixuan; CHEN, Jia. “Efficient Densest Flow Queries in Transaction Flow Networks (Complete Version)”. Preprint arXiv, 2026.
- DOI ou URL: Não informado no material disponível.
- Base de origem: Não identificada no material disponível.
- Leitor responsável: Guilherme Libório
- Data da leitura: 17/10/2026.

### Fichamento

#### Problema investigado

Redes de fluxo de transações são usadas para investigar lavagem de dinheiro, wash trading, fraude de cartão e redes de contas intermediárias. Métodos que classificam nós individualmente podem não capturar padrões globais de fluxo entre múltiplas origens e destinos, enquanto consultas de fluxo densas são computacionalmente caras.

#### Objetivo do estudo

Formular a consulta *S-T Densest Flow* (STDF) e desenvolver técnicas para respondê-la de forma eficiente em redes de transações.

#### Método utilizado

O artigo formaliza uma consulta de fluxo denso entre conjuntos de fontes e destinos e apresenta uma transformação em duas etapas, com mecanismo baseado em arrependimento/regret para reduzir o espaço de busca, seguido de avaliação da consulta. O estudo inclui análise algorítmica e experimentos de desempenho em redes de transações e conjuntos sintéticos/industriais descritos no PDF.

#### Contexto, amostra ou dados

O trabalho é motivado por uma aplicação de pagamentos digitais do colaborador Grab e também usa conjuntos sintéticos IBM para avaliar eficiência e comportamento das consultas. O foco é a estrutura global dos fluxos, não apenas atributos de uma transação isolada.

#### Principais resultados

Os autores reportam acelerações de até três ordens de magnitude em consultas em comparação com métodos de referência em determinadas configurações. O ganho varia conforme a consulta, a densidade e os parâmetros da rede.

#### Limitações

É um trabalho centrado em consulta/descoberta de sub-redes densas; não constitui, por si só, um classificador validado de fraude. O desempenho depende da formulação da consulta e das características do grafo. A versão recebida é um preprint completo, então não se deve atribuir a ele uma publicação em periódico sem confirmação externa específica.

#### Contribuição para o nosso artigo

Oferece uma formulação para encontrar grupos de transações fortemente conectados por fluxos financeiros, potencialmente úteis para priorizar investigações de fraude ou lavagem de dinheiro.

#### Comentário crítico

A densidade do fluxo é um indício estrutural, não prova de ilegalidade. A utilização prática exige combinar a saída com contexto temporal, atributos de transação, regras regulatórias e revisão de analistas para reduzir falsos positivos.

#### Citação literal opcional

Não utilizada.

### Checklist

- [x] O problema, objetivo, método e resultados foram identificados.
- [x] As limitações foram registradas.
- [x] A conexão com o tema foi explicada.
- [x] A referência foi revisada.
- [x] Não foram incluídas citações literais sem página.

---

## Ficha 06/14 — CAPOZZI et al. — WeirdFlows (2025)

### Identificação do artigo

- Referência completa: CAPOZZI, Arthur; VILELLA, Salvatore; MONCALVO, Dario; FORNASIERO, Marco; RICCI, Valeria; RONCHIADIN, Silvia; RUFFO, Giancarlo. “WeirdFlows: Anomaly Detection in Financial Transaction Flows”. In: *ITADATA2024: The 3rd Italian Conference on Big Data and Data Science*. Preprint arXiv:2503.15896, versão de 1º de abril de 2025.
- DOI ou URL: Não informado no material disponível.
- Base de origem: Não identificada no material disponível.
- Leitor responsável: Guilherme Libório
- Data da leitura: 17/10/2026.

### Fichamento

#### Problema investigado

Investigações de crimes financeiros enfrentam falta de dados rotulados, padrões criminosos que mudam com o tempo e necessidade de explicabilidade para sustentar relatórios formais. Métodos baseados em padrões previamente definidos podem deixar escapar estratégias novas.

#### Objetivo do estudo

Apresentar WeirdFlows, um pipeline de busca top-down em redes temporais de transações para localizar fluxos e agentes potencialmente suspeitos sem exigir uma lista prévia de padrões fraudulentos ou um conjunto de treino rotulado.

#### Método utilizado

A partir de dados de transações, o sistema cria redes direcionadas em diferentes níveis de granularidade (por exemplo, país, BIC ou conta) e agrega transferências em intervalos temporais distintos. Um algoritmo calcula caminhos/fluxos entre nós selecionados; analistas exploram os caminhos e comparam variações temporais para detectar padrões incomuns e estimar valores movimentados através de intermediários.

#### Contexto, amostra ou dados

O artigo avalia o método em dados fornecidos pelo banco Intesa Sanpaolo, com 80 milhões de transações transfronteiriças ao longo de 15 meses. O caso de uso concentra-se em possíveis tentativas de contornar sanções econômicas europeias após fevereiro de 2022.

#### Principais resultados

O estudo relata escalabilidade para milhões de transações e identificação de fluxos/atores suspeitos, com achados corroborados por especialistas de AFC do banco. A interpretabilidade é apresentada como parte central do valor do método.

#### Limitações

A abordagem é exploratória e depende da escolha de um ponto inicial e da granularidade da rede pelo analista. O resultado identifica anomalias suspeitas, não determina automaticamente que houve crime. A validação é feita em contexto institucional específico, e a generalização a outras instituições exige avaliação adicional.

#### Contribuição para o nosso artigo

É diretamente pertinente à detecção de fraude financeira baseada em redes, sobretudo quando não há rótulos confiáveis e é necessário rastrear transações por intermediários ao longo do tempo.

#### Comentário crítico

A combinação de busca em rede e interpretação humana é valiosa para auditoria, mas a análise depende de decisões do investigador. Uma implementação operacional deveria registrar critérios de seleção, limiares e justificativas, além de medir falsos positivos e falsos negativos em casos confirmados.

#### Citação literal opcional

Não utilizada.

### Checklist

- [x] O problema, objetivo, método e resultados foram identificados.
- [x] As limitações foram registradas.
- [x] A conexão com o tema foi explicada.
- [x] A referência foi revisada.
- [x] Não foram incluídas citações literais sem página.

---

## Ficha 07/14 — CAPOZZI et al. — FlowSeries (2025)

### Identificação do artigo

- Referência completa: CAPOZZI, Arthur; VILELLA, Salvatore; MONCALVO, Dario; FORNASIERO, Marco; RICCI, Valeria; RONCHIADIN, Silvia; RUFFO, Giancarlo. “FlowSeries: Flow Analysis on Financial Networks”. *Applied Network Science*, v. 10, art. 28, 2025.
- DOI ou URL: https://doi.org/10.1007/s41109-025-00711-0
- Base de origem: Springer Nature.
- Leitor responsável: Guilherme Libório
- Data da leitura: 17/10/2026.

### Fichamento

#### Problema investigado

As investigações de crimes financeiros precisam de métodos interpretáveis e enfrentam escassez de dados rotulados. Padrões de movimentação ilícita são complexos e evoluem para escapar de regras fixas; sistemas totalmente automáticos e opacos são difíceis de justificar perante autoridades.

#### Objetivo do estudo

Apresentar FlowSeries, uma metodologia top-down de exploração de fluxos financeiros que ajuda analistas de AFC a identificar entidades suspeitas e padrões anômalos em redes de transações.

#### Método utilizado

A ferramenta permite explorar fluxos a partir de um ponto inicial, refinando a análise de níveis agregados (como países) para entidades mais específicas, como bancos/BICs e transações. O processo combina análise de redes, exploração iterativa e interpretação especializada; não é apresentado como detector autônomo do tipo caixa-preta.

#### Contexto, amostra ou dados

A avaliação usa dados fornecidos pelo Intesa Sanpaolo, com cerca de 80 milhões de transações, e inclui casos de uso investigativos. O artigo relata integração do método ao fluxo de trabalho de uma unidade de AFC.

#### Principais resultados

FlowSeries auxilia na identificação e rastreamento de fluxos suspeitos e na descoberta de relações que podem indicar atividade ilícita. O valor central relatado é apoiar a investigação e tornar os padrões visíveis e interpretáveis, e não substituir a decisão do analista.

#### Limitações

É necessário que o analista escolha o ponto de partida e interprete os resultados. A ausência de rótulos e a confidencialidade dos dados financeiros dificultam a validação quantitativa padronizada. Os autores reconhecem incerteza na interpretação dos padrões encontrados.

#### Contribuição para o nosso artigo

Complementa métodos automáticos de classificação com uma abordagem explicável para investigar redes e fluxos de transações, permitindo que alertas sejam rastreados até relações financeiras concretas.

#### Comentário crítico

O papel do especialista aumenta a interpretabilidade, mas pode introduzir variabilidade entre investigadores. Uma avaliação adicional poderia medir a concordância entre analistas, o tempo de investigação e a taxa de confirmação de alertas.

#### Citação literal opcional

Não utilizada.

### Checklist

- [x] O problema, objetivo, método e resultados foram identificados.
- [x] As limitações foram registradas.
- [x] A conexão com o tema foi explicada.
- [x] A referência foi revisada.
- [x] Não foram incluídas citações literais sem página.

---

## Ficha 08/14 — ZHOU et al. — Node2vec para detecção de fraude (2021)

### Identificação do artigo

- Referência completa: ZHOU, Hangjun; SUN, Guang; FU, Sha; WANG, Linli; HU, Juan; GAO, Ying. “Internet Financial Fraud Detection Based on a Distributed Big Data Approach With Node2vec”. *IEEE Access*, v. 9, pp. 23145–23156, 2021.
- DOI ou URL: https://doi.org/10.1109/ACCESS.2021.3062467
- Base de origem: IEEE Xplore.
- Leitor responsável: Ryan Santos
- Data da leitura: 17/10/2026.

### Fichamento

#### Problema investigado

O crescimento dos dados financeiros on-line dificulta a detecção de fraude por sistemas baseados apenas em regras ou atributos tradicionais. Os fraudadores também alteram suas estratégias, e a estrutura de relações entre contas pode conter informação importante que não aparece na análise isolada de cada registro.

#### Objetivo do estudo

Desenvolver uma abordagem distribuída de big data para detectar fraude financeira na Internet, usando Node2vec para representar características topológicas de uma rede financeira e uma rede neural profunda para classificar os exemplos.

#### Método utilizado

O método constrói um grafo de relações financeiras, aprende embeddings vetoriais de baixa dimensão com Node2vec e usa esses vetores na classificação por rede neural. O processamento distribuído é implementado com Apache Spark GraphX e Hadoop, visando lidar com conjuntos de dados de grande porte.

#### Contexto, amostra ou dados

O artigo apresenta experimentos em conjuntos de dados de fraude descritos pelos autores e compara métricas de classificação e eficiência com abordagens de referência. A ficha não atribui nomes ou dimensões adicionais aos conjuntos além do que foi confirmado no texto extraído.

#### Principais resultados

Os autores reportam melhoria de precisão, recall, F1 e F2, além de maior eficiência de detecção, em comparação com os métodos usados como referência nos experimentos.

#### Limitações

A qualidade depende da construção do grafo, da representatividade dos dados e da escolha dos parâmetros de embedding e classificação. Embeddings podem dificultar a explicação direta de por que uma transação foi sinalizada. O desempenho de benchmark não garante a mesma qualidade diante de novas formas de fraude ou mudança de distribuição.

#### Contribuição para o nosso artigo

Fornece um exemplo de integração entre representação de grafos, aprendizado de máquina e infraestrutura distribuída para detectar fraude financeira em escala.

#### Comentário crítico

É importante comparar a abordagem com modelos que usem atributos transacionais e temporais, e avaliar não só métricas agregadas, mas também custo computacional, desbalanceamento de classes e explicabilidade dos alertas.

#### Citação literal opcional

Não utilizada.

### Checklist

- [x] O problema, objetivo, método e resultados foram identificados.
- [x] As limitações foram registradas.
- [x] A conexão com o tema foi explicada.
- [x] A referência foi revisada.
- [x] Não foram incluídas citações literais sem página.

---

## Ficha 09/14 — HAN et al. — TempASD (2025)

### Identificação do artigo

- Referência completa: HAN, Xiaolin; ZHANG, Yikun; MA, Chenhao; et al. “TempASD: Temporal Anomalous Subgraph Discovery in Large-Scale Dynamic Financial Networks”. In: *Proceedings of the ACM SIGKDD Conference on Knowledge Discovery and Data Mining* (KDD ’25), 2025.
- DOI ou URL: https://doi.org/10.1145/3711896.3737149
- Base de origem: ACM Digital Library.
- Leitor responsável: Ryan Santos
- Data da leitura: 17/10/2026.

### Fichamento

#### Problema investigado

Em redes financeiras dinâmicas, fraudes podem surgir como subgrafos que são simultaneamente incomuns em estrutura e comportamento temporal. Métodos estáticos ignoram a evolução temporal; abordagens temporais podem não distinguir adequadamente diferenças entre vértices ou padrões de referência.

#### Objetivo do estudo

Detectar subgrafos anômalos em grandes redes financeiras dinâmicas, explorando padrões temporais e contrastes entre vértices para encontrar estruturas que se desviem do comportamento esperado.

#### Método utilizado

TempASD formula a descoberta de subgrafos anômalos com uma função de anomalia que considera características temporais e estruturais. O método procura padrões contrastantes em vértices e utiliza uma avaliação experimental extensa contra 13 métodos concorrentes. O artigo inclui análise de efetividade, eficiência e ablação dos componentes.

#### Contexto, amostra ou dados

O PDF descreve avaliações em redes financeiras dinâmicas, incluindo o conjunto ETH-Jan-18, e experimentos de escalabilidade. O artigo também compara o método com abordagens de descoberta de subgrafos densos e métodos de referência.

#### Principais resultados

Os autores reportam que TempASD supera concorrentes em métricas de efetividade e mantém escalabilidade para redes grandes. O artigo apresenta evidências experimentais, incluindo estudo de ablação, para mostrar a contribuição dos componentes temporais e contrastivos.

#### Limitações

Os resultados dependem da definição de anomalia e da disponibilidade de informação temporal adequada. A avaliação usa conjuntos específicos e uma definição operacional de subgrafo anômalo; padrões detectados são candidatos à investigação, não provas automáticas de fraude. Algumas comparações são limitadas pelas diferenças entre os objetivos dos métodos concorrentes.

#### Contribuição para o nosso artigo

É relevante para detectar grupos de contas/transações com comportamento temporal anômalo, em vez de analisar transações de forma isolada. Pode complementar detecção por ciclos, caminhos ou classificadores.

#### Comentário crítico

A descoberta de subgrafos pode revelar padrões coletivos difíceis de capturar por modelos por transação, mas é necessário traduzir a pontuação de anomalia em explicações compreensíveis para investigadores e validar os achados com casos rotulados ou análise especializada.

#### Citação literal opcional

Não utilizada.

### Checklist

- [x] O problema, objetivo, método e resultados foram identificados.
- [x] As limitações foram registradas.
- [x] A conexão com o tema foi explicada.
- [x] A referência foi revisada.
- [x] Não foram incluídas citações literais sem página.

---

## Ficha 10/14 — ZHENG et al. — Temporal Cycle Enumeration (publicação 2025; DOI 2024)

### Identificação do artigo

- Referência completa: ZHENG, Lixiao; XIAO, Jipeng; MA, Shuai; CHEN, Zuxi; LUO, Xiangyu. “Temporal Cycle Enumeration for Detecting Financial Fraud”. *Data Intelligence*, v. 7, pp. 567–590, art. 2025r19, 2025.
- DOI ou URL: https://doi.org/10.3724/2096-7004.di.2024.0058
- Base de origem: Data Intelligence / SciEngine.
- Leitor responsável: Ryan Santos
- Data da leitura: 17/10/2026.

### Fichamento

#### Problema investigado

Alguns esquemas de fraude movimentam dinheiro por uma sequência de contas até que ele retorne à conta de origem. A enumeração convencional de ciclos pode produzir muito trabalho redundante e, em alguns casos, depende de limites de comprimento ou janela temporal inadequados ao cenário financeiro.

#### Objetivo do estudo

Desenvolver um método eficiente para enumerar ciclos temporais em grafos de transações e usar esses ciclos como sinais de possíveis fraudes financeiras.

#### Método utilizado

O sistema pré-processa os dados e constrói um grafo de transações, divide-o em componentes fortemente conexos e enumera ciclos temporais em paralelo, distribuindo componentes entre múltiplas threads. O trabalho estende a abordagem de Johnson para enumeração de ciclos e explora concorrência e restrições temporais adequadas à aplicação.

#### Contexto, amostra ou dados

Os experimentos são descritos com conjuntos Codecraft1, Codecraft2, Transactions e FinalTrans, avaliando desempenho e consumo de memória sob diferentes configurações de concorrência.

#### Principais resultados

O artigo relata que o método paralelo melhora a eficiência da enumeração de ciclos em relação às alternativas comparadas e pode processar dados de transações em larga escala com maior aproveitamento de múltiplos núcleos.

#### Limitações

A utilidade depende de fraudes que gerem ciclos temporais detectáveis; outros esquemas de lavagem ou fraude podem não retornar fundos à origem. A enumeração de ciclos pode continuar custosa quando há muitos ciclos ou grafos densos, e a presença de um ciclo não prova por si só atividade ilícita.

#### Contribuição para o nosso artigo

Oferece uma técnica específica para reconhecer fluxos circulares e sequências temporais potencialmente suspeitas, complementando métodos de detecção de caminhos e subgrafos anômalos.

#### Comentário crítico

O trabalho é adequado quando o padrão investigado tem forma cíclica, mas deve ser combinado com valores, intervalos temporais, relações entre contas e contexto do negócio. A ficha adota 2025 como ano da publicação do volume, preservando 2024 apenas no identificador DOI.

#### Citação literal opcional

Não utilizada.

### Checklist

- [x] O problema, objetivo, método e resultados foram identificados.
- [x] As limitações foram registradas.
- [x] A conexão com o tema foi explicada.
- [x] A referência foi revisada.
- [x] Não foram incluídas citações literais sem página.

---

## Ficha 11/14 — WU et al. — TRacer (2023)

### Identificação do artigo

- Referência completa: WU, Zhiying; WU, Jiajing; ZHENG, Zibin; LIU, Jieli. “TRacer: Scalable Graph-based Transaction Tracing for Account-based Blockchain Trading Systems”. *IEEE Transactions on Information Forensics and Security*, v. 18, pp. 2541–2555, 2023.
- DOI ou URL: Não informado no material disponível.
- Base de origem: IEEE Xplore.
- Leitor responsável: Ryan Santos
- Data da leitura: 17/10/2026.

### Fichamento

#### Problema investigado

Sistemas de blockchain baseados em contas facilitam o rastreamento de fundos, mas o grande volume de transações e a complexidade dos caminhos tornam difícil identificar e priorizar trajetórias suspeitas. Abordagens baseadas apenas em heurísticas ou análise de taint têm limitações de escalabilidade, generalidade e priorização.

#### Objetivo do estudo

Apresentar TRacer, um método escalável de rastreamento de transações em sistemas de negociação blockchain account-based, para apoiar a análise de fluxos suspeitos e priorizar caminhos de investigação.

#### Método utilizado

O trabalho modela transações como grafo e utiliza uma estratégia de rastreamento e ranqueamento de caminhos/direções de movimentação, combinando informação estrutural e heurísticas para priorizar a análise. O artigo apresenta análise teórica e avaliação experimental, incluindo cenários de rastreamento de fundos ilícitos e de alerta de risco.

#### Contexto, amostra ou dados

O estudo se concentra em sistemas blockchain account-based e em tarefas de rastreamento de transações, com experimentos que comparam a eficácia e a escalabilidade com métodos anteriores. O domínio é blockchain, não a totalidade dos pagamentos bancários tradicionais.

#### Principais resultados

Os autores reportam que TRacer melhora a escalabilidade do rastreamento e a priorização de trajetórias suspeitas em comparação com abordagens de referência. O artigo argumenta que o ranqueamento ajuda a concentrar recursos de auditoria nos caminhos mais promissores.

#### Limitações

O rastreamento depende das informações e heurísticas disponíveis no grafo; a atribuição de suspeição não demonstra intenção criminosa. Resultados de blockchains account-based não devem ser transferidos diretamente para sistemas bancários sem adaptação. Mudanças nas estratégias de ocultação também podem afetar as heurísticas.

#### Contribuição para o nosso artigo

É útil como referência para rastreamento de transações por grafos, análise de caminhos e priorização de investigação em redes financeiras digitais.

#### Comentário crítico

O foco em priorizar caminhos é operacionalmente valioso, mas a avaliação deve separar desempenho computacional da qualidade investigativa. Para adoção, seria importante avaliar explicabilidade, robustez a estratégias novas e desempenho em grafos com características diferentes.

#### Citação literal opcional

Não utilizada.

### Checklist

- [x] O problema, objetivo, método e resultados foram identificados.
- [x] As limitações foram registradas.
- [x] A conexão com o tema foi explicada.
- [x] A referência foi revisada.
- [x] Não foram incluídas citações literais sem página.

---

## Ficha 12/14 — DARWISH et al. — Intelligent Memetic Approach (2025)

### Identificação do artigo

- Referência completa: DARWISH, Saad M.; SALAMA, Amr Ibrahim; ELZOGHABI, Adel A.; EL-SHOAFY, Noha A. “An Intelligent Memetic Approach to Detect Online Fraud for Distributed FinTech Environments”. *Electronic Commerce Research*, 2025.
- DOI ou URL: https://doi.org/10.1007/s10660-025-10050-y
- Base de origem: Springer Nature.
- Leitor responsável: Ryan Santos
- Data da leitura: 17/10/2026.

### Fichamento

#### Problema investigado

A detecção de fraude em fintech enfrenta dados desbalanceados, mudanças rápidas no comportamento dos fraudadores e dificuldade dos modelos tradicionais em reconhecer a classe minoritária de transações fraudulentas. O monitoramento também precisa lidar com ameaças ao nível da rede e operar em ambientes distribuídos.

#### Objetivo do estudo

Propor um método híbrido memético-ABC para melhorar a detecção de fraude on-line, equilibrando dados desbalanceados, construindo perfis comportamentais e integrando alertas de anomalia transacional com detecção distribuída de intrusões.

#### Método utilizado

O framework combina Artificial Bee Colony (ABC) para exploração global e refinamento memético local para gerar amostras sintéticas da classe minoritária, orientadas por importância de atributos. Um pipeline em múltiplos níveis usa detecção de anomalias, agrupamento de perfis de traders e classificação/decisão; a arquitetura é estendida a um Distributed Intrusion Detection System (DIDS) para correlacionar anomalias transacionais e ameaças de rede.

#### Contexto, amostra ou dados

O artigo apresenta avaliação experimental de métodos de classificação e de balanceamento de classes em contexto de fraude on-line/fintech. A ficha não atribui nomes, dimensões ou proporções específicas aos conjuntos de dados sem os reproduzir integralmente do texto/tabelas.

#### Principais resultados

Os autores reportam aproximadamente 10% de melhoria na acurácia em relação a técnicas de referência. Também argumentam que a abordagem hierárquica pode reduzir falsos positivos ao refinar gradualmente os casos suspeitos.

#### Limitações

Os próprios autores apontam como trabalho futuro melhorar eficiência, adaptabilidade e generalização para conjuntos grandes e dinâmicos, além de otimizar parâmetros do ABC. A acurácia agregada, isoladamente, pode ser enganosa em dados desbalanceados; são necessárias métricas por classe e validação externa. A geração de amostras sintéticas também pode introduzir artefatos se não for validada.

#### Contribuição para o nosso artigo

É uma referência direta sobre detecção de fraude em fintech com dados desbalanceados, perfis de comportamento e arquitetura distribuída. Complementa métodos de grafos ao tratar classificação e detecção de anomalias.

#### Comentário crítico

A combinação de amostragem, classificação e alertas de rede é abrangente, mas a alegação de melhoria de acurácia precisa ser interpretada junto de precisão, recall, F1, custo computacional e taxas de falso negativo. A generalização deve ser testada em instituições e períodos distintos.

#### Citação literal opcional

Não utilizada.

### Checklist

- [x] O problema, objetivo, método e resultados foram identificados.
- [x] As limitações foram registradas.
- [x] A conexão com o tema foi explicada.
- [x] A referência foi revisada.
- [x] Não foram incluídas citações literais sem página.

---

## Ficha 13/14 — IYER et al. — ASAP (2018)

### Identificação do artigo

- Referência completa: IYER, Anand Padmanabha; LIU, Zaoxing; JIN, Xin; VENKATARAMAN, Shivaram; BRAVERMAN, Vladimir; STOICA, Ion. “ASAP: Fast, Approximate Graph Pattern Mining at Scale”. In: *13th USENIX Symposium on Operating Systems Design and Implementation* (OSDI ’18), 2018, pp. 745–761.
- DOI ou URL: Não informado no material disponível.
- Base de origem: USENIX (anais de conferência; não ACM Digital Library como indicado implicitamente no template).
- Leitor responsável: Ryan Santos
- Data da leitura: 17/10/2026.

### Fichamento

#### Problema investigado

A mineração exata de padrões em grafos grandes pode exigir muito tempo e memória. Sistemas existentes frequentemente focam padrões específicos ou não oferecem uma forma geral de controlar o compromisso entre precisão e tempo de resposta.

#### Objetivo do estudo

Apresentar ASAP, um mecanismo distribuído e baseado em amostragem para mineração aproximada de padrões gerais em grafos, permitindo ajustar o equilíbrio entre precisão e latência.

#### Método utilizado

ASAP estende ideias de aproximação e amostragem para padrões gerais em ambiente distribuído. O sistema usa uma estrutura de construção chamada ELP para permitir que o usuário controle o trade-off entre precisão do resultado e tempo de execução. O artigo descreve a implementação sobre Apache Spark e compara o sistema com soluções exatas e outras abordagens.

#### Contexto, amostra ou dados

Avaliação em grafos de diferentes tamanhos e tarefas de mineração de padrões, incluindo contagem de triângulos e outros padrões estruturais. Os experimentos analisam tempo, escalabilidade e erro de aproximação.

#### Principais resultados

Os autores relatam que ASAP supera soluções exatas de referência por mais de uma ordem de magnitude em determinados cenários e escala para grafos grandes, mantendo baixo uso relativo de recursos. O benefício é obtido aceitando aproximação controlada.

#### Limitações

Como é um método aproximado, os resultados têm erro e dependem da amostragem e dos parâmetros escolhidos. A vantagem de desempenho varia com o padrão e a estrutura do grafo. A aproximação pode não ser aceitável em decisões regulatórias que exijam exatidão ou rastreabilidade completa.

#### Contribuição para o nosso artigo

Fornece uma base técnica para análise exploratória de grafos financeiros em grande escala quando consultas exatas são caras. Pode ajudar a estimar rapidamente estruturas ou priorizar análises mais detalhadas.

#### Comentário crítico

A aproximação é útil para triagem e exploração, mas os resultados que embasam uma decisão de fraude podem exigir verificação exata posterior. A arquitetura deveria expor o erro estimado e preservar a reprodutibilidade da amostragem.

#### Citação literal opcional

Não utilizada.

### Checklist

- [x] O problema, objetivo, método e resultados foram identificados.
- [x] As limitações foram registradas.
- [x] A conexão com o tema foi explicada.
- [x] A referência foi revisada.
- [x] Não foram incluídas citações literais sem página.

---

## Ficha 14/14 — PARK et al. — cuRPQ (2026)

### Identificação do artigo

- Referência completa: PARK, Sungwoo; KIM, Seohyeon; KIM, Min-Soo. “cuRPQ: A High-Performance GPU-Based Framework for Processing Regular and Conjunctive Regular Path Queries”. *Proceedings of the ACM on Management of Data*, v. 4, n. 3, artigo 156, SIGMOD 2026.
- DOI ou URL: https://doi.org/10.1145/3802033
- Base de origem: ACM Digital Library.
- Leitor responsável: Ryan Santos
- Data da leitura: 17/10/2026.

### Fichamento

#### Problema investigado

Consultas de caminhos regulares (RPQs) e consultas de caminhos regulares conjuntivas (CRPQs) são importantes para análise de alcançabilidade e relações em grafos, mas podem ser muito caras. Abordagens baseadas em álgebra podem materializar resultados intermediários enormes, enquanto soluções em GPU enfrentam limitações de memória, sincronização e exploração de caminhos.

#### Objetivo do estudo

Desenvolver cuRPQ, uma estrutura otimizada para GPU que processe RPQs e CRPQs com alto desempenho, sem comprometer a correção da exploração de caminhos.

#### Método utilizado

O sistema propõe algoritmo de travessia, gerenciamento eficiente do conjunto de vértices visitados e exploração concorrente separada da materialização dos resultados. A exploração ocorre na GPU, enquanto a materialização é desacoplada para reduzir migração de dados e sincronização. A avaliação compara cuRPQ com métodos algébricos e automata-based.

#### Contexto, amostra ou dados

Os experimentos incluem consultas em grafos de benchmark, como LDBC Social Network Benchmark e StackOverflow, com consultas de caminhos regulares e conjuntivas. O artigo avalia escalabilidade e consultas que produzem quantidades muito grandes de resultados.

#### Principais resultados

O artigo relata que cuRPQ processa consultas com trilhões de resultados e atinge aceleração de até 4.945× frente a métodos algébricos e 269× frente a métodos baseados em autômatos, nos cenários avaliados.

#### Limitações

O método foi projetado para RPQs/CRPQs; não é um detector de fraude pronto para uso. O desempenho depende da consulta, do grafo e da configuração de hardware. Extensões para restrições adicionais de caminho são apresentadas como possibilidades futuras, não como funcionalidades já avaliadas no trabalho.

#### Contribuição para o nosso artigo

Pode apoiar a infraestrutura de análise de redes transacionais, especialmente consultas que procuram relações e caminhos com restrições de sequência. É uma contribuição de processamento de grafos, não de modelagem direta de fraude.

#### Comentário crítico

Os ganhos de GPU são expressivos, mas sua aplicação a fraude financeira exige traduzir regras de negócio em consultas RPQ/CRPQ e avaliar custo de preparação, memória, atualizações do grafo e interpretabilidade dos caminhos encontrados.

#### Citação literal opcional

Não utilizada.

### Checklist

- [x] O problema, objetivo, método e resultados foram identificados.
- [x] As limitações foram registradas.
- [x] A conexão com o tema foi explicada.
- [x] A referência foi revisada.
- [x] Não foram incluídas citações literais sem página.

