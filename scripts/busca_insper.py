# coding: utf8

import os
import math 
import numpy as np
from map.occupancy_grid import OccupancyGrid

import projeto_busca

FRONTEIRA = (255, 255, 0)
ANALISADO = (50, 255, 50)
ROTA = (255, 0, 0)

# Load map and lines
filedir = os.path.dirname(os.path.abspath(__file__))
map_name = os.path.normpath(os.path.normpath(filedir+'/../maps/map.yaml'))

# Build the map
map = OccupancyGrid(map_name)

class Node:
    def __init__(self, pos, custo, anterior, heuristica=0):
        self.posicao = pos
        self.custo = anterior.custo + custo if anterior else custo
        self.pai = anterior
        self.heuristica = heuristica


class Model:
    def __init__(self, mapa, passo, destino):
        self.map = mapa
        self.step = passo
        self.destino = destino

    def sucessor(self, pos):
        '''
        Define as posições sucessoreas no mapa
        '''
        next_ = list()
        candidates = (
            (pos[0] + self.step, pos[1]),
            (pos[0] + self.step, pos[1] + self.step),
            (pos[0], pos[1] + self.step),
            (pos[0] - self.step, pos[1] + self.step),
            (pos[0] - self.step, pos[1]),
            (pos[0] - self.step, pos[1] - self.step),
            (pos[0], pos[1] - self.step),
            (pos[0] + self.step, pos[1] - self.step)
        )
        for candidate in candidates:
            if map.contains(candidate[0], candidate[1]) and\
                map.can_move(pos[0], pos[1], candidate[0], candidate[1]):
                next_.append(candidate)

        return next_

    def termino(self, pos):
        ''' Verifica se `pos` é a posição mais próxima ao destino
            algum considerando o passo do problema
        '''
        return abs(self.destino[0] - pos[0]) <= self.step/2 and\
               abs(self.destino[1] - pos[1]) <= self.step/2

    def custo(self, pos0, pos1):
        return projeto_busca.calcula_custo(pos0, pos1)

    def heuristica(self, pos):
        return projeto_busca.calcula_heuristica(pos, self.destino)

    def gera_imagem(self, fronteira, visitados, caminho):
        img = np.ones_like(map.color_image)*255
        
        for pos in visitados:
            min_j, min_i = self.map.convert_to_grid((pos[0]-self.step/2, pos[1]-self.step/2))
            max_j, max_i = self.map.convert_to_grid((pos[0]+self.step/2, pos[1]+self.step/2))
            img[int(min_i):int(max_i), int(min_j):int(max_j), :] = ANALISADO

        for node in fronteira:
            min_j, min_i = self.map.convert_to_grid((node.posicao[0]-self.step/2, node.posicao[1]-self.step/2))
            max_j, max_i = self.map.convert_to_grid((node.posicao[0]+self.step/2, node.posicao[1]+self.step/2))
            img[int(min_i):int(max_i), int(min_j):int(max_j), :] = FRONTEIRA

        for node in caminho:
            min_j, min_i = self.map.convert_to_grid((node.posicao[0]-self.step/2, node.posicao[1]-self.step/2))
            max_j, max_i = self.map.convert_to_grid((node.posicao[0]+self.step/2, node.posicao[1]+self.step/2))
            img[int(min_i):int(max_i), int(min_j):int(max_j), :] = ROTA
        
        return img


