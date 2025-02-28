import mmh3
from random import randint


def get_seeds(n):
    seeds = set()
    while len(seeds) < n:
        seeds.add(randint(1, 10000))
    return list(seeds)


def compare(signature1, signature2):
    matches = sum(1 for x, y in zip(signature1, signature2) if x == y)
    return matches / len(signature1)


class MinHashAlgorithm:
    def __init__(self, k):
        self.seeds = get_seeds(k)

    def execute(self, array):
        signature = []
        for seed in self.seeds:
            hash_values = [mmh3.hash(x, seed=seed) for x in array]
            signature.append(min(hash_values))
        return signature
