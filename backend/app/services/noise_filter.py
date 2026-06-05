"""
NoiseFilter — removes noisy lines from document text by index.

Pure string manipulation with no external dependencies. Removes page headers,
page numbers, footers, and metadata artifacts as identified by the LLM in
SectionDetector (D-07 noise types).
"""


class NoiseFilter:
    """Removes noisy lines (page headers, page numbers, footers, document metadata) from document text per D-07.

    Operates on 0-indexed line numbers. Pure string manipulation with no I/O
    or external dependencies.
    """

    def filter(self, text: str, noisy_lines: set[int]) -> str:
        """Remove lines at given 0-indexed indices. Returns cleaned text with remaining lines joined by newline.

        Args:
            text: Original document text (split by newline).
            noisy_lines: Set of 0-indexed line numbers to remove.

        Returns:
            Cleaned text with noisy lines removed, structure preserved.
        """
        # Handle empty/None input gracefully
        if text is None or text == "":
            return ""

        # Optimization: if no noisy lines, return text as-is to avoid split/join overhead
        if not noisy_lines:
            return text

        lines = text.splitlines(keepends=False)

        # Keep lines whose index is NOT in noisy_lines
        cleaned = [
            line for idx, line in enumerate(lines)
            if idx not in noisy_lines
        ]

        return "\n".join(cleaned)
