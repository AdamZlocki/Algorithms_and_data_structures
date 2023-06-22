# skończone

class Elem:
    def __init__(self, value, priority):
        self.value = value
        self.priority = priority

    def __str__(self):
        result = f"{self.priority} : {self.value}"
        return result

    def __lt__(self, other):
        if self.priority < other.priority:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.priority > other.priority:
            return True
        else:
            return False


class Queue:
    def __init__(self):
        self.tab = []

    def is_empty(self):
        if not self.tab:
            return True
        else:
            return False

    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.tab[0].value

    def dequeue(self):
        if self.is_empty():
            return None
        elif len(self.tab) == 1:
            return self.tab.pop().value
        else:
            self.tab[0], self.tab[-1] = self.tab[-1], self.tab[0]
            result = self.tab.pop().value

            actual_idx = 0
            while actual_idx > -1:
                actual = self.tab[actual_idx]

                left_child_idx = self.left(actual_idx)
                right_child_idx = self.right(actual_idx)

                left_child = None
                right_child = None
                if left_child_idx:
                    left_child = self.tab[left_child_idx]
                if right_child_idx:
                    right_child = self.tab[right_child_idx]
                if left_child and right_child:
                    if not left_child < right_child:
                        if not actual < left_child:
                            break
                        else:
                            self.tab[actual_idx], self.tab[left_child_idx] = self.tab[left_child_idx], self.tab[
                                actual_idx]
                            actual_idx = self.left(actual_idx)
                    else:
                        if not actual < right_child:
                            break
                        else:
                            self.tab[actual_idx], self.tab[right_child_idx] = self.tab[right_child_idx], self.tab[
                                actual_idx]
                            actual_idx = self.right(actual_idx)
                elif left_child and not right_child:
                    if not actual < left_child:
                        break
                    else:
                        self.tab[actual_idx], self.tab[left_child_idx] = self.tab[left_child_idx], \
                                                                         self.tab[actual_idx]
                        actual_idx = self.left(actual_idx)
                elif not left_child and right_child:
                    if not actual < right_child:
                        break
                    else:
                        self.tab[actual_idx], self.tab[right_child_idx] = self.tab[right_child_idx], self.tab[
                            actual_idx]
                        actual_idx = self.right(actual_idx)
                else:
                    break

            return result

    def enqueue(self, value, priority):
        added = Elem(value, priority)
        self.tab.append(added)

        actual_idx = len(self.tab) - 1
        while actual_idx > -1:
            actual = self.tab[actual_idx]
            parent_key = self.parent(actual_idx)
            if parent_key is not None:
                parent = self.tab[parent_key]
                if parent < actual:
                    self.tab[actual_idx], self.tab[parent_key] = self.tab[parent_key], self.tab[actual_idx]
                    actual_idx = self.parent(actual_idx)
                else:
                    break
            else:
                break

    def left(self, idx):
        return_idx = 2 * idx + 1
        if return_idx >= len(self.tab):
            return None
        else:
            return return_idx

    def right(self, idx):
        return_idx = 2 * idx + 2
        if return_idx >= len(self.tab):
            return None
        else:
            return return_idx

    def parent(self, idx):
        if idx == 0:
            return None
        else:
            return_idx = (idx - 1) // 2
            return return_idx

    def print_tab(self):
        print('{', end=' ')
        if not self.is_empty():
            for i in range(len(self.tab) - 1):
                print(self.tab[i], end=', ')
            if self.tab[len(self.tab) - 1]:
                print(self.tab[len(self.tab) - 1], end=' ')
        print('}')

    def print_tree(self, idx, lvl):
        if idx is not None:
            if idx < len(self.tab):
                self.print_tree(self.right(idx), lvl + 1)
                print(2 * lvl * '  ', self.tab[idx] if self.tab[idx] else None)
                self.print_tree(self.left(idx), lvl + 1)


def main():
    kolejka1 = Queue()
    keys = [4, 7, 6, 7, 5, 2, 2, 1]
    values = "ALGORYTM"
    for i in range(len(keys)):
        kolejka1.enqueue(values[i], keys[i])
    kolejka1.print_tree(0, 0)
    kolejka1.print_tab()
    print(kolejka1.dequeue())
    print(kolejka1.peek())
    kolejka1.print_tab()
    while not kolejka1.is_empty():
        print(kolejka1.dequeue())
    kolejka1.print_tab()


if __name__ == '__main__':
    main()
