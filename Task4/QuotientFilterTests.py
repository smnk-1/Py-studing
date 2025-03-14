import unittest
from QuotientFilter import QuotientFilter


class TestQuotientFilter(unittest.TestCase):
    def setUp(self):
        self.qf = QuotientFilter(size=16, remainder_bits=4, seed=42)

    def test_hash_function(self):
        q, r = self.qf._hash('apple')
        self.assertTrue(0 <= q < self.qf.size)
        self.assertTrue(0 <= r < (2 ** self.qf.remainder_bits))

    def test_insert_and_lookup(self):
        elements = ['apple', 'banana', 'cherry', 'grape', 'mango']
        for el in elements:
            self.qf.insert(el)
        for el in elements:
            self.assertTrue(self.qf.check(el))

    def test_internal_bits_for_canonical_insertion(self):
        self.qf = QuotientFilter(size=8, remainder_bits=3, seed=1)
        self.qf.insert('test_canonical')
        q, r = self.qf._hash('test_canonical')
        self.assertTrue(self.qf.occupied[q])
        self.assertFalse(self.qf.shift[q])
        self.assertFalse(self.qf.continuation[q])


if __name__ == '__main__':
    unittest.main()
