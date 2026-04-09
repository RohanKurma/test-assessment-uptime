"""Unit tests for text analyzer logic."""

from pathlib import Path

import pytest

from src.text_analyzer.statistics_report import StatisticsReport
from src.text_analyzer.text_reader import TextReader
from src.text_analyzer.word_counter import WordCounter


@pytest.fixture
def sample_normalized_text() -> str:
    """Return a small normalized text sample for repeated tests."""

    return "data science data analysis machine learning data model learning"


def test_normalize_text_removes_punctuation_and_lowercases() -> None:
    """Normalization should lowercase text and remove punctuation."""

    raw_text = "Hello, World! Data-Science is GREAT."
    normalized = TextReader.normalize_text(raw_text)
    assert normalized == "hello world data science is great"


def test_read_and_normalize_raises_for_missing_file() -> None:
    """Missing files should raise FileNotFoundError."""

    reader = TextReader()

    with pytest.raises(FileNotFoundError):
        reader.read_and_normalize("missing_file.txt")


def test_tokenize_filters_short_words_and_stop_words() -> None:
    """Tokens shorter than 3 chars and stop words should be removed."""

    counter = WordCounter(stop_words={"the", "and", "data"})
    tokens = counter.tokenize("the data map ai science and code")
    assert tokens == ["map", "science", "code"]


def test_count_words_returns_expected_frequencies(sample_normalized_text: str) -> None:
    """Word frequencies should match occurrences in the input text."""

    counter = WordCounter(stop_words=set())
    frequencies = counter.count_words(sample_normalized_text)
    assert frequencies["data"] == 3
    assert frequencies["learning"] == 2
    assert frequencies["science"] == 1


def test_get_top_n_words_orders_by_count_then_alphabetically(sample_normalized_text: str) -> None:
    """Top N results should be deterministic for ties."""

    counter = WordCounter(stop_words=set())
    counter.count_words(sample_normalized_text)
    assert counter.get_top_n_words(3) == [("data", 3), ("learning", 2), ("analysis", 1)]


def test_get_words_starting_with_returns_sorted_matches(sample_normalized_text: str) -> None:
    """Prefix-based word search should return alphabetical results."""

    counter = WordCounter(stop_words=set())
    counter.count_words(sample_normalized_text)
    assert counter.get_words_starting_with("da") == ["data"]


def test_summary_statistics(sample_normalized_text: str) -> None:
    """Total count, unique count, longest, and most frequent words should be correct."""

    counter = WordCounter(stop_words=set())
    counter.count_words(sample_normalized_text)

    assert counter.get_total_word_count() == 9
    assert counter.get_unique_word_count() == 6
    assert counter.get_longest_word() == "analysis"
    assert counter.get_most_frequent_word() == "data"
    assert round(counter.get_average_word_length(), 2) == 6.11


def test_empty_content_statistics() -> None:
    """Empty filtered content should produce safe default statistics."""

    counter = WordCounter(stop_words=set())
    counter.count_words("")

    assert counter.get_total_word_count() == 0
    assert counter.get_unique_word_count() == 0
    assert counter.get_average_word_length() == 0.0
    assert counter.get_longest_word() == ""
    assert counter.get_most_frequent_word() == ""


def test_export_report_writes_output_file(tmp_path: Path, sample_normalized_text: str) -> None:
    """Report export should write a formatted report file."""

    counter = WordCounter(stop_words=set())
    counter.count_words(sample_normalized_text)
    report = StatisticsReport(counter)

    output_file = tmp_path / "report.txt"
    report.export_report(str(output_file), top_n=3)

    content = output_file.read_text(encoding="utf-8")
    assert "TEXT ANALYSIS REPORT" in content
    assert "Total word count" in content
    assert "Top 3 words" in content
