from random import randint


class HashFunction:
    def __init__(self):
        self.r = randint(1, 100) # значения r могут пересекаться, можно исправить используя set в конструкторе фильтра, вынести отсюда генерацию

    def execute(self, s):
        value = 0
        for i, char in enumerate(s):
            value += (ord(char)*(i+1))*self.r
        return value


class BloomFilter:  # если элемент был добавлен, он должен определяться как присутствующий
    def __init__(self, m, k):
        self.m = m
        self.k = k
        self.hash_functions = [HashFunction() for _ in range(0, self.k)]
        self.bit_array = [0]*m

    def _get_hash(self, string):
        return [(f.execute(string)) % self.m for f in self.hash_functions]

    def add(self, string):
        hashes = self._get_hash(string)
        for bit in hashes:
            self.bit_array[bit] = 1

    def check(self, string):
        checking_hash = self._get_hash(string)
        for bit in checking_hash:
            if self.bit_array[bit] == 0:
                return False
        return True

    def unite_filters(self, bloom_filter):
        if self.m == bloom_filter.m and self.k == bloom_filter.k:
            new_bit_array =[]
            for i in range(0, self.m):
                new_bit_array[i] = self.bit_array[i] or bloom_filter.bit_array[i]
            self.bit_array = new_bit_array

    def intersect_filters(self, bloom_filter):
        if self.m == bloom_filter.m and self.k == bloom_filter.k:
            new_bit_array =[]
            for i in range(0, self.m):
                new_bit_array[i] = self.bit_array[i] and bloom_filter.bit_array[i]
            self.bit_array = new_bit_array
