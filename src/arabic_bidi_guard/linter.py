"""Core structural BiDi linter for Markdown documents and LLM agent outputs."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Iterable

ARABIC_RE = re.compile(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]")
LATIN_WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_./:-]*")
INLINE_CODE_RE = re.compile(r"`[^`]+`")
HIDDEN_BIDI_RE = re.compile(r"[\u200E\u200F\u202A-\u202E\u2066-\u2069]")
MIXED_PAREN_RE = re.compile(r"\([^)]*[A-Za-z][^)]*\)")
TRAILING_LTR_DOT_RE = re.compile(r"[A-Za-z0-9_`]+\.[\s]*$")


@dataclass(frozen=True)
class Violation:
    line: int
    rule: str
    message: str
    snippet: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def strip_hidden_bidi_controls(text: str) -> tuple[str, int]:
    """Remove invisible Unicode directional control characters and return (clean_text, count_removed)."""
    matches = HIDDEN_BIDI_RE.findall(text)
    if not matches:
        return text, 0
    return HIDDEN_BIDI_RE.sub("", text), len(matches)


def _is_table_row(stripped: str) -> bool:
    return stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") >= 2


def lint_markdown(text: str) -> list[Violation]:
    """
    Analyze Markdown text for RTL/LTR BiDi collisions that scramble rendering in LTR chat UIs.
    Skips fenced code blocks and evaluates Markdown table cells independently.
    """
    violations: list[Violation] = []
    in_fence = False
    fence_marker = ""

    for idx, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()

        # Check for invisible BiDi control characters anywhere (even in code!)
        if HIDDEN_BIDI_RE.search(raw_line):
            violations.append(
                Violation(
                    line=idx,
                    rule="HIDDEN_BIDI_CONTROLS",
                    message="Contains invisible Unicode BiDi control characters (U+200E..U+2069) that break linters and copy-paste.",
                    snippet=stripped[:100],
                )
            )

        # Track fenced code blocks (``` or ~~~)
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif stripped.startswith(fence_marker):
                in_fence = False
                fence_marker = ""
            continue

        if in_fence or not stripped:
            continue

        # Evaluate table cells independently so dedicated English + Arabic columns pass cleanly
        segments: Iterable[str]
        if _is_table_row(stripped):
            segments = [cell.strip() for cell in stripped.strip("|").split("|")]
        else:
            segments = [stripped]

        for seg in segments:
            if not ARABIC_RE.search(seg):
                continue

            # Rule 1: Inline backtick code inside an Arabic sentence
            if INLINE_CODE_RE.search(seg):
                violations.append(
                    Violation(
                        line=idx,
                        rule="INLINE_CODE_IN_ARABIC",
                        message="Inline code span (`...`) embedded inside an Arabic run; isolate code on its own bullet, code block, or table column.",
                        snippet=seg[:100],
                    )
                )
                continue

            # Rule 2: Mixed parentheses containing Latin characters inside an Arabic line
            if MIXED_PAREN_RE.search(seg):
                violations.append(
                    Violation(
                        line=idx,
                        rule="MIXED_PARENTHESES",
                        message="Latin text inside parentheses within an Arabic sentence mirrors awkwardly in LTR containers.",
                        snippet=seg[:100],
                    )
                )
                continue

            # Rule 3: Trailing Latin word followed by a period at the end of an Arabic sentence
            if TRAILING_LTR_DOT_RE.search(seg):
                violations.append(
                    Violation(
                        line=idx,
                        rule="TRAILING_LTR_PERIOD",
                        message="Arabic sentence ends with a Latin token and period, causing visual jump to the wrong margin.",
                        snippet=seg[:100],
                    )
                )
                continue

            # Rule 4: Inline Latin words mixed into an Arabic prose run
            if LATIN_WORD_RE.search(seg):
                violations.append(
                    Violation(
                        line=idx,
                        rule="MIXED_RTL_LTR_PROSE",
                        message="Mixed Arabic (RTL) and Latin (LTR) tokens on the same prose line; transliterate or move technical identifiers to standalone bullets/columns.",
                        snippet=seg[:100],
                    )
                )

    return violations
