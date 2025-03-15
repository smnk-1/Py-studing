import random


class CountMinSketch:
    def __init__(self, width, depth):
        self.width = width
        self.depth = depth
        self.table = [[0] * width for _ in range(depth)]
        self.seeds = [random.randint(0, 100000) for _ in range(depth)]

    def add(self, item, count=1):
        for i in range(self.depth):
            index = hash((self.seeds[i], item)) % self.width
            self.table[i][index] += count

    def frequency(self, item):
        min_count = float('inf')
        for i in range(self.depth):
            index = hash((self.seeds[i], item)) % self.width
            min_count = min(min_count, self.table[i][index])
        return min_count
