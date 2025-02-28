from MinHash import MinHashAlgorithm, compare
import pandas as pd
import matplotlib.pyplot as plt


def jaccard_similarity(A, B):
    setA = set(A)
    setB = set(B)
    union = setA.union(setB)
    intersection = setA.intersection(setB)
    return len(intersection) / len(union) if union else 1


common_count = 6500
unique_count = 1750


common_elements = [f'common_{i}' for i in range(common_count)]

unique_A = [f'unique_A_{i}' for i in range(common_count, common_count + unique_count)]
unique_B = [f'unique_B_{i}' for i in range(common_count + unique_count, common_count + 2 * unique_count)]

A = common_elements + unique_A
B = common_elements + unique_B


J_true = jaccard_similarity(A, B)
print('Истинная Jaccard-схожесть:', J_true)


results = []
trials = 15
for k in range(1, 25, 2):
    total = 0
    for _ in range(trials):
        mnh = MinHashAlgorithm(k)
        s1 = mnh.execute(A)
        s2 = mnh.execute(B)
        total += compare(s1, s2)
    estimated = total / trials
    print(f'k = {k}, Jaccard = {J_true:.2f}, MinHash оценка = {estimated:.2f}')
    results.append({'k': k, 'J_abs_dif': abs(J_true-estimated)*100})

df = pd.DataFrame(results)

plt.plot(df['k'], df['J_abs_dif'])
plt.xlabel('k')
plt.ylabel('Абсолютная разница (%)')
plt.title('Зависимость разницы между J и estimated от k')
plt.grid(True)
plt.savefig('../Images/MinHashAbsDiffBetwJAndEstimated.png')
plt.show()
