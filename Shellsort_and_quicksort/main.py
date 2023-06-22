# skończone
import random
import statistics
import time
from typing import List


def Shell(list):
    if not isinstance(list, List):
        return None
    else:
        h = 0
        k = 1
        while k:
            if (3 ** k - 1) // 2 < len(list) / 3:
                h = (3 ** k - 1) // 2
                k += 1
            else:
                break
        while h:
            # for i in range(h):
            #     help_list = list[i:len(list):h]
            #     for j in range(i, len(list), h):
            #         if list[j] > min(help_list):
            #             idx = j
            #             for m in range(j, len(list), h):
            #                 if list[m] == min(help_list):
            #                     idx = m
            #                     break
            #             list[j], list[idx] = min(help_list), list[j]
            #         help_list[help_list.index(min(help_list))] = float('inf')

            # for i in range(h):
            #     while i < len(list):
            #         for j in range(i + h, len(list), h):
            #             if list[j] < list[i]:
            #                 list[i], list[j] = list[j], list[i]
            #         i += h

            for i in range(h):
                for j in range(i + h, len(list), h):
                    idx = j
                    for m in range(j - h, -1, -h):
                        if not list[m] <= list[idx]:
                            list[idx], list[m] = list[m], list[idx]
                            idx = m
                        else:
                            break
            h = h // 3


def insert_sort(list):
    if not isinstance(list, List):
        return None
    else:
        for i in range(1, len(list)):
            inserted = list[i]
            idx = -1
            for j in range(i - 1, -1, -1):
                if not list[j] <= inserted:
                    list[j + 1] = list[j]
                else:
                    idx = j
                    break
            if idx != -1:
                list[idx + 1] = inserted
            else:
                list[0] = inserted


def quicksort(list):
    if not isinstance(list, List):
        return None
    else:
        x = list[0]
        bigger = [i for i in list if i > x]
        smaller = [i for i in list if i < x]
        equal = [i for i in list if i == x]
        if bigger:
            bigger = quicksort(bigger)
        if smaller:
            smaller = quicksort(smaller)

        list = smaller + equal + bigger
        return list


def quicksort_magic5(list):
    if not isinstance(list, List):
        return None
    else:
        mediany = median(list)
        while len(mediany) > 1:
            mediany = median(mediany)

        x = mediany[0]
        bigger = [i for i in list if i > x]
        smaller = [i for i in list if i < x]
        equal = [i for i in list if i == x]
        if bigger:
            bigger = quicksort_magic5(bigger)
        if smaller:
            smaller = quicksort_magic5(smaller)

        list = smaller + equal + bigger
        return list


def median(list):
    mediany = []
    for i in range(0, len(list), 5):
        actual_list = list[i:i + 5]
        mediany.append(statistics.median(actual_list))
        # case = len(actual_list)
        # if case == 5:
        #     mediany.append(median_5(actual_list))
        # elif case == 4:
        #     mediany.append(median_4(actual_list))
        # elif case == 3:
        #     mediany.append(median_3(actual_list))
        # elif case == 2:
        #     mediany.append((list[0] + list[1]) / 2)
        # elif case == 1:
        #     mediany.append((list[0]))
    return mediany


def median_3(list):
    a = list[0]
    b = list[1]
    c = list[2]
    return max(min(a, b), min(c, max(a, b)))


def median_4(list):
    a = list[0]
    b = list[1]
    c = list[2]
    d = list[3]

    f = max(min(a, b), min(c, d))  # usuwa najmniejsza z 4
    g = min(max(a, b), max(c, d))  # usuwa największą z 4
    return (f + g)/2


def median_5(list):
    a = list[0]
    b = list[1]
    c = list[2]
    d = list[3]
    e = list[4]

    f = max(min(a, b), min(c, d))  # usuwa najmniejsza z 4
    g = min(max(a, b), max(c, d))  # usuwa największą z 4
    help_list = [e, f, g]
    return median_3(help_list)


def main():
    lista1 = []
    while len(lista1) < 10000:
        lista1.append(int(random.random() * 100))

    lista2 = lista1.copy()

    lista3 = lista1.copy()
    lista4 = lista1.copy()

    t_start = time.perf_counter()
    Shell(lista1)
    t_stop = time.perf_counter()
    print("Czas obliczeń (Shell):", "{:.7f}".format(t_stop - t_start))

    t_start = time.perf_counter()
    insert_sort(lista2)
    t_stop = time.perf_counter()
    print("Czas obliczeń (insertion sort):", "{:.7f}".format(t_stop - t_start))

    t_start = time.perf_counter()
    quicksort(lista3)
    t_stop = time.perf_counter()
    print("Czas obliczeń (quicksort):", "{:.7f}".format(t_stop - t_start))

    t_start = time.perf_counter()
    quicksort_magic5(lista4)
    t_stop = time.perf_counter()
    print("Czas obliczeń (Mediana median):", "{:.7f}".format(t_stop - t_start))


if __name__ == '__main__':
    main()
