"""Utilities for reading and normalizing text files."""

import re
from pathlib import Path


class TextReader:
    """Reads a plain text file and normalizes its content.

    Normalization rules:
    - convert text to lowercase
    - keep only alphanumeric characters and spaces
    - replace punctuation with spaces
    - collapse repeated whitespace
    """

    def read_and_normalize(self, file_path: str) -> str:
        """Read text from a file and return normalized content.

        Args:
            file_path: Path to the input text file.

        Returns:
            Normalized string content.

        Raises:
            FileNotFoundError: If the file path does not exist.
        """

        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        text = path.read_text(encoding="utf-8")
        return self.normalize_text(text)

    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize raw text according to the assignment rules."""

        lowered = text.lower()
        cleaned = re.sub(r"[^a-z0-9\s]", " ", lowered)
        normalized = re.sub(r"\s+", " ", cleaned).strip()
        return normalized
