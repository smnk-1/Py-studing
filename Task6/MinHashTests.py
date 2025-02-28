from MinHash import MinHashAlgorithm, compare
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

common_elements = [f"word_{i}" for i in range(70)]

# 15 уникальных элементов для A
unique_A = [f"unique_A_{i}" for i in range(70, 85)]

# 15 уникальных элементов для B
unique_B = [f"unique_B_{i}" for i in range(85, 100)]

# Создаём массивы
A = common_elements + unique_A
B = common_elements + unique_B

for k in range(1, 20):
    j = 0
    J = jaccard_similarity(A, B)
    for i in range(0, 10):
        mnh = MinHashAlgorithm(k)
        s1 = mnh.execute(A)
        s2 = mnh.execute(B)
        j += compare(s1, s2)
    print(J, j/10)

