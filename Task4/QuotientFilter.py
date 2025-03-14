import mmh3


class QuotientFilter:
    def __init__(self, size, remainder_bits, seed=None):
        self.size = size
        self.remainder_bits = remainder_bits
        self.table = [None] * size
        self.occupied = [False] * size  # Q-bit: каноническая ячейка занята
        self.shift = [False] * size  # S-bit: элемент вставлен не в свою каноническую ячейку
        self.continuation = [False] * size  # C-bit: элемент является продолжением
        if seed is None:
            from random import randint
            self.seed = randint(1, 100)
        else:
            self.seed = seed

    def _hash(self, x):
        h = mmh3.hash(x, seed=self.seed)
        quotient = h % self.size
        remainder = h % (2 ** self.remainder_bits)
        return quotient, remainder

    def insert(self, x):
        q, r = self._hash(x)

        if not self.occupied[q]:    # Если каноническая ячейка q свободна, вставляем туда элемент.
            self.table[q] = r
            self.occupied[q] = True
            self.shift[q] = False
            self.continuation[q] = False
            return

        # Если ячейка q занята, ищем следующий свободный слот для вставки.
        index = (q + 1) % self.size
        while self.occupied[index]:
            index = (index + 1) % self.size

        self.table[index] = r
        self.occupied[index] = True
        self.shift[index] = True
        if index == (q + 1) % self.size:
            self.continuation[index] = False
        else:
            self.continuation[index] = True

    def check(self, x):
        q, r = self._hash(x)
        if not self.occupied[q]:
            return False

        if self.table[q] == r:
            return True

        index = (q + 1) % self.size
        while self.occupied[index] and self.continuation[index]:
            if self.table[index] == r:
                return True
            index = (index + 1) % self.size

        return False
