import mmh3
from matplotlib.pyplot import close

def count_leading_zeros(string):
    count = 0
    for i in range(0, len(string)):
        if string[i] == '1':
            break
        else:
            count += 1
    return count

class HyperLogLog:
    def __init__(self, b):
        self.b = b
        self.buckets = [0]*2**b
        print(len(self.buckets))


    def proceed_element(self, string):
        hash_value = bin(mmh3.hash(string, signed=False))
        bucket_index = int(hash_value[2:self.b+2:], 2)
        leading_zeros = count_leading_zeros(hash_value[self.b+2::])
        self.buckets[bucket_index] = max(self.buckets[bucket_index], leading_zeros)
