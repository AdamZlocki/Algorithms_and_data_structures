# skończone
import os

import cv2
import matplotlib.pyplot as plt
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

    def __repr__(self):
        return f"{self.key}"


class Edge:
    def __init__(self, start, end, weight=1):
        self.start = start
        self.end = end
        self.weight = weight
        length = np.sqrt((end.key[0] - start.key[0]) ** 2 + (end.key[1] - start.key[1]) ** 2)
        help_wektor = [end.key[0] - start.key[0], end.key[1] - start.key[1]]
        help_wektor_ox = [1, 0]
        orientation = np.arccos((help_wektor[0] * help_wektor_ox[0] + help_wektor[1] * help_wektor_ox[1]) / length)
        self.params = [length, orientation]

    def __repr__(self):
        result = f"{self.params[0], self.params[1]}"
        return result

    def __eq__(self, other):
        if self.start == other.start and self.end == other.end and self.weight == other.weight:
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
        if vertex in self.list:
            vertex_idx = self.dict[vertex]
            for i in range(self.order()):
                if i != vertex_idx:
                    count = 0
                    for j in self.neighbour_list[i]:
                        if j[0] > vertex_idx:
                            new_idx = j[0] - 1
                            new_edge = j[1]
                            self.neighbour_list[i][count] = (new_idx, new_edge)
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


class BiometricGraph(GraphList):

    def __init__(self):
        super().__init__()

    def plot_graph(self, v_color, e_color):
        X = []
        Y = []
        for vertex in self.list:
            X.append(vertex.key[0])
            Y.append(vertex.key[1])
        plt.scatter(Y, X, c=v_color[0])
        edges = self.edges()
        for edge in edges:
            plt.plot([edge.start.key[1], edge.end.key[1]], [edge.start.key[0], edge.end.key[0]], e_color[0])
        plt.gca().invert_yaxis()
        # plt.show()

    def rotate_and_move(self, move_vector, alfa):
        for vertex in self.list:
            new_x = vertex.key[0] * np.cos(alfa) + vertex.key[1] * np.sin(alfa) + move_vector[0]
            new_y = -vertex.key[0] * np.sin(alfa) + vertex.key[1] * np.cos(alfa) + move_vector[1]
            vertex.key = (new_x, new_y)

        for start_idx, lst in enumerate(self.neighbour_list):
            for edge in lst:
                edge[1].start = self.getVertex(start_idx)
                edge[1].end = self.getVertex(edge[0])
                help_wektor = [edge[1].end.key[0] - edge[1].start.key[0], edge[1].end.key[1] - edge[1].start.key[1]]
                help_wektor_ox = [1, 0]
                new_length = np.sqrt(
                    (edge[1].end.key[0] - edge[1].start.key[0]) ** 2 + (edge[1].end.key[1] - edge[1].start.key[1]) ** 2)
                new_orientation = np.arccos(
                    (help_wektor[0] * help_wektor_ox[0] + help_wektor[1] * help_wektor_ox[1]) / new_length)
                edge[1].params = [new_length, new_orientation]


def fill_biometric_graph_from_image(img, graph):
    X, Y = img.shape
    for x in range(X):
        for y in range(Y):
            if img[x, y]:
                if not Vertex((x, y)) in graph.list:
                    graph.insertVertex(Vertex((x, y)))
                    if 0 < x < X - 1 and 0 < y < Y - 1:
                        for nx in range(x - 1, x + 1):
                            if nx == x - 1:
                                for ny in range(y - 1, y + 2):
                                    if img[nx, ny]:
                                        if not Vertex((nx, ny)) in graph.list:
                                            graph.insertVertex(Vertex((nx, ny)))
                                        graph.insertEdge(Vertex((x, y)), Vertex((nx, ny)),
                                                         Edge(Vertex((x, y)), Vertex((nx, ny))))
                                        graph.insertEdge(Vertex((nx, ny)), Vertex((x, y)),
                                                         Edge(Vertex((nx, ny)), Vertex((x, y))))
                            else:
                                ny = y - 1
                                if img[nx, ny]:
                                    if not Vertex((nx, ny)) in graph.list:
                                        graph.insertVertex(Vertex((nx, ny)))
                                    graph.insertEdge(Vertex((x, y)), Vertex((nx, ny)),
                                                     Edge(Vertex((x, y)), Vertex((nx, ny))))
                                    graph.insertEdge(Vertex((nx, ny)), Vertex((x, y)),
                                                     Edge(Vertex((nx, ny)), Vertex((x, y))))


def unclutter_biometric_graph(graph):
    to_delete = []
    to_add = []
    for idx, vertex in enumerate(graph.list):
        neighbours = graph.neighbours(idx)
        if len(neighbours) != 2:
            for neighbour in neighbours:
                previous = idx
                current = neighbour[0]
                current_neighbours = graph.neighbours(current)
                while len(current_neighbours) == 2:
                    to_delete.append(graph.getVertex(current))
                    for c_neighbour in current_neighbours:
                        if c_neighbour[0] != previous:
                            previous = current
                            current = c_neighbour[0]
                            current_neighbours = graph.neighbours(current)
                            break

                to_add.append(Edge(vertex, graph.getVertex(current)))
                to_add.append(Edge(graph.getVertex(current), vertex))

    for i in to_add:
        graph.insertEdge(i.start, i.end, i)
    for i in to_delete:
        graph.deleteVertex(i)

    correct_graph = GraphList()
    correct_graph.list, correct_graph.dict = graph.list.copy(), graph.dict.copy()
    correct_graph.neighbour_list = [[] for _ in range(graph.order())]

    for i in range(graph.order()):
        for j in range(len(graph.neighbour_list[i])):
            in_correct_list = False
            for k in range(len(correct_graph.neighbour_list[i])):
                if graph.neighbour_list[i][j][1] == correct_graph.neighbour_list[i][k][1]:
                    in_correct_list = True
                    break
            if not in_correct_list:
                correct_graph.neighbour_list[i].append(graph.neighbour_list[i][j])

    graph.neighbour_list = correct_graph.neighbour_list.copy()


def merge_near_vertices(graph, thr):
    to_connect = [[] for _ in range(graph.order())]
    for idx, vertex in enumerate(graph.list):
        in_to_connect = False
        for lst in to_connect:
            if vertex in lst:
                in_to_connect = True
                break
        if not in_to_connect:
            to_connect[idx].append(vertex)
            for i in range(idx, graph.order()):
                v = graph.list[i]
                in_to_connect = False
                for lst in to_connect:
                    if v in lst:
                        in_to_connect = True
                        break
                if not in_to_connect:
                    distance = np.sqrt((v.key[0] - vertex.key[0]) ** 2 + (v.key[1] - vertex.key[1]) ** 2)
                    if distance < thr:
                        to_connect[idx].append(v)

    xs = []
    ys = []
    ready_to_connect = [[] for _ in range(graph.order())]
    for idx, connections in enumerate(to_connect):
        if to_connect[idx]:
            for v in connections:
                xs.append(v.key[0])
                ys.append(v.key[1])

            new_x = int(np.mean(xs))
            new_y = int(np.mean(ys))
            ready_to_connect[idx].append(Vertex((new_x, new_y)))
            xs = []
            ys = []

    for idx, connections in enumerate(to_connect):
        if to_connect[idx]:
            new_neighbours = []
            for v in connections:
                v_neighbours = graph.neighbours(graph.getVertexIdx(v))
                for neighbour in v_neighbours:
                    if graph.getVertex(neighbour[0]) not in to_connect[idx]:
                        for end_idx, lst in enumerate(to_connect):
                            if graph.getVertex(neighbour[0]) in lst:
                                if len(to_connect[end_idx]) <= 1:
                                    new_neighbours.append(graph.getVertex(neighbour[0]))
                                else:
                                    new_neighbours.append(ready_to_connect[end_idx][0])
                                break

            ready_to_connect[idx].append(new_neighbours)

    for i in range(graph.order()):
        if to_connect[i]:
            for j in range(len(to_connect[i])):
                graph.deleteVertex(to_connect[i][j])
            graph.insertVertex(ready_to_connect[i][0])

    for i in range(len(to_connect)):
        if to_connect[i]:
            for j in range(len(ready_to_connect[i][1])):
                graph.insertEdge(ready_to_connect[i][0], ready_to_connect[i][1][j],
                                 Edge(ready_to_connect[i][0], ready_to_connect[i][1][j]))
                graph.insertEdge(ready_to_connect[i][1][j], ready_to_connect[i][0],
                                 Edge(ready_to_connect[i][1][j], ready_to_connect[i][0]))


def biometric_graph_registration(graph1, graph2, Ni, eps):
    edges_graph1 = graph1.edges()
    edges_graph2 = graph2.edges()

    edges_pairs = []

    for edge1 in edges_graph1:
        for edge2 in edges_graph2:
            s = np.sqrt((edge1.params[0] - edge2.params[0]) ** 2 + (edge1.params[1] - edge2.params[1]) ** 2) / (
                    0.5 * (edge1.params[0] + edge2.params[0]))
            edges_pairs.append((edge1, edge2, s))

    edges_pairs_sorted = sorted(edges_pairs, key=lambda x: x[2])
    edges_pairs_sorted = edges_pairs_sorted[:Ni]

    graphs_distance = [float('inf') for _ in range(len(edges_pairs_sorted))]

    for idx, pair in enumerate(edges_pairs_sorted):
        help_graph1, help_graph2 = BiometricGraph(), BiometricGraph()
        help_graph1.list, help_graph1.neighbour_list, help_graph1.dict = \
            graph1.list.copy(), graph1.neighbour_list.copy(), graph1.dict.copy()
        help_graph2.list, help_graph2.neighbour_list, help_graph2.dict = \
            graph2.list.copy(), graph2.neighbour_list.copy(), graph2.dict.copy()

        help_graph1.rotate_and_move([-pair[0].start.key[0], -pair[0].start.key[1]], -pair[0].params[1])
        help_graph2.rotate_and_move([-pair[1].start.key[0], -pair[1].start.key[1]], -pair[1].params[1])

        C = 0
        for vertex1 in help_graph1.list:
            for vertex2 in help_graph2.list:
                if np.sqrt((vertex2.key[0] - vertex1.key[0]) ** 2 + (vertex2.key[1] - vertex1.key[1]) ** 2) < eps:
                    C += 1
                    break

        graphs_distance[idx] = 1 - C/np.sqrt(help_graph1.order() * help_graph2.order())

    best_pair = edges_pairs_sorted[graphs_distance.index(min(graphs_distance))]
    graph1.rotate_and_move([-best_pair[0].start.key[0], -best_pair[0].start.key[1]], -best_pair[0].params[1])
    graph2.rotate_and_move([-best_pair[1].start.key[0], -best_pair[1].start.key[1]], -best_pair[1].params[1])
    return graph1, graph2


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
    # img = cv2.imread('Retina_graph_easy_1.png')
    # img_1ch = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # _, img_bin = cv2.threshold(img_1ch, 127, 255, cv2.THRESH_BINARY)
    # graph = BiometricGraph()
    # fill_biometric_graph_from_image(img_bin, graph)
    # unclutter_biometric_graph(graph)
    # merge_near_vertices(graph, 5)
    # graph.plot_graph("red", "green")

    data_path = "./Images"
    img_level = "easy"
    img_list = [f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f))]

    input_data = []
    for img_name in img_list:
        if img_name[-3:] == "png":
            if img_name.split('_')[-2] == img_level:
                print("Processing ", img_name, "...")

                img = cv2.imread(os.path.join(data_path, img_name))
                img_1ch = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                _, img_bin = cv2.threshold(img_1ch, 127, 255, cv2.THRESH_BINARY)

                graph = BiometricGraph()
                fill_biometric_graph_from_image(img_bin, graph)
                unclutter_biometric_graph(graph)
                merge_near_vertices(graph, thr=5)

                input_data.append((img_name, graph))
                print("Saved!")

    for i in range(len(input_data)):
        for j in range(len(input_data)):
            graph1_input = input_data[i][1]
            graph2_input = input_data[j][1]

            graph1, graph2 = biometric_graph_registration(graph1_input, graph2_input, Ni=50, eps=10)

            plt.figure()
            graph1.plot_graph(v_color='red', e_color='green')

            graph2.plot_graph(v_color='gold', e_color='blue')
            plt.title('Graph comparison')
            plt.show()


if __name__ == '__main__':
    main()
