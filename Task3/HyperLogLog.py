import mmh3

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
        leading_zeros = count_leading_zeros(remaining) + 1
        self.buckets[bucket_index] = max(self.buckets[bucket_index], leading_zeros)
