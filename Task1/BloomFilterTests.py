from BloomFilter import BloomFilter
from random import randint


def bloom_filter_test(items_to_add, items_to_check, bloom_filter):
    for item in items_to_add:
        bloom_filter.add(item)

    false_positive_count = 0

    for item in items_to_check:
        if bloom_filter.check(item) and item not in items_to_add:
            false_positive_count += 1

    return false_positive_count / len(items_to_check)


def generate_unique_items(count, start=1_000, end=1_000_000):
    items = set()
    while len(items) < count:
        items.add(str(randint(start, end)))
    return list(items)


items_to_add = generate_unique_items(10_000)
items_to_check = generate_unique_items(100, start=1_000_001, end=2_000_000)

m = 5_000
k = 7
bloom_filter = BloomFilter(m, k)
tests_number = 100
value = 0
for _ in range(0, tests_number):
    value += bloom_filter_test(items_to_add, items_to_check, bloom_filter)

print(f'Вероятность ложно-положительного срабатывания при m={m}, k={k}: '
      f'{round(value/tests_number*100, 3)}%')
