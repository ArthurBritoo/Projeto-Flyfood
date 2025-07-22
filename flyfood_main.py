from algoritmo_genetico import FlyFoodAG, ConfiguracoesAG
from forca_bruta import ler_matriz, encontrar_pontos, calcular_distancia, gerar_permutacoes


def calcular_custo_rota(origem, pontos_dict, rota):
    custo = 0
    atual = origem
    for ponto in rota:
        custo += calcular_distancia(atual, pontos_dict[ponto])
        atual = pontos_dict[ponto]
    custo += calcular_distancia(atual, origem)
    return custo


def resolver_forca_bruta(matriz):
    pontos = encontrar_pontos(matriz)
    origem = pontos['R']
    pontos_entrega = [p for p in pontos if p != 'R']

    permutacoes = gerar_permutacoes(pontos_entrega)
    menor_custo = None
    melhor_rota = None

    for rota in permutacoes:
        custo = calcular_custo_rota(origem, pontos, rota)
        if menor_custo is None or custo < menor_custo:
            menor_custo = custo
            melhor_rota = rota

    return melhor_rota


def matriz_para_string(matriz):
    linhas = len(matriz)
    colunas = len(matriz[0]) if matriz else 0
    texto = f"{linhas} {colunas}\n"
    for linha in matriz:
        texto += ' '.join(linha) + "\n"
    return texto


def main():
    matriz = ler_matriz()
    pontos = encontrar_pontos(matriz)
    pontos_entrega = [p for p in pontos if p != 'R']
    if len(pontos_entrega) <= 9:
        print("\n🔵 Algoritmo escolhido: Força Bruta")
        rota = resolver_forca_bruta(matriz)
        print('Melhor rota encontrada:', ' '.join(rota))
    else:
        print("\n🟢 Algoritmo escolhido: Algoritmo Genético com Order Crossover (OX)")
        matriz_txt = matriz_para_string(matriz)
        configuracoes = ConfiguracoesAG(tamanho_populacao=150, numero_geracoes=1000, metodo_crossover='order')
        ga = FlyFoodAG(configuracoes=configuracoes)
        melhor, inicio, pontos_entregas, matriz, distancias = ga.executar(matriz_txt)
        print('Melhor rota encontrada:', ' '.join(melhor))


if __name__ == "__main__":
    print("Cole sua matriz: ")
    main()
