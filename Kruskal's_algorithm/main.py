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

    def __repr__(self):
        return f"{self.key}"


class Edge:
    def __init__(self, start, end, weight=1):
        self.start = start
        self.end = end
        self.weight = weight

    def __repr__(self):
        return f"{self.weight}"

    def __gt__(self, other):
        if self.weight > other.weight:
            return True
        else:
            return False


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
                result.append(self.neighbour_list[i][j][1])
        return result


class UnionFind:
    def __init__(self, graph):
        self.parent = [_ for _ in range(graph.order())]
        self.size = [1] * graph.order()
        self.n = graph.order()

    def find(self, v):
        if self.parent[v] == v:
            return v
        else:
            return UnionFind.find(self, self.parent[v])

    def union_sets(self, s1,s2):
        s1_root = UnionFind.find(self, s1)
        s2_root = UnionFind.find(self, s2)
        if s1_root != s2_root:
            if self.size[s1_root] < self.size[s2_root]:
                self.parent[s1_root] = s2_root
            elif self.size[s1_root] > self.size[s2_root]:
                self.parent[s2_root] = s1_root
            else:
                self.parent[s1_root] = s2_root
                self.size[s1_root] += 1

    def same_component(self, s1, s2):
        if UnionFind.find(self, s1) == UnionFind.find(self, s2):
            return True
        else:
            return False


def Kruskal(graph):
    edges = graph.edges()
    edges_sorted = []
    while edges:
        edges_sorted.append(edges.pop(edges.index(min(edges))))

    tree = GraphList()
    tree.list, tree.dict = graph.list.copy(), graph.dict.copy()
    tree.neighbour_list = [[] for _ in range(graph.order())]

    union_find = UnionFind(graph)

    for i in edges_sorted:
        w1 = graph.dict[i.start]
        w2 = graph.dict[i.end]

        if not union_find.same_component(w1, w2):
            union_find.union_sets(w1, w2)
            tree.insertEdge(i.start, i.end, Edge(i.start, i.end, i.weight))
            tree.insertEdge(i.end, i.start, Edge(i.end, i.start, i.weight))

    return tree


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


def str_to_ascii(g):
    for i in g.list:
        i.key = ord(i.key)

    for i in g.neighbour_list:
        for j in i:
            j[1].start.key = ord(j[1].start.key)
            j[1].end.key = ord(j[1].end.key)


def main():
    graf1 = GraphList()

    for i in graf_mst.graf:
        if not Vertex(i[0]) in graf1.list:
            graf1.insertVertex(Vertex(i[0]))
        if not Vertex(i[1]) in graf1.list:
            graf1.insertVertex(Vertex(i[1]))

        graf1.insertEdge(Vertex(i[0]), Vertex(i[1]), Edge(Vertex(i[0]), Vertex(i[1]), i[2]))
        graf1.insertEdge(Vertex(i[1]), Vertex(i[0]), Edge(Vertex(i[1]), Vertex(i[0]), i[2]))

    printGraph(Kruskal(graf1))


if __name__ == '__main__':
    main()
