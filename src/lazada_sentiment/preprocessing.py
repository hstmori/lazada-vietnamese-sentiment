from __future__ import annotations

from pathlib import Path
import re
import unicodedata

from underthesea import pos_tag, sent_tokenize, word_tokenize


class TextProcessor:
    """Normalize Vietnamese review text with the dictionaries in ``resources/nlp``."""

    RESOURCE_FILES = {
        "emoji": "emojicon.txt",
        "teencode": "teencode.txt",
        "english": "english-vnmese.txt",
        "wrong": "wrong-word.txt",
        "stopwords": "vietnamese-stopwords.txt",
    }

    def __init__(self, resource_dir: str | Path):
        self.resource_dir = Path(resource_dir)
        missing = [
            filename
            for filename in self.RESOURCE_FILES.values()
            if not (self.resource_dir / filename).exists()
        ]
        if missing:
            raise FileNotFoundError(
                f"Missing NLP resources in {self.resource_dir}: {', '.join(missing)}"
            )

        self.emoji_dict = self._load_mapping(
            self.RESOURCE_FILES["emoji"], lowercase_key=False
        )
        self.teencode_dict = self._load_mapping(self.RESOURCE_FILES["teencode"])
        self.english_dict = self._load_mapping(self.RESOURCE_FILES["english"])
        self.wrong_words = self._load_word_set(self.RESOURCE_FILES["wrong"])

        raw_stopwords = self._load_word_set(self.RESOURCE_FILES["stopwords"])
        self.stopwords = raw_stopwords | {
            word.replace(" ", "_") for word in raw_stopwords
        }
        self.negators = {
            "không",
            "chẳng",
            "chả",
            "chưa",
            "đừng",
            "khỏi",
            "không_hề",
        }
        self.stopwords.difference_update(self.negators)

        # N/NP keeps the object being praised or criticized. M is retained because
        # the tagger occasionally assigns it to short adjectives in review text.
        self.keep_pos = {"A", "AB", "V", "VB", "VY", "R", "N", "NP", "M"}

    @staticmethod
    def _normalize(text: str) -> str:
        return unicodedata.normalize("NFC", text.strip())

    def _load_mapping(self, filename: str, lowercase_key: bool = True) -> dict[str, str]:
        mapping: dict[str, str] = {}
        path = self.resource_dir / filename
        for line_number, raw_line in enumerate(
            path.read_text(encoding="utf-8-sig").splitlines(), start=1
        ):
            if not raw_line.strip():
                continue
            if "\t" not in raw_line:
                raise ValueError(
                    f"Line {line_number} in {path} must use the key\\tvalue format."
                )
            key, value = raw_line.split("\t", 1)
            key = self._normalize(key)
            if lowercase_key:
                key = key.lower()
            mapping[key] = self._normalize(value).lower()
        return mapping

    def _load_word_set(self, filename: str) -> set[str]:
        path = self.resource_dir / filename
        return {
            self._normalize(line).lower()
            for line in path.read_text(encoding="utf-8-sig").splitlines()
            if line.strip()
        }

    def replace_emoji_to_text(self, sentence: str) -> str:
        # Long sequences go first so variation selectors are handled consistently.
        for icon, meaning in sorted(
            self.emoji_dict.items(), key=lambda item: -len(item[0])
        ):
            sentence = sentence.replace(icon, f" {meaning} ")
        return sentence

    @staticmethod
    def _replace_tokens(sentence: str, mapping: dict[str, str]) -> str:
        return " ".join(mapping.get(token, token) for token in sentence.split())

    def replace_teencode_to_text(self, sentence: str) -> str:
        return self._replace_tokens(sentence, self.teencode_dict)

    def translate_english_to_vietnam(
        self,
        sentence: str,
        extra_mapping: dict[str, str] | None = None,
    ) -> str:
        mapping = dict(self.english_dict)
        if extra_mapping:
            mapping.update(
                {str(key).lower(): str(value).lower() for key, value in extra_mapping.items()}
            )
        return self._replace_tokens(sentence, mapping)

    def remove_typo_tokens(self, sentence: str) -> str:
        return " ".join(
            token for token in sentence.split() if token not in self.wrong_words
        )

    def process_negation(self, text: str) -> str:
        tokens = text.split()
        result: list[str] = []
        index = 0
        while index < len(tokens):
            token = tokens[index]
            if token in self.negators and index + 1 < len(tokens):
                result.append(f"{token}_{tokens[index + 1]}")
                index += 2
            else:
                result.append(token)
                index += 1
        return " ".join(result)

    def _clean_sentence(self, sentence: str) -> str:
        sentence = re.sub(r"https?://\S+|www\.\S+|\S+@\S+", " ", sentence)
        sentence = re.sub(r"(.)\1{3,}", r"\1\1", sentence)
        sentence = re.sub(r"[^0-9A-Za-zÀ-ỹ_\s]", " ", sentence)
        sentence = re.sub(r"\d+", " ", sentence)
        sentence = re.sub(r"\s+", " ", sentence).strip()
        sentence = self.replace_teencode_to_text(sentence)
        sentence = self.translate_english_to_vietnam(sentence)
        sentence = self.process_negation(sentence)
        sentence = self.remove_typo_tokens(sentence)
        return re.sub(r"\s+", " ", sentence).strip()

    def basic_clean(self, sentence: object) -> str:
        text = unicodedata.normalize("NFC", str(sentence).lower().replace("’", "'"))
        text = re.sub(r"\.+", ".", text)
        text = self.replace_emoji_to_text(text)
        parts = sent_tokenize(text) or [text]
        cleaned = [self._clean_sentence(part) for part in parts]
        return ". ".join(part for part in cleaned if part)

    def apply_pos_filter(self, text: str) -> str:
        processed: list[str] = []
        for sentence in sent_tokenize(text):
            segmented = word_tokenize(sentence.replace(".", " "), format="text")
            protected = self.process_negation(segmented)
            kept: list[str] = []
            for token, tag in pos_tag(protected):
                is_negation = any(
                    token.startswith(f"{negator}_") for negator in self.negators
                )
                if tag.upper() in self.keep_pos or is_negation:
                    kept.append(token)
            if kept:
                processed.append(" ".join(kept))
        return " ".join(processed)

    def remove_stopwords(self, sentence: str) -> str:
        kept: list[str] = []
        for token in sentence.split():
            is_negation = any(
                token.startswith(f"{negator}_") for negator in self.negators
            )
            if token not in self.stopwords or is_negation:
                kept.append(token)
        return " ".join(kept)

    def transform(self, sentence: object) -> str:
        text = self.basic_clean(sentence)
        text = self.apply_pos_filter(text)
        text = self.remove_stopwords(text)
        return re.sub(r"\s+", " ", text).strip()

    def resource_summary(self) -> dict[str, int]:
        return {
            "emoji": len(self.emoji_dict),
            "teencode": len(self.teencode_dict),
            "english_vietnamese": len(self.english_dict),
            "wrong_words": len(self.wrong_words),
            "stopwords": len(self.stopwords),
        }

