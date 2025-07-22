import os
import re
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns

def parse_filename(filename):
    """Extrai parâmetros do nome do arquivo"""
    # Formato: pop{pop_min}_gen{generations}_{method}_{rows}x{cols}_{n_points}_distances.json
    pattern = r'pop(\d+)_gen(\d+)_(\w+)_(\d+)x(\d+)_(\d+)_distances\.json'
    match = re.match(pattern, filename)
    
    if match:
        pop_min, generations, method, rows, cols, n_points = match.groups()
        return {
            'pop_size': int(pop_min) + 50 if int(pop_min) > 0 else 50,  # pop_min é o limite inferior
            'generations': int(generations),
            'method': method,
            'grid_size': f"{rows}x{cols}",
            'rows': int(rows),
            'cols': int(cols),
            'n_points': int(n_points),
            'delivery_multiplier': int(n_points) // (int(rows) + int(cols))
        }
    return None

def analyze_subset_results():
    """Analisa os resultados dos experimentos do subconjunto"""
    base_path = "/home/ubuntu/experimentos_flyfood_subset"
    
    results = []
    
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith("_distances.json"):
                filepath = os.path.join(root, file)
                params = parse_filename(file)
                
                if params:
                    with open(filepath, 'r') as f:
                        distances = json.load(f)
                    
                    params['final_distance'] = distances[-1] if distances else None
                    params['min_distance'] = min(distances) if distances else None
                    params['distances'] = distances # Armazenar a lista completa para análise de convergência
                    results.append(params)
    
    df = pd.DataFrame(results)
    
    if df.empty:
        print("Nenhum resultado encontrado no subconjunto!")
        return None
    
    print(f"Total de experimentos no subconjunto: {len(df)}")
    return df

def create_comparative_plots(df):
    """Cria gráficos comparativos dos métodos de crossover"""
    
    plt.rcParams['font.size'] = 10
    
    # Comparação da distância final por método e número de gerações
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='generations', y='final_distance', hue='method', data=df)
    plt.title('Distância Final por Geração e Método de Crossover')
    plt.xlabel('Número de Gerações')
    plt.ylabel('Distância Final')
    plt.grid(True)
    plt.savefig('/home/ubuntu/comparativo_distancia_final.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Comparação da distância final por método e tamanho da população
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='pop_size', y='final_distance', hue='method', data=df)
    plt.title('Distância Final por Tamanho da População e Método de Crossover')
    plt.xlabel('Tamanho da População')
    plt.ylabel('Distância Final')
    plt.grid(True)
    plt.savefig('/home/ubuntu/comparativo_distancia_final_pop.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Análise de convergência (exemplo para uma configuração específica)
    # Escolha um experimento para visualizar a convergência
    # Pode ser necessário iterar sobre diferentes configurações para uma análise completa
    
    # Exemplo: pop_size=50, generations=1000, grid_size=10x10, n_points=20
    example_data = df[(df['pop_size'] == 50) & (df['generations'] == 1000) & 
                      (df['grid_size'] == '10x10') & (df['n_points'] == 20)]
    
    if not example_data.empty:
        plt.figure(figsize=(12, 6))
        for index, row in example_data.iterrows():
            plt.plot(row['distances'], label=f"{row['method']} (Final: {row['final_distance']:.2f})")
        plt.title(f'Convergência da Distância para Pop={example_data.iloc[0]["pop_size"]}, Gen={example_data.iloc[0]["generations"]}, Grid={example_data.iloc[0]["grid_size"]}, Pontos={example_data.iloc[0]["n_points"]}')
        plt.xlabel('Geração')
        plt.ylabel('Distância')
        plt.grid(True)
        plt.legend()
        plt.savefig('/home/ubuntu/convergencia_exemplo.png', dpi=300, bbox_inches='tight')
        plt.close()
    else:
        print("Não foi possível gerar o gráfico de convergência para a configuração de exemplo.")

if __name__ == "__main__":
    print("Iniciando análise dos resultados do subconjunto...")
    df_subset = analyze_subset_results()
    
    if df_subset is not None:
        print("\nCriando gráficos comparativos...")
        create_comparative_plots(df_subset)
        
        # Gerar estatísticas comparativas
        print("\n=== Estatísticas Comparativas ===")
        for method in df_subset['method'].unique():
            method_df = df_subset[df_subset['method'] == method]
            print(f"\n--- Método: {method.upper()} ---")
            print(method_df[['final_distance', 'generations', 'pop_size', 'grid_size', 'n_points']].describe())
            
            # Comparação por gerações
            print(f"\nDistância final média por gerações para {method}:")
            print(method_df.groupby('generations')['final_distance'].mean().reset_index())
            
            # Comparação por tamanho de população
            print(f"\nDistância final média por tamanho de população para {method}:")
            print(method_df.groupby('pop_size')['final_distance'].mean().reset_index())

        df_subset.to_csv('/home/ubuntu/resultados_analise_subset.csv', index=False)
        print(f"\nDataFrame do subconjunto salvo em: /home/ubuntu/resultados_analise_subset.csv")
        print("Gráficos comparativos salvos em: /home/ubuntu/comparativo_distancia_final.png, /home/ubuntu/comparativo_distancia_final_pop.png e /home/ubuntu/convergencia_exemplo.png")




