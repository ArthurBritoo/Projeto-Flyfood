import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import numpy as np

def parse_filename(filename):
    """Extrai parâmetros do nome do arquivo"""
    # Formato: pop{pop_min}_gen{generations}_{method}_{rows}x{cols}_{n_points}_grafico.png
    pattern = r'pop(\d+)_gen(\d+)_(\w+)_(\d+)x(\d+)_(\d+)_grafico\.png'
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

def extract_final_distance_from_image(image_path):
    """Tenta extrair a distância final do gráfico (aproximação visual)"""
    try:
        # Esta é uma aproximação - idealmente precisaríamos dos dados brutos
        # Por enquanto, vamos retornar None e usar outras métricas
        return None
    except:
        return None

def analyze_results():
    """Analisa os resultados dos experimentos"""
    base_path = "/home/ubuntu/resultados_extraidos"
    
    # Lista para armazenar os dados
    results = []
    
    # Percorre todos os arquivos de gráfico
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith("_grafico.png"):
                filepath = os.path.join(root, file)
                params = parse_filename(file)
                
                if params:
                    params['filepath'] = filepath
                    results.append(params)
    
    # Cria DataFrame
    df = pd.DataFrame(results)
    
    if df.empty:
        print("Nenhum resultado encontrado!")
        return None
    
    print(f"Total de experimentos encontrados: {len(df)}")
    print(f"Métodos de crossover: {df['method'].unique()}")
    print(f"Tamanhos de população: {sorted(df['pop_size'].unique())}")
    print(f"Números de gerações: {sorted(df['generations'].unique())}")
    print(f"Tamanhos de grid: {sorted(df['grid_size'].unique())}")
    
    return df

def create_analysis_plots(df):
    """Cria gráficos de análise"""
    
    # Configuração do matplotlib para português
    plt.rcParams['font.size'] = 10
    
    # 1. Distribuição de experimentos por método
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Gráfico 1: Distribuição por método
    method_counts = df['method'].value_counts()
    axes[0,0].pie(method_counts.values, labels=method_counts.index, autopct='%1.1f%%')
    axes[0,0].set_title('Distribuição de Experimentos por Método de Crossover')
    
    # Gráfico 2: Experimentos por tamanho de população
    pop_counts = df['pop_size'].value_counts().sort_index()
    axes[0,1].bar(pop_counts.index, pop_counts.values)
    axes[0,1].set_title('Experimentos por Tamanho de População')
    axes[0,1].set_xlabel('Tamanho da População')
    axes[0,1].set_ylabel('Número de Experimentos')
    
    # Gráfico 3: Experimentos por número de gerações
    gen_counts = df['generations'].value_counts().sort_index()
    axes[1,0].plot(gen_counts.index, gen_counts.values, marker='o')
    axes[1,0].set_title('Experimentos por Número de Gerações')
    axes[1,0].set_xlabel('Número de Gerações')
    axes[1,0].set_ylabel('Número de Experimentos')
    axes[1,0].grid(True)
    
    # Gráfico 4: Heatmap de experimentos por grid size e método
    pivot_table = df.pivot_table(values='filepath', index='grid_size', columns='method', aggfunc='count', fill_value=0)
    sns.heatmap(pivot_table, annot=True, fmt='d', ax=axes[1,1])
    axes[1,1].set_title('Número de Experimentos por Tamanho de Grid e Método')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analise_distribuicao.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Análise por complexidade do problema
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Gráfico 1: Relação entre tamanho do grid e número de pontos
    for method in df['method'].unique():
        method_data = df[df['method'] == method]
        axes[0,0].scatter(method_data['rows'] * method_data['cols'], method_data['n_points'], 
                         label=method, alpha=0.6)
    axes[0,0].set_xlabel('Tamanho do Grid (rows × cols)')
    axes[0,0].set_ylabel('Número de Pontos de Entrega')
    axes[0,0].set_title('Complexidade do Problema por Método')
    axes[0,0].legend()
    axes[0,0].grid(True)
    
    # Gráfico 2: Distribuição de multiplicadores de entrega
    mult_counts = df['delivery_multiplier'].value_counts().sort_index()
    axes[0,1].bar(mult_counts.index, mult_counts.values)
    axes[0,1].set_title('Distribuição de Multiplicadores de Entrega')
    axes[0,1].set_xlabel('Multiplicador de Entrega')
    axes[0,1].set_ylabel('Número de Experimentos')
    
    # Gráfico 3: Boxplot de número de pontos por método
    df.boxplot(column='n_points', by='method', ax=axes[1,0])
    axes[1,0].set_title('Distribuição do Número de Pontos por Método')
    axes[1,0].set_xlabel('Método de Crossover')
    axes[1,0].set_ylabel('Número de Pontos de Entrega')
    
    # Gráfico 4: Relação entre população e gerações
    for method in df['method'].unique():
        method_data = df[df['method'] == method]
        axes[1,1].scatter(method_data['pop_size'], method_data['generations'], 
                         label=method, alpha=0.6)
    axes[1,1].set_xlabel('Tamanho da População')
    axes[1,1].set_ylabel('Número de Gerações')
    axes[1,1].set_title('Relação População vs Gerações por Método')
    axes[1,1].legend()
    axes[1,1].grid(True)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analise_complexidade.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return df

def generate_summary_stats(df):
    """Gera estatísticas resumidas"""
    
    summary = {
        'total_experiments': len(df),
        'methods': list(df['method'].unique()),
        'pop_sizes': sorted(df['pop_size'].unique()),
        'generations_range': [df['generations'].min(), df['generations'].max()],
        'grid_sizes': sorted(df['grid_size'].unique()),
        'n_points_range': [df['n_points'].min(), df['n_points'].max()],
        'experiments_by_method': df['method'].value_counts().to_dict(),
        'experiments_by_pop_size': df['pop_size'].value_counts().sort_index().to_dict(),
        'avg_experiments_per_config': len(df) / (len(df['method'].unique()) * len(df['pop_size'].unique()) * len(df['generations'].unique()))
    }
    
    return summary

if __name__ == "__main__":
    print("Iniciando análise dos resultados...")
    df = analyze_results()
    
    if df is not None:
        print("\nCriando gráficos de análise...")
        df = create_analysis_plots(df)
        
        print("\nGerando estatísticas resumidas...")
        summary = generate_summary_stats(df)
        
        print("\n=== RESUMO DA ANÁLISE ===")
        print(f"Total de experimentos: {summary['total_experiments']}")
        print(f"Métodos testados: {', '.join(summary['methods'])}")
        print(f"Tamanhos de população: {summary['pop_sizes']}")
        print(f"Faixa de gerações: {summary['generations_range'][0]} - {summary['generations_range'][1]}")
        print(f"Tamanhos de grid: {len(summary['grid_sizes'])} diferentes")
        print(f"Faixa de pontos de entrega: {summary['n_points_range'][0]} - {summary['n_points_range'][1]}")
        
        print("\nExperimentos por método:")
        for method, count in summary['experiments_by_method'].items():
            print(f"  {method}: {count}")
        
        print("\nExperimentos por tamanho de população:")
        for pop_size, count in summary['experiments_by_pop_size'].items():
            print(f"  {pop_size}: {count}")
        
        # Salva o DataFrame para análise posterior
        df.to_csv('/home/ubuntu/resultados_analise.csv', index=False)
        print(f"\nDataFrame salvo em: /home/ubuntu/resultados_analise.csv")
        print("Gráficos salvos em: /home/ubuntu/analise_distribuicao.png e /home/ubuntu/analise_complexidade.png")

