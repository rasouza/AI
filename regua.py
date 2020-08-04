#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Problema():
	def setInit(self, estado):
		self.init = estado
		self.n = int((len(estado)-1)/2)
	def getInit(self):
		return self.init

	def checkGoal(self, R):
		for i in range(2*self.n+1):
			if R[i] == 'B':
				for j in range(i):
					if R[j] == 'A':
						return False
		return True

	def actions(self, R):
		l = [] # lista de jogadas possiveis
		vazio = R.getEstado().index('-') # Posicao do espaço vazio
		rangeEsquerda = range(max(0,vazio-self.n), vazio)
		rangeDireita = range(vazio+1, min(2*self.n+1, vazio+self.n+1))
		ordem = list(reversed(rangeEsquerda)) + list(rangeDireita)
		for i in ordem:
			temp = R.getEstado()[:]
			temp[i], temp[vazio] = temp[vazio], temp[i]
			l.append(Jogada(temp, abs(i - vazio)))
		return l

	def solution(self, jogada, explorados, gerados, verbose = True):

		custo = 0
		passos = 0
		while(jogada.getPai()):
			custo += jogada.getCusto()
			passos += 1
			if verbose:
				print("%s | Custo: %d" % (jogada.getEstado(), jogada.getCusto()))
			jogada = jogada.getPai()
		if verbose:
			print(jogada.getEstado())

		# Estatisticas
			print("Número de nós explorados: %s" % explorados)
			print("Número de nós gerados: %s" % gerados)
			print("Profundidade da meta: %s" % passos)
			print("Custo da solução: %d" % custo)
			print("Fator de ramificação médio: %d" % (gerados/explorados))

		# Retorna a profundidade, necessario para BPL
		return passos

class Jogada():
	def __init__(self, R, custo = 1):
		self.estado = R[:]
		self.explorado = False
		self.pai = None
		self.custo = custo

	def setCusto(self, n):
		self.custo = n
	def getCusto(self):
		return self.custo
	def getCustoRaiz(self):
		custo = 0
		jogada = self
		while jogada.getPai():
			custo += jogada.getCusto()
			jogada = jogada.getPai()
		return custo

	def setPai(self, pai):
		self.pai = pai
	def getPai(self):
		return self.pai

	def setEstado(self, R):
		self.estado = R[:]
	def getEstado(self):
		return self.estado

	def setExplorado(self):
		self.explorado = True
	def explorado(self):
		return self.explorado
	def __str__(self):
		return str(self.getEstado())

	# Workaround para PriorityQueues
	# com nós de mesmo custo,
	# tanto faz a prioridade nesse caso
	def __lt__(self, jogada2):
		return True

def abre(path):
	with open(path, 'r') as f:
		(n, regua) = f.readlines()

	n = int(n)
	R = []
	for v in regua[:-1]:
		R.append(v)

	return [n,R]
