class Vertex:
    def __init__(self,key):
        self._id = key
        self.connectedTo = {}

    def addNeighbor(self,nbr,weight=0):
        self.connectedTo[nbr] = weight

    def __str__(self):
        return str(self._id) + ' connectedTo: ' + str([x._id for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self._id

    def getWeight(self,nbr):
        return self.connectedTo[nbr]


class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self,node):
        self.numVertices = self.numVertices + 1
        newVertex = node
        self.vertList[node.getId()] = newVertex
        return newVertex

    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self,n):
        return n.getId() in self.vertList

    def addEdge(self,f,t,cost = 1):
        if f.getId() not in self.vertList:
            nv = self.addVertex(f)
            print("\t(%s) nao existe. Inserindo" % f.getId())
        if t.getId() not in self.vertList:
            nv = self.addVertex(t)
            print("\t(%s) nao existe (2). Inserindo no grafo" % f.getId())
        self.getVertex(f.getId()).addNeighbor(self.getVertex(t.getId()), cost)

    def getVertices(self):
        return self.vertList.values()

    def __iter__(self):
        return iter(self.vertList.values())

    def __len__(self):
        return len(g.getVertices())

class Tile(Vertex):
    def __init__(self,x,y):
        super().__init__("%d,%d" % (x,y))
        self.x = x
        self.y = y


dirs = [[0,1], [1,0], [-1,0], [0,-1]]

g = Graph()
for x in range(1,6):
    for y in range(1,6):
        v = g.addVertex(Tile(x,y))

for v in tuple(g):
    for dir in dirs:
        tile = Tile(v.x + dir[0], v.y + dir[1])
        if tile in g:
            g.addEdge(v, Tile(v.x + dir[0], v.y + dir[1]))

print("Criado grafo com %d vertices" % len(g))
