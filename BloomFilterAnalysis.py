import pandas as pd
import matplotlib.pyplot as plt
from random import randint
from BloomFilter import BloomFilter


def generate_unique_items(count, start=1_000, end=1_000_000):
    items = set()
    while len(items) < count:
        items.add(str(randint(start, end)))
    return list(items)


def experiment(m, k, times, items_n):
    false_positive_count = 0
    for _ in range(0, times):
        bf = BloomFilter(m, k)
        items_to_add = generate_unique_items(items_n)
        items_to_check = generate_unique_items(items_n, 1_000_001, 2_000_000)

        for item in items_to_add:
            bf.add(item)

        for item in items_to_check:
            if bf.check(item):
                false_positive_count += 1

    return false_positive_count / (times*items_n)


m_values = [100, 300, 500, 1000]
k_values = [x for x in range(1, 10)]
times = 100
items_n = 100

results = []
for m in m_values:
    for k in k_values:
        res = experiment(m, k, times, items_n)
        results.append({'m': m, 'k': k, 'res': res})
df = pd.DataFrame(results)
print("Результаты экспериментов:")
print(df) # нормальную табличку вывода значений на экран

plt.figure(figsize=(10, 6))
for m in m_values:
    subset = df[df["m"] == m]
    plt.plot(subset["k"], subset["res"], marker='o', label=f"m = {m}")

plt.xlabel("Число хеш-функций (k)")
plt.ylabel("Эмпирическая вероятность ложноположительного срабатывания")
plt.title("Зависимость вероятности от числа хеш-функций для различных m (m фиксировано)")
plt.legend()
plt.grid(True)
plt.savefig('Images/Empirical_probability_of_a_false_positive.png')
plt.show()
plt.close()
