# skończone

class Node:
    def __init__(self, key=None, value=None, left_child=None, right_child=None):
        self.key = key
        self.value = value
        self.left_child = left_child
        self.right_child = right_child


class Tree:
    def __init__(self):
        self.root = None

    def search(self, key):
        actual = self.root
        while actual:
            if actual.key == key:
                return actual.value
            elif actual.key < key:
                actual = actual.right_child
            else:
                actual = actual.left_child
        return None

    def insert(self, key, value):
        actual = self.root
        added = Node(key, value)
        if actual:
            previous = None
            replaced = 0
            while actual:
                if actual.key == key:
                    actual.value = added.value
                    replaced = 1
                    break
                elif actual.key < key:
                    previous = actual
                    actual = actual.right_child
                elif actual.key > key:
                    previous = actual
                    actual = actual.left_child
            if replaced == 0:
                if added.key < previous.key:
                    previous.left_child = added
                else:
                    previous.right_child = added
        else:
            self.root = added

    def delete(self, key):
        previous = None
        actual = self.root
        while actual:
            if actual.key == key:
                if not actual.left_child and not actual.right_child:  # brak dzieci
                    if previous:
                        if previous.left_child == actual:
                            previous.left_child = None
                        else:
                            previous.right_child = None
                    else:
                        self.root = None
                    break
                elif actual.left_child and not actual.right_child:  # lewe dziecko
                    if previous:
                        if previous.left_child == actual:
                            previous.left_child = actual.left_child
                        else:
                            previous.right_child = actual.left_child
                    else:
                        self.root = actual.left_child
                    break
                elif not actual.left_child and actual.right_child:  # prawe dziecko
                    if previous:
                        if previous.left_child == actual:
                            previous.left_child = actual.right_child
                        else:
                            previous.right_child = actual.right_child
                    else:
                        self.root = actual.right_child
                    break
                else:   # oboje dzieci
                    min = actual.right_child
                    while min.left_child:
                        min = min.left_child
                    self.delete(min.key)
                    min.left_child, min.right_child = actual.left_child, actual.right_child
                    if previous:
                        if previous.left_child == actual:
                            previous.left_child = min
                        else:
                            previous.right_child = min
                    else:
                        self.root = min
                    break

            elif actual.key < key:  # klucz aktualnego jest minejszy niż szukany -> idziemy w prawo
                previous = actual
                actual = actual.right_child
            else:  # klucz aktualnego jest większy niż szukany -> idziemy w lewo
                previous = actual
                actual = actual.left_child

    def heigh(self, key):
        start = self.root
        if start:
            while start:
                if start.key == key:
                    break
                elif start.key < key:
                    start = start.right_child
                else:
                    start = start.left_child

            heigh = 1
            actual = start
            while actual:
                if actual.left_child and actual.right_child:
                    heigh_left = self.heigh(actual.left_child.key)
                    heigh_right = self.heigh(actual.right_child.key)
                    if heigh_left > heigh_right:
                        heigh += heigh_left
                    else:
                        heigh += heigh_right
                    break
                elif actual.left_child:
                    actual = actual.left_child
                    heigh += 1
                elif actual.right_child:
                    actual = actual.right_child
                    heigh += 1
                else:
                    break
            return heigh

        else:
            return 0

    def in_order(self):
        result = ""
        help_tree = Tree()
        actual = self.root
        if actual.left_child:
            help_tree.root = actual.left_child
            result += help_tree.in_order()
        node = "{" + f"{actual.key}:{actual.value}" + "}, "
        result += node
        if actual.right_child:
            help_tree.root = actual.right_child
            result += help_tree.in_order()
        return result

    def print(self):
        result = "[" + self.in_order()[:-2] + "]"
        print(result)

    def print_tree(self):
        print("==============")
        self._print_tree(self.root, 0)
        print("==============")

    def _print_tree(self, node, lvl):
        if node is not None:
            self._print_tree(node.right_child, lvl + 5)

            print()
            print(lvl * " ", node.key, node.value)

            self._print_tree(node.left_child, lvl + 5)


def main():
    drzewo1 = Tree()
    keys = [50, 15, 62, 5, 20, 58, 91, 3, 8, 37, 60, 24]
    for i in range(len(keys)):
        drzewo1.insert(keys[i], chr(ord('A')+i))

    drzewo1.print_tree()
    drzewo1.print()
    print(drzewo1.search(24))
    drzewo1.insert(20, 'AA')
    drzewo1.insert(6, 'M')
    drzewo1.delete(62)
    drzewo1.insert(59, 'N')
    drzewo1.insert(100, 'P')
    drzewo1.delete(8)
    drzewo1.delete(15)
    drzewo1.insert(55, 'R')
    drzewo1.delete(50)
    drzewo1.delete(5)
    drzewo1.delete(24)
    print(drzewo1.heigh(drzewo1.root.key))
    drzewo1.print()
    drzewo1.print_tree()


if __name__ == '__main__':
    main()

