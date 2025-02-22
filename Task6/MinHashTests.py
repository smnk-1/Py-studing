from MinHash import MinHashAlgorithm
from random import randint

def generate_items(n):
    return [str(randint(0, 10_000)) for _ in range(0, n)]

