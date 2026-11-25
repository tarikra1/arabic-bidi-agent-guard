"""Arabic BiDi Agent Guard — Structural RTL/LTR Markdown linter and sanitizer."""

from .linter import Violation, lint_markdown, strip_hidden_bidi_controls

__all__ = ["Violation", "lint_markdown", "strip_hidden_bidi_controls"]
__version__ = "1.1.0"
