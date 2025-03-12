from HyperLogLog import HyperLogLog
from random import randint
import matplotlib.pyplot as plt

def run_empirical_test(true_cardinality, b_values):
    _results = {}
    unique_elements = {str(randint(0, 10 ** 9)) for _ in range(true_cardinality)}

    for b in b_values:
        hll = HyperLogLog(b)

        for elem in unique_elements:
            hll.proceed_element(elem)

        estimated = hll.estimate_cardinality()
        error = abs(estimated - true_cardinality) / true_cardinality
        _results[b] = (estimated, error)

    return _results


true_cardinality = 100_000
buckets = range(4, 16)

results = run_empirical_test(true_cardinality, buckets)

b_list = list(results.keys())
estimated_values = [results[b][0] for b in b_list]
errors = [results[b][1] for b in b_list]

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(b_list, estimated_values, marker='o', linestyle='-', label='Оценка')
plt.axhline(y=true_cardinality, color='r', linestyle='--', label='Реальное значение')
plt.xlabel('b (логарифм числа корзин)')
plt.ylabel('Оценённое кол-во уникальных')
plt.title('Оценка количества уникальных элементов')
plt.legend()
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(b_list, errors, marker='o', linestyle='-', color='orange')
plt.xlabel('b (логарифм числа корзин)')
plt.ylabel('Относительная ошибка')
plt.title('Ошибка в зависимости от числа корзин')
plt.grid()

plt.tight_layout()
plt.savefig('../Images/HyperLogLogEmpiricalTests')
plt.show()
