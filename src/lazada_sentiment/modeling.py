from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def build_sentiment_pipeline(
    vectorizer: str = "tfidf",
    class_weight: str | None = None,
    random_state: int = 42,
) -> Pipeline:
    """Build the vectorizer + Logistic Regression baseline used in the notebook."""

    vectorizer_name = vectorizer.strip().lower()
    if vectorizer_name == "tfidf":
        text_features = TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95,
            sublinear_tf=True,
        )
    elif vectorizer_name == "count":
        text_features = CountVectorizer(
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95,
        )
    else:
        raise ValueError("vectorizer must be either 'tfidf' or 'count'.")

    classifier = LogisticRegression(
        max_iter=1_000,
        class_weight=class_weight,
        random_state=random_state,
    )
    return Pipeline([
        ("vectorizer", text_features),
        ("logreg", classifier),
    ])

