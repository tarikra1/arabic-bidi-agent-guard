# arabic-bidi-agent-guard

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-3776AB.svg)](pyproject.toml)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-success.svg)](pyproject.toml)

**Prevent Arabic RTL / English LTR text scrambling in AI coding agents and Markdown interfaces—without injecting invisible Unicode watermarks.**

Most developer chat interfaces, IDE panels, and Markdown renderers (**Claude Code**, **Cursor**, **GitHub**, **VS Code**, **Antigravity**) render paragraph containers left-to-right (`LTR`) without automatic per-span `<bdi>` isolation. When an LLM mixes Arabic prose with inline English identifiers, CLI flags, backtick spans, or parentheses on the same line, the Unicode Bidirectional Algorithm scrambles word order, flips parentheses, and jumps trailing punctuation across the line.

`arabic-bidi-agent-guard` solves this at both layers:
1. **Preventive Agent Rule (`rules/AGENTS.md`):** Drop-in instruction file for `CLAUDE.md`, `AGENTS.md`, or `.cursorrules` that trains LLMs to keep Arabic sentences purely Arabic while isolating English identifiers into standalone bullets, code blocks, or dedicated Markdown table columns.
2. **Deterministic CLI Linter & Sanitizer (`bidi-guard`):** Zero-dependency Python CLI and library for CI pipelines and post-generation agent hooks that catches BiDi collisions and strips hidden directional control characters (`U+200E`–`U+2069`).

---

## Why Not Just Inject Unicode `RLM` / `LRI` Characters?

LLMs that try to "fix" Arabic alignment by emitting hidden characters (`U+200F`, `U+202B`, `U+2067`) silently break code copy-pasting, corrupt JSON/YAML parsers, trigger GitHub "hidden bidirectional Unicode" security warnings, and leave invisible watermarks in social copy and documentation. **Structural separation** produces clean UTF-8 Markdown that renders identically everywhere.

---

## Quickstart

### 1. Install the CLI & Library

```bash
git clone https://github.com/tarikra1/arabic-bidi-agent-guard.git
cd arabic-bidi-agent-guard
pip install -e .
```

### 2. Lint Markdown Outputs

```bash
# Human-readable report
bidi-guard check docs/ README.md

# Machine-readable JSON for CI or AI agent self-correction loops
bidi-guard check draft.md --json

# Strip invisible Unicode BiDi control characters in-place
bidi-guard strip-controls draft.md
```

### 3. Add to Claude Code / Cursor / Antigravity

Append [`rules/AGENTS.md`](rules/AGENTS.md) to your project or global agent instructions:

```bash
cat rules/AGENTS.md >> CLAUDE.md
# or for Antigravity / Codex:
cat rules/AGENTS.md >> AGENTS.md
```

---

## Rules Enforced by `bidi-guard`

| Rule ID | What It Catches | Structural Fix |
| :--- | :--- | :--- |
| `INLINE_CODE_IN_ARABIC` | Inline `` `code` `` embedded mid-sentence in Arabic | Move commands/identifiers to fenced code blocks, sub-bullets, or a dedicated table column |
| `MIXED_PARENTHESES` | Mixed `(English)` parentheses inside Arabic prose | Express naturally in Arabic or split into structured bullets |
| `TRAILING_LTR_PERIOD` | Arabic line ending with `LatinWord.` | Transliterate common tech terms into Arabic script or move to a bullet |
| `MIXED_RTL_LTR_PROSE` | Raw Latin tokens mixed inside an Arabic sentence | Separate RTL prose and LTR identifiers onto distinct lines or table cells |
| `HIDDEN_BIDI_CONTROLS` | Hidden `U+200E`..`U+2069` directional characters | Run `bidi-guard strip-controls <file>` |

---

## نظرة عامة بالعربية

توفّر هذه الحزمة حلاً جذرياً لمشكلة تداخل وبعثرة النصوص العربية مع المصطلحات البرمجية في واجهات الذكاء الاصطناعي وملفات ماركداون:

- فصل الجمل العربية الصافية عن الأكواد والمسارات والروابط عبر قوائم نقطية وجداول منظمة.
- أداة فحص سريعة بدون أي مكتبات خارجية لاكتشاف الأسطر المختلطة تلقائياً قبل النشر.
- تنظيف الملفات من محارف الاتجاه الخفية التي تفسد النسخ واللصق وتُظهر تحذيرات أمنية في مستودعات الكود.

---

## Running Tests

```bash
python -m unittest discover -s tests -v
```

## License

Released under the [MIT License](LICENSE).
