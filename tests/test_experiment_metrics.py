"""Tests for lightweight experiment metrics."""

import unittest

from tools.experiment_metrics import compute_response_metrics


class ExperimentMetricsTests(unittest.TestCase):
    def test_compute_response_metrics_with_url(self) -> None:
        metrics = compute_response_metrics("Useful output with source https://example.com")
        self.assertEqual(metrics["non_empty_response"], 1)
        self.assertEqual(metrics["contains_url"], 1)
        self.assertEqual(metrics["url_count"], 1)

    def test_compute_response_metrics_empty(self) -> None:
        metrics = compute_response_metrics("   ")
        self.assertEqual(metrics["non_empty_response"], 0)
        self.assertEqual(metrics["contains_url"], 0)
        self.assertEqual(metrics["response_length_chars"], 0)


if __name__ == "__main__":
    unittest.main()
