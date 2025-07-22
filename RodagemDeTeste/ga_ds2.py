
import random
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass

@dataclass
class GASettings:
    pop_size: int = 150
    num_generations: int = 1000
    elitism: bool = True
    mutation_rate: float = 0.2
    selection_method: str = 'tournament'
    crossover_method: str = 'order'  # 'order' ou 'pmx'

class FlyFoodGA:
    def __init__(self, settings: Optional[GASettings] = None):
        self.settings = settings if settings else GASettings()

    @staticmethod
    def manhattan(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    @staticmethod
    def generate_labels(n: int) -> List[str]:
        labels = []
        for i in range(n):
            label = ''
            temp = i
            while True:
                label = chr(65 + temp % 26) + label
                temp = temp // 26 - 1
                if temp < 0:
                    break
            labels.append(label)
        return labels

    @staticmethod
    def generate_random_matrix(rows: int, cols: int, num_points: int) -> Tuple[List[List[str]], Tuple[int, int], Dict[str, Tuple[int, int]]]:
        matrix = [['0' for _ in range(cols)] for _ in range(rows)]
        all_positions = [(r, c) for r in range(rows) for c in range(cols)]
        start_pos = random.choice(all_positions)
        matrix[start_pos[0]][start_pos[1]] = 'R'
        all_positions.remove(start_pos)
        delivery_labels = FlyFoodGA.generate_labels(num_points)
        delivery_points = {}
        for label in delivery_labels:
            pos = random.choice(all_positions)
            all_positions.remove(pos)
            matrix[pos[0]][pos[1]] = label
            delivery_points[label] = pos
        return matrix, start_pos, delivery_points

    @staticmethod
    def matrix_to_string(matrix: List[List[str]]) -> str:
        return f"{len(matrix)} {len(matrix[0])}\n" + "\n".join(" ".join(row) for row in matrix)

    @staticmethod
    def parse_input(raw_input: str) -> Tuple[List[List[str]], Tuple[int, int], Dict[str, Tuple[int, int]]]:
        lines = raw_input.strip().split("\n")
        rows, cols = map(int, lines[0].split())
        matrix = [line.split() for line in lines[1:]]
        delivery_points = {}
        start_pos = None
        for r in range(rows):
            for c in range(cols):
                val = matrix[r][c]
                if val == 'R':
                    start_pos = (r, c)
                elif val != '0':
                    delivery_points[val] = (r, c)
        if start_pos is None:
            raise ValueError("Ponto de partida 'R' não encontrado na matriz")
        return matrix, start_pos, delivery_points

    def fitness(self, individual: List[str], start: Tuple[int, int], points: Dict[str, Tuple[int, int]]) -> float:
        total = 0
        current = start
        for p in individual:
            total += self.manhattan(current, points[p])
            current = points[p]
        total += self.manhattan(current, start)
        return -total

    def selection(self, population: List[List[str]], scores: List[float]) -> List[List[str]]:
        selected = []
        for _ in range(len(population)):
            contestants = random.sample(list(zip(population, scores)), 2)
            winner = max(contestants, key=lambda x: x[1])[0]
            selected.append(winner.copy())
        return selected

    def crossover_order(self, p1: List[str], p2: List[str]) -> List[str]:
        size = len(p1)
        a, b = sorted(random.sample(range(size), 2))
        hole = set(p1[a:b+1])
        child = [None]*size
        child[a:b+1] = p1[a:b+1]
        fill = [item for item in p2 if item not in hole]
        idx = 0
        for i in range(size):
            if child[i] is None:
                child[i] = fill[idx]
                idx += 1
        return child

    def crossover_pmx(self, p1: List[str], p2: List[str]) -> List[str]:
        size = len(p1)
        a, b = sorted(random.sample(range(size), 2))
        child = [None]*size
        child[a:b+1] = p1[a:b+1]
        mapping = {p1[i]: p2[i] for i in range(a, b+1)}
        for i in list(range(0, a)) + list(range(b+1, size)):
            candidate = p2[i]
            while candidate in child:
                candidate = mapping.get(candidate, candidate)
            child[i] = candidate
        return child

    def mutate(self, individual: List[str]) -> None:
        if random.random() < self.settings.mutation_rate:
            i, j = random.sample(range(len(individual)), 2)
            individual[i], individual[j] = individual[j], individual[i]

    def run(self, matrix_txt: str) -> Tuple[List[str], Tuple[int, int], Dict[str, Tuple[int, int]], List[List[str]], List[int]]:
        matrix, start, delivery_points = self.parse_input(matrix_txt)
        labels = list(delivery_points.keys())
        population = [random.sample(labels, len(labels)) for _ in range(self.settings.pop_size)]
        best_distances = []
        for _ in range(self.settings.num_generations):
            scores = [self.fitness(ind, start, delivery_points) for ind in population]
            next_gen = []
            if self.settings.elitism:
                best = max(zip(scores, population), key=lambda x: x[0])[1]
                next_gen.append(best.copy())
            selected = self.selection(population, scores)
            for _ in range(len(population) - len(next_gen)):
                p1, p2 = random.sample(selected, 2)
                if self.settings.crossover_method == 'pmx':
                    child = self.crossover_pmx(p1, p2)
                else:
                    child = self.crossover_order(p1, p2)
                self.mutate(child)
                next_gen.append(child)
            population = next_gen
            best_score = max(scores)
            best_distances.append(-best_score)
        best = max(population, key=lambda ind: self.fitness(ind, start, delivery_points))
        return best, start, delivery_points, matrix, best_distances

    @staticmethod
    def plot_route(route: List[str], start: Tuple[int, int], points: Dict[str, Tuple[int, int]], 
                   matrix: List[List[str]], title: str = 'Rota', save_path: Optional[str] = None) -> None:
        plt.figure(figsize=(8, 8))
        plt.title(title)
        for r in range(len(matrix)):
            for c in range(len(matrix[0])):
                plt.scatter(c, -r, color='lightgray')
                val = matrix[r][c]
                if val != '0':
                    plt.text(c, -r, val, fontsize=8, ha='center', va='center')
        if points:
            xs = [coord[1] for coord in points.values()]
            ys = [-coord[0] for coord in points.values()]
            plt.scatter(xs, ys, c='orange', s=60, marker='o', label='Entregas')
        path = [start] + [points[p] for p in route] + [start]
        for i in range(len(path)-1):
            p0 = path[i]
            p1 = path[i+1]
            x0, y0 = p0[1], -p0[0]
            x1, y1 = p1[1], -p1[0]
            inter_x, inter_y = x1, y0
            plt.plot([x0, inter_x], [y0, inter_y], 'b-')
            plt.plot([inter_x, x1], [inter_y, y1], 'b-')
            dist = abs(p0[0] - p1[0]) + abs(p0[1] - p1[1])
            xm = (x0 + inter_x + x1) / 3
            ym = (y0 + inter_y + y1) / 3
            plt.text(xm, ym, f"{dist}", color='purple', fontsize=8, ha='center', va='center', 
                     bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', boxstyle='round,pad=0.2'))
        plt.scatter(start[1], -start[0], c='red', label='Start (R)')
        plt.legend()
        plt.grid(True)
        plt.axis('equal')
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()
        plt.close()

    @staticmethod
    def plot_progression(distances: List[int], save_path: Optional[str] = None) -> None:
        plt.figure(figsize=(10, 4))
        plt.plot(distances, label='Melhor distância')
        plt.title("Evolução da distância por geração")
        plt.xlabel("Geração")
        plt.ylabel("Distância")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()
        plt.close()
