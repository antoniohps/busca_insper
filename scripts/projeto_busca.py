# coding: utf8
import math
import random
from collections import deque
from sortedcontainers import SortedKeyList
'''
Arquivo contendo as variáveis e funções que devem ser
ajustadas para a execuçã odo projeto
'''

# ======= Variáveis de interesse do projeto
# --- Postura (x, y, theta) inicial do robô, em metros/radianos
robot = (0 ,0, math.pi/4)
# --- Posição (x, y) de destino do robô, em metros
destino = (5, 5)
# --- Passo de discretização do mapa, em metros
passo = 0.5
# --- Tipo de busca
tipos_busca = ["largura", "profundidade", "custo uniforme", "gulosa", "A*"]

tipo_busca = "largura"
fronteira = deque()

# ===================================================
# Inicializa a fronteira a partir do tipo de busca a ser
# realizada. O tipo de lista usada depende do tipo de busca:
# ---- Busca em largura ou profundidade: uma lista duplamente encadeada
#      (deque) é usada como fila (FIFO) ou pilha (LIFO), dependendo
#      da posição onde os nodes são reitrados
# ---- Busca de custo uniforme, gulosa ou A*: usamos uma lista ordenada
#      pela função de custo total (SortedKeyList)  

def set_numero_busca(num):
    """ Define  o tipo de busca a ser realizada """
    global fronteira
    global tipo_busca
    if 0 <= num <= 1:
        fronteira = deque()
    elif 2 <= num <len (tipos_busca):
        fronteira = SortedKeyList(key=custo_total)
    else: raise ValueError()
    tipo_busca = tipos_busca[num]


# ============== Insere na fronteira ===================#
# Usa a API da `deque` ou da SortedKeyList para inserir um novo node 
def insere_fronteira(node):
    if tipo_busca == "largura" or tipo_busca == "profundidade":
        fronteira.append(node)
    else: 
        fronteira.add(node)

# ============== Retira da fronteira ===================#
# Usa a API da `deque` ou da SortedKeyList para remover e retorna um novo node 
def retira_fronteira():
    if tipo_busca == "largura":
        return fronteira.popleft()
    elif tipo_busca == "profundidade":
        return fronteira.pop()
    else: return fronteira.pop(0)
    

# ============== Atividade 1 ===================#
# Implementar a função `calcula_custo(pos0, pos1)` que calcula a distância
# euclidiana de pos0=(x0, y0) a pos1=(x1, y1)
def calcula_custo(pos0, pos1):
    return 1 
    
# ============== Atividade 2 ===================#
# Implementar a função `calcula_heurísica(pos0, pos1)` que calcula a distância
# de pos0=(x0, y0) a pos1=(x1, y1).
# Pode escolher entre distância Manhattan, xadrez ou euclidiana
def calcula_heuristica(pos0, pos1):
    return 0 

# ============== Atividade 3 ===================#
# Implementar a função `custo_total(node)` que calcula o custo total
# usado para encontrar a ordem de análise dos nodes da fronteira.
# Depende do tipo de busca sendo realizada (custo unforme, gulosa ou A*)
def custo_total(node):
    # TODO
    pass