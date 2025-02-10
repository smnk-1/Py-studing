from random import randint

def mod(number, module):
    return number % module


class HashFunction:
    def __init__(self):
        self.r = randint(1, 100)

    def execute(self, s):
        value = 0
        for i, char in enumerate(s):
            value += (ord(char)*(i+1))*self.r
        return value


class BloomFilter: #если элемент был добавлен, он должен определяться как присутствующий
    def __init__(self, m, k):
        self.m = m
        self.k = k
        self.hash_functions = [HashFunction() for _ in range(0, self.k)]
        self.filer_array = []

    def get_hash(self, string):
        hash_res = [f.execute(string) for f in self.hash_functions]
        mod_res = [mod(x, self.m) for x in hash_res]
        return mod_res

    def get_bit_array(self, hashes):
        bit_array = [0]*self.m
        for bit in hashes:
            bit_array[bit]=1
        return bit_array

    def add(self, string):
        hashes = self.get_hash(string)
        bit_array = self.get_bit_array(hashes)
        self.filer_array.append(bit_array)

    def check(self, string):
        checking_hash = self.get_hash(string)
        checking_bit_array = self.get_bit_array(checking_hash)

        for bit_array in self.filer_array:
            for i in range(0, self.m):
                check = True
                if bit_array[i] == checking_bit_array[i]:
                    check = False
                if check: return False
        return True


def test(items_to_add, items_to_check, bloom_filter):
    for item in items_to_add:
        bloom_filter.add(item)
    for item in items_to_check:
        bloom_filter.check(item)
        print(f'Is item <{item}> in {items_to_add}: {bloom_filter.check(item)}')


test(['apple'], ['apple', 'orange', 'banana'], BloomFilter(7, 4))
print('---')
test(['banana'], ['apple', 'orange', 'banana'], BloomFilter(7, 4))
