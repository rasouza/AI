#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import *

#__________________________________
#
# Definição do problema específico
#__________________________________

class ReguaPuzzle(Problem):

    def __init__(self, path):
        with open(path, 'r') as f:
            (n, regua) = f.readlines()

        n = int(n)
        self.initial = regua[:-1]

    def successor(self, state):
        l = [] # lista de jogadas possiveis
        vazio = state.index('-') # Posicao do espaço vazio
        n = (len(state)-1)/2
        rangeEsquerda = range(max(0, vazio - n), vazio)
        rangeDireita = range(vazio + 1, min(2 * n + 1, vazio + n + 1))
        ordem = list(reversed(rangeEsquerda)) + list(rangeDireita)
        for i in ordem:
            temp = list(state)
            temp[i], temp[vazio] = temp[vazio], temp[i]
            l.append((temp.index('-'), ''.join(temp)))
        return l

    def goal_test(self, state):
        n = (len(state)-1)/2
        for i in range(2*n+1):
            if state[i] == 'B':
                for j in range(i):
                    if state[j] == 'A':
                        return False
        return True

    def path_cost(self, c, state1, action, state2):
        vazio1 = state1.index('-')
        vazio2 = state2.index('-')
        return abs(vazio2 - vazio1) + c


    def h1(self, node):
        """Número de casas fora do estado-meta"""
        count = 0
        for i,k in enumerate(node.state):
            if node.state[i] == 'A':
                count += node.state[i:].count('B')
        return count


    def h2(self, node):
        ''' Distancia das casas ate a meta '''
        n = (len(node.state)-1)/2
        index = node.state.index('-')
        if index <= 4:
            b = node.state[:n+1]
            a = node.state[n+1:]
        else:
            b = node.state[:n]
            a = node.state[n:]
        return b.count('A') + a.count('B')


def solution(node, problem):
    print "caminho:"
    for n in node.path()[::-1]:
        print n.state, "|", n.path_cost
    print "Nós explorados: %d" % p.explorados
    print "Nós gerados: %d" % p.gerados
    print "Profundidade: %d" % node.depth
    print "Custo: %d" % node.path_cost
    print "Fator de ramificação médio: %d" % int(p.gerados/p.explorados)

#__________________________________
#
# Programa
#__________________________________

p = ReguaPuzzle('regua1.txt')

if len(sys.argv) == 1:
    print sys.argv[0], "precisa de ao menos um parametro para rodar (BL, BP, BPL, BPI, BCU, A*, IDA*, RBFS)"
    sys.exit(0)

if sys.argv[1] == 'BL':
    solucao = BL(p)
elif sys.argv[1] == 'BP':
    solucao = BP(p)
elif sys.argv[1] == 'BPL':
    solucao = BL(p)
    d = solucao.depth

    # Limite aumentado em 10% do limite da BL
    print('\n===== LIMITE: %d =====' % (d*1.10))
    solucao = BPL(p, int(d*1.10))
    solution(solucao, p)

    # Limite aumentado em 20% do limite da BL
    print('\n===== LIMITE: %d =====' % (d*1.20))
    solucao = BPL(p, int(d*1.20))
    solution(solucao, p)

    # Limite aumentado em 30% do limite da BL
    print('\n===== LIMITE: %d =====' % (d*1.30))
    solucao = BPL(p, int(d*1.30))
    solution(solucao, p)
    sys.exit(0)

elif sys.argv[1] == 'BPI':
    solucao = BPI(p)
elif sys.argv[1] == 'BCU':
    solucao = BCU(p)
elif sys.argv[1] == 'A*':
    solucao = a_estrela(p, [p.h1, p.h2])
elif sys.argv[1] == 'IDA*':
    solucao = IDA_estrela(p, p.h1)
elif sys.argv[1] == 'RBFS':
    solucao = RBFS(p, h1)

print sys.argv[1]
solution(solucao, p)
print "\n\n"

