"""Demo script for the text analyzer.

Run with:
    python -m src.text_analyzer.demo
"""

from pathlib import Path

from .statistics_report import StatisticsReport
from .text_reader import TextReader
from .word_counter import WordCounter


def main() -> None:
    """Read a sample file, analyze it, print results, and export a report."""

    project_root = Path(__file__).resolve().parents[2]
    sample_file = project_root / "sample_text.txt"
    output_file = project_root / "text_analysis_report.txt"

    reader = TextReader()
    normalized_text = reader.read_and_normalize(str(sample_file))

    counter = WordCounter()
    counter.count_words(normalized_text)

    report = StatisticsReport(counter)

    print(report.build_report(top_n=10))
    print()
    print("Words starting with 'data':")
    print(counter.get_words_starting_with("data"))

    report.export_report(str(output_file), top_n=10)
    print()
    print(f"Report exported to: {output_file}")


if __name__ == "__main__":
    main()
