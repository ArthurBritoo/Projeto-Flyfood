def ler_matriz():
    """Lê a matriz da entrada padrão conforme o formato especificado"""
    primeira_linha = input().strip()
    while primeira_linha == '':
        primeira_linha = input().strip()
    
    partes = primeira_linha.split()
    linhas = int(partes[0])
    
    matriz = []
    for _ in range(linhas):
        linha = input().strip()
        while linha == '':
            linha = input().strip()
        elementos = linha.split()
        matriz.append(elementos)
    
    return matriz

def encontrar_pontos(matriz):
    """Encontra todos os pontos nomeados na matriz e suas coordenadas"""
    pontos = {}
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            valor = matriz[i][j]
            if valor != '0':
                pontos[valor] = (i, j)
    return pontos

def calcular_distancia(p1, p2):
    """Calcula a distância Manhattan entre dois pontos"""
    diff_linha = p1[0] - p2[0]
    diff_coluna = p1[1] - p2[1]
    
    # Calcula valores absolutos sem usar a função abs()
    if diff_linha < 0:
        diff_linha = -diff_linha
    if diff_coluna < 0:
        diff_coluna = -diff_coluna
    
    return diff_linha + diff_coluna

def gerar_permutacoes(elementos):
    """Gera todas as permutações possíveis de uma lista de elementos"""
    if len(elementos) <= 1:
        return [elementos]
    
    resultado = []
    for i in range(len(elementos)):
        elemento_atual = elementos[i]
        elementos_restantes = elementos[:i] + elementos[i+1:]
        for p in gerar_permutacoes(elementos_restantes):
            resultado.append([elemento_atual] + p)
    
    return resultado

def encontrar_rota_otimizada():
    """Encontra a rota mais curta para as entregas do drone"""
    matriz = ler_matriz()
    pontos = encontrar_pontos(matriz)
    
    if 'R' not in pontos:
        return "Ponto R não encontrado"
    
    origem = pontos['R']
    pontos_entrega = [p for p in pontos if p != 'R']
    
    if not pontos_entrega:
        return ""
    
    permutacoes = gerar_permutacoes(pontos_entrega)
    menor_custo = None
    melhor_rota = None
    
    for rota in permutacoes:
        custo = 0
        ponto_atual = origem
        
        for ponto in rota:
            proximo_ponto = pontos[ponto]
            custo += calcular_distancia(ponto_atual, proximo_ponto)
            ponto_atual = proximo_ponto
        
        # Volta para a origem
        custo += calcular_distancia(ponto_atual, origem)
        
        if menor_custo is None or custo < menor_custo:
            menor_custo = custo
            melhor_rota = rota
    
    # Formata a saída como string
    if melhor_rota:
        return ' '.join(melhor_rota)
    return ""

if __name__ == "__main__":
    resultado = encontrar_rota_otimizada()
    print(resultado)