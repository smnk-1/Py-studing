import random
import matplotlib.pyplot as plt
import seaborn as sns
from CountMinSketch import CountMinSketch


def simulate_false_positive_rate(n, width, depth, test_size=1000, iterations=10):
    rates = []
    for _ in range(iterations):
        cms = CountMinSketch(width, depth)
        for _ in range(n):
            item = random.randint(0, n * 10)
            cms.add(item)
        false_positive_count = 0
        for _ in range(test_size):
            test_item = random.randint(n * 10 + 1, n * 10 * 2)
            if cms.frequency(test_item) > 0:
                false_positive_count += 1
        rate = (false_positive_count / test_size) * 100
        rates.append(rate)
    return sum(rates) / len(rates)


def theoretical_fp_rate(n, width, depth):
    p = 1 - (1 - 1 / width) ** n
    fp = (p ** depth) * 100
    return fp


def main():
    sns.set(style='whitegrid')

    # Параметры CMS
    width = 1000
    depth = 5
    test_size = 1000
    iterations = 10

    n_values = [100, 500, 1000, 2000, 5000, 10000]
    simulated_rates = []
    theoretical_rates = []

    for n in n_values:
        sim_rate = simulate_false_positive_rate(n, width, depth, test_size, iterations)
        theo_rate = theoretical_fp_rate(n, width, depth)
        simulated_rates.append(sim_rate)
        theoretical_rates.append(theo_rate)

    plt.figure(figsize=(10, 6))
    plt.plot(n_values, simulated_rates, marker='o', label='Simulated FP Rate')
    plt.plot(n_values, theoretical_rates, marker='s', linestyle='--', label='Theoretical FP Rate')
    plt.xscale('log')
    plt.xlabel('Количество добавленных элементов (n)')
    plt.ylabel('Ложноположительное срабатывание (%)')
    plt.title('Зависимость ложно-положительных срабатываний от количества добавленных элементов')
    plt.legend()
    plt.tight_layout()
    plt.savefig('../Images/CountMinSketchEmpiricalTestsResults')
    plt.show()


if __name__ == '__main__':
    main()
