# Detecção de Fraudes em Transações Financeiras via Arquiteturas Híbridas (DFA/CEP + Grafos) — Artigo Científico

> Repositório de documentação acadêmica e escrita da Iniciação Científica / Artigo Acadêmico focado na análise comparativa entre travessia em grafos e pré-filtragem por Autômatos Finitos Determinísticos.

---

## 👥 Autores

* **Guilherme Lombardi
* **Caio Winkler Marangoni
* **Guilherme Liborio Camargo
* **Ryan dos Santos Veloso
* **Julia Emily Leonardo Barbosa

---

## 📌 Resumo do Projeto

Este repositório contém a documentação metodológica, o fluxo de Revisão Sistemática da Literatura (PRISMA 2020) e os arquivos-fonte do artigo científico que avalia a eficiência de uma arquitetura híbrida para detecção de fraudes financeiras em tempo real.

A pesquisa investiga em que medida uma camada de pré-filtragem leve baseada em **Autômatos Finitos Determinísticos (DFA/CEP)** reduz a complexidade assintótica no pior caso de algoritmos densos de busca em grafos (como DFS e Kosaraju para identificação de Componentes Fortemente Conectados - SCC).

---

## 🎯 Objetivos da Pesquisa

### Objetivo Geral
Avaliar a aplicação de uma camada de pré-filtragem baseada em Autômatos Finitos Determinísticos (DFA/CEP) em pipelines de detecção de fraudes bancárias em tempo real, com o propósito de reduzir a complexidade assintótica no pior caso e otimizar o tempo de resposta em relação aos algoritmos tradicionais de travessia em grafos (DFS/Kosaraju).

### Objetivos Específicos
* **Mapeamento Teórico:** Revisar e estruturar o estado da arte referente a algoritmos de busca em grafos (DFS/Kosaraju) para identificação de SCCs em redes financeiras.
* **Modelagem de Autômatos:** Conceituar a pré-filtragem via DFA/CEP para reconhecimento de padrões temporais em fluxos contínuos.
* **Análise de Complexidade:** Comparar teoricamente as ordens de complexidade assintótica entre o modelo tradicional e o modelo híbrido.
* **Benchmarking Prático:** Analisar métricas de latência, *throughput* e consumo de memória sob o *dataset* PaySim.
* **Avaliação de Impacto:** Mensurar a taxa de retenção de eventos e a eficiência do descarte preliminar na performance global do sistema.

---

## 📚 Metodologia e Normatização

* **Revisão Sistemática:** Conduzida sob a metodologia **PRISMA 2020** (16 artigos selecionados de uma amostra inicial de 721 resultados).
* **Normatização Bibliográfica:** **ABNT NBR 6023** para citações e referências bibliográficas.
* **Ferramenta de Compilação:** LaTeX / Overleaf (ABNTex2).

---

## 🔗 Repositório de Código-Fonte

O código-fonte da aplicação prática, os *benchmarks* e os scripts do ecossistema estão hospedados no repositório irmão:
👉 `[https://github.com/1s4ntos/NodeWatch.git]`
