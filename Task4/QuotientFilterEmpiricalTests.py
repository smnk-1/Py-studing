import random
import string
import matplotlib.pyplot as plt
import seaborn as sns
from QuotientFilter import QuotientFilter


def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def empirical_test():
    sns.set_theme(style='darkgrid')

    size = 1000
    remainder_bits = 8

    inserted_counts = list(range(0, 950, 50))
    false_positive_rates = []
    num_queries = 10000

    for count in inserted_counts:
        qf = QuotientFilter(size=size, remainder_bits=remainder_bits, seed=42)
        inserted_set = set()

        while len(inserted_set) < count:
            inserted_set.add(random_string(8))
        for key in inserted_set:
            qf.insert(key)

        false_positive = 0
        total_queries = 0
        while total_queries < num_queries:
            query = random_string(8)
            if query in inserted_set:
                continue
            total_queries += 1
            if qf.check(query):
                false_positive += 1
        false_positive_rate = false_positive / num_queries
        false_positive_rates.append(false_positive_rate)

    plt.figure(figsize=(10, 6))
    sns.lineplot(x=inserted_counts, y=false_positive_rates, marker='o', linewidth=2.5, color='green', alpha=0.35)
    sns.regplot(x=inserted_counts, y=false_positive_rates, scatter=False, color='blue', order=2)

    plt.xlabel('Number of Inserted Items', fontsize=12)
    plt.ylabel('False Positive Rate', fontsize=12)
    plt.title('False Positive Rate vs. Inserted Items (Quotient Filter)', fontsize=14)
    plt.legend()
    plt.savefig('../Images/QF_EmpiricalTests.png', dpi=300)
    plt.show()


if __name__ == '__main__':
    empirical_test()
