#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import *
import pdb

#__________________________________
#
# Definição do problema específico
#__________________________________

class Travessia(Problem):

    def __init__(self, path):
        self.t = []
        self.initial = []
        with open(path, 'r') as f:
            (self.n, self.MAX) = f.readline().split(' ')
            self.n = int(self.n)
            self.MAX = int(self.MAX)

            f.readline() # Pula uma linha em branco

            for line in f:
                self.t.append(int(line))

        for n in range(self.n):
            self.initial.append(1)
        self.initial.append('O') # Posicao da lanterna

        self.initial = self.estado(self.initial)

    def estado(self, state):
        return ''.join(str(i) for i in state)

    def successor(self, state):
        l = [] # lista de jogadas possiveis
        state = list(state)

        # Ir com a lanterna (até 2)
        if state[-1] == 'O':
            for i in range(len(state) - 1): # Ńao iterar sobre a posicao da lanterna
                for j in range(i+1, len(state) - 1):
                    temp = state[:]
                    temp[-1] = 'L'

                    if temp[i] == '1' and temp[j] == '1':
                        temp[i] = 0
                        temp[j] = 0
                        l.append((str(i) + ' ' + str(j) + ' ' + temp[-1], self.estado(temp)))
                    elif temp[i] == '1':
                        temp[i] = 0
                        l.append((str(i) + ' ' + temp[-1], self.estado(temp)))

        # Voltar com a lanterna (apenas 1)
        if state[-1] == 'L':
            for i in range(len(state) - 1): # Ńao iterar sobre a posicao da lanterna
                temp = state[:]
                temp[-1] = 'O'
                if temp[i] == '0':
                    temp[i] = 1
                    l.append((str(i) + ' ' + temp[-1], self.estado(temp)))
        return l

    def goal_test(self, state):
        n = len(state) - 1
        return state == (n*'0' + 'L')

    def path_cost(self, c, state1, action, state2):
        acao = action.split(' ')
        custo = 0
        if len(acao) == 3: # Dois foram movidos
            return max(self.t[int(acao[0])], self.t[int(acao[1])]) + c
        elif len(acao) == 2: # Apenas 1 se moveu
            return self.t[int(acao[0])] + c

    def h(self, node):
        tempo = [self.t[k] for k, v in enumerate(node.state) if v == '1']
        return min(tempo)

def solution(node, problem):
    for n in node.path()[::-1]:
        if n.action is not None:
            acao = n.action.split(' ')
            if len(acao) == 3:
                if acao[2] == 'L': sentido = '>>'
                if acao[2] == 'O': sentido = '<<'
                print problem.t[int(acao[0])], problem.t[int(acao[1])], sentido
            elif len(acao) == 2:
                if acao[1] == 'L': sentido = '>>'
                if acao[1] == 'O': sentido = '<<'
                print problem.t[int(acao[0])], sentido
    print 'Custo:', node.path_cost

#__________________________________
#
# Programa
#__________________________________

p = Travessia('travessia.txt')


print "Solucao do caminho sem se importar com o tempo MAX"
print "==================================================="
solucao = BL(p)
solution(solucao,p)

print "Solucao do caminho de menor tempo possível"
print "==================================================="
solucao = BCU(p)
solution(solucao,p)

print "Solucao do caminho usando busca informada"
print "==================================================="
solucao = a_estrela(p, p.h)
solution(solucao,p)

