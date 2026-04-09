"""Word tokenization and frequency analysis utilities."""

from collections import Counter
from typing import Dict, List, Set, Tuple


class WordCounter:
    """Tokenizes normalized text and computes word statistics."""

    DEFAULT_STOP_WORDS: Set[str] = {
        "the",
        "and",
        "is",
        "at",
        "which",
        "on",
        "a",
        "an",
        "as",
        "are",
        "was",
        "were",
        "been",
        "be",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "for",
        "from",
        "that",
        "this",
        "with",
        "into",
        "their",
        "they",
        "them",
        "but",
        "not",
        "you",
        "your",
    }

    def __init__(self, stop_words: Set[str] | None = None) -> None:
        """Initialize the counter with a stop-word set."""

        self.stop_words = stop_words if stop_words is not None else self.DEFAULT_STOP_WORDS
        self.word_frequencies: Counter[str] = Counter()
        self.filtered_words: List[str] = []

    def tokenize(self, normalized_text: str) -> List[str]:
        """Split normalized text into filtered tokens.

        Filtering rules:
        - ignore empty tokens
        - ignore words shorter than 3 characters
        - ignore stop words
        """

        tokens = normalized_text.split()
        filtered = [
            token for token in tokens if len(token) >= 3 and token not in self.stop_words
        ]
        return filtered

    def count_words(self, normalized_text: str) -> Dict[str, int]:
        """Count word frequencies from normalized text.

        Returns:
            A standard dictionary sorted by internal Counter insertion order.
        """

        self.filtered_words = self.tokenize(normalized_text)
        self.word_frequencies = Counter(self.filtered_words)
        return dict(self.word_frequencies)

    def get_top_n_words(self, n: int) -> List[Tuple[str, int]]:
        """Return the top N words sorted by frequency descending.

        Ties are resolved alphabetically for deterministic output.
        """

        if n < 0:
            raise ValueError("n must be non-negative.")

        ranked_words = sorted(
            self.word_frequencies.items(),
            key=lambda item: (-item[1], item[0]),
        )
        return ranked_words[:n]

    def get_words_starting_with(self, prefix: str) -> List[str]:
        """Return counted words that begin with a prefix, sorted alphabetically."""

        lowered_prefix = prefix.lower()
        matching_words = [word for word in self.word_frequencies if word.startswith(lowered_prefix)]
        return sorted(matching_words)

    def get_total_word_count(self) -> int:
        """Return total count of filtered words."""

        return len(self.filtered_words)

    def get_unique_word_count(self) -> int:
        """Return count of unique filtered words."""

        return len(self.word_frequencies)

    def get_average_word_length(self) -> float:
        """Return average length of filtered words.

        Returns 0.0 if there are no filtered words.
        """

        if not self.filtered_words:
            return 0.0

        total_characters = sum(len(word) for word in self.filtered_words)
        return total_characters / len(self.filtered_words)

    def get_longest_word(self) -> str:
        """Return the longest filtered word.

        If multiple words have the same length, the alphabetically first word
        is returned to keep output deterministic.
        """

        if not self.word_frequencies:
            return ""

        return sorted(self.word_frequencies.keys(), key=lambda word: (-len(word), word))[0]

    def get_most_frequent_word(self) -> str:
        """Return the most frequent filtered word.

        If multiple words tie, the alphabetically first word is returned.
        """

        if not self.word_frequencies:
            return ""

        return sorted(self.word_frequencies.items(), key=lambda item: (-item[1], item[0]))[0][0]
