class TriDeque:
    def __init__(self, max_size):
        self.queue = []
        self.max_size = max_size

    def push_left(self, item):
        if len(self.queue) < self.max_size:
            self.queue.insert(0, item)
        else:
            print("Queue is full")

    def push_right(self, item):
        if len(self.queue) < self.max_size:
            self.queue.append(item)
        else:
            print("Queue is full")

    def push(self, item):
        self.push_right(item)

    def pop_left(self):
        if len(self.queue) > 0:
            return self.queue.pop(0)
        else:
            print("Queue is empty")

    def pop_right(self):
        if len(self.queue) > 0:
            return self.queue.pop()
        else:
            print("Queue is empty")

    def size(self):
        return len(self.queue)

    def __getitem__(self, index):
        return self.queue[index]

    def __iter__(self):
        return iter(self.queue)

