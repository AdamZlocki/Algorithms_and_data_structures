# skończone

class ListElement:

    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next


class LinkedList:

    def __init__(self):
        self.head = None

    def destroy(self):
        self.head = None

    def add(self, elem):
        if not isinstance(elem, ListElement):
            elem = ListElement(elem)
        if self.is_empty():
            self.head = elem
        else:
            elem.next, self.head = self.head, elem

    def remove(self):
        self.head = self.head.next

    def is_empty(self):
        if self.head is None:
            return True
        else:
            return False

    def length(self):
        length = 0
        actual = self.head
        while actual is not None:
            length += 1
            actual = actual.next
        return length

    def get(self):
        return self.head.data

    def print_list(self):
        if self.is_empty():
            print("[]\n")
        elif self.length() == 1:
            print(f"{self.head.data} -> None\n")
        else:
            print(f"{self.head.data} ->")
            actual = self.head
            while actual.next is not None:
                if actual.next.next is not None:
                    print(f"{actual.next.data} ->")
                else:
                    print(f"{actual.next.data} -> None\n")
                actual = actual.next

    def add_end(self, elem):
        if not isinstance(elem, ListElement):
            elem = ListElement(elem)
        if self.is_empty():
            self.head = ListElement(elem.data)
        else:
            actual = self.head
            while actual.next is not None:
                actual = actual.next
            actual.next = ListElement(elem.data)

    def remove_end(self):
        actual = self.head
        while actual.next.next is not None:
            actual = actual.next
        actual.next = None

    def take(self, n: int):
        result = LinkedList()
        actual = self.head
        while actual is not None:
            result.add_end(actual)
            actual = actual.next
        loop_range = self.length() - n
        if loop_range < 1:
            return result
        else:
            for i in range(loop_range):
                result.remove_end()
                i += 1
            return result

    def drop(self, n: int):
        result = LinkedList()
        actual = self.head
        while actual is not None:
            result.add_end(actual)
            actual = actual.next
        loop_range = self.length() - n
        if loop_range < 1:
            return LinkedList()
        else:
            for i in range(n):
                result.remove()
                i += 1
            return result


def main():
    list0 = [('AGH', 'Kraków', 1919), ('UJ', 'Kraków', 1364), ('PW', 'Warszawa', 1915), ('UW', 'Warszawa', 1915),
             ('UP', 'Poznań', 1919), ('PG', 'Gdańsk', 1945)]
    list1 = LinkedList()
    list1.add(list0[1])
    list1.add(list0[0])
    for i in range(2, len(list0)):
        list1.add_end(list0[i])
    list1.print_list()

    print("Remove:")
    list1.remove()
    list1.print_list()

    list1.remove_end()
    list1.print_list()

    print("Get:")
    print(list1.get())

    print("Length:")
    print(list1.length())

    print("Take:")
    list2 = list1.take(3)
    list2.print_list()
    list1.print_list()

    print("Drop:")
    list2 = list1.drop(1)
    list2.print_list()
    list1.print_list()

    print("Is empty i destroy:")
    print(list1.is_empty())
    list1.print_list()

    list1.destroy()
    list1.print_list()
    print(list1.is_empty(), "\n")


if __name__ == '__main__':
    main()
