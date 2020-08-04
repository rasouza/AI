# -*- coding: utf-8 -*-

import bisect, sys, pdb

#__________________________________
#
# Modelo de Problema e Nó genéricos
#
# *A ideia foi baseada no AIMA-python
# (Artificial Inteligence: a Modern
# Approach)
#
# *Modificações: contar o número de
# nós explorados, nós gerados, custo
# total do caminho
#__________________________________

class Problem:
    """The abstract class for a formal problem.  You should subclass this and
    implement the method successor, and possibly __init__, goal_test, and
    path_cost. Then you will create instances of your subclass and solve them
    with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

        self.explorados = 0
        self.gerados = 0

    def successor(self, state):
        """Given a state, return a sequence of (action, state) pairs reachable
        from this state. If there are many successors, consider an iterator
        that yields the successors one at a time, rather than building them
        all at once. Iterators will work fine within the framework."""
        abstract

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Implement this
        method if checking against a single self.goal is not enough."""
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self):
        """For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value."""
        abstract

class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state.  Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node.  Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        "Create a search tree Node, derived from a parent by an action."
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0

        self.f = 0 # Apenas para o caso RBFS

        if parent:
            self.depth = parent.depth + 1



    def __repr__(self):
        return "<Node %s>" % (self.state,)

    def path(self):
        "Create a list of nodes from the root to this node."
        x, result = self, [self]
        while x.parent:
            result.append(x.parent)
            x = x.parent
        return result

    def expand(self, problem):
        "Return a list of nodes reachable from this node. [Fig. 3.8]"
        return [Node(next, self, act,
                     problem.path_cost(self.path_cost, self.state, act, next))
                for (act, next) in problem.successor(self.state)]

#__________________________________
#
# Utils
#__________________________________

class Queue:
    def __init__(self):
        abstract
    def extend(self, items):
        for item in items: self.append(item)

def Stack():
    return [] # Stack é uma lista nativa do python

class FIFOQueue(Queue):
    """A First-In-First-Out Queue."""
    def __init__(self):
        self.A = []; self.start = 0
    def append(self, item):
        self.A.append(item)
    def __len__(self):
        return len(self.A) - self.start
    def extend(self, items):
        self.A.extend(items)
    def pop(self):
        e = self.A[self.start]
        self.start += 1
        if self.start > 5 and self.start > len(self.A)/2:
            self.A = self.A[self.start:]
            self.start = 0
        return e

class PriorityQueue(Queue):
    """Fila de prioridades para buscas de custo uniforme"""
    def __init__(self, order=min, f=lambda x: x):

        self.A = []
        self.order = order
        self.f = f
    def append(self, item):
        bisect.insort(self.A, (self.f(item), item))
    def __len__(self):
        return len(self.A)
    def pop(self):
        if self.order == min:
            return self.A.pop(0)[1]
        else:
            return self.A.pop()[1]

def memoize(fn, slot=None):
    """Memoize fn: make it remember the computed value for any argument list.
    If slot is specified, store result in that slot of first argument.
    If slot is false, store results in a dictionary."""
    if slot:
        def memoized_fn(obj, *args):
            if hasattr(obj, slot):
                return getattr(obj, slot)
            else:
                val = fn(obj, *args)
                setattr(obj, slot, val)
                return val
    else:
        def memoized_fn(*args):
            if not memoized_fn.cache.has_key(args):
                memoized_fn.cache[args] = fn(*args)
            return memoized_fn.cache[args]
        memoized_fn.cache = {}
    return memoized_fn

infinity = 1.0e400
#__________________________________
#
# Implementação dos algoritmos utilizados
#__________________________________

def busca_em_arvore(problem, borda):
    """Busca por sucessores de um nó sem se
    preocupar por nós repetidos"""

    # Inicializa a borda com o problema inicial
    problem.explorados = problem.gerados = 0
    borda.append(Node(problem.initial))
    while borda:
        node = borda.pop()
        problem.explorados += 1
        if problem.goal_test(node.state):
            return node
        borda.extend(node.expand(problem))
        problem.gerados += len(node.expand(problem))
    return None

def busca_em_grafo(problem, borda):
    """Busca por nós em um dado problema evitando
    nós repetidos"""

    # Inicializa a borda com o problema inicial
    # e nós explorados vazio
    closed = {}
    borda.append(Node(problem.initial))
    problem.explorados = problem.gerados = 0
    while borda:
        node = borda.pop()
        problem.explorados += 1
        if problem.goal_test(node.state):
            return node
        if node.state not in closed:
            closed[node.state] = True
            suc = node.expand(problem)
            borda.extend(suc)
            problem.gerados += len(suc)
    return None

def BL(problem):
    return busca_em_grafo(problem, FIFOQueue())
def BP(problem):
    return busca_em_grafo(problem, Stack())

def BPL(problem, limit=50):
    def recursive_dls(node, problem, limit):
        corte_ocorreu = False
        if problem.goal_test(node.state):
            return node
        elif node.depth == limit:
            return 'corte'
        else:
            problem.gerados += len(node.expand(problem))
            for successor in node.expand(problem):
                result = recursive_dls(successor, problem, limit)
                problem.explorados += 1
                if result == 'corte':
                    corte_ocorreu = True
                elif result != None:
                    return result
        if corte_ocorreu:
            return 'corte'
        else:
            return None
    # Fim recursive_dls()
    problem.explorados = problem.gerados = 0
    return recursive_dls(Node(problem.initial), problem, limit)

def BPI(problem):
    explorados = gerados = 0
    for depth in xrange(sys.maxint):
        result = BPL(problem, depth)
        gerados += problem.gerados
        explorados += problem.explorados
        if result is not 'corte':
            problem.gerados = gerados
            problem.explorados = explorados
            return result

def BCU(problem):
    def total_cost(node):
        "Return the total cost to reach the root node"
        cost = 0
        for n in node.path():
            cost += n.path_cost
        return cost
    # Fim total_cost()
    return busca_em_grafo(problem, PriorityQueue(min, total_cost))

def best_first_search(problem, f):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have depth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    return busca_em_grafo(problem, PriorityQueue(min, f))

def a_estrela(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search.
    Uses the pathmax trick: f(n) = max(f(n), g(n)+h(n))."""
    h = h or problem.h
    def f(n):
        # Caso de heuristicas compostas
        if type(h) is list:
            heuristicas = [x(n) for x in h]
            return max(getattr(n, 'f', -infinity), n.path_cost + max(heuristicas))
        else:
            return max(getattr(n, 'f', -infinity), n.path_cost + h(n))
    return best_first_search(problem, f)

def IDA_estrela(problem, h):
    def recursive_dls(node, problem, limit):
        corte_ocorreu = False
        minimo = infinity
        if problem.goal_test(node.state):
            return node, node.f
        elif node.f > limit:
            return None, node.f
        else:
            problem.gerados += len(node.expand(problem))
            successors = node.expand(problem)
            for s in successors:
                s.f = s.path_cost + problem.h1(s)

            for successor in successors:
                result, newlimit = recursive_dls(successor, problem, limit)
                problem.explorados += 1
                minimo = min(newlimit, minimo)
                if result != None:
                    return result, result.path_cost
        return None, minimo
    # Fim recursive_dls()

    problem.explorados = problem.gerados = 0
    initial = Node(problem.initial)
    limit = h(initial)
    while limit < infinity:
        result, limit = recursive_dls(initial, problem, limit)

        if result is not None:
            return result
        if limit == infinity:
            return None

def RBFS(problem, h):
    def RBFS_recursion(problem, node, flimit):
        if problem.goal_test(node.state):
            return node
        successors = node.expand(problem)
        if len(successors) == 0:
            return None, infinity
        for s in successors:
            s.f = max(s.path_cost + h(s), node.f)
        while True:
            successors.sort(key = lambda x: x.f)
            best = successors[0]
            if best.f > flimit:
                return None, best.f
            alternative = successors[1]
            result, best.f = RBFS_recursion(problem, best, min(flimit, alternative))
            if result is not None:
                return result
    initial = Node(problem.initial)
    initial.f = h(initial)
    return RBFS_recursion(problem, initial, infinity)
