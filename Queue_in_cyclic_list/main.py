# skończone

def realloc(tab, size):
    oldSize = len(tab)
    return [tab[i] if i < oldSize else None for i in range(size)]


class Queue:

    def __init__(self):
        self.size = 5
        self.queue = [None for i in range(self.size)]
        self.read_idx = 0
        self.write_idx = 0

    def is_empty(self):
        if self.read_idx == self.write_idx:
            return True
        else:
            return False

    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.queue[self.read_idx]

    def dequeue(self):
        if self.is_empty():
            return None
        else:
            self.read_idx += 1
            if self.read_idx == self.size:
                self.read_idx = 0
            result, self.queue[self.read_idx - 1] = self.queue[self.read_idx - 1], None
            return result

    def enqueue(self, data):
        self.queue[self.write_idx] = data
        self.write_idx += 1
        if self.write_idx == self.size:
            self.write_idx = 0
        if self.write_idx == self.read_idx:
            self.queue = realloc(self.queue, 2 * self.size)
            for i in range(self.read_idx, self.size):
                self.queue[i], self.queue[i + self.size] = None, self.queue[i]
            self.read_idx += self.size
            self.size *= 2

    def print_tab(self):
        print(self.queue)

    def print_queue(self):
        result = "["
        for i in range(self.read_idx, self.size):
            if self.queue[i] is not None:
                if i == self.read_idx:
                    result += f'{self.queue[i]}'
                else:
                    result += f', {self.queue[i]}'
        for i in range(self.read_idx):
            if self.queue[i] is not None:
                result += f', {self.queue[i]}'
        result += "]"
        print(result)


def main():
    queue1 = Queue()

    queue1.enqueue(1)
    queue1.enqueue(2)
    queue1.enqueue(3)
    queue1.enqueue(4)

    print(queue1.dequeue())
    print(queue1.peek())

    queue1.print_queue()

    queue1.enqueue(5)
    queue1.enqueue(6)
    queue1.enqueue(7)
    queue1.enqueue(8)

    queue1.print_tab()

    while not queue1.is_empty():
        print(queue1.dequeue())

    queue1.print_queue()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
