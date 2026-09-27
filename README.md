# Detecção de Fraudes em Transações Financeiras via Arquiteturas Híbridas (DFA/CEP + Grafos) — Artigo Científico

> Repositório de documentação acadêmica e escrita da Iniciação Científica / Artigo Acadêmico focado na análise comparativa entre travessia em grafos e pré-filtragem por Autômatos Finitos Determinísticos.

---

## 👥 Integrantes atuais

* **Guilherme Lombardi**
* **Caio Winkler Marangoni**
* **Guilherme Liborio Camargo**
* **Ryan dos Santos Veloso**

Quando Julia Emily Leonardo Barbosa saiu do grupo, eu, Caio Winkler Marangoni, dei continuidade às partes que ficaram em aberto e assumi as pendências correspondentes. Preservei nos documentos as contribuições históricas declaradas, sem redistribuir retroativamente horas ou percentuais.

---

## 📌 Resumo do Projeto

Este repositório reúne a documentação acadêmica de uma revisão da literatura sobre complexidade e desempenho de pipelines para detecção de fraudes financeiras em tempo real. O recorte das etapas (a)–(c) é a comparação teórica e documental, sem execução própria de experimentos.

A pesquisa investiga as condições em que uma camada de pré-filtragem **DFA/CEP** pode reduzir o volume de eventos encaminhado a algoritmos de grafos, como DFS e Kosaraju para identificação de componentes fortemente conectados (SCC). A análise distingue a redução do volume processado de uma mudança da ordem assintótica e utiliza os resultados reportados nas fontes, sem pressupor melhoria no pior caso.

---

## 🎯 Objetivos da Pesquisa

### Objetivo Geral
Comparar, com base na literatura selecionada na etapa (b), a complexidade assintótica e os tempos de resposta reportados para DFS/Kosaraju e para pipelines com pré-filtragem DFA/CEP, no contexto de detecção de fraudes bancárias em tempo real.

### Objetivos Específicos
* **Mapeamento Teórico:** Revisar e estruturar o estado da arte referente a algoritmos de busca em grafos (DFS/Kosaraju) para identificação de SCCs em redes financeiras.
* **Modelagem de Autômatos:** Conceituar a pré-filtragem via DFA/CEP para reconhecimento de padrões temporais em fluxos contínuos.
* **Análise de Complexidade:** Comparar teoricamente as ordens de complexidade assintótica entre o modelo tradicional e o modelo híbrido.
* **Comparação Documental:** Analisar métricas de latência, *throughput* e consumo de memória reportadas pelos artigos revisados, considerando as condições de cada estudo.
* **Avaliação de Impacto:** Discutir, a partir dos resultados publicados, as taxas de retenção de eventos e o efeito do descarte preliminar no desempenho global, incluindo limites de comparação entre as fontes.

---

## 📚 Metodologia e Normatização

* **Revisão Bibliográfica:** Fluxo de seleção documentado com referência ao **PRISMA 2020**: 721 resultados iniciais declarados, 14 artigos no conjunto definitivo e 2 teses em fundamentação teórica complementar. A documentação individual de busca e triagem ainda está pendente.
* **Normatização Bibliográfica:** **ABNT NBR 6023** para citações e referências bibliográficas.
* **Ferramenta de Compilação:** LaTeX / Overleaf (ABNTex2).

---

## 📎 Evidências individuais pendentes

**Status do ajuste 4: Em andamento.** Reuni no [registro de evidências individuais](evidencias_individuais/README.md) os registros dos arquivos atuais e das versões antigas, junto das pendências por pessoa. Recuperei 36 registros declarados de busca, somando 684 resultados; ainda não localizei a origem da diferença de 37 em relação aos 721 declarados. Prints/exports e decisões de triagem artigo a artigo ainda precisam ser anexados e conferidos por responsável. Preservei a autoria histórica de Julia separadamente da minha continuidade. O ajuste não está resolvido.

## 🔗 Repositório relacionado

[NodeWatch](https://github.com/1s4ntos/NodeWatch.git) é o repositório relacionado indicado pelo grupo. Seu vínculo é mantido como contexto; o escopo atual das etapas (a)–(c) está restrito à revisão e análise teórica descritas acima.
