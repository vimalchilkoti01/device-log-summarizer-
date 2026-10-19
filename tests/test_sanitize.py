import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sanitize import clean_readings


class TestCleanReadings(unittest.TestCase):
    def test_mixed_inputs(self):
        data = ["12.5", None, -3, "abc", 600, 42, "499.9", "-0.1"]
        self.assertEqual(clean_readings(data), [12.5, 500.0, 42.0, 499.9])

    def test_empty_list(self):
        self.assertEqual(clean_readings([]), [])
        self.assertEqual(clean_readings(None), [])

    def test_all_invalid(self):
        self.assertEqual(clean_readings([None, "x", -1, {}, "nan"]), [])


if __name__ == "__main__":
    unittest.main()
