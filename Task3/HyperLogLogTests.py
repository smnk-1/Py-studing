from HyperLogLog import HyperLogLog, count_leading_zeros
import unittest
import mmh3

class TestHyperLogLog(unittest.TestCase):

    def test_count_leading_zeros(self):
        self.assertEqual(count_leading_zeros("000100"), 3)
        self.assertEqual(count_leading_zeros("100000"), 0)
        self.assertEqual(count_leading_zeros("000000"), 6)

    def test_proceed_element(self):
        hll = HyperLogLog(4)  # 16 корзин
        hll.proceed_element("test_string")

        self.assertTrue(any(bucket > 0 for bucket in hll.buckets)) # хотя бы в одной корзине значение изменилось

    def test_bucket_indexing(self):
        hll = HyperLogLog(4)  # 16 корзин
        hash_value = format(mmh3.hash("test", signed=False), '032b')
        bucket_index = int(hash_value[:4], 2)

        hll.proceed_element("test")
        self.assertGreater(hll.buckets[bucket_index], 0)  # в необходимой корзине увеличилось значение

if __name__ == "__main__":
    unittest.main()
