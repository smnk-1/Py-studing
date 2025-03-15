import unittest
from CountMinSketch import CountMinSketch


class TestCountMinSketch(unittest.TestCase):
    def setUp(self):
        self.cms = CountMinSketch(width=100, depth=5)

    def test_no_item(self):
        self.assertEqual(self.cms.frequency('nonexistent'), 0)

    def test_overestimation_due_to_collision(self):
        self.cms.add('apple', count=10)
        self.cms.add('apple', count=5)
        estimated_freq = self.cms.frequency('apple')
        self.assertGreaterEqual(estimated_freq, 15)


if __name__ == '__main__':
    unittest.main()
