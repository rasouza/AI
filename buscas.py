# -*- coding: utf-8 -*-

import pdb
import sys
from queue import *
from heapq import *
from regua import *

def BL(problema):
    start = Jogada(problema.getInit(), 0) # Inicia o problema com Estado Inicial e Custo 0
    explorados = [] # Inicializa a lista dos estados explorados
    gerados = 0 # Número de nós gerados
    borda = Queue() # Borda FIFO
    borda.put(start)

    # Teste de meta
    if problema.checkGoal(start.getEstado()):
        return start, len(explorados), gerados

    # Enquanto a pilha existir
    while (borda.qsize() > 0):
        jogada = borda.get()
        explorados.append(jogada.getEstado()) # Explora o estado

        jogadas = p.actions(jogada) # Expande os nós-filho
        gerados += len(jogadas)
        # Gera todas as ações possiveis a partir de uma jogada
        for jogadaPossivel in jogadas:
            if jogadaPossivel.getEstado() not in explorados:
                borda.put(jogadaPossivel)
                jogadaPossivel.setPai(jogada)

                #Teste de meta
                if p.checkGoal(jogadaPossivel.getEstado()):
                    return jogadaPossivel, len(explorados), gerados

    return -1 # Falha, não achou nenhuma solução

def BP(problema):
    start = Jogada(problema.getInit(), 0) # Inicia o problema com Estado Inicial e Custo 0
    explorados = [] # Inicializa a lista dos estados explorados
    gerados = 0 # Número de nós gerados
    borda = [start] # Borda LIFO

    # Teste de meta
    if problema.checkGoal(start.getEstado()):
        return start, len(explorados), gerados

    # Enquanto a pilha existir
    while (len(borda) > 0):
        jogada = borda.pop()
        explorados.append(jogada.getEstado()) # Explora o estado

        jogadas = p.actions(jogada) # Expande os nós-filho
        gerados += len(jogadas)
        # Gera todas as ações possiveis a partir de uma jogada
        for jogadaPossivel in jogadas:
            if jogadaPossivel.getEstado() not in explorados:
                borda.append(jogadaPossivel)
                jogadaPossivel.setPai(jogada)

                #Teste de meta
                if p.checkGoal(jogadaPossivel.getEstado()):
                    return jogadaPossivel, len(explorados), gerados

    return -1 # Falha, não achou nenhuma solução

def BPL(problema, limite):
    def BPLrecursiva(jogada, problema, limite, explorados, gerados):
        if problema.checkGoal(jogada.getEstado()):
            return jogada
        elif limite == 0:
            return 'corte'
        else:
            corte_ocorreu = False
            jogadas = problema.actions(jogada)

            # Como listas são mutáveis, é possível passar
            # a variavel como referência
            gerados[0] += len(jogadas)

            for jogadaPossivel in jogadas:
                jogadaPossivel.setPai(jogada)

                # Como listas são mutáveis, é possível passar
                # a variavel como referência
                explorados[0] += 1

                resultado = BPLrecursiva(jogadaPossivel, problema, limite-1, explorados, gerados)
                if resultado == 'corte':
                    corte_ocorreu = True
                elif resultado != -1:
                    return resultado
            if corte_ocorreu == True:
                return 'corte'
            else:
                return -1
    explorados = gerados = [0]
    jogada = BPLrecursiva(Jogada(problema.getInit(),0), problema, limite, explorados, gerados)
    return jogada, explorados[0], gerados[0]

# TO-DO Fazer a contagem de nós gerados e explorados
def BPI(problema):
    falha = False
    limite = 0
    while not falha:
        resultado, explorados, gerados = BPL(problema, limite)
        if resultado == -1:
            return -1 # Falha
        elif type(resultado) is Jogada:
            return resultado, explorados, gerados # Sucesso
        limite += 1

def BCU(problema):
    def procura_custo_maior(borda, estado, custo):
        ''' Retorna a posição do nó na borda com custo
            maior que o custo especificado '''
        lista = list(filter(lambda v: v[1] == estado and v[0] > custo, borda.queue))
        if lista:
            return borda.queue.index(lista[0])
        else:
            return False

    start = Jogada(problema.getInit(), 0) # Problema inicial de Custo 0
    borda = PriorityQueue() # Fronteira como Fila de prioridades
    borda.put((0, start))
    explorados = []
    gerados = 0

    while(not borda.empty()):
        custo, jogada = borda.get()

        explorados.append(jogada.getEstado())

        # Teste de meta
        if problema.checkGoal(jogada.getEstado()):
            return jogada, len(explorados), gerados

        # Expande as jogadas possiveis
        jogadas = problema.actions(jogada)
        gerados += len(jogadas)
        for jogadaPossivel in jogadas:
            jogadaPossivel.setPai(jogada)
            if jogadaPossivel.getEstado() not in explorados:
                borda.put((jogadaPossivel.getCusto() + custo, jogadaPossivel))

            # Verifica se existe uma jogada na borda com custo maior,
            # então faz a troca
            troca = procura_custo_maior(borda, jogadaPossivel.getEstado(), jogadaPossivel.getCusto() + custo)
            if troca:
                del borda.queue[troca]
                borda.put((jogadaPossivel.getCusto() + custo, jogadaPossivel))

    return -1 # Falha

def A_estrela(problema, h):
    def procura_custo_maior(borda, estado, custo):
        ''' Retorna a posição do nó na borda com custo
            maior que o custo especificado '''
        lista = list(filter(lambda v: v[1] == estado and v[0] > custo, borda.queue))
        if lista:
            return borda.queue.index(lista[0])
        else:
            return False

    start = Jogada(problema.getInit(), 0) # Problema inicial de Custo 0
    borda = PriorityQueue() # Fronteira como Fila de prioridades
    borda.put((0, start))
    explorados = []
    gerados = 0

    while(not borda.empty()):
        f, jogada = borda.get()
        print("Utilizando jogada de custo %d" % f)
        explorados.append(jogada.getEstado())

        # Teste de meta
        if problema.checkGoal(jogada.getEstado()):
            return jogada, len(explorados), gerados

        # Expande as jogadas possiveis
        jogadas = problema.actions(jogada)
        gerados += len(jogadas)
        for jogadaPossivel in jogadas:
            jogadaPossivel.setPai(jogada)
            if jogadaPossivel.getEstado() not in explorados:
                f = jogadaPossivel.getCustoRaiz() + max([heuristica(jogadaPossivel.getEstado()) for heuristica in h])
                borda.put((f, jogadaPossivel))

            # Verifica se existe uma jogada na borda com custo maior,
            # então faz a troca
            troca = procura_custo_maior(borda, jogadaPossivel.getEstado(), f)
            if troca:
                del borda.queue[troca]
                borda.put((f, jogadaPossivel))

    return -1 # Falha


p = Problema()
n, R = abre('regua.txt')
p.setInit(R)

if sys.argv[1] == 'BL':
    solucao = BL(p)
    p.solution(*solucao)
elif sys.argv[1] == 'BP':
    solucao = BP(p)
    p.solution(*solucao)
elif sys.argv[1] == 'BPL':
    solucao = BL(p)
    d = p.solution(*solucao, verbose = False)

    # Limite aumentado em 10% do limite da BL
    print('\n===== LIMITE: %d =====' % (d*1.10))
    solucao = BPL(p, int(d*1.10))
    p.solution(*solucao)

    # Limite aumentado em 20% do limite da BL
    print('\n===== LIMITE: %d =====' % (d*1.20))
    solucao = BPL(p, int(d*1.20))
    p.solution(*solucao)

    # Limite aumentado em 30% do limite da BL
    print('\n===== LIMITE: %d =====' % (d*1.30))
    solucao = BPL(p, int(d*1.30))
    p.solution(*solucao)
elif sys.argv[1] == 'BPI':
    solucao = BPI(p)
    p.solution(*solucao)
elif sys.argv[1] == 'BCU':
    solucao = BCU(p)
    p.solution(*solucao)
elif sys.argv[1] == 'A*':
    def h1(n):
        ''' Número de casas fora do estado-meta '''
        goal = ['B', 'B', 'B', '-', 'A', 'A', 'A']
        return sum(i != j for i, j in zip(n,goal))
    def h2(n):
        ''' Distancia das casas ate a meta '''
        distancias = 0
        for k, i in enumerate(n[:]):
            goal = ['B', 'B', 'B', '-', 'A', 'A', 'A']
            indice = goal.index(i)
            if abs(indice - k) <= 3:
                distancias += abs(indice - k)
            goal[indice] = '*' # Elimina a posição para não contar espaços repetidos
        return distancias
    solucao = A_estrela(p, [h1,h2])
    p.solution(*solucao)


# BP(p)
# BPL(p, 100)
# BPI(p)
# BCU(p)
