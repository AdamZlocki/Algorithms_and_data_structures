# skończone

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
    def __init__(self, isResidual=False, weight=1):
        self.weight = weight
        self.flow = 0
        self.residual = weight
        self.isResidual = isResidual

    def __repr__(self):
        result = f"{self.weight} {self.flow} {self.residual} {self.isResidual}"
        return result


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
        self.neighbour_list[idx1].append([idx2, edge])

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


def BFS(graph):
    visited = [0] * graph.order()
    parent = [-1] * graph.order()
    queue = [0]
    visited[0] = 1

    while queue:
        elem = queue.pop()
        elem_neighbours = graph.neighbours(elem)

        for i in elem_neighbours:
            if not visited[i[0]] and i[1].residual > 0:
                queue.append(i[0])
                visited[i[0]] = 1
                parent[i[0]] = elem

    return parent


def min_capacity(graph, start, end, parent):
    actual = end
    mini_capacity = float('Inf')
    if parent[actual] != -1:
        while actual != start:
            parent_neighbours = graph.neighbours(parent[actual])
            for i in parent_neighbours:
                if i[0] == actual:
                    if i[1].residual < mini_capacity:
                        mini_capacity = i[1].residual
                    actual = parent[actual]
        return mini_capacity
    else:
        return 0


def augmentation(graph, start, end, parent, mini_capacity):
    actual = end
    if parent[actual] != -1:
        while actual != start:
            parent_neighbours = graph.neighbours(parent[actual])
            for i in parent_neighbours:
                if i[0] == actual:
                    i[1].flow += mini_capacity
                    i[1].residual -= mini_capacity
            actual_neighbours = graph.neighbours(actual)
            for i in actual_neighbours:
                if i[0] == parent[actual]:
                    i[1].residual += mini_capacity
            actual = parent[actual]


def Ford_Fulkerson(graph):
    end = graph.list.index(Vertex("t"))
    parent = BFS(graph)
    if not parent[end] == -1:
        flow = 0
        mini_capacity = min_capacity(graph, 0, end, parent)
        flow += mini_capacity
        while mini_capacity > 0:
            augmentation(graph, 0, end, parent, mini_capacity)
            parent = BFS(graph)
            mini_capacity = min_capacity(graph, 0, end, parent)
            flow += mini_capacity
        return flow


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
    graf0 = GraphList()
    graf_0 = [('s', 'u', 2), ('u', 't', 1), ('u', 'v', 3), ('s', 'v', 1), ('v', 't', 2)]
    for i in graf_0:
        if not Vertex(i[0]) in graf0.list:
            graf0.insertVertex(Vertex(i[0]))
        if not Vertex(i[1]) in graf0.list:
            graf0.insertVertex(Vertex(i[1]))
        graf0.insertEdge(Vertex(i[0]), Vertex(i[1]), Edge(weight=i[2]))
        graf0.insertEdge(Vertex(i[1]), Vertex(i[0]), Edge(isResidual=True, weight=0))
    print(Ford_Fulkerson(graf0))
    printGraph(graf0)

    graf1 = GraphList()
    graf_1 = [('s', 'a', 16), ('s', 'c', 13), ('a', 'c', 10), ('c', 'a', 4), ('a', 'b', 12), ('b', 'c', 9),
              ('b', 't', 20), ('c', 'd', 14), ('d', 'b', 7), ('d', 't', 4)]
    for i in graf_1:
        if not Vertex(i[0]) in graf1.list:
            graf1.insertVertex(Vertex(i[0]))
        if not Vertex(i[1]) in graf1.list:
            graf1.insertVertex(Vertex(i[1]))
        graf1.insertEdge(Vertex(i[0]), Vertex(i[1]), Edge(weight=i[2]))
        graf1.insertEdge(Vertex(i[1]), Vertex(i[0]), Edge(isResidual=True, weight=0))
    print(Ford_Fulkerson(graf1))
    printGraph(graf1)

    graf2 = GraphList()
    graf_2 = [('s', 'a', 3), ('s', 'c', 3), ('a', 'b', 4), ('b', 's', 3), ('b', 'c', 1), ('b', 'd', 2), ('c', 'e', 6),
              ('c', 'd', 2), ('d', 't', 1), ('e', 't', 9)]
    for i in graf_2:
        if not Vertex(i[0]) in graf2.list:
            graf2.insertVertex(Vertex(i[0]))
        if not Vertex(i[1]) in graf2.list:
            graf2.insertVertex(Vertex(i[1]))
        graf2.insertEdge(Vertex(i[0]), Vertex(i[1]), Edge(weight=i[2]))
        graf2.insertEdge(Vertex(i[1]), Vertex(i[0]), Edge(isResidual=True, weight=0))
    print(Ford_Fulkerson(graf2))
    printGraph(graf2)

    graf3 = GraphList()
    graf_3 = [('s', 'a', 8), ('s', 'd', 3), ('a', 'b', 9), ('b', 'd', 7), ('b', 't', 2), ('c', 't', 5), ('d', 'b', 7),
              ('d', 'c', 4)]
    for i in graf_3:
        if not Vertex(i[0]) in graf3.list:
            graf3.insertVertex(Vertex(i[0]))
        if not Vertex(i[1]) in graf3.list:
            graf3.insertVertex(Vertex(i[1]))
        graf3.insertEdge(Vertex(i[0]), Vertex(i[1]), Edge(weight=i[2]))
        graf3.insertEdge(Vertex(i[1]), Vertex(i[0]), Edge(isResidual=True, weight=0))
    print(Ford_Fulkerson(graf3))
    printGraph(graf3)


if __name__ == '__main__':
    main()
