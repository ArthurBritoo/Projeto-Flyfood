import random
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass

@dataclass
class ConfiguracoesAG:
    tamanho_populacao: int = 150
    numero_geracoes: int = 1000
    elitismo: bool = True
    taxa_mutacao: float = 0.2
    metodo_selecao: str = 'torneio'
    metodo_crossover: str = 'order'  # 'order' ou 'pmx'

class FlyFoodAG:
    def __init__(self, configuracoes: Optional[ConfiguracoesAG] = None):
        self.configuracoes = configuracoes if configuracoes else ConfiguracoesAG()

    @staticmethod
    def manhattan(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    @staticmethod
    def gerar_rotulos(n: int) -> List[str]:
        rotulos = []
        for i in range(n):
            r = ''
            temp = i
            while True:
                r = chr(65 + temp % 26) + r
                temp = temp // 26 - 1
                if temp < 0:
                    break
            rotulos.append(r)
        return rotulos

    @staticmethod
    def gerar_matriz_aleatoria(linhas: int, colunas: int, num_pontos: int) -> Tuple[List[List[str]], Tuple[int, int], Dict[str, Tuple[int, int]]]:
        matriz = [['0' for _ in range(colunas)] for _ in range(linhas)]
        todas_posicoes = [(r, c) for r in range(linhas) for c in range(colunas)]
        posicao_inicio = random.choice(todas_posicoes)
        matriz[posicao_inicio[0]][posicao_inicio[1]] = 'R'
        todas_posicoes.remove(posicao_inicio)
        rotulos_entregas = FlyFoodAG.gerar_rotulos(num_pontos)
        pontos_entregas = {}
        for rotulo in rotulos_entregas:
            pos = random.choice(todas_posicoes)
            todas_posicoes.remove(pos)
            matriz[pos[0]][pos[1]] = rotulo
            pontos_entregas[rotulo] = pos
        return matriz, posicao_inicio, pontos_entregas

    @staticmethod
    def matriz_para_texto(matriz: List[List[str]]) -> str:
        return f"{len(matriz)} {len(matriz[0])}\n" + "\n".join(" ".join(linha) for linha in matriz)

    @staticmethod
    def ler_matriz_texto(entrada_texto: str) -> Tuple[List[List[str]], Tuple[int, int], Dict[str, Tuple[int, int]]]:
        linhas = entrada_texto.strip().split("\n")
        l, c = map(int, linhas[0].split())
        matriz = [linha.split() for linha in linhas[1:]]
        pontos_entregas = {}
        posicao_inicio = None
        for i in range(l):
            for j in range(c):
                valor = matriz[i][j]
                if valor == 'R':
                    posicao_inicio = (i, j)
                elif valor != '0':
                    pontos_entregas[valor] = (i, j)
        if posicao_inicio is None:
            raise ValueError("Ponto de partida 'R' não encontrado na matriz")
        return matriz, posicao_inicio, pontos_entregas

    def avaliacao(self, individuo: List[str], inicio: Tuple[int, int], pontos: Dict[str, Tuple[int, int]]) -> float:
        custo_total = 0
        atual = inicio
        for p in individuo:
            custo_total += self.manhattan(atual, pontos[p])
            atual = pontos[p]
        custo_total += self.manhattan(atual, inicio)
        return -custo_total

    def selecao(self, populacao: List[List[str]], pontuacoes: List[float]) -> List[List[str]]:
        selecionados = []
        for _ in range(len(populacao)):
            concorrentes = random.sample(list(zip(populacao, pontuacoes)), 2)
            vencedor = max(concorrentes, key=lambda x: x[1])[0]
            selecionados.append(vencedor.copy())
        return selecionados

    def crossover_order(self, pai1: List[str], pai2: List[str]) -> List[str]:
        tamanho = len(pai1)
        a, b = sorted(random.sample(range(tamanho), 2))
        conjunto_fixo = set(pai1[a:b+1])
        filho = [None] * tamanho
        filho[a:b+1] = pai1[a:b+1]
        restante = [p for p in pai2 if p not in conjunto_fixo]
        idx = 0
        for i in range(tamanho):
            if filho[i] is None:
                filho[i] = restante[idx]
                idx += 1
        return filho

    def crossover_pmx(self, pai1: List[str], pai2: List[str]) -> List[str]:
        tamanho = len(pai1)
        a, b = sorted(random.sample(range(tamanho), 2))
        filho = [None] * tamanho
        filho[a:b+1] = pai1[a:b+1]
        mapeamento = {pai1[i]: pai2[i] for i in range(a, b+1)}
        for i in list(range(0, a)) + list(range(b+1, tamanho)):
            candidato = pai2[i]
            while candidato in filho:
                candidato = mapeamento.get(candidato, candidato)
            filho[i] = candidato
        return filho

    def mutar(self, individuo: List[str]) -> None:
        if random.random() < self.configuracoes.taxa_mutacao:
            i, j = random.sample(range(len(individuo)), 2)
            individuo[i], individuo[j] = individuo[j], individuo[i]

    def executar(self, matriz_txt: str) -> Tuple[List[str], Tuple[int, int], Dict[str, Tuple[int, int]], List[List[str]], List[int]]:
        matriz, inicio, pontos_entregas = self.ler_matriz_texto(matriz_txt)
        rotulos = list(pontos_entregas.keys())
        populacao = [random.sample(rotulos, len(rotulos)) for _ in range(self.configuracoes.tamanho_populacao)]
        melhores_distancias = []

        for _ in range(self.configuracoes.numero_geracoes):
            pontuacoes = [self.avaliacao(ind, inicio, pontos_entregas) for ind in populacao]
            nova_geracao = []

            if self.configuracoes.elitismo:
                melhor = max(zip(pontuacoes, populacao), key=lambda x: x[0])[1]
                nova_geracao.append(melhor.copy())

            selecionados = self.selecao(populacao, pontuacoes)

            for _ in range(len(populacao) - len(nova_geracao)):
                pai1, pai2 = random.sample(selecionados, 2)
                if self.configuracoes.metodo_crossover == 'pmx':
                    filho = self.crossover_pmx(pai1, pai2)
                else:
                    filho = self.crossover_order(pai1, pai2)
                self.mutar(filho)
                nova_geracao.append(filho)

            populacao = nova_geracao
            melhor_pontuacao = max(pontuacoes)
            melhores_distancias.append(-melhor_pontuacao)

        melhor = max(populacao, key=lambda ind: self.avaliacao(ind, inicio, pontos_entregas))
        return melhor, inicio, pontos_entregas, matriz, melhores_distancias

    @staticmethod
    def plotar_rota(rota: List[str], inicio: Tuple[int, int], pontos: Dict[str, Tuple[int, int]], matriz: List[List[str]], titulo: str = 'Rota', salvar_em: Optional[str] = None) -> None:
        plt.figure(figsize=(8, 8))
        plt.title(titulo)

        for r in range(len(matriz)):
            for c in range(len(matriz[0])):
                plt.scatter(c, -r, color='lightgray')
                valor = matriz[r][c]
                if valor != '0':
                    plt.text(c, -r, valor, fontsize=8, ha='center', va='center')

        if pontos:
            xs = [coord[1] for coord in pontos.values()]
            ys = [-coord[0] for coord in pontos.values()]
            plt.scatter(xs, ys, c='orange', s=60, marker='o', label='Entregas')

        caminho = [inicio] + [pontos[p] for p in rota] + [inicio]
        for i in range(len(caminho) - 1):
            p0 = caminho[i]
            p1 = caminho[i + 1]
            x0, y0 = p0[1], -p0[0]
            x1, y1 = p1[1], -p1[0]
            inter_x, inter_y = x1, y0
            plt.plot([x0, inter_x], [y0, inter_y], 'b-')
            plt.plot([inter_x, x1], [inter_y, y1], 'b-')
            dist = abs(p0[0] - p1[0]) + abs(p0[1] - p1[1])
            xm = (x0 + inter_x + x1) / 3
            ym = (y0 + inter_y + y1) / 3
            plt.text(xm, ym, f"{dist}", color='purple', fontsize=8, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', boxstyle='round,pad=0.2'))

        plt.scatter(inicio[1], -inicio[0], c='red', label='Início (R)')
        plt.legend()
        plt.grid(True)
        plt.axis('equal')
        if salvar_em:
            plt.savefig(salvar_em)
        else:
            plt.show()
        plt.close()

    @staticmethod
    def plotar_evolucao(distancias: List[int], salvar_em: Optional[str] = None) -> None:
        plt.figure(figsize=(10, 4))
        plt.plot(distancias, label='Melhor distância')
        plt.title("Evolução da distância por geração")
        plt.xlabel("Geração")
        plt.ylabel("Distância")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        if salvar_em:
            plt.savefig(salvar_em)
        else:
            plt.show()
        plt.close()

if __name__ == "__main__":
    print("Cole sua matriz: ")

    linhas = []
    while True:
        try:
            linha = input()
            if linha.strip() == '':
                break
            linhas.append(linha)
        except EOFError:
            break  # Se o usuário der Ctrl+D para encerrar entrada

    matriz_exemplo = '\n'.join(linhas)

    configuracoes = ConfiguracoesAG(tamanho_populacao=150, numero_geracoes=500, metodo_crossover='order')
    ga = FlyFoodAG(configuracoes=configuracoes)

    melhor, inicio, pontos_entregas, matriz, distancias = ga.executar(matriz_exemplo)

    print("\n✅ Algoritmo Genético")
    print('Melhor rota encontrada:', ' '.join(melhor))

    FlyFoodAG.plotar_rota(melhor, inicio, pontos_entregas, matriz)
    FlyFoodAG.plotar_evolucao(distancias)