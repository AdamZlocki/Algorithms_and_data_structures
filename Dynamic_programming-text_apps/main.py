# skończone
import numpy as np


def string_compare(P, T, i, j):
    if i == 0:
        return len(T[:j])
    if j == 0:
        return len(P[:i])

    swaps = string_compare(P, T, i-1, j-1) + (P[i] != T[j])
    insertions = string_compare(P, T, i, j-1) + 1
    delete = string_compare(P, T, i-1, j) + 1

    min_cost = min(swaps, insertions, delete)
    return min_cost


def string_comparePD(P, T, i, j):
    D = np.zeros((i+1, j+1))
    parents = np.full((i+1, j+1), "X")
    for m in range(1, len(P)):
        D[m][0] = m
        parents[m][0] = "D"
    for n in range(1, len(T)):
        D[0][n] = n
        parents[0][n] = "I"

    for x in range(1, i+1):
        for y in range(1, j+1):
            swaps = D[x-1][y-1] + (P[x] != T[y])
            insertions = D[x][y-1] + 1
            delete = D[x-1][y] + 1
            min_cost = min(swaps, insertions, delete)
            D[x][y] = min_cost
            if min_cost == swaps:
                if P[x] == T[y]:
                    parents[x][y] = "M"
                else:
                    parents[x][y] = "S"
            elif min_cost == delete:
                parents[x][y] = "D"
            elif min_cost == insertions:
                parents[x][y] = "I"

    x, y = i, j
    path = ''
    while parents[x, y] != 'X':
        path = parents[x, y] + path
        if parents[x, y] == 'M' or parents[x, y] == "S":
            x -= 1
            y -= 1
        elif parents[x, y] == 'D':
            x -= 1
        elif parents[x][y] == 'I':
            y -= 1

    return D[len(P)-1][len(T)-1], path


def string_comparePD_with_find_str(P, T, i, j):
    D = np.zeros((i + 1, j + 1))
    parents = np.full((i + 1, j + 1), "X")
    for m in range(1, len(P)):
        D[m][0] = m
        parents[m][0] = "D"

    for x in range(1, i + 1):
        for y in range(1, j + 1):
            swaps = D[x - 1][y - 1] + (P[x] != T[y])
            insertions = D[x][y - 1] + 1
            delete = D[x - 1][y] + 1
            min_cost = min(swaps, insertions, delete)
            D[x][y] = min_cost
            if min_cost == swaps:
                if P[x] == T[y]:
                    parents[x][y] = "M"
                else:
                    parents[x][y] = "S"
            elif min_cost == insertions:
                parents[x][y] = "I"
            elif min_cost == delete:
                parents[x][y] = "D"

    j = 0
    for k in range(len(T)):
        if D[i][k] < D[i][j]:
            j = k

    x, y = i, j
    path = ''
    while parents[x, y] != 'X':
        path = parents[x, y] + path
        if parents[x, y] == 'M' or parents[x, y] == "S":
            x -= 1
            y -= 1
        elif parents[x, y] == 'D':
            x -= 1
        elif parents[x][y] == 'I':
            y -= 1

    return D[len(P) - 1][len(T) - 1], path, j


def longest_mutual(P, T, i, j):
    D = np.zeros((i+1, j+1))
    parents = np.full((i+1, j+1), "X")
    for m in range(1, len(P)):
        D[m][0] = m
        parents[m][0] = "D"
    for n in range(1, len(T)):
        D[0][n] = n
        parents[0][n] = "I"

    for x in range(1, i+1):
        for y in range(1, j+1):
            swaps = D[x-1][y-1] + 100000000 if P[x] != T[y] else D[x-1][y-1]
            insertions = D[x][y-1] + 1
            delete = D[x-1][y] + 1
            min_cost = min(swaps, insertions, delete)
            D[x][y] = min_cost
            if min_cost == swaps:
                if P[x] == T[y]:
                    parents[x][y] = "M"
                else:
                    parents[x][y] = "S"
            elif min_cost == delete:
                parents[x][y] = "D"
            elif min_cost == insertions:
                parents[x][y] = "I"

    x, y = i, j
    path = ''
    while parents[x, y] != 'X':
        path = parents[x, y] + path
        if parents[x, y] == 'M' or parents[x, y] == "S":
            x -= 1
            y -= 1
        elif parents[x, y] == 'D':
            x -= 1
        elif parents[x][y] == 'I':
            y -= 1

    result = P[1:]
    l = 0
    idx = 0
    while l < len(path):
        if path[l] == 'M':
            l += 1
            idx += 1
        elif path[l] == 'D':
            l += 1
            result = result[:idx] + result[idx + 1:]
        elif path[l] == 'I':
            l += 1

    return D[len(P)-1][len(T)-1], path, result


def main():
    P = ' kot'
    T = ' pies'
    print(string_compare(P, T, len(P)-1, len(T)-1))

    P = ' biały autobus'
    T = ' czarny autokar'
    print(string_comparePD(P, T, len(P) - 1, len(T) - 1)[0])

    P = ' thou shalt not'
    T = ' you should not'
    print(string_comparePD(P, T, len(P) - 1, len(T) - 1)[1])

    P = ' bin'
    T = ' mokeyssbanana'
    print("bez zaliczania spacji w tekście źródłowym:",
          string_comparePD_with_find_str(P, T, len(P) - 1, len(T) - 1)[2] - len(P[1:]))
    print("z zaliczeniem spacji w tekście źródłowym:",
          string_comparePD_with_find_str(P, T, len(P) - 1, len(T) - 1)[2] - len(P[1:]) + 1)

    P = ' democrat'
    T = ' republican'
    print(longest_mutual(P, T, len(P) - 1, len(T) - 1)[2])

    T = ' 243517698'
    P = ' '
    p = []
    for i in range(1, len(T)):
        if i != 1:
            for j in range(len(p)):
                if int(T[i]) < p[j]:
                    p.insert(j, int(T[i]))
                    break
                if j == len(p) - 1 and int(T[i]) >= p[j]:
                    p.append(int(T[i]))
        else:
            p.append(int(T[i]))
    for i in range(len(p)):
        P += str(p[i])
    print(longest_mutual(P, T, len(P) - 1, len(T) - 1)[2])


if __name__ == '__main__':
    main()
