
import os
import zipfile
import shutil
import random
from ga_ds2 import FlyFoodGA, GASettings

import matplotlib.pyplot as plt

# Novo método para salvar imagens
def save_route_image(route, start, points, matrix, path):
    plt.figure(figsize=(8, 8))
    plt.title("Rota")
    FlyFoodGA.plot_route(route, start, points, matrix, title="")
    plt.savefig(path)
    plt.close()

def save_progression_image(distances, path):
    plt.figure(figsize=(10, 4))
    plt.plot(distances, label='Melhor distância')
    plt.title("Evolução da distância por geração")
    plt.xlabel("Geração")
    plt.ylabel("Distância")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

def run_experiments():
    base_path = "experimentos_flyfood"
    os.makedirs(base_path, exist_ok=True)

    pop_ranges = [(0, 50), (50, 100), (100, 150), (150, 200)]
    generations_list = list(range(100, 2001, 100))
    sizes = list(range(5, 51, 5))
    crossover_methods = ['order', 'pmx']

    for pop_min, pop_max in pop_ranges:
        pop_folder = f"pop{pop_min}"
        for generations in generations_list:
            gen_folder = f"gen{generations}"
            for size in sizes:
                for delivery_multiplier in [1, 2]:
                    rows, cols = size, size
                    n_points = delivery_multiplier * (rows + cols)

                    matrix, start, delivery_points = FlyFoodGA.generate_random_matrix(rows, cols, n_points)
                    matrix_str = FlyFoodGA.matrix_to_string(matrix)

                    for method in crossover_methods:
                        settings = GASettings(
                            pop_size=pop_max,
                            num_generations=generations,
                            mutation_rate=0.2,
                            crossover_method=method
                        )
                        ga = FlyFoodGA(settings)
                        best_route, start, points, matrix, distances = ga.run(matrix_str)

                        filename_base = f"pop{pop_min}_gen{generations}_{method}_{rows}x{cols}_{n_points}"
                        save_dir = os.path.join(base_path, pop_folder, gen_folder, f"{rows}x{cols}")
                        os.makedirs(save_dir, exist_ok=True)

                        route_img = os.path.join(save_dir, filename_base + "_rota.png")
                        graph_img = os.path.join(save_dir, filename_base + "_grafico.png")

                        save_route_image(best_route, start, points, matrix, route_img)
                        save_progression_image(distances, graph_img)

    # Compactar resultados
    zip_path = os.path.join(base_path, "resultados", "resultados.zip")
    os.makedirs(os.path.dirname(zip_path), exist_ok=True)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(base_path):
            for file in files:
                if file.endswith(".png"):
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, base_path)
                    zipf.write(full_path, arcname)

if __name__ == "__main__":
    run_experiments()
