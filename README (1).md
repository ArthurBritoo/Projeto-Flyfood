
# 🛩️ FlyFood

**FlyFood** é um projeto acadêmico que simula um sistema de entregas por drones em uma cidade representada por uma matriz bidimensional. O objetivo principal é otimizar a rota das entregas, minimizando a distância total percorrida com base na **distância de Manhattan** e respeitando as limitações físicas dos drones (movimentação apenas horizontal e vertical).

## 📌 Motivação

A crescente demanda por entregas rápidas nas cidades encontra desafios como congestionamento e altos custos operacionais. Drones surgem como uma alternativa promissora para a logística urbana. No entanto, sua autonomia limitada exige um planejamento rigoroso das rotas para otimizar o consumo de bateria e garantir a viabilidade da operação.

Este projeto propõe soluções computacionais adaptadas do clássico **Problema do Caixeiro Viajante (TSP)**, utilizando algoritmos exatos e heurísticos para lidar com diferentes escalas do problema.

## 🎯 Objetivo

Desenvolver e comparar diferentes estratégias computacionais para encontrar a rota ideal de entregas de um drone, partindo e retornando sempre a um ponto fixo `R`, minimizando a distância total percorrida (em **dronômetros**, nossa unidade baseada na distância de Manhattan).

## 🗂️ Estrutura do Projeto

```
Projeto-Flyfood/
├── 2VA/
│   ├── algoritmo_genetico.py    # Algoritmo Genético com OX e PMX
│   ├── vizinho_mais_proximo.py  # Heurística do Vizinho Mais Próximo
│   ├── forca_bruta.py           # Algoritmo de Força Bruta (Benchmark ótimo)
│   └── flyfood_main.py          # Arquivo principal com a solução híbrida final
├── resultados/                  # Imagens e gráficos dos testes comparativos
├── relatorio/                   # Relatório acadêmico completo
├── pseudo_codigo.txt             # Pseudocódigo geral do projeto
└── README.md                     # Este arquivo
```

### 📌 Sobre cada arquivo `.py` da pasta `2VA`:

- **forca_bruta.py**  
  Algoritmo exato que gera todas as permutações possíveis e retorna a rota ótima.  
  Funciona bem para instâncias pequenas (≤ 9 pontos).

- **vizinho_mais_proximo.py**  
  Heurística gulosa simples que escolhe sempre o ponto mais próximo ainda não visitado.  
  Muito rápida, mas não garante soluções boas para todos os casos.

- **algoritmo_genetico.py**  
  Algoritmo Genético com suporte aos métodos **Order Crossover (OX)** e **Partially Mapped Crossover (PMX)**.  
  Avalia populações de soluções buscando as melhores rotas ao longo das gerações.

- **flyfood_main.py**  
  Arquivo principal que implementa nossa **solução final híbrida**:  
  - Usa **força bruta** quando há 9 pontos ou menos.  
  - Usa **algoritmo genético com OX** para mais de 9 pontos.

> 🔹 Todos esses arquivos permitem rodar matrizes de forma independente, mas **flyfood_main.py** representa nossa solução final recomendada.

## 🖥️ Como Executar

### ✅ Requisitos
- Python 3.10 ou superior  
- Sistema operacional Windows, Linux ou macOS  
- Terminal ou Prompt de Comando

### ▶️ Passos

```bash
git clone https://github.com/ArthurBritoo/Projeto-Flyfood.git
cd Projeto-Flyfood/2VA
```

### Para rodar a solução principal:
```bash
python flyfood_main.py
```

Ou, para testar cada algoritmo individualmente:
```bash
python forca_bruta.py
python vizinho_mais_proximo.py
python algoritmo_genetico.py
```

## 🔧 Detalhes Técnicos

- A matriz é lida manualmente via terminal.
- O ponto inicial e final é `R`.
- Pontos de entrega são letras maiúsculas (`A, B, C...`).
- Movimentação restrita a direções **vertical e horizontal** (não há diagonais).
- A distância é medida pela **distância de Manhattan**.
- O algoritmo genético permite escolher entre **OX e PMX** para o crossover.

## 🧪 Exemplo de Entrada

```
4 5
0 0 0 0 D
0 A 0 0 0
0 0 0 0 C
R 0 B 0 0
```

### ✅ Exemplo de Saída

```
Ordem ótima: A D C B
Custo total: 18 dronômetros
```

## 🔍 Estratégia

### Força Bruta
🔹 Garante a solução ótima, mas inviável com mais de 9 pontos (complexidade O(n!)).

### Vizinho Mais Próximo
🔹 Extremamente rápido (O(n²)), mas pode gerar rotas ruins em certos cenários.

### Algoritmo Genético
🔹 Melhor solução para casos maiores.  
🔹 Permite controle da população, gerações, mutação e crossover (OX e PMX).  
🔹 O **Order Crossover (OX)** se mostrou mais estável e com melhores resultados médios do que o PMX.

## 🚩 Solução Final Recomendada
| Número de Pontos | Método           |
|------------------|------------------|
| ≤ 9              | Força Bruta       |
| > 9              | Algoritmo Genético (OX) |

## 📚 Base Teórica
- Problema do Caixeiro Viajante (TSP)
- Distância de Manhattan
- Algoritmos de Força Bruta
- Heurísticas e Meta-Heurísticas
- Algoritmos Genéticos (Crossover OX e PMX)

## 👥 Autores
Projeto desenvolvido por estudantes do Bacharelado em Sistemas de Informação – UFRPE para a disciplina Projeto Integrador de Sistemas de Informação 2 (PISI2):

- Arthur de Brito Lima  
- Arthur Ferreira Barbosa  
- Carolinne Celestino Corrêa de Amorim  
- Gabriel Sabino Pinho Leite  
- Gustavo Macena Pagnossin  

## 📜 Licença
Projeto acadêmico, disponível para fins educacionais.  
Para uso comercial, entre em contato com os autores.

🔗 [Repositório no GitHub](https://github.com/ArthurBritoo/Projeto-Flyfood)
