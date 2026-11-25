"""CLI entrypoint for arabic-bidi-agent-guard (`bidi-guard`)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .linter import lint_markdown, strip_hidden_bidi_controls


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="bidi-guard",
        description="Lint and sanitize Markdown files for clean, scramble-free Arabic RTL/LTR formatting.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    check_p = sub.add_parser("check", help="Check Markdown files for RTL/LTR BiDi collisions.")
    check_p.add_argument("paths", nargs="+", help="Markdown file(s) or directories to lint.")
    check_p.add_argument("--json", action="store_true", help="Emit machine-readable JSON diagnostics.")

    strip_p = sub.add_parser("strip-controls", help="Remove invisible Unicode BiDi control characters in-place.")
    strip_p.add_argument("paths", nargs="+", help="Files to sanitize.")

    args = parser.parse_args(argv)

    if sys.stdout and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    targets: list[Path] = []
    for raw in args.paths:
        p = Path(raw)
        if p.is_dir():
            targets.extend(sorted(p.rglob("*.md")))
        elif p.is_file():
            targets.append(p)
        else:
            print(f"Error: path not found: {raw}", file=sys.stderr)
            return 2

    if args.command == "strip-controls":
        total_removed = 0
        for f in targets:
            content = f.read_text(encoding="utf-8")
            cleaned, count = strip_hidden_bidi_controls(content)
            if count > 0:
                f.write_text(cleaned, encoding="utf-8", newline="\n")
                total_removed += count
                print(f"{f}: stripped {count} hidden BiDi control character(s)")
        if total_removed == 0:
            print("No hidden BiDi control characters found.")
        return 0

    all_findings: dict[str, list[dict[str, object]]] = {}
    exit_code = 0
    for f in targets:
        findings = lint_markdown(f.read_text(encoding="utf-8"))
        if findings:
            exit_code = 1
            all_findings[str(f)] = [v.to_dict() for v in findings]

    if args.json:
        print(json.dumps({"ok": exit_code == 0, "files": all_findings}, ensure_ascii=False, indent=2))
    else:
        if not all_findings:
            print(f"OK: {len(targets)} file(s) passed BiDi structural checks with zero collisions.")
        else:
            for file_path, items in all_findings.items():
                for item in items:
                    print(f"{file_path}:{item['line']} [{item['rule']}] {item['message']}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
