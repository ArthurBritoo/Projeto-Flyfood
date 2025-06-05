# 🛩️ FlyFood

**FlyFood** é um projeto acadêmico que simula um sistema de entregas por drones em uma cidade representada por uma matriz. O objetivo é otimizar a rota de entregas, minimizando a distância total percorrida com base na **distância de Manhattan**, respeitando restrições de movimentação e a autonomia da bateria do drone.

## 📌 Motivação

Com o crescimento da logística urbana e os desafios enfrentados por empresas de delivery (como trânsito intenso e altos custos operacionais), a automação com drones surge como uma solução promissora. No entanto, a autonomia limitada desses dispositivos exige um planejamento eficiente das rotas.

Este projeto propõe uma abordagem inspirada no **Problema do Caixeiro Viajante (TSP)**, adaptada para movimentação apenas horizontal e vertical em uma matriz bidimensional.

## 🎯 Objetivo

Desenvolver um algoritmo que determine a sequência ideal de visitas aos pontos de entrega por um drone, partindo e retornando a um ponto fixo (`R`), minimizando o custo total em **dronômetros** (unidade de distância com base na distância de Manhattan).

## 🗂️ Estrutura do Projeto
<pre lang="markdown"> 
Projeto-Flyfood/
├── flyfood.py # Código principal com algoritmo de força bruta
├── entrada_exemplo.txt # (Opcional) Exemplo de entrada
├── relatorios/ # Documentos e relatórios do projeto
└── README.md # Este arquivo
</pre>

## 🖥️ Como executar

### ✅ Requisitos

- Python 3.9 ou superior
- Sistema operacional Windows, Linux ou macOS
- Terminal ou prompt de comando

### ▶️ Passo a passo

#### 1. Clone o repositório:

```bash
git clone https://github.com/ArthurBritoo/Projeto-Flyfood.git
cd Projeto-Flyfood
```
#### Execute o script:
```bash
python flyfood.py
```
#### Quando solicitado, digite ou cole a matriz de entrada:
```code
4 5
0 0 0 0 D
0 A 0 0 0
0 0 0 0 C
R 0 B 0 0
```
#### A saída será a ordem ótima dos pontos de entrega, por exemplo:

```code
A D C B
```
## 🔧 Detalhes Técnicos
- A matriz é lida da entrada padrão (input manual no terminal).

- O ponto de origem e retorno é sempre marcado com R.

- Os pontos de entrega são letras maiúsculas (A, B, C...).

- A movimentação é permitida apenas nas direções horizontal e vertical.

- A distância entre dois pontos é calculada com base na distância de Manhattan.

- Permutações são geradas manualmente, sem uso de bibliotecas como itertools.

### 🧪 Exemplo de Entrada
```code
4 5
0 0 0 0 D
0 A 0 0 0
0 0 0 0 C
R 0 B 0 0
```
### ✅ Exemplo de Saída
```code
A D C B
```
## 🔍 Estratégia
Este projeto utiliza um algoritmo exato de força bruta, que testa todas as possíveis ordens de entrega e retorna a que possui o menor custo total de deslocamento. É uma abordagem viável apenas para instâncias pequenas (até 6 ou 7 entregas), devido à complexidade exponencial (O(n!)).

## 🚧 Trabalhos Futuros
- Implementar heurísticas como:

  - Vizinho Mais Próximo

  - 2-opt

- Comparar desempenho com a força bruta

- Permitir leitura direta de arquivos .txt

- Suportar múltiplos drones

- Adicionar interface visual ou simulação gráfica

## 📚 Base Teórica
- Problema do Caixeiro Viajante (TSP)

- Distância de Manhattan

- Complexidade Computacional

- Algoritmos de força bruta

- Heurísticas para otimização de rotas

## 👥 Autores
Projeto desenvolvido por estudantes do Bacharelado em Sistemas de Informação – UFRPE para a disciplina Projeto Integrador de Sistemas de Informação 2 (PISI2):

- Arthur de Brito Lima

- Arthur Ferreira Barbosa

- Carolinne Amorim

- Gabriel Sabino Pinho Leite

- Gustavo Macena

## 📜 Licença
Este projeto é de caráter acadêmico e está disponível para uso educacional. Para uso comercial ou profissional, entre em contato com os autores.

Repositório no GitHub:
🔗 https://github.com/ArthurBritoo/Projeto-Flyfood

---








