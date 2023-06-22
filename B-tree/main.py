# skończone

class Node:
    def __init__(self, num_of_children):
        self.keys = []
        self.children = [None] * num_of_children
        self.size = 0

    def insert_node(self, key, child=None):
        if self.size == len(self.children) - 1:
            middle = self.keys.pop(int(self.size/2))
            new_node = Node(len(self.children))
            for i in range(int(self.size/2) + 1, self.size):
                new_node.keys.append(self.keys.pop(int(self.size/2)))
                new_node.size += 1
            for i in range(int(self.size/2) + 1, self.size + 1):
                new_node.children[i - int(self.size/2) - 1] = self.children[i]
                self.children[i] = None

            self.size = len(self.keys)
            if key > middle:
                new_node.insert_node(key)
            else:
                self.insert_node(key)
            return middle, new_node

        else:
            idx = 0
            if self.size > 0:
                if key > self.keys[-1]:
                    idx = self.size
                else:
                    for i in range(self.size):
                        if self.keys[i] > key:
                            idx = i
                            break

            if idx == self.size:
                self.keys.append(key)
            else:
                self.keys.append(None)
                actual = key
                for i in range(idx, len(self.keys)):
                    self.keys[i], actual = actual, self.keys[i]
            actual = child
            for i in range(idx, len(self.keys)):
                self.children[i + 1], actual = actual, self.children[i + 1]
            self.size += 1
            return None


class Tree:
    def __init__(self, num_of_children):
        self.num_of_children = num_of_children
        self.root = Node(self.num_of_children)

    def insert(self, actual, key):
        idx = 0
        if actual.size > 0:
            if key > actual.keys[-1]:
                idx = actual.size
            else:
                for i in range(actual.size):
                    if actual.keys[i] > key:
                        idx = i
                        break

        if not actual.children[0]:
            result = actual.insert_node(key)
            if actual == self.root:
                if result:
                    new_root = Node(self.num_of_children)
                    new_root.keys.append(result[0])
                    new_root.size = len(new_root.keys)
                    new_root.children[0], new_root.children[1] = self.root, result[1]
                    self.root = new_root

            return result
        else:
            result = self.insert(actual.children[idx], key)
            if result:
                new_result = actual.insert_node(result[0], result[1])
                if actual == self.root:
                    if new_result:
                        new_root = Node(self.num_of_children)
                        new_root.keys.append(new_result[0])
                        new_root.size = len(new_root.keys)
                        for i in range(len(new_result[1].children)):
                            if new_result[1].children[i] is None:
                                new_result[1].children[i] = result[1]
                                break
                        new_root.children[0], new_root.children[1] = self.root, new_result[1]
                        self.root = new_root
                else:
                    if new_result:
                        for i in range(len(new_result[1].children)):
                            if new_result[1].children[i] is None:
                                new_result[1].children[i] = result[1]
                                break
                    return new_result

    def print_tree(self):
        print("==============")
        self._print_tree(self.root, 0)
        print("==============")

    def _print_tree(self, node, lvl):
        if node is not None:
            for i in range(node.size + 1):
                self._print_tree(node.children[i], lvl + 1)
                if i < node.size:
                    print(lvl * '  ', node.keys[i])


def main():
    drzewo1 = Tree(4)
    keys = [5, 17, 2, 14, 7, 4, 12, 1, 16, 8, 11, 9, 6, 13, 0, 3, 18, 15, 10, 19]
    for i in keys:
        drzewo1.insert(drzewo1.root, i)
    drzewo1.print_tree()

    drzewo2 = Tree(4)
    for i in range(20):
        drzewo2.insert(drzewo2.root, i)
    drzewo2.print_tree()

    for i in range(20, 200):
        drzewo2.insert(drzewo2.root, i)
    drzewo2.print_tree()

    drzewo3 = Tree(6)
    for i in range(200):
        drzewo3.insert(drzewo3.root, i)
    drzewo3.print_tree()


if __name__ == '__main__':
    main()
