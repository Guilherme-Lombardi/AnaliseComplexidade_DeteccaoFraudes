# Tabelas da auditoria (geradas por scripts/g_consolidar.py)

## Rede — estado da próxima medição (teste 05/10/2026, 46.105 medições)

| Candidato | Treino (ajuste) | Macro-F1 val | Macro-F1 teste | Recall RISCO / FALHA (teste) | Balanced acc. (teste) | Inícios de evento detectados | Falsos alertas por fluxo-hora | Treino (s, mediana de 3) | Latência 1 linha, ms (mediana / p99) | Vazão lote (linhas/s) | Memória de pico no ajuste (MB) | Tamanho joblib compress=3 (MB = 10⁶ bytes) | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Classe majoritária | sem ajuste | 0,312 | 0,311 | 0,000 / 0,000 | 0,333 | 0,000 | 0,00 | 0 | ~0 | — | — | — | medido |
| Persistência (classe_atual) | sem ajuste | 0,711 | 0,711 | 0,507 / 0,681 | 0,711 | 0,000 | 0,73 | 0 | ~0 | — | — | — | medido |
| Regra de limiares da medição atual | sem ajuste | 0,710 | 0,712 | 0,506 / 0,687 | 0,712 | 0,000 | 0,73 | 0 | ~0 | — | — | — | medido |
| Pior estado das últimas k medições (pior_estado_k1, k no treino) | regra ajustada | 0,711 | 0,711 | 0,507 / 0,681 | 0,711 | 0,000 | 0,73 | ~0 | ~0 | — | — | — | medido |
| Regressão logística {'C': 0.1, 'class_weight': None} | treino 28/09–03/10 | 0,590 | 0,642 | 0,397 / 0,395 | 0,593 | 0,044 | 0,29 | 1,7 | 5,4 / 7,5 | 1.336.834 | 57 | 0,00 | medido |
| HistGradientBoosting {'max_iter': 200, 'learning_rate': 0.1, 'max_leaf_nodes': 31, 'class_weight': None} | treino 28/09–03/10 | 0,762 | 0,750 | 0,438 / 0,686 | 0,704 | 0,066 | 0,27 | 4,5 | 8,1 / 14,6 | 283.869 | 126 | 0,97 | medido |
| Random Forest (grade de produção) {'n_estimators': 150, 'min_samples_leaf': 20, 'max_samples': 0.5, 'class_weight': None} | treino 28/09–03/10 | 0,763 | 0,750 | 0,418 / 0,697 | 0,702 | 0,045 | 0,31 | 12,2 | 27,7 / 29,5 | 289.027 | 133 | 17,59 | medido |
| Random Forest (configuração do notebook da professora) {'n_estimators': 100, 'min_samples_leaf': 5, 'max_samples': None, 'class_weight': None} | treino 28/09–03/10 | 0,767 | 0,755 | 0,438 / 0,696 | 0,708 | 0,059 | 0,29 | 24,4 | 35,8 / 51,2 | 239.840 | 230 | 39,21 | medido |
| Random Forest com 50 árvores (mesma folha da produção) {'n_estimators': 50, 'min_samples_leaf': 20, 'max_samples': 0.5, 'class_weight': None} | treino 28/09–03/10 | 0,764 | 0,751 | 0,420 / 0,695 | 0,702 | 0,045 | 0,25 | 5,8 | 23,2 / 39,9 | 550.605 | 94 | 5,87 | medido |
| XGBoost (hist, CPU) {'max_depth': 6, 'pesos': None} | treino 28/09–03/10 | 0,766 | 0,752 | 0,430 / 0,698 | 0,706 | 0,060 | 0,29 | 4,1 | 5,3 / 8,1 | 451.591 | 58 | 0,86 | medido |

## Lavagem — IBM AML HI-Small (teste 09–10/09/2022, 862.792 transações, 956 positivas)

| Candidato | AP val | AP teste | Precisão / recall / F1 no limiar da validação (teste) | Falsos positivos por 10 mil (teste) | Recall@1000 por dia (09/09; 10/09) | Treino (s, mediana de 3) | Latência 1 linha, ms (mediana / p99) | Vazão lote (linhas/s) | Memória de pico no ajuste (MB) | Tamanho joblib compress=3 (MB = 10⁶ bytes) | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Prevalência (constante) | 0,0011 | 0,0011 | — | — | — | 0 | ~0 | — | — | — | medido |
| Taxa de lavagem do formato (treino) | 0,0068 | 0,0064 | 0,007 / 0,872 / 0,014 | 1371,8 | — | 0 | ~0 | — | — | — | medido |
| Regra F2_motivos>=2 | 0,0145 | 0,0112 | 0,014 / 0,820 / 0,027 | 661,7 | — | ~0 | ~0 | — | — | — | medido |
| Regra F3_formato_risco & par_novo | — (sem ranking) | — (sem ranking) | 0,036 / 0,780 / 0,069 | 229,8 | — | ~0 | ~0 | — | — | — | medido |
| Regressão logística {'C': 0.1} | 0,1690 | 0,1693 | 0,176 / 0,411 / 0,247 | 21,3 | 0,346; 0,446 | 4,0 | 4,4 / 8,6 | 802,234 | 132 | 0.0 | medido |
| HistGradientBoosting {'max_iter': 300, 'learning_rate': 0.1, 'max_leaf_nodes': 31, 'l2_regularization': 1.0} | 0,4497 | 0,4139 | 0,616 / 0,394 / 0,481 | 2,7 | 0,488; 0,593 | 19,3 | 4,5 / 8,4 | 240,653 | 565 | 0.4 | medido |
| Random Forest (grade de produção) {'n_estimators': 100, 'min_samples_leaf': 50, 'max_samples': 0.5} | 0,4950 | 0,4610 | 0,521 / 0,446 / 0,481 | 4,5 | 0,541; 0,611 | 42,7 | 26,3 / 29,2 | 622,377 | 175 | 2.7 | medido |
| Random Forest (busca com 4 tentativas) {'n_estimators': 200, 'min_samples_leaf': 10, 'max_samples': 0.5} | 0,5247 | 0,4781 | 0,651 / 0,412 / 0,505 | 2,4 | 0,558; 0,631 | 85,4 | 39,5 / 56,0 | 287,802 | 199 | 9.0 | medido |
| XGBoost (hist, CPU) {'max_depth': 6, 'min_child_weight': 10} | 0,5548 | 0,5087 | 0,685 / 0,447 / 0,541 | 2,3 | 0,539; 0,663 | 6,6 | 4,3 / 7,8 | 1,188,339 | 99 | 0.1 | medido |

## Orçamento de busca e variação por semente

| Domínio | Família | Tentativas | Segundos (busca) | Escolhido | Métrica val (sementes 42–44) | Métrica teste (sementes 42–44) |
|---|---|---|---|---|---|---|
| rede | Regressão logística | 4 | 7,9 | {'C': 0.1, 'class_weight': None} | 0,5900–0,5900 | 0,6425–0,6425 |
| rede | HistGradientBoosting | 4 | 20,4 | {'max_iter': 200, 'learning_rate': 0.1, 'max_leaf_nodes': 31, 'class_weight': None} | 0,7572–0,7618 | 0,7456–0,7500 |
| rede | Random Forest (grade de produção) | 4 | 44,6 | {'n_estimators': 150, 'min_samples_leaf': 20, 'max_samples': 0.5, 'class_weight': None} | 0,7628–0,7635 | 0,7499–0,7508 |
| rede | Random Forest (configuração do notebook da professora) | 1 | 20,7 | {'n_estimators': 100, 'min_samples_leaf': 5, 'max_samples': None, 'class_weight': None} | 0,7670–0,7678 | 0,7536–0,7557 |
| rede | Random Forest com 50 árvores (mesma folha da produção) | 1 | 6,3 | {'n_estimators': 50, 'min_samples_leaf': 20, 'max_samples': 0.5, 'class_weight': None} | 0,7617–0,7641 | 0,7504–0,7506 |
| rede | XGBoost (hist, CPU) | 4 | 71,9 | {'max_depth': 6, 'pesos': None} | 0,7662–0,7662 | 0,7515–0,7515 |
| lavagem | Regressão logística | 2 | 8,3 | {'C': 0.1} | 0,1690–0,1690 | 0,1693–0,1693 |
| lavagem | HistGradientBoosting | 2 | 51,7 | {'max_iter': 300, 'learning_rate': 0.1, 'max_leaf_nodes': 31, 'l2_regularization': 1.0} | 0,4404–0,4737 | 0,4139–0,4439 |
| lavagem | Random Forest (grade de produção) | 1 | 53,8 | {'n_estimators': 100, 'min_samples_leaf': 50, 'max_samples': 0.5} | 0,4867–0,4950 | 0,4610–0,4629 |
| lavagem | Random Forest (busca com 4 tentativas) | 4 | 269,8 | {'n_estimators': 200, 'min_samples_leaf': 10, 'max_samples': 0.5} | 0,5118–0,5247 | 0,4699–0,4781 |
| lavagem | XGBoost (hist, CPU) | 4 | 251,9 | {'max_depth': 6, 'min_child_weight': 10} | 0,5548–0,5548 | 0,5087–0,5087 |

## Incerteza

Rede: bootstrap pareado por id_fluxo (135 fluxos, B=2000).

| Diferença no teste | Macro-F1 | IC 95% | Fração > 0 |
|---|---|---|---|
| persistencia - rf | -0,0391 | [-0,0535; -0,0171] | 0,002 |
| lr - rf | -0,1074 | [-0,1876; -0,0435] | 0,000 |
| hgb - rf | 0,0001 | [-0,0076; 0,0070] | 0,524 |
| rf_nb - rf | 0,0055 | [0,0007; 0,0110] | 0,983 |
| rf_red - rf | 0,0007 | [-0,0004; 0,0021] | 0,886 |
| xgb - rf | 0,0016 | [-0,0030; 0,0057] | 0,765 |

Lavagem: AP por dia do teste.

| Família | 2022-09-09 | 2022-09-10 |
|---|---|---|
| Regressão logística | 0,1442 | 0,2005 |
| HistGradientBoosting | 0,3737 | 0,4607 |
| Random Forest (grade de produção) | 0,4396 | 0,4887 |
| Random Forest (busca com 4 tentativas) | 0,4582 | 0,5047 |
| XGBoost (hist, CPU) | 0,4655 | 0,5610 |
