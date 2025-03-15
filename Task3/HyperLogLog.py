import mmh3
import math

def count_leading_zeros(bits):
    count = 0
    for bit in bits:
        if bit == '1':
            break
        count += 1
    return count

class HyperLogLog:
    def __init__(self, b):
        self.b = b
        self.m = 2 ** b
        self.buckets = [0] * self.m

    def proceed_element(self, element):
        hash_value = format(mmh3.hash(element, signed=False), '032b')
        bucket_index = int(hash_value[:self.b], 2)
        remaining = hash_value[self.b:]
        leading_zeros = count_leading_zeros(remaining)
        self.buckets[bucket_index] = max(self.buckets[bucket_index], leading_zeros)

    def estimate_cardinality(self):
        """
        Оценка кардинальности (кол-ва уникальных элементов) по списку buckets.

        """

        # 1. Вычисляем константу alpha_m
        alpha_m = 0.7213 / (1 + 1.079 / self.m)

        # 2. Считаем сумму Z = sum(2^(-M[i]))
        Z = sum(2 ** (-r) for r in self.buckets)

        # 3. Вычисляем "сырую" оценку по формуле HyperLogLog:
        #    E = alpha_m * m^2 / Z
        E = alpha_m * self.m**2 / Z

        # 4. Коррекция для маленьких оценок (линейное исправление)
        if E <= 2.5 * self.m:
            # V = количество пустых корзин
            V = self.buckets.count(0)
            if V != 0:
                E = self.m * math.log(self.m / V)

        # 5. Коррекция для очень больших оценок (ограничение 32-битного пространства)
        elif E > (1 / 30) * (2 ** 32):
            E = -(2 ** 32) * math.log(1 - E / (2 ** 32))

        # 7. Округляем результат и возвращаем
        return round(E)
