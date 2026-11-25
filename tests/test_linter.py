import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from arabic_bidi_guard import lint_markdown, strip_hidden_bidi_controls


class TestArabicBidiGuard(unittest.TestCase):
    def test_pure_arabic_and_isolated_code_pass(self) -> None:
        clean_doc = """# دليل الاستخدام السريع

هذا النص مكتوب باللغة العربية الصافية بدون أي تداخل مع حروف لاتينية في نفس السطر.

لتشغيل الأداة استخدم الأمر التالي:

```bash
bidi-guard check README.md
```

| الأمر | الوصف بالعربية |
| :--- | :--- |
| `bidi-guard check` | فحص ملفات ماركداون والتأكد من سلامة اتجاه النص |
| `bidi-guard strip-controls` | إزالة محارف الاتجاه الخفية من الملفات |
"""
        self.assertEqual(lint_markdown(clean_doc), [])

    def test_detects_inline_code_in_arabic(self) -> None:
        bad = "شغّل الأمر `npm install` لتثبيت الحزم."
        res = lint_markdown(bad)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].rule, "INLINE_CODE_IN_ARABIC")

    def test_detects_mixed_parentheses(self) -> None:
        bad = "يتم تفعيل الإعداد العام (Global) تلقائياً."
        res = lint_markdown(bad)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].rule, "MIXED_PARENTHESES")

    def test_detects_trailing_ltr_period(self) -> None:
        bad = "يعمل هذا النظام بسلاسة داخل بيئة Windows."
        res = lint_markdown(bad)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].rule, "TRAILING_LTR_PERIOD")

    def test_detects_mixed_prose(self) -> None:
        bad = "نستخدم مكتبة Python لمعالجة البيانات بسرعة."
        res = lint_markdown(bad)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].rule, "MIXED_RTL_LTR_PROSE")

    def test_strips_hidden_bidi_controls(self) -> None:
        contaminated = "مرحبا\u200f بالعالم\u202b!"
        findings = lint_markdown(contaminated)
        self.assertTrue(any(v.rule == "HIDDEN_BIDI_CONTROLS" for v in findings))
        cleaned, removed = strip_hidden_bidi_controls(contaminated)
        self.assertEqual(removed, 2)
        self.assertEqual(cleaned, "مرحبا بالعالم!")


if __name__ == "__main__":
    unittest.main()
