"""Formatted reporting for word frequency statistics."""

from pathlib import Path

from .word_counter import WordCounter


class StatisticsReport:
    """Generates a formatted report from a populated WordCounter."""

    def __init__(self, word_counter: WordCounter) -> None:
        """Store a word counter instance for report generation."""

        self.word_counter = word_counter

    def build_report(self, top_n: int = 10) -> str:
        """Build a formatted multi-line text report."""

        total_word_count = self.word_counter.get_total_word_count()
        unique_word_count = self.word_counter.get_unique_word_count()
        average_word_length = self.word_counter.get_average_word_length()
        longest_word = self.word_counter.get_longest_word()
        most_frequent_word = self.word_counter.get_most_frequent_word()
        top_words = self.word_counter.get_top_n_words(top_n)

        lines = [
            "TEXT ANALYSIS REPORT",
            "=" * 40,
            f"Total word count   : {total_word_count}",
            f"Unique word count  : {unique_word_count}",
            f"Average word length: {average_word_length:.2f}",
            f"Longest word       : {longest_word}",
            f"Most frequent word : {most_frequent_word}",
            "",
            f"Top {top_n} words:",
        ]

        if top_words:
            for word, count in top_words:
                lines.append(f"- {word}: {count}")
        else:
            lines.append("- No words available")

        return "\n".join(lines)

    def export_report(self, output_file_path: str, top_n: int = 10) -> None:
        """Write the formatted report to a text file."""

        path = Path(output_file_path)
        report_content = self.build_report(top_n=top_n)
        path.write_text(report_content, encoding="utf-8")
