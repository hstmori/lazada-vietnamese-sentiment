import unittest

from lazada_sentiment import build_sentiment_pipeline


class ModelingTests(unittest.TestCase):
    def test_pipeline_can_fit_a_small_dataset(self):
        model = build_sentiment_pipeline("tfidf", random_state=42)
        comments = [
            "sản phẩm đẹp",
            "giao hàng nhanh",
            "sản phẩm rất tệ",
            "giao hàng quá chậm",
        ]
        labels = ["POS", "POS", "NEG", "NEG"]

        model.fit(comments, labels)

        self.assertLessEqual(set(model.predict(comments)), {"POS", "NEG"})

    def test_pipeline_rejects_unknown_vectorizer(self):
        with self.assertRaisesRegex(ValueError, "vectorizer"):
            build_sentiment_pipeline("unknown")


if __name__ == "__main__":
    unittest.main()

