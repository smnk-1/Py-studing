from MinHash import MinHashAlgorithm
from random import randint


def jaccard_similarity(A, B):
    a = set(A)
    b = set(B)
    union = set.union(a, b)
    intersection = set.intersection(a, b)
    if len(union) != 0:
        return len(intersection)/len(union)
    else:
        return 1


def generate_items(n):
    return [str(randint(0, 10_000)) for _ in range(0, n)]


