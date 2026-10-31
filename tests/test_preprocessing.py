from pathlib import Path
import unittest

from lazada_sentiment import TextProcessor


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = PROJECT_ROOT / "resources" / "nlp"


class PreprocessingTests(unittest.TestCase):
    def test_resources_are_loaded(self):
        processor = TextProcessor(RESOURCE_DIR)
        summary = processor.resource_summary()

        self.assertTrue(all(count > 0 for count in summary.values()))

    def test_transform_is_deterministic_and_normalizes_teencode(self):
        processor = TextProcessor(RESOURCE_DIR)
        comment = "Ko đáng tiền, giao hàng chậm 😡"

        first = processor.transform(comment)
        second = processor.transform(comment)

        self.assertTrue(first)
        self.assertEqual(first, second)
        self.assertNotIn("ko", first.split())


if __name__ == "__main__":
    unittest.main()

