from random import randint

def hash_with_seed(seed):
    return lambda value: seed*hash(value)

def get_seeds(n):
    seeds = set()
    while len(seeds) < n:
        seeds.add(randint(-9999, 9999))
    return seeds

class MinHashAlgorithm:
    def __init__(self, k):
        self.k = k
        self.hash_funcs = [hash_with_seed(seed) for seed in get_seeds(k)]

    def execute(self, array):
        return [min([hash_func(element) for element in array]) for hash_func in self.hash_funcs]

    def compare(self, min_hashes1, min_hashes2):
        pass