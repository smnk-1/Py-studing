from random import randint


class HashFunction:
    def __init__(self, seed):
        self.r = seed

    def execute(self, s):
        value = 0
        for i, char in enumerate(s):
            value += (ord(char)*(i+1))*self.r
        return value


class BloomCountFilter:
    def __init__(self, m, k):
        self.m = m
        self.k = k
        self.seeds = set()
        while len(self.seeds) < k:
            self.seeds.add(randint(2, 100))
        self.hash_functions = [HashFunction(list(self.seeds)[i]) for i in range(0, self.k)]
        self.count_array = [0]*m

    def _get_hash(self, string):
        return [(f.execute(string)) % self.m for f in self.hash_functions]

    def add(self, string):
        hashes = self._get_hash(string)
        for bit in hashes:
            self.count_array[bit] += 1

    def check(self, string):
        checking_hash = self._get_hash(string) # может выдавать неправильно, если определенное число накидывает в бины больше 1
        for bit in checking_hash:
            if self.count_array[bit] == 0:
                return False
        return True

    def delete(self, string):
        if self.check(string):
            for bit in self._get_hash(string):
                self.count_array[bit] -= 1

    def unite_filters(self, bloom_count_filter):
        if self.m == bloom_count_filter.m and self.k == bloom_count_filter.k:
            new_count_array = []
            for i in range(0, self.m):
                new_count_array[i] = max(self.count_array[i], bloom_count_filter.count_array[i])
            self.count_array = new_count_array

    def intersect_filters(self, bloom_count_filter):
        if self.m == bloom_count_filter.m and self.k == bloom_count_filter.k:
            new_count_array = []
            for i in range(0, self.m):
                new_count_array[i] = min(self.count_array[i], bloom_count_filter.count_array[i])
            self.count_array = new_count_array
