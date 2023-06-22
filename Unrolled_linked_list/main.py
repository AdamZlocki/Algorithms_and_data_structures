# skończone

table_size = 6


class ListElement:

    def __init__(self, next=None):
        self.table = [None for _ in range(table_size)]
        self.size = 0
        self.next = next

    def table_insert(self, data, idx=0):
        if self.size <= idx:
            self.table[self.size] = data
        else:
            help_data = self.table[idx]
            for i in range(idx, self.size):
                self.table[i + 1], help_data = help_data, self.table[i + 1]
            self.table[idx] = data
        self.size += 1

    def table_delete(self, idx):
        for i in range(idx, self.size - 1):
            self.table[i] = self.table[i + 1]
        self.table[self.size - 1] = None
        self.size -= 1

    def print_table(self):
        result = f'[{self.table[0]}'
        for i in range(1, self.size):
            if self.table[i] is not None:
                result += f', {self.table[i]}'
        result += ']'
        return result


class UnrolledLinkedList:

    def __init__(self):
        self.head = None

    def length(self):
        length = 0
        actual = self.head
        while actual is not None:
            length += 1
            actual = actual.next
        return length

    def add_end(self):
        elem = ListElement()
        if self.head is None:
            self.head = ListElement(elem.table)
        else:
            actual = self.head
            while actual.next is not None:
                actual = actual.next
            actual.next = elem

    def size(self):
        size = 0
        actual = self.head
        while actual is not None:
            size += actual.size
            actual = actual.next
        return size

    def get(self, idx):
        size = self.size()

        if self.head is None:
            raise Exception('List is empty!')
        elif idx >= size or idx < 0:
            raise Exception('Index out of range!')
        else:
            actual = self.head
            skipped_size = 0
            while idx > actual.size - 1 + skipped_size:
                skipped_size += actual.size
                actual = actual.next

            idx -= skipped_size
            return actual.table[idx]

    def insert(self, data, idx):
        if self.head is None:
            self.head = ListElement()
            self.head.table_insert(data)
        else:
            size = self.size()
            if idx >= size:  # indeks spoza zakresu
                actual = self.head
                skipped_size = 0
                while actual.next is not None:
                    skipped_size += actual.size
                    actual = actual.next
                if actual.size == table_size:  # - i ostatnia tablica pełna
                    self.add_end()
                    new = self.head
                    while new.next is not None:
                        new = new.next
                    old = self.head
                    while old.next.next is not None:
                        old = old.next
                    for i in range(int(table_size / 2), table_size):
                        j = i - int(table_size / 2)
                        new.table_insert(old.table[i], j)
                        old.table[i] = None
                    old.size -= int(table_size / 2)
                    idx = new.size
                    new.table_insert(data, idx)
                else:  # - jest miejsce w ostatniej tablicy
                    last = self.head
                    while last.next is not None:
                        last = last.next
                    new_idx = last.size
                    last.table_insert(data, new_idx)
            else:  # indeks w zakresie
                actual = self.head
                skipped_size = 0
                while idx > actual.size - 1 + skipped_size:
                    skipped_size += actual.size
                    actual = actual.next
                if actual.size == table_size:  # - tablica do której ma trafić pełna
                    self.add_end()
                    new = self.head
                    while new.next is not None:
                        new = new.next
                    for i in range(int(table_size / 2), table_size):
                        j = i - int(table_size / 2)
                        new.table_insert(actual.table[i], j)
                        actual.table[i] = None
                    actual.size -= int(table_size / 2)
                    actual = self.head
                    skipped_size = 0
                    while idx > actual.size - 1 + skipped_size:
                        skipped_size += actual.size
                        actual = actual.next
                    idx -= skipped_size
                    actual.table_insert(data, idx)
                else:  # - jest miejsce w docelowej tablicy
                    idx -= skipped_size
                    actual.table_insert(data, idx)

    def delete(self, idx):
        size = self.size()
        if self.head is None:
            raise Exception('List is empty!')
        elif idx >= size or idx < 0:
            raise Exception('Index out of range!')
        else:
            actual = self.head
            skipped_size = 0
            while idx > actual.size - 1 + skipped_size:
                skipped_size += actual.size
                actual = actual.next
            idx -= skipped_size
            actual.table_delete(idx)
            if actual.size < int(table_size / 2):  # sprawdzenie czy tablica po usunięciu ma mniej niż połowę
                # możliwych elementów
                if actual.next.size <= int(table_size / 2):  # sprawdzenie czy następna tablica ma połowę
                    # lub mniej możliwych elementów
                    for i in range(actual.next.size):
                        actual.table[actual.size + i] = actual.next.table[i]
                    actual.next = actual.next.next
                    actual.size += actual.next.size
                else:
                    actual.table_insert(actual.next.table[0], actual.size)
                    actual.next.table_delete(0)

    def print_list(self):
        if self.head is None:
            print("[]\n")
        elif self.length() == 1:
            print(f"[{self.head.print_table()}]\n")
        else:
            result = '['
            actual = self.head
            while actual is not None:
                if actual.next is not None:
                    result += ' ' + actual.print_table() + ' ->'
                else:
                    result += ' ' + actual.print_table() + ']\n'
                actual = actual.next
            result = result[0] + result[2:]
            print(result)


def main():
    list1 = UnrolledLinkedList()
    for i in range(1, 10):
        list1.insert(i, i - 1)
    list1.print_list()
    print(list1.get(4), "\n")
    list1.insert(10, 1)
    list1.insert(11, 8)
    list1.print_list()
    list1.delete(1)
    list1.delete(2)
    list1.print_list()


if __name__ == '__main__':
    main()
