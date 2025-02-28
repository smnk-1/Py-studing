from random import randint


def hash_with_seed(seed):
    return lambda value: seed*hash(value)


def get_seeds(n):
    seeds = set()
    while len(seeds) < n:
        seeds.add(randint(-9999, 9999))
    return seeds


def compare(signature1, signature2):
    matches = sum(1 for x, y in zip(signature1, signature2) if x == y)
    return matches / len(signature1)


class MinHashAlgorithm:
    def __init__(self, k):
        self.k = k
        self.hash_funcs = [hash_with_seed(seed) for seed in get_seeds(k)]

    def execute(self, array):
        signature = []
        for h in self.hash_funcs:
            hash_res = []
            for element in array:
                hash_res.append(h(element))
            signature.append(min(hash_res))
        return signature
