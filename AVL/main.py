# skończone

class Node:
    def __init__(self, key=None, value=None, left_child=None, right_child=None):
        self.key = key
        self.value = value
        self.left_child = left_child
        self.right_child = right_child
        self.balance = 0


class AVLTree:
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
        if self.search(key):
            actual = self.root
            added = Node(key, value)
            if actual:
                while actual:
                    if actual.key == key:
                        actual.value = added.value
                        break
                    elif actual.key < key:
                        actual = actual.right_child
                    elif actual.key > key:
                        actual = actual.left_child
        else:
            actual = self.root
            added = Node(key, value)
            if not actual:
                self.root = added
            else:
                help_tree = AVLTree()
                if actual.key < key:
                    if actual.right_child:
                        help_tree.root = actual.right_child
                        help_tree.insert(key, value)
                        actual.right_child = help_tree.root
                    else:
                        actual.right_child = added

                elif actual.key > key:
                    if actual.left_child:
                        help_tree.root = actual.left_child
                        help_tree.insert(key, value)
                        actual.left_child = help_tree.root
                    else:
                        actual.left_child = added

                left_height = 0
                right_height = 0
                if actual.left_child:
                    left_height = self.heigh(actual.left_child.key)
                if actual.right_child:
                    right_height = self.heigh(actual.right_child.key)
                actual.balance = left_height - right_height

                if actual.balance < -1:
                    self.rotate_left(actual)
                elif actual.balance > 1:
                    self.rotate_right(actual)

    def delete(self, key):
        if self.search(key):
            actual = self.root
            if actual.key == key:
                if actual.left_child and not actual.right_child:  # lewe dziecko
                    self.root = actual.left_child

                elif not actual.left_child and actual.right_child:  # prawe dziecko
                    self.root = actual.right_child

                else:  # oboje dzieci
                    min = actual.right_child
                    while min.left_child:
                        min = min.left_child
                    self.delete(min.key)
                    min.left_child, min.right_child = actual.left_child, actual.right_child
                    self.root = min

                    left_height = 0
                    right_height = 0
                    if min.left_child:
                        left_height = self.heigh(min.left_child.key)
                    if min.right_child:
                        right_height = self.heigh(min.right_child.key)
                    min.balance = left_height - right_height

                    left_height = 0
                    right_height = 0
                    if min.right_child.left_child:
                        left_height = self.heigh(min.right_child.left_child.key)
                    if min.right_child.right_child:
                        right_height = self.heigh(min.right_child.right_child.key)
                    min.right_child.balance = left_height - right_height

            else:
                if actual.left_child.key == key or actual.right_child.key == key: #  dziecko aktualnego jest usuwanym elem
                    child = actual.left_child
                    if actual.right_child:
                        if actual.right_child.key == key:
                            child = actual.right_child
                    if not child.left_child and not child.right_child:  # brak dzieci
                        if actual.left_child == child:
                            actual.left_child = None
                        else:
                            actual.right_child = None

                    elif child.left_child and not child.right_child:  # lewe dziecko
                        if actual.left_child == child:
                            actual.left_child = child.left_child
                        else:
                            actual.right_child = child.left_child

                    elif not child.left_child and child.right_child:  # prawe dziecko
                        if actual.left_child == child:
                            actual.left_child = child.right_child
                        else:
                            actual.right_child = child.right_child

                    else:  # oboje dzieci
                        min = child.right_child
                        while min.left_child:
                            min = min.left_child
                        if min == child.right_child:
                            child.right_child = child.right_child.right_child
                        else:
                            self.delete(min.key)

                        min.left_child, min.right_child = child.left_child, child.right_child
                        if actual.left_child.key == child.key:
                            actual.left_child = min
                        else:
                            actual.right_child = min

                        left_height = 0
                        right_height = 0
                        if min.left_child:
                            left_height = self.heigh(min.left_child.key)
                        if min.right_child:
                            right_height = self.heigh(min.right_child.key)
                        min.balance = left_height - right_height

                        help_tree = AVLTree()
                        help_tree.root = min
                        if min.balance < -1:
                            help_tree.rotate_left(min)
                        elif min.balance > 1:
                            help_tree.rotate_right(min)

                        if actual.left_child.key == min.key:
                            actual.left_child = help_tree.root
                        else:
                            actual.right_child = help_tree.root

                        left_height = 0
                        right_height = 0
                        if min.right_child.left_child:
                            left_height = self.heigh(min.right_child.left_child.key)
                        if min.right_child.right_child:
                            right_height = self.heigh(min.right_child.right_child.key)
                        min.right_child.balance = left_height - right_height

                elif actual.key < key:  # klucz aktualnego jest minejszy niż szukany -> idziemy w prawo
                    help_tree = AVLTree()
                    help_tree.root = actual.right_child
                    help_tree.delete(key)
                    actual.right_child = help_tree.root

                else:  # klucz aktualnego jest większy niż szukany -> idziemy w lewo
                    help_tree = AVLTree()
                    help_tree.root = actual.left_child
                    help_tree.delete(key)
                    actual.left_child = help_tree.root

                left_height = 0
                right_height = 0
                if actual.left_child:
                    left_height = self.heigh(actual.left_child.key)
                if actual.right_child:
                    right_height = self.heigh(actual.right_child.key)
                actual.balance = left_height - right_height

                if actual.balance < -1:
                    self.rotate_left(actual)
                elif actual.balance > 1:
                    self.rotate_right(actual)

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
        help_tree = AVLTree()
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

    def rotate_left(self, actual):
        if actual.right_child:
            if actual.right_child.balance > 0:
                copy_actual_right_child = Node(actual.right_child.key, actual.right_child.value,
                                               actual.right_child.left_child.right_child,
                                               actual.right_child.right_child)
                left_height = 0
                right_height = 0
                if copy_actual_right_child.left_child:
                    left_height = self.heigh(copy_actual_right_child.left_child.key)
                if copy_actual_right_child.right_child:
                    right_height = self.heigh(copy_actual_right_child.right_child.key)
                copy_actual_right_child.balance = left_height - right_height

                actual.right_child = actual.right_child.left_child

                actual.right_child.right_child = copy_actual_right_child

            copy_actual = Node(actual.key, actual.value, actual.left_child, actual.right_child.left_child)

            self.root = actual.right_child
            actual = self.root
            actual.left_child = copy_actual

            left_height = 0
            right_height = 0
            if actual.left_child:
                left_height = self.heigh(actual.left_child.key)
            if actual.right_child:
                right_height = self.heigh(actual.right_child.key)
            actual.balance = left_height - right_height

            left_height = 0
            right_height = 0
            if actual.left_child.left_child:
                left_height = self.heigh(actual.left_child.left_child.key)
            if actual.left_child.right_child:
                right_height = self.heigh(actual.left_child.right_child.key)
            actual.left_child.balance = left_height - right_height

    def rotate_right(self, actual):
        if actual.left_child:
            if actual.left_child.balance < 0:
                copy_actual_left_child = Node(actual.left_child.key, actual.left_child.value,
                                              actual.left_child.left_child, actual.left_child.right_child.left_child)

                left_height = 0
                right_height = 0
                if copy_actual_left_child.left_child:
                    left_height = self.heigh(copy_actual_left_child.left_child.key)
                if copy_actual_left_child.right_child:
                    right_height = self.heigh(copy_actual_left_child.right_child.key)
                copy_actual_left_child.balance = left_height - right_height

                actual.left_child = actual.left_child.right_child

                actual.left_child.left_child = copy_actual_left_child

            copy_actual = Node(actual.key, actual.value, actual.left_child.right_child, actual.right_child)

            self.root = actual.left_child
            actual = self.root
            actual.right_child = copy_actual

            left_height = 0
            right_height = 0
            if actual.left_child:
                left_height = self.heigh(actual.left_child.key)
            if actual.right_child:
                right_height = self.heigh(actual.right_child.key)
            actual.balance = left_height - right_height

            left_height = 0
            right_height = 0
            if actual.right_child.left_child:
                left_height = self.heigh(actual.right_child.left_child.key)
            if actual.right_child.right_child:
                right_height = self.heigh(actual.right_child.right_child.key)
            actual.right_child.balance = left_height - right_height


def main():
    drzewo1 = AVLTree()
    keys = [50, 15, 62, 5, 2, 1, 11, 100, 7, 6, 55, 52, 51, 57, 8, 9, 10, 99, 12]
    for i in range(len(keys)):
        drzewo1.insert(keys[i], chr(ord('A') + i))

    drzewo1.print_tree()
    drzewo1.print()
    print(drzewo1.search(10))
    keys2 = [50, 52, 11, 57, 1, 12]
    for i in range(len(keys2)):
        drzewo1.delete(keys2[i])
    drzewo1.insert(3, "AA")
    drzewo1.insert(4, "BB")
    drzewo1.delete(7)
    drzewo1.delete(8)
    drzewo1.print_tree()
    drzewo1.print()

if __name__ == '__main__':
    main()
