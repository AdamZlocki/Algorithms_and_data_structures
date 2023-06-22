# skończone
import numpy as np


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
    def __init__(self, weight=1):
        self.weight = weight

    def __repr__(self):
        result = f"{self.weight}"
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


def ullman(G, P, used_columns=None, current_row=0, M=None, no_recursion=0, M0=None, do_prune=False, count=0):
    no_recursion += 1
    if not used_columns:
        used_columns = []
    if current_row == M.shape[0]:
        if np.equal(np.matmul(M, np.transpose(np.matmul(M, G))), P).all():
            count += 1
        return count, no_recursion
    copy_M = M.copy()

    if do_prune:
        wasChange = True
        while wasChange:
            wasChange = False
            for i in range(copy_M.shape[0]):
                for j in range(copy_M.shape[1]):
                    if copy_M[i][j]:
                        x, y = i, j
                        x_neighbours = []
                        for k in range(P.shape[0]):
                            if P[x][k]:
                                x_neighbours.append(k)
                        y_neighbours = []
                        for m in range(G.shape[0]):
                            if G[y][m]:
                                y_neighbours.append(m)

                        for neigbour_x in x_neighbours:
                            isNeighbour = False
                            for neigbour_y in y_neighbours:
                                if copy_M[neigbour_x][neigbour_y]:
                                    isNeighbour = True
                                    break
                            if not isNeighbour:
                                copy_M[i][j] = 0
                                wasChange = True
                                break
        empty_rows = 0
        for i in range(copy_M.shape[0]):
            if 1 not in copy_M[i]:
                empty_rows += 1
        if empty_rows > 0:
            return count, no_recursion

    for c in range(copy_M.shape[1]):
        if c not in used_columns:
            if M0 is None:
                copy_M[current_row] = [0] * copy_M.shape[1]
                copy_M[current_row][c] = 1
                used_columns.append(c)
                count, no_recursion = ullman(G, P, used_columns, current_row + 1, copy_M, no_recursion, do_prune=do_prune, count=count)
                used_columns.pop(used_columns.index(c))
            else:
                copy_M[current_row] = [0] * copy_M.shape[1]
                if M0[current_row][c] == 1:
                    copy_M[current_row][c] = 1
                    used_columns.append(c)
                    count, no_recursion = ullman(G, P, used_columns, current_row + 1, copy_M, no_recursion, M0, do_prune=do_prune, count=count)
                    used_columns.pop(used_columns.index(c))

    return count, no_recursion


def main():
    graph_G = [('A', 'B', 1), ('B', 'F', 1), ('B', 'C', 1), ('C', 'D', 1), ('C', 'E', 1), ('D', 'E', 1)]
    graph_P = [('A', 'B', 1), ('B', 'C', 1), ('A', 'C', 1)]

    G_graf = GraphMatrix()
    for i in graph_G:
        if not Vertex(i[0]) in G_graf.list:
            G_graf.insertVertex(Vertex(i[0]))
        if not Vertex(i[1]) in G_graf.list:
            G_graf.insertVertex(Vertex(i[1]))
        G_graf.insertEdge(Vertex(i[0]), Vertex(i[1]), Edge())
        G_graf.insertEdge(Vertex(i[1]), Vertex(i[0]), Edge())

    P_graf = GraphMatrix()
    for i in graph_P:
        if not Vertex(i[0]) in P_graf.list:
            P_graf.insertVertex(Vertex(i[0]))
        if not Vertex(i[1]) in P_graf.list:
            P_graf.insertVertex(Vertex(i[1]))
        P_graf.insertEdge(Vertex(i[0]), Vertex(i[1]), Edge())
        P_graf.insertEdge(Vertex(i[1]), Vertex(i[0]), Edge())

    G = np.array(G_graf.matrix)
    P = np.array(P_graf.matrix)
    M = np.ones((P.shape[0], G.shape[0]))
    M0 = np.zeros((P.shape[0], G.shape[0]))
    for i in range(P.shape[0]):
        for j in range(G.shape[0]):
            if len(P_graf.neighbours(i)) <= len(G_graf.neighbours(j)):
                M0[i][j] = 1
    print(f"Wersja 1.0: ", ullman(G, P, M=M))

    M = np.ones((P.shape[0], G.shape[0]))
    print(f"Wersja 2.0: ", ullman(G, P, M=M, M0=M0))

    M = np.ones((P.shape[0], G.shape[0]))
    print(f"Wersja 3.0: ", ullman(G, P, M=M, M0=M0, do_prune=True))
    print(f"Liczba wywołań rekurencji nie zmniejszyła się poniważ jej wyowałenie nie zależt od kopi M, którą zmienia prune")


if __name__ == '__main__':
    main()
