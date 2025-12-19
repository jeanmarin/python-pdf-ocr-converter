import unittest

from pdf_ocr_converter.diffing import changed_lines, format_page_header


class TestDiffing(unittest.TestCase):
    def test_changed_lines_keeps_only_added_removed(self) -> None:
        raw = "hello\nworld\n"
        corrected = "hello\nWORLD\n"

        lines = changed_lines(raw, corrected)

        # ndiff will include removed and added lines, but we should not include
        # intraline markers ("? ") or unchanged ("  ").
        self.assertTrue(any(line.startswith("- ") for line in lines))
        self.assertTrue(any(line.startswith("+ ") for line in lines))
        self.assertFalse(any(line.startswith("? ") for line in lines))
        self.assertFalse(any(line.startswith("  ") for line in lines))

    def test_format_page_header(self) -> None:
        self.assertEqual(format_page_header(3), "*********** PAGE 3 ***********")


if __name__ == "__main__":
    unittest.main()


