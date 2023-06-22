# skończone
import polska


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
        self.neighbour_list[idx1].append((idx2, vertex2, edge.weight))

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
        return self.list[vertex_idx]

    def neighbours(self, vertex_idx):
        result = []
        for i in self.neighbour_list[vertex_idx]:
            result.append(i[0])
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


class GraphMatrix:
    def __init__(self):
        self.list = []
        self.dict = {}
        self.matrix = [[]]

    def insertVertex(self, vertex):
        self.list.append(vertex)
        self.dict[vertex] = self.order() - 1
        if self.order() != 1:
            for i in range(len(self.matrix)):
                self.matrix[i].append(0)
            self.matrix.append([0] * len(self.matrix[0]))
        else:
            self.matrix[0].append(0)

    def insertEdge(self, vertex1, vertex2, edge):
        idx1 = self.dict[vertex1]
        idx2 = self.dict[vertex2]
        if idx1 is not None and idx2 is not None:
            self.matrix[idx1][idx2] = edge.weight

    def deleteVertex(self, vertex):
        vertex_idx = self.dict[vertex]
        for i in range(self.order()):
            if i != vertex_idx:
                self.matrix[i].pop(vertex_idx)
        self.matrix.pop(vertex_idx)
        self.list.pop(vertex_idx)
        self.dict.pop(vertex)
        for i in range(vertex_idx, self.order()):
            actual = self.list[i]
            self.dict[actual] -= 1

    def deleteEdge(self, vertex1, vertex2):
        vertex1_idx = self.dict[vertex1]
        vertex2_idx = self.dict[vertex2]
        for i in range(len(self.matrix[vertex1_idx])):
            if self.matrix[vertex1_idx][vertex2_idx] != 0:
                self.matrix[vertex1_idx][vertex2_idx] = 0

    def getVertexIdx(self, vertex):
        return self.dict[vertex]

    def getVertex(self, vertex_idx):
        return self.list[vertex_idx]

    def neighbours(self, vertex_idx):
        result = []
        for i in range(len(self.matrix[vertex_idx])):
            if self.matrix[vertex_idx][i] == 1:
                result.append(i)
        return result

    def order(self):
        return len(self.list)

    def size(self):
        result = 0
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if self.matrix[i][j] != 0:
                    result += 1
        return result

    def edges(self):
        result = []
        for i in range(self.order()):
            for j in range(self.order()):
                if self.matrix[i][j]:
                    result.append((self.list[i].key, self.list[j].key))
        return result


def color(graph, method):
    if method == "BFS":
        BFS(graph)
    elif method == "DFS":
        DFS(graph)
    else:
        print("Wrong method name")
    result = []
    for i in graph.list:
        result.append((i.key, i.color))
    return result


def BFS(graph):
    collection = []
    for i in graph.list:
        i.color = 0
    graph.list[0].color = 1
    collection.append(graph.list[0])
    while collection:
        node = collection.pop(0)
        node_neighbours = graph.neighbours(graph.dict[node])
        if node_neighbours:
            for i in node_neighbours:
                v = graph.list[i]
                if v.color == 0:
                    v_neighbours = graph.neighbours(graph.dict[v])
                    v_color = 1
                    colors = []
                    for j in v_neighbours:
                        neigh = graph.list[j]
                        colors.append(neigh.color)
                    while v_color in colors or v_color == node.color:
                        v_color += 1
                    graph.list[i].color = v_color
                    collection.append(graph.list[i])


def DFS(graph):
    collection = []
    for i in graph.list:
        i.color = 0
    graph.list[11].color = 1
    collection.append(graph.list[11])
    while collection:
        node = collection.pop()
        node_neighbours = graph.neighbours(graph.dict[node])
        if node_neighbours:
            for i in node_neighbours:
                v = graph.list[i]
                if v.color == 0:
                    v_neighbours = graph.neighbours(graph.dict[v])
                    v_color = 1
                    colors = []
                    for j in v_neighbours:
                        neigh = graph.list[j]
                        colors.append(neigh.color)
                    while v_color in colors or v_color == node.color:
                        v_color += 1
                    graph.list[i].color = v_color
                    collection.append(graph.list[i])


def function_test(color_method, method='list'):
    if method == 'matrix':
        graf = GraphMatrix()
    else:
        graf = GraphList()

    for i in polska.polska:
        graf.insertVertex(Vertex(i[2]))

    for i in polska.graf:
        graf.insertEdge(Vertex(i[0]), Vertex(i[1]), Edge(i[0], i[1]))

    print(graf.edges())
    polska.draw_map(graf.edges(), color(graf, color_method))


def main():
    #function_test("BFS", 'list')
    #function_test("DFS", 'list')

    #function_test("BFS", 'matrix')
    function_test("DFS", 'matrix')


if __name__ == '__main__':
    main()
