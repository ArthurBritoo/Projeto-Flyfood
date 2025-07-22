# Relatório Comparativo de Métodos de Crossover para TSP

## Introdução

Este relatório apresenta uma análise dos resultados de um algoritmo genético para o Problema do Caixeiro Viajante (TSP), com foco na comparação de diferentes métodos de crossover: Order Crossover e Partially Mapped Crossover (PMX). Os dados foram gerados a partir da execução do script `batch_runner.py`, que simula diversos cenários variando parâmetros como tamanho da população, número de gerações e complexidade do problema (tamanho do grid e número de pontos de entrega).

Inicialmente, a análise foi limitada aos metadados dos arquivos devido à ausência dos dados brutos de distância. No entanto, após a execução de um subconjunto de experimentos, foi possível obter informações mais detalhadas sobre a evolução da distância, permitindo uma comparação mais aprofundada do desempenho de cada método.

## Metodologia dos Experimentos

O script `batch_runner.py` executa uma série de experimentos com as seguintes variações:

- **Tamanho da População (`pop_size`):** Variando em faixas de 50 (ex: 0-50, 50-100, 100-150, 150-200).
- **Número de Gerações (`num_generations`):** De 100 a 2000, em incrementos de 100.
- **Tamanho do Grid (`rows` x `cols`):** De 5x5 a 50x50, em incrementos de 5.
- **Número de Pontos de Entrega (`n_points`):** Definido por um multiplicador (1 ou 2) do tamanho do grid (rows + cols).
- **Método de Crossover (`crossover_method`):** 'order' (Order Crossover) e 'pmx' (Partially Mapped Crossover).

Para cada combinação desses parâmetros, o algoritmo genético é executado, e são geradas imagens da rota final e do gráfico de evolução da distância. Na re-execução de um subconjunto de experimentos, os dados brutos de distância também foram salvos em arquivos JSON, permitindo a análise quantitativa.

## Análise da Distribuição dos Experimentos

A análise inicial dos arquivos extraídos do `resultados.zip` original revelou uma distribuição equitativa de experimentos entre os métodos de crossover (`order` e `pmx`), com 712 experimentos para cada. Os experimentos cobriram uma ampla gama de tamanhos de população (100 a 250), gerações (100 a 1700) e complexidade de problemas (grids de 5x5 a 50x50, com 10 a 200 pontos de entrega).

## Análise Comparativa Abrangente dos Métodos de Crossover

Com base nos dados obtidos da execução do subconjunto de experimentos, foi possível realizar uma análise comparativa mais robusta entre os métodos Order Crossover e PMX. Esta análise focou em como cada método se comporta em relação à distância final alcançada, à velocidade de convergência e à sua robustez sob diferentes condições.

### Desempenho Geral e Distância Final

Em média, o **Order Crossover** demonstrou um desempenho ligeiramente superior ao **PMX** na obtenção de rotas mais curtas. As estatísticas resumidas do subconjunto de dados indicaram que o Order Crossover tendeu a alcançar distâncias finais médias menores em comparação com o PMX. Isso sugere que, para os tipos de problemas e configurações testadas, o Order Crossover pode ser marginalmente mais eficaz em encontrar soluções otimizadas.

### Convergência e Número de Gerações

Ambos os métodos exibiram uma clara tendência de **melhora na distância final com o aumento do número de gerações**. Isso é um comportamento esperado para algoritmos genéticos, onde mais iterações permitem uma exploração mais aprofundada do espaço de soluções. Os gráficos de convergência média (e.g., `convergencia_media_geracao.png` e `convergencia_detalhada.png`) ilustram que a distância final diminui progressivamente à medida que o número de gerações aumenta. Embora ambos os métodos se beneficiem de mais gerações, o Order Crossover pareceu atingir distâncias menores mais rapidamente em alguns cenários, indicando uma potencial vantagem em termos de velocidade de convergência.

### Impacto da Complexidade do Problema

A complexidade do problema, definida pelo tamanho do grid e pelo número de pontos de entrega, teve um impacto significativo na distância final alcançada por ambos os métodos. Como esperado, problemas com maior número de pontos e grids maiores resultaram em distâncias finais mais elevadas. Os gráficos de impacto do grid (`impacto_grid_size.png`) e do número de pontos (`impacto_n_points.png`) mostram como a distância final se correlaciona com esses parâmetros, e como os métodos se comportam em diferentes níveis de dificuldade. A análise visual sugere que o Order Crossover mantém sua ligeira vantagem mesmo em problemas mais complexos.

### Robustez e Distribuição dos Resultados

A distribuição da distância final (`distribuicao_distancia.png`) para cada método oferece insights sobre sua robustez. Embora ambos os métodos apresentem variabilidade nos resultados, a análise geral indica que o Order Crossover não apenas alcança distâncias menores em média, mas também pode apresentar uma distribuição de resultados mais concentrada em torno de valores ótimos em certas configurações, sugerindo maior consistência.

### Eficiência e Desempenho por Configuração

Os gráficos de eficiência (`eficiencia_geracoes.png`) e o heatmap de desempenho (`heatmap_performance.png`) fornecem uma visão consolidada do comportamento dos métodos. O heatmap, em particular, permite identificar rapidamente as configurações (combinações de tamanho do grid, método e gerações) onde cada método se sobressai ou encontra dificuldades. De forma geral, o Order Crossover demonstrou um desempenho superior em diversas configurações, especialmente com um número maior de gerações.

## Conclusões Finais

Com base na análise abrangente dos dados disponíveis, o **Order Crossover** emerge como o método de crossover com desempenho ligeiramente superior para o problema do Caixeiro Viajante (TSP) nas condições testadas. Ele tende a encontrar rotas mais curtas e demonstra uma convergência eficaz ao longo das gerações. A performance de ambos os métodos é, como esperado, influenciada pela complexidade do problema, com o Order Crossover mantendo sua vantagem relativa.

É importante notar que esta análise foi realizada com base em um subconjunto de dados. Para conclusões mais definitivas e generalizáveis, seria ideal ter acesso e processar o conjunto completo de dados gerados pelo `batch_runner.py` original. No entanto, as tendências observadas neste estudo fornecem uma base sólida para futuras investigações e para a escolha de métodos de crossover em problemas de otimização similares.

## Anexos

- `analise_distribuicao.png`
- `analise_complexidade.png`
- `comparativo_distancia_final.png`
- `comparativo_distancia_final_pop.png`
- `convergencia_exemplo.png`
- `convergencia_media_geracao.png`
- `impacto_grid_size.png`
- `impacto_n_points.png`
- `distribuicao_distancia.png`
- `heatmap_performance.png`
- `eficiencia_geracoes.png`
- `convergencia_detalhada.png`


