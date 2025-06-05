def ler_matriz_flyfood():
    """
    Lê a matriz da entrada padrão.
    A primeira linha contém as dimensões (linhas colunas).
    As linhas seguintes contêm os elementos da matriz.
    Evita map() para conversão inicial de dimensões.
    """
    dimensoes_str = input().split()  # Ex: ['4', '5']
    numero_linhas = int(dimensoes_str[0])
    # numero_colunas = int(dimensoes_str[1])  # Não é estritamente usado abaixo

    matriz = []
    for _ in range(numero_linhas):
        # input().strip().split() lê uma linha, remove espaços extras e divide em uma lista.
        linha_matriz = input().strip().split()
        matriz.append(linha_matriz)
    return matriz

def encontrar_pontos(matriz):
    """
    Encontra as coordenadas de todos os pontos nomeados na matriz.
    Retorna um dicionário {nome_ponto: (linha, coluna)}.
    """
    pontos = {}
    numero_linhas = len(matriz)
    if numero_linhas == 0:
        return pontos
    numero_colunas = len(matriz[0])

    for i in range(numero_linhas):
        for j in range(numero_colunas):
            valor = matriz[i][j]
            if valor != "0":
                pontos[valor] = (i, j)
    return pontos

def distancia_manhattan(p1, p2):
    """
    Calcula a distância de Manhattan entre dois pontos p1 e p2.
    p1 e p2 são tuplas (linha, coluna).
    Implementa abs() manualmente.
    """
    # Diferença nas linhas
    diferenca_linhas = p1[0] - p2[0]
    if diferenca_linhas < 0:
        diferenca_absoluta_linhas = -diferenca_linhas
    else:
        diferenca_absoluta_linhas = diferenca_linhas

    # Diferença nas colunas
    diferenca_colunas = p1[1] - p2[1]
    if diferenca_colunas < 0:
        diferenca_absoluta_colunas = -diferenca_colunas
    else:
        diferenca_absoluta_colunas = diferenca_colunas
    
    return diferenca_absoluta_linhas + diferenca_absoluta_colunas

def gerar_permutacoes(elementos):
    """
    Gera todas as permutações de uma lista de elementos.
    Implementação recursiva sem usar bibliotecas como itertools.
    """
    if len(elementos) == 0:
        return [[]]  # Uma permutação da lista vazia é uma lista contendo uma lista vazia
    
    if len(elementos) == 1:
        return [elementos[:]]  # Retorna uma lista contendo uma cópia da lista original

    todas_as_permutacoes = []
    for i in range(len(elementos)):
        novo_elemento = elementos[i]
        
        # Cria a lista de elementos restantes
        elementos_restantes = []
        for j in range(len(elementos)):
            if i != j:
                elementos_restantes.append(elementos[j])
        
        permutacoes_dos_restantes = gerar_permutacoes(elementos_restantes)
        
        for p_restante in permutacoes_dos_restantes:
            # Constrói a nova permutação manualmente
            nova_permutacao = [novo_elemento]
            for item in p_restante:
                nova_permutacao.append(item)
            todas_as_permutacoes.append(nova_permutacao)
            
    return todas_as_permutacoes

def resolver_flyfood_forca_bruta():
    """
    Resolve o problema FlyFood usando força bruta.
    """
    matriz = ler_matriz_flyfood()
    coordenadas_dos_pontos = encontrar_pontos(matriz)

    if 'R' not in coordenadas_dos_pontos:
        # Caso onde o ponto de origem R não é encontrado.
        # Dependendo dos requisitos, pode retornar erro ou uma string vazia.
        return "Ponto R não encontrado" 

    origem_r = coordenadas_dos_pontos['R']
    
    pontos_de_entrega = []
    # Coleta nomes dos pontos de entrega (todos exceto 'R')
    # A ordem aqui pode depender da implementação do dicionário se não for ordenado.
    # Para garantir consistência (opcional), poderia ordenar os nomes antes de permutar,
    # mas a força bruta testará todas as ordens de qualquer maneira.
    for nome_ponto in coordenadas_dos_pontos:
        if nome_ponto != 'R':
            pontos_de_entrega.append(nome_ponto)

    if not pontos_de_entrega:  # Nenhum ponto de entrega
        return ""

    todas_as_rotas = gerar_permutacoes(pontos_de_entrega)
    
    menor_custo_total = -1  # Usado para armazenar a menor distância encontrada
                            # Inicializado com -1 ou um número muito grande
    melhor_rota = []

    for sequencia_entrega_atual in todas_as_rotas:
        custo_total_atual = 0
        ponto_anterior = origem_r  # Começa em R
        
        # Calcula a distância do percurso: R -> P1 -> P2 -> ... -> Pn
        for nome_ponto in sequencia_entrega_atual:
            ponto_atual = coordenadas_dos_pontos[nome_ponto]
            custo_total_atual += distancia_manhattan(ponto_anterior, ponto_atual)
            ponto_anterior = ponto_atual
        
        # Adiciona a distância do último ponto de entrega de volta para R
        custo_total_atual += distancia_manhattan(ponto_anterior, origem_r)
        
        if menor_custo_total == -1 or custo_total_atual < menor_custo_total:
            menor_custo_total = custo_total_atual
            melhor_rota = sequencia_entrega_atual
            
    # Formata a saída como uma string "P1 P2 P3"
    resultado_str = ""
    if melhor_rota:  # Se encontrou alguma rota (lista não vazia)
        resultado_str = melhor_rota[0]
        for i in range(1, len(melhor_rota)):
            resultado_str += " " + melhor_rota[i]
            
    return resultado_str

if __name__ == "__main__":
    # Exemplo de como chamar a função principal e imprimir o resultado
    # O input será lido do console/terminal
    melhor_rota_str = resolver_flyfood_forca_bruta()
    print(melhor_rota_str)


