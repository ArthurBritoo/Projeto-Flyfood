def ler_matriz_input():
    # Lê as dimensões da matriz
    linhas, colunas = map(int, input().strip().split())

    # Lê as linhas da matriz
    matriz = []
    for _ in range(linhas):
        linha = input().strip().split()
        matriz.append(linha)
    
    return matriz

def encontrar_pontos(matriz):
    # Encontra os pontos não nulos e armazena suas coordenadas
    posicoes = {}
    for i, linha in enumerate(matriz):
        for j, valor in enumerate(linha):
            if valor != "0":
                posicoes[valor] = (i, j)
    return posicoes

def distancia_manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def encontrar_rota_mais_proxima(posicoes, ponto_origem):
    pontos_entrega = {nome: coord for nome, coord in posicoes.items() if nome != 'R'}
    rota = []
    posicao_atual = ponto_origem

    while pontos_entrega:
        ponto_mais_proximo = None
        menor_distancia = float('inf')

        for nome_ponto, coordenada in pontos_entrega.items():
            dist = distancia_manhattan(posicao_atual, coordenada)
            if dist < menor_distancia:
                menor_distancia = dist
                ponto_mais_proximo = nome_ponto

        rota.append(ponto_mais_proximo)
        posicao_atual = pontos_entrega.pop(ponto_mais_proximo)

    return rota

def main():
    matriz = ler_matriz_input()
    posicoes = encontrar_pontos(matriz)
    ponto_origem = posicoes['R']
    rota = encontrar_rota_mais_proxima(posicoes, ponto_origem)
    print("Sequência de entrega:", " ".join(rota))

if __name__ == "__main__":
    main()
