# skończone
import graf_mst


class Vertex:
    def __init__(self, key):
        self.key = key
        self.visited = 0
        self.color = 0

    def __eq__(self, other):
        if self.key == other.key:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.key)


class Edge:
    def __init__(self, start, end, weight=1):
        self.start = start
        self.end = end
        self.weight = weight


class GraphList:
    def __init__(self):
        self.list = []
        self.dict = {}
        self.neighbour_list = []

    def insertVertex(self, vertex):
        self.list.append(vertex)
        self.dict[vertex] = self.order() - 1
        self.neighbour_list.append([])

    def insertEdge(self, vertex1, vertex2, edge):
        idx1 = self.dict[vertex1]
        idx2 = self.dict[vertex2]
        self.neighbour_list[idx1].append([idx2, edge.weight])

    def deleteVertex(self, vertex):
        vertex_idx = self.dict[vertex]
        for i in range(self.order()):
            if i != vertex_idx:
                count = 0
                for j in self.neighbour_list[i]:
                    if j[0] > vertex_idx:
                        new_idx = j[0] - 1
                        new_vertex = j[1]
                        new_edge = j[2]
                        self.neighbour_list[i][count] = (new_idx, new_vertex, new_edge)
                    elif j[0] == vertex_idx:
                        self.neighbour_list[i].pop(count)
                        count -= 1
                    count += 1
        self.neighbour_list.pop(vertex_idx)
        self.list.pop(vertex_idx)
        self.dict.pop(vertex)
        for i in range(vertex_idx, self.order()):
            actual = self.list[i]
            self.dict[actual] -= 1

    def deleteEdge(self, vertex1, vertex2):
        vertex1_idx = self.dict[vertex1]
        vertex2_idx = self.dict[vertex2]
        for i in range(len(self.neighbour_list[vertex1_idx])):
            if self.neighbour_list[vertex1_idx][i][0] == vertex2_idx:
                self.neighbour_list[vertex1_idx].pop(i)
                break

    def getVertexIdx(self, vertex):
        return self.dict[vertex]

    def getVertex(self, vertex_idx):
        return self.list[vertex_idx].key

    def neighbours(self, vertex_idx):
        result = []
        for i in self.neighbour_list[vertex_idx]:
            result.append(i)
        return result

    def order(self):
        return len(self.list)

    def size(self):
        result = 0
        for i in range(len(self.list)):
            result += len(self.neighbour_list[i])
        return result

    def edges(self):
        result = []
        for i in range(self.order()):
            for j in range(len(self.neighbour_list[i])):
                result.append((self.list[i].key, self.neighbour_list[i][j][1].key))
        return result


def Prim(G):
    if not isinstance(G, GraphList):
        return None
    else:
        intree = [0] * G.order()
        distance = [float('inf')] * G.order()
        parent = [-1] * G.order()
        length = 0

        tree = GraphList()
        tree.list, tree.dict = G.list.copy(), G.dict.copy()
        tree.neighbour_list = [[] for _ in range(G.order())]
        actual = 0
        while intree[actual] == 0:
            intree[actual] = 1
            actual_neighbours = G.neighbours(actual)
            for i in actual_neighbours:
                if i[1] < distance[i[0]] and not intree[i[0]]:
                    distance[i[0]] = i[1]
                    parent[i[0]] = actual

            mini = float('inf')
            idx = -1
            for i in range(tree.order()):
                if intree[i] == 0:
                    if distance[i] < mini:
                        mini = int(distance[i])
                        idx = i
            if idx != -1:
                tree.insertEdge(tree.list[parent[idx]], tree.list[idx], Edge(tree.list[parent[idx]], tree.list[idx], mini))
                tree.insertEdge(tree.list[idx], tree.list[parent[idx]], Edge(tree.list[idx], tree.list[parent[idx]], mini))
                length += mini
                actual = idx

        return tree, length


def printGraph(g):
    n = g.order()
    print("------GRAPH------", n)
    for i in range(n):
        v = g.getVertex(i)
        print(v, end=" -> ")
        nbrs = g.neighbours(i)
        for (j, w) in nbrs:
            print(g.getVertex(j), w, end=";")
        print()
    print("-------------------")


def main():
    graf1 = GraphList()

    for i in graf_mst.graf:
        if not Vertex(i[0]) in graf1.list:
            graf1.insertVertex(Vertex(i[0]))
        if not Vertex(i[1]) in graf1.list:
            graf1.insertVertex(Vertex(i[1]))

        graf1.insertEdge(Vertex(i[0]), Vertex(i[1]), Edge(Vertex(i[0]), Vertex(i[1]), i[2]))
        graf1.insertEdge(Vertex(i[1]), Vertex(i[0]), Edge(Vertex(i[1]), Vertex(i[0]), i[2]))

    drzewo, dlugosc = Prim(graf1)
    printGraph(drzewo)
    print(dlugosc)


if __name__ == '__main__':
    main()
