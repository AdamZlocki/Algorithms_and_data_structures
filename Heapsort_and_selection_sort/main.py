# skończone
import random
import time
from typing import List


class Elem:
    def __init__(self, value, priority):
        self.value = value
        self.priority = priority

    def __repr__(self):
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
    def __init__(self, tab=None):
        if not tab:
            self.tab = []
            self.size = 0
        else:
            self.tab = tab
            self.size = len(self.tab)
            self.hipify()

    def hipify(self):
        for i in range(self.size - 1, -1, -1):
            left_child_idx = self.left(i)
            right_child_idx = self.right(i)
            if left_child_idx or right_child_idx:
                self.repair(i)

    def is_empty(self):
        if self.size == 0:
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
            result = self.tab[0].value
            return result
        else:
            self.size -= 1
            self.tab[0], self.tab[self.size] = self.tab[self.size], self.tab[0]

            result = self.tab[self.size].value

            self.repair(0)
            return result

    def repair(self, actual_idx):
        left_child_idx = self.left(actual_idx)
        right_child_idx = self.right(actual_idx)
        while left_child_idx:
            actual = self.tab[actual_idx]
            right_child = None
            left_child = self.tab[left_child_idx]
            if right_child_idx:
                right_child = self.tab[right_child_idx]
            if left_child and right_child:
                if actual < left_child or actual < right_child:
                    if not left_child < right_child:
                        self.tab[actual_idx], self.tab[left_child_idx] = self.tab[left_child_idx], self.tab[actual_idx]
                        actual_idx = left_child_idx
                        left_child_idx = self.left(actual_idx)
                        right_child_idx = self.right(actual_idx)
                    else:
                        self.tab[actual_idx], self.tab[right_child_idx] = self.tab[right_child_idx], \
                                                                          self.tab[actual_idx]
                        actual_idx = right_child_idx
                        left_child_idx = self.left(actual_idx)
                        right_child_idx = self.right(actual_idx)
                else:
                    break
            elif left_child and not right_child:
                if not actual < left_child:
                    break
                else:
                    self.tab[actual_idx], self.tab[left_child_idx] = self.tab[left_child_idx], self.tab[actual_idx]
                    actual_idx = left_child_idx
                    left_child_idx = self.left(actual_idx)
                    right_child_idx = self.right(actual_idx)

    def enqueue(self, value, priority):
        added = Elem(value, priority)
        self.tab.append(added)
        self.size += 1

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
        if return_idx >= self.size:
            return None
        else:
            return return_idx

    def right(self, idx):
        return_idx = 2 * idx + 2
        if return_idx >= self.size:
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


def swap(list):
    if isinstance(list, List):
        for i in range(len(list) - 1):
            minimum_idx = list.index(min(list[i:]))
            list[i], list[minimum_idx] = list[minimum_idx], list[i]
        return list
    else:
        return None


def shift(list):
    if isinstance(list, List):
        for i in range(len(list) - 1):
            minimum_idx = list.index(min(list[i:]))
            list.insert(i, list.pop(minimum_idx))
        return list
    else:
        return None


def main():
    data = [(5, 'A'), (5, 'B'), (7, 'C'), (2, 'D'), (5, 'E'), (1, 'F'), (7, 'G'), (5, 'H'), (1, 'I'), (2, 'J')]

    for i in range(len(data)):
        data[i] = Elem(data[i][1], data[i][0])

    kolejka1 = Queue(data)
    kolejka1.print_tab()
    kolejka1.print_tree(0, 0)
    while not kolejka1.is_empty():
        kolejka1.dequeue()
    kolejka1.print_tab()
    print('Niestabilne (kopiec)')

    kolejka2 = Queue()
    while kolejka2.size < 10000:
        data_num = int(random.random() * 100)
        kolejka2.enqueue("A", data_num)

    t_start = time.perf_counter()
    while not kolejka2.is_empty():
        kolejka2.dequeue()
    t_stop = time.perf_counter()
    print("Czas obliczeń (kopiec):", "{:.7f}".format(t_stop - t_start))

    kolejka1_swap = data
    print(swap(kolejka1_swap))
    print('Niestabilne (swap)')

    kolejka1_shift = data
    print(shift(kolejka1_shift))
    print('Niestabilne (shift)')

    kolejka2_swap = []
    while len(kolejka2_swap) < 10000:
        data_num = int(random.random() * 1000)
        kolejka2_swap.append(Elem("A", data_num))
    t_start = time.perf_counter()
    swap(kolejka2_swap)
    t_stop = time.perf_counter()
    print("Czas obliczeń (swap):", "{:.7f}".format(t_stop - t_start))

    kolejka2_shift = []
    while len(kolejka2_shift) < 10000:
        data_num = int(random.random() * 1000)
        kolejka2_shift.append(Elem("A", data_num))
    t_start = time.perf_counter()
    shift(kolejka2_shift)
    t_stop = time.perf_counter()
    print("Czas obliczeń (shift):", "{:.7f}".format(t_stop - t_start))

    print('Obie metody ponad 100 razy wolniejsze niż sortowanie kopcowe')


if __name__ == '__main__':
    main()
