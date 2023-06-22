# skończone
from random import random


def randomLevel(maxLevel, p=0.5):
    lvl = 1
    while random() < p and lvl < maxLevel:
        lvl = lvl + 1
    return lvl


class ListElem:
    def __init__(self, max_lvl, key=None, value=None):
        self.key = key
        self.value = value
        self.num_of_lvls = max_lvl
        self.next = [None for _ in range(self.num_of_lvls)]


class SkipList:

    def __init__(self, max_lvl: int):
        self.max_lvl = max_lvl
        self.head = ListElem(self.max_lvl)

    def search(self, key):
        actual = self.head.next[0]
        if actual.key == key:
            return actual.value
        else:
            i = actual.num_of_lvls-1
            while actual:
                if actual.next[i]:
                    if actual.next[i].key == key:
                        return actual.next[i].value
                    elif actual.next[i].key < key:
                        actual = actual.next[i]
                        i = actual.num_of_lvls-1
                    else:
                        i -= 1
                else:
                    i -= 1

            return None

    def insert(self, key, value):
        node = self.head.next[0]  # pierwszy element na poziomie 0
        keys = []  # lista kluczy na tym poziomie
        while node is not None:
            keys.append(node.key)
            node = node.next[0]
        if key not in keys:
            added_elem = ListElem(randomLevel(self.max_lvl), key, value)
            backs = [None for _ in range(added_elem.num_of_lvls)]
            for i in range(added_elem.num_of_lvls - 1, -1, -1):
                actual = self.head.next[i]
                if actual:
                    if actual.key > key:
                        backs[i] = self.head
                    else:
                        while actual:
                            if actual.next[i]:
                                if actual.next[i].key > key:
                                    backs[i] = actual
                                    break
                                else:
                                    actual = actual.next[i]
                            else:
                                backs[i] = actual
                                break
                else:
                    backs[i] = self.head

            for i in range(len(backs)):
                backs[i].next[i], added_elem.next[i] = added_elem, backs[i].next[i]
        else:
            actual = self.head
            if actual.key == key:
                return actual.value
            else:
                while actual.key != key:
                    for i in range(len(actual.next)):
                        if actual.next[i]:
                            if actual.next[i].key == key:
                                actual.next[i].value = value
                    if actual.next[0] is None:
                        return None
                    else:
                        actual = actual.next[0]

    def remove(self, key):
        node = self.head.next[0]  # pierwszy element na poziomie 0
        keys = []  # lista kluczy na tym poziomie
        while node is not None:
            keys.append(node.key)
            node = node.next[0]
        if key in keys:
            backs = [None for _ in range(self.max_lvl)]
            for i in range(self.max_lvl - 1, -1, -1):
                actual = self.head.next[i]
                if actual:
                    if actual.key == key:
                        backs[i] = self.head
                    else:
                        while actual:
                            if actual.next[i]:
                                if actual.next[i].key == key:
                                    backs[i] = actual
                                    break
                                else:
                                    actual = actual.next[i]
                            else:
                                backs[i] = actual
                                break
                else:
                    backs[i] = self.head

            for i in range(len(backs)):
                if backs[i].next[i]:
                    backs[i].next[i] = backs[i].next[i].next[i]
        else:
            print("Brak takiego klucza!")

    def displayList_(self):
        node = self.head.next[0]  # pierwszy element na poziomie 0
        keys = []  # lista kluczy na tym poziomie
        while node is not None:
            keys.append(node.key)
            node = node.next[0]

        for lvl in range(self.max_lvl - 1, -1, -1):
            print("{}: ".format(lvl), end=" ")
            node = self.head.next[lvl]
            idx = 0
            while node is not None:
                while node.key > keys[idx]:
                    print("  ", end=" ")
                    idx += 1
                idx += 1
                print("{:2d}".format(node.key), end=" ")
                node = node.next[lvl]
            print("")

    def __str__(self):
        # wersja wypisująca wszystkie poziomy
        # node = self.head.next[0]  # pierwszy element na poziomie 0
        # keys = []  # lista kluczy na tym poziomie
        # while node is not None:
        #     keys.append(node.key)
        #     node = node.next[0]
        #
        # result = ""
        #
        # for lvl in range(self.max_lvl - 1, -1, -1):
        #     lvl_result = ""
        #     lvl_result += str(lvl) + ": ["
        #     node = self.head.next[lvl]
        #     while node is not None:
        #         lvl_result += f"({node.key}, {node.value}), "
        #         node = node.next[lvl]
        #     if lvl_result != str(lvl) + ": [":
        #         lvl_result = lvl_result[:-2]
        #         lvl_result += ']\n'
        #         result += lvl_result
        # return result
        # wersja wypisująca poziom 0
        result = "["
        lvl = 0
        node = self.head.next[lvl]
        while node is not None:
            result += f"({node.key}:{node.value}), "
            node = node.next[lvl]
        result = result[:-2]
        result += ']\n'
        return result



def main():
    lista1 = SkipList(5)
    for i in range(1, 16):
        lista1.insert(i, chr(ord('A') + i - 1))
    print(lista1)
    print(lista1.search(2))
    lista1.insert(2, 'Z')
    print(lista1.search(2), "\n")
    for i in range(5, 8):
        lista1.remove(i)
    print(lista1)
    lista1.insert(6, 'W')
    print(lista1)

    print("------------------------------------")

    lista2 = SkipList(5)
    for i in range(15, 0, -1):
        lista2.insert(i, chr(ord('A') + i - 1))
    print(lista2)
    print(lista2.search(2))
    lista2.insert(2, 'Z')
    print(lista2.search(2), "\n")
    for i in range(5, 8):
        lista2.remove(i)
    print(lista2)
    lista2.insert(6, 'W')
    print(lista2)



if __name__ == '__main__':
    main()
