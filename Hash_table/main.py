# skończone

class TableElement:
    def __init__(self, key, data):
        self.key = key
        self.data = data


class HashTable:

    def __init__(self, size, c1=1, c2=0):
        self.size = size
        self.table = [None for _ in range(self.size)]
        self.c1 = c1
        self.c2 = c2
        self.num_of_elems = 0

    def hash(self, key):
        if isinstance(key, str):
            idx = 0
            for i in range(len(key)):
                idx += ord(key[i])
        else:
            idx = key

        right_idx = idx % self.size
        return right_idx

    def del_conflict(self, key, i):
        right_idx = (self.hash(key) + self.c1 * i + self.c2 * i ** 2) % self.size
        return right_idx

    def insert(self, key, data):
        idx = self.hash(key)
        repeat = 0
        if self.table[idx] and self.table[idx].key == key:
            self.table[idx].data = data
        else:
            i = self.del_conflict(key, repeat + 1)
            while repeat < self.size:
                if self.table[i] and self.table[i].key == key:
                    self.table[i].data = data
                    break
                else:
                    i = self.del_conflict(key, repeat + 1)
                    repeat += 1

        if repeat == self.size and self.num_of_elems < self.size:  # jest miejsce w tablicy i nienadpisane
            i = 1
            if self.table[idx]:
                while self.table[idx]:
                    if i == self.size + 1:
                        print("Brak miejsca!")
                        return 0
                    idx = self.del_conflict(key, i)
                    i += 1
                self.table[idx] = TableElement(key, data)
                self.num_of_elems += 1
            else:
                self.table[idx] = TableElement(key, data)
                self.num_of_elems += 1

        elif repeat == self.size:  # tablica pełna i niendpisane
            print("Brak miejsca!")

    def search(self, key):
        idx = self.hash(key)
        repeat = 0
        if self.table[idx] and self.table[idx].key == key:
            return self.table[idx].data
        else:
            i = self.del_conflict(key, repeat + 1)
            while repeat <= self.size:
                if self.table[i] and self.table[i].key == key:
                    return self.table[i].data
                else:
                    i = self.del_conflict(key, repeat + 1)
                    repeat += 1

        if repeat == self.size:
            return None

    def remove(self, key):
        idx = self.hash(key)
        repeat = 0
        if self.table[idx] and self.table[idx].key == key:
            self.table[idx] = None
            self.num_of_elems -= 1
        else:
            i = self.del_conflict(key, repeat + 1)
            while repeat <= self.size:
                if self.table[i] and self.table[i].key == key:
                    self.table[i] = None
                    self.num_of_elems -= 1
                    break
                else:
                    i = self.del_conflict(key, repeat + 1)
                    repeat += 1

        if repeat == self.size:
            print("Brak danej!")

    def __str__(self):
        result = "{"
        for i in range(self.size - 1):
            if self.table[i]:
                result += f"{self.table[i].key}:{self.table[i].data}" + ", "
            else:
                result += "None, "
        if self.table[self.size - 1]:
            result += f"{self.table[self.size - 1].key}:{self.table[self.size - 1].data}" + "}"
        else:
            result += "None}"
        return result


def function_test1(size, c1, c2):
    tab = HashTable(size, c1, c2)
    for i in range(1, 16):
        if i == 6:
            tab.insert(18, chr(ord('A')+i-1))
        elif i == 7:
            tab.insert(31, chr(ord('A')+i-1))
        else:
            tab.insert(i, chr(ord('A')+i-1))
    print(tab)
    print(tab.search(5))
    print(tab.search(14))
    tab.insert(5, 'Z')
    print(tab.search(5))
    tab.remove(5)
    print(tab)
    print(tab.search(31))
    tab.insert('test', 'W')
    print(tab)


def function_test2(size, c1, c2):
    tab = HashTable(size, c1, c2)
    for i in range(1, 16):
        tab.insert(13*i, chr(ord('A') + i - 1))
    print(tab)


def main():
    function_test1(13, 1, 0)
    print("\n")
    function_test2(13, 1, 0)
    print("\n")
    function_test2(13, 0, 1)
    print("\n")
    function_test1(13, 0, 1)


if __name__ == '__main__':
    main()


