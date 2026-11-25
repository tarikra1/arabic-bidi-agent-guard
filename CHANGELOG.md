# Changelog

All notable changes to `arabic-bidi-agent-guard` are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-11-25

### Added
- Automated multi-version GitHub Actions CI matrix (`Python 3.10`, `3.11`, `3.12`) with self-linting verification across repository Markdown files.
- `SECURITY.md` documenting hidden bidirectional Unicode (`Trojan Source` / `CVE-2021-42574`) mitigation via `bidi-guard strip-controls`.
- `CHANGELOG.md` release history tracking.

## [1.0.0] - 2026-11-25

### Added
- Zero-dependency structural BiDi linter (`arabic_bidi_guard.linter`) detecting inline code collisions, mixed parentheses, trailing LTR punctuation, mixed RTL/LTR prose runs, and hidden directional control characters.
- `bidi-guard` CLI supporting `check` (human-readable + `--json`) and `strip-controls` in-place sanitization.
- Drop-in `rules/AGENTS.md` instruction file for `CLAUDE.md`, `AGENTS.md`, and `.cursorrules`.
