import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def generate_additional_plots(df):
    plt.rcParams["font.size"] = 10

    # 1. Convergência Média por Método e Geração
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='generations', y='final_distance', hue='method', data=df, marker='o', errorbar=None)
    plt.title('Convergência Média da Distância Final por Geração e Método de Crossover')
    plt.xlabel('Número de Gerações')
    plt.ylabel('Distância Final Média')
    plt.grid(True)
    plt.legend(title='Método')
    plt.savefig('/home/ubuntu/convergencia_media_geracao.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Impacto do Tamanho do Grid
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='grid_size', y='final_distance', hue='method', data=df)
    plt.title('Distância Final por Tamanho do Grid e Método de Crossover')
    plt.xlabel('Tamanho do Grid')
    plt.ylabel('Distância Final')
    plt.grid(True)
    plt.legend(title='Método')
    plt.savefig('/home/ubuntu/impacto_grid_size.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 3. Impacto do Número de Pontos de Entrega
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='n_points', y='final_distance', hue='method', data=df)
    plt.title('Distância Final por Número de Pontos de Entrega e Método de Crossover')
    plt.xlabel('Número de Pontos de Entrega')
    plt.ylabel('Distância Final')
    plt.grid(True)
    plt.legend(title='Método')
    plt.savefig('/home/ubuntu/impacto_n_points.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 4. Distribuição de Resultados (Histograma)
    plt.figure(figsize=(12, 6))
    for method in df['method'].unique():
        method_data = df[df['method'] == method]['final_distance']
        plt.hist(method_data, alpha=0.7, label=method, bins=10)
    plt.title('Distribuição da Distância Final por Método de Crossover')
    plt.xlabel('Distância Final')
    plt.ylabel('Frequência')
    plt.legend(title='Método')
    plt.grid(True)
    plt.savefig('/home/ubuntu/distribuicao_distancia.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 5. Heatmap de Performance por Configuração
    pivot_table = df.pivot_table(values='final_distance', index='grid_size', columns=['method', 'generations'], aggfunc='mean')
    plt.figure(figsize=(15, 8))
    sns.heatmap(pivot_table, annot=True, fmt='.1f', cmap='viridis_r')
    plt.title('Heatmap da Distância Final Média por Configuração')
    plt.ylabel('Tamanho do Grid')
    plt.xlabel('Método e Número de Gerações')
    plt.savefig('/home/ubuntu/heatmap_performance.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 6. Comparação de Eficiência (Distância Final vs Número de Gerações)
    plt.figure(figsize=(12, 6))
    for method in df['method'].unique():
        method_data = df[df['method'] == method]
        plt.scatter(method_data['generations'], method_data['final_distance'], 
                   label=method, alpha=0.7, s=60)
    plt.title('Eficiência: Distância Final vs Número de Gerações')
    plt.xlabel('Número de Gerações')
    plt.ylabel('Distância Final')
    plt.legend(title='Método')
    plt.grid(True)
    plt.savefig('/home/ubuntu/eficiencia_geracoes.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 7. Análise de Convergência Detalhada (usando dados de distância completos)
    # Vamos criar um gráfico mostrando a convergência média para cada método
    plt.figure(figsize=(15, 8))
    
    # Preparar dados para convergência
    convergence_data = []
    for index, row in df.iterrows():
        distances = eval(row['distances']) if isinstance(row['distances'], str) else row['distances']
        for gen, dist in enumerate(distances):
            convergence_data.append({
                'generation': gen,
                'distance': dist,
                'method': row['method'],
                'experiment_id': index
            })
    
    convergence_df = pd.DataFrame(convergence_data)
    
    # Calcular média por geração e método
    avg_convergence = convergence_df.groupby(['generation', 'method'])['distance'].mean().reset_index()
    
    # Plotar convergência média
    for method in avg_convergence['method'].unique():
        method_data = avg_convergence[avg_convergence['method'] == method]
        plt.plot(method_data['generation'], method_data['distance'], 
                label=f'{method} (média)', linewidth=2, marker='o', markersize=3)
    
    plt.title('Convergência Média da Distância ao Longo das Gerações')
    plt.xlabel('Geração')
    plt.ylabel('Distância Média')
    plt.legend(title='Método')
    plt.grid(True)
    plt.savefig('/home/ubuntu/convergencia_detalhada.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("Todos os gráficos adicionais foram gerados com sucesso!")
    print("Gráficos gerados:")
    print("1. convergencia_media_geracao.png")
    print("2. impacto_grid_size.png")
    print("3. impacto_n_points.png")
    print("4. distribuicao_distancia.png")
    print("5. heatmap_performance.png")
    print("6. eficiencia_geracoes.png")
    print("7. convergencia_detalhada.png")

if __name__ == "__main__":
    try:
        df_subset = pd.read_csv('/home/ubuntu/resultados_analise_subset.csv')
        generate_additional_plots(df_subset)
    except FileNotFoundError:
        print("Erro: O arquivo resultados_analise_subset.csv não foi encontrado. Certifique-se de que a análise do subconjunto foi executada.")
    except Exception as e:
        print(f"Ocorreu um erro ao gerar os gráficos adicionais: {e}")

