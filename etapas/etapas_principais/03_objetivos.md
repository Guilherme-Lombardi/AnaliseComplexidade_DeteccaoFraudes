# Etapa 3 Objetivo geral e objetivos específicos

## Solicitação

Defina o objetivo geral e os objetivos específicos do artigo.

## Problema de pesquisa

Segundo a literatura revisada, como se comparam a complexidade assintótica no pior caso e os tempos de resposta reportados para a abordagem direta em grafos (DFS/Kosaraju) e para uma arquitetura com pré-filtragem por DFA/CEP no contexto da detecção de fraudes financeiras em tempo real, e sob quais hipóteses a redução de carga pode afetar esses custos?

## Objetivo geral

Analisar, com base na literatura selecionada na etapa (b), a complexidade assintótica e as métricas de desempenho reportadas para a abordagem direta em grafos (DFS/Kosaraju) e para uma arquitetura com pré-filtragem por DFA/CEP na detecção de fraudes financeiras em tempo real, identificando as hipóteses, os custos e as limitações de cada abordagem.

## Objetivos específicos

1. Mapear os fundamentos teóricos dos algoritmos de travessia em grafos (DFS e Kosaraju) aplicados à identificação de ciclos e Componentes Fortemente Conectados (SCC) em redes de transações financeiras.
2. Conceituar a modelagem de Autômatos Finitos Determinísticos (DFA) e de Processamento de Eventos Complexos (CEP) para reconhecimento de padrões e pré-filtragem em fluxos de dados contínuos.
3. Comparar teoricamente, a partir das fontes da etapa (b), as ordens de complexidade assintótica no pior caso entre o pipeline tradicional de varredura em grafos e a arquitetura híbrida com pré-filtragem DFA/CEP, incluindo o custo do pré-filtro e as hipóteses sobre o tamanho dos grafos processados.
4. Comparar documentalmente os tempos de resposta (latência) e a vazão (throughput) reportados nas fontes e avaliar, exclusivamente a partir dos resultados publicados, o impacto da pré-filtragem na taxa de retenção de eventos e no uso de recursos computacionais, identificando fontes, condições de avaliação, limitações de comparação e lacunas de evidência.

> ⚠️ **REVISAR:** (c) tem **5** objetivos específicos (2 conceituais e 3 técnicos), e este template aceita 3 a 4. Mantive os 2 conceituais (itens 1 e 2), o 1º técnico (item 3) e **fundi o 2º e o 3º técnicos no item 4**. Se preferirem manter os 5, confirmem com a orientadora.
> ⚠️ **REVISAR:** o assunto 5 de (c) fala em impacto da redução de carga (load shedding e poda) nas taxas de **falsos positivos e falsos negativos**, mas nenhum objetivo específico de (c) cobre isso (eles falam em retenção de eventos e recursos). Decidam se incluem ou se removem o assunto 5.

## Quadro de alinhamento

| Elemento | Texto |
|---|---|
| Problema | Segundo a literatura revisada, como se comparam a complexidade assintótica no pior caso e os tempos de resposta reportados para a abordagem direta em grafos (DFS/Kosaraju) e para uma arquitetura com pré-filtragem por DFA/CEP no contexto da detecção de fraudes financeiras em tempo real? |
| Objetivo geral |Analisar, com base na literatura selecionada na etapa (b), a complexidade assintótica e as métricas de desempenho reportadas para a abordagem direta em grafos (DFS/Kosaraju) e para uma arquitetura com pré-filtragem por DFA/CEP na detecção de fraudes financeiras em tempo real, identificando as hipóteses, os custos e as limitações de cada abordagem. |
| Resultado esperado | Uma análise comparativa teórica e documental que apresente (i) os fundamentos de DFS/Kosaraju e de DFA/CEP, (ii) a comparação das ordens de complexidade assintótica no pior caso entre o pipeline direto e o híbrido, (iii) a síntese dos tempos de resposta, vazão e consumo de memória reportados nos artigos revisados, com suas condições e limitações, (iv) o impacto da redução de carga reportado na literatura, incluindo as taxas de falsos positivos e falsos negativos, e (v) a distinção entre redução do volume processado e mudança da ordem assintótica. |

> ⚠️ **PENDENTE:** (c) não tem um campo "resultado esperado". O texto acima foi montado a partir da estrutura do artigo (c, seção 2.3) e do escopo de (a). Confirmem ou reescrevam.

## Produto da etapa

Um objetivo geral e de três a quatro objetivos específicos.

## Checklist

- [x] Os objetivos começam com verbos no infinitivo.
- [x] O objetivo geral responde ao problema.
- [x] Os objetivos específicos detalham o objetivo geral.
- [x] Os objetivos são compatíveis com uma revisão bibliográfica.
