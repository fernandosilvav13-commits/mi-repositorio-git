"""
LayoutNormalizer — normalizes whitespace, inserts section markers, standardizes bullets.

Pure string manipulation with no external dependencies. Implements D-08 (whitespace
collapse + section markers) and D-09 (bullet normalization).
"""

import re

from app.schemas.preprocessing import SectionBoundary


class LayoutNormalizer:
    """Normalizes whitespace, adds section boundary markers, and standardizes bullet points.

    Implements D-08: collapse inline whitespace within paragraphs, preserve paragraph
    breaks, add section boundary markers.
    Implements D-09: standardize bullet points to consistent format.
    """

    # Detects paragraph boundaries (2+ newlines with optional whitespace between)
    PARAGRAPH_BREAK = re.compile(r"\n\s*\n")

    # Matches non-newline whitespace (spaces, tabs) within lines
    INLINE_WHITESPACE = re.compile(r"[^\S\n]+")

    # Bullet patterns - anchored to line start per Pitfall 4 safeguard
    BULLET_PATTERNS: list[re.Pattern] = [
        # Common bullet characters: • ● ▪ ➢ ➤ - – — *
        re.compile(r"^[\s]*[•●▪➢➤\-–—\*]\s+", re.MULTILINE),
        # Numbered list items: 1. 2) 3. etc.
        re.compile(r"^[\s]*\d+[.)]\s+", re.MULTILINE),
    ]

    # Standard bullet prefix per D-09
    STANDARD_BULLET = "* "

    def normalize(self, text: str, sections: dict[str, SectionBoundary]) -> str:
        """Apply layout normalization: collapse inline whitespace, normalize bullets, insert section markers.

        IMPORTANT: The sections dict contains BOUNDARIES RELATIVE TO THE ORIGINAL TEXT
        (before noise removal). After noise filter removes lines, these boundaries
        are offset. This function assumes sections have already been adjusted to
        match the cleaned text (adjustment happens in PreprocessingPipeline, Plan 03).

        Args:
            text: Text AFTER noise filter has removed noisy lines.
            sections: Section boundaries ADJUSTED to cleaned text line numbering.

        Returns:
            Normalized text with whitespace collapsed, bullets standardized,
            and section markers inserted.
        """
        # Handle empty/None text gracefully
        if text is None or text == "":
            return ""

        # Step 1: Collapse inline whitespace within paragraphs, preserve paragraph breaks
        text = self._normalize_whitespace(text)

        # Handle case where whitespace-only text becomes empty after normalization
        if not text:
            return ""

        # Step 2: Normalize bullet points to standard format
        text = self._normalize_bullets(text)

        # Step 3: Insert section boundary markers (if sections provided)
        if sections:
            text = self._insert_section_markers(text, sections)

        return text

    def _normalize_whitespace(self, text: str) -> str:
        """Collapse inline whitespace while preserving paragraph breaks.

        - Split by paragraph breaks (double newlines)
        - For each paragraph, collapse inline whitespace to single space and strip
        - Rejoin with double newlines

        Args:
            text: Original text to normalize.

        Returns:
            Text with inline whitespace collapsed but paragraph breaks preserved.
        """
        # Split by paragraph boundaries
        paragraphs = self.PARAGRAPH_BREAK.split(text)

        # Normalize each paragraph: collapse inline whitespace, strip edges
        normalized_paragraphs = []
        for p in paragraphs:
            # Collapse multiple spaces/tabs within line to single space
            collapsed = self.INLINE_WHITESPACE.sub(" ", p)
            # Strip leading/trailing whitespace from paragraph
            stripped = collapsed.strip()
            if stripped:  # Only add non-empty paragraphs
                normalized_paragraphs.append(stripped)

        # Rejoin with double newlines to preserve paragraph breaks
        return "\n\n".join(normalized_paragraphs)

    def _normalize_bullets(self, text: str) -> str:
        """Standardize various bullet formats to "* " per D-09.

        Applies regex patterns sequentially. The patterns are anchored to line
        start (^) with re.MULTILINE flag, so dashes in the middle of lines
        (like "proven - management") are not matched (Pitfall 4 safeguard).

        Args:
            text: Text with potentially varied bullet formats.

        Returns:
            Text with all bullets standardized to "* ".
        """
        for pattern in self.BULLET_PATTERNS:
            text = pattern.sub(self.STANDARD_BULLET, text)
        return text

    def _insert_section_markers(self, text: str, sections: dict[str, SectionBoundary]) -> str:
        """Insert section boundary markers at correct positions.

        Inserts markers from BOTTOM TO TOP (sorted by start_line descending) to
        preserve line numbering for subsequent insertions (anti-pattern avoidance).

        Section names come from the LLM detection response dynamically — no
        hardcoded section names (anti-pattern avoidance).

        Args:
            text: Normalized text to insert markers into.
            sections: Dict of section names to SectionBoundary with start_line/end_line.

        Returns:
            Text with "== SectionName ==" markers inserted at section start positions.
        """
        lines = text.splitlines()

        # Sort sections by start_line DESCENDING (bottom-to-top insertion)
        # This preserves line indices for subsequent insertions
        sorted_sections = sorted(
            sections.items(),
            key=lambda item: item[1].start_line,
            reverse=True,
        )

        for section_name, boundary in sorted_sections:
            # Only insert if start_line is within valid range
            if 0 <= boundary.start_line < len(lines):
                marker = f"== {section_name} =="
                lines.insert(boundary.start_line, marker)

        return "\n".join(lines)
