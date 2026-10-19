import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from summarizer import aggregate, filter_devices, main


class TestSummarizer(unittest.TestCase):
    def test_aggregate_and_filter(self):
        rows = [
            {"device_id": "A", "status": "ERROR", "temperature": 70.0},
            {"device_id": "A", "status": "ACTIVE", "temperature": 80.0},
            {"device_id": "B", "status": "ACTIVE", "temperature": 95.0},
        ]
        summary = aggregate(rows)
        self.assertEqual(summary[0], {"device_id": "A", "total_records": 2, "avg_temperature": 75.0, "error_count": 1})
        self.assertEqual([d["device_id"] for d in filter_devices(summary)], ["A"])

    def test_missing_file_returns_error_code(self):
        self.assertEqual(main(["does_not_exist.csv"]), 1)


if __name__ == "__main__":
    unittest.main()
