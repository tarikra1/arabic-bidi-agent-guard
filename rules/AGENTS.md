# Global Arabic Formatting & BiDi Anti-Scrambling Rule

Most AI chat and IDE Markdown canvases (Claude Code, Cursor, Antigravity, GitHub, VS Code) render Markdown blocks with left-to-right alignment and no inline BiDi isolation. Mixing Arabic (RTL) and Latin/English (LTR) tokens on the same line scrambles word order, parentheses, and line wraps.

Whenever your response (or any section of it) is written in **Arabic**, you MUST follow these rules strictly:

## 1. Keep Arabic Sentences Purely Arabic
- Write every Arabic paragraph and narrative sentence using **Arabic script only** so each line remains a single uninterrupted RTL run.
- **Never** embed raw English words, package/skill/tool names, CLI commands, flags, file paths, inline backtick spans (`` `...` ``), or URLs inside the middle of an Arabic sentence.
- When mentioning common technologies in flowing prose, transliterate them naturally in Arabic (e.g., بايثون، جافاسكريبت، تايب سكريبت، جيت هاب، دوكر، ويندوز) rather than switching to Latin script mid-line.

## 2. Isolate Technical Identifiers on Separate Lines or Columns
- Whenever you need to show English identifiers, skill names, slash commands, clickable file links (`[name](file:///...)`), URLs, or code spans:
  - Put them on **their own standalone bullet items** or **indented sub-bullets**,
  - Place them inside **fenced code blocks**, or
  - Use a **Markdown table** with dedicated columns (e.g., one column for the English identifier/link and a separate column for the pure-Arabic explanation).

## 3. Avoid Mixed Parentheses, Operators, and Trailing LTR Tokens
- Never write mixed parentheses such as `(Global)` or `(13 مهارة + أدوات Python)` inside an Arabic sentence. Express them in pure Arabic prose or break them into bullets.
- Use standard Arabic punctuation (`،` `؛` `؟`) in Arabic text.
- Never end an Arabic sentence with a Latin word followed by a period (e.g., `Claude.`).

## 4. Do Not Inject Invisible BiDi Control Characters
- Never insert hidden Unicode directional characters (`U+200E`, `U+200F`, `U+202A`–`U+202E`, `U+2066`–`U+2069`) into user-facing text, drafts, social media copy, or code, as they create invisible watermarks and break linters. Rely exclusively on the structural separation rules above.
