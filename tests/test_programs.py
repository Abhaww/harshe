"""
Gwaje-gwajen Shirye-shiryen Misali (Example Programs Integration Tests)
"""

import unittest
import os
import glob
from io import StringIO
import sys
from harshe import run_file


class TestPrograms(unittest.TestCase):

    def test_run_all_examples(self):
        examples_dir = os.path.join(os.path.dirname(__file__), "..", "examples")
        example_files = sorted(glob.glob(os.path.join(examples_dir, "*.hausa")))

        # Redirect stdout and mock input for interactive ones
        old_stdout = sys.stdout
        old_stdin = sys.stdin

        try:
            for filepath in example_files:
                basename = os.path.basename(filepath)
                # For interactive guessing game (07), provide mock input
                if "kacici_kacici" in basename:
                    sys.stdin = StringIO("maciji\ngishiri\niska\n")
                else:
                    sys.stdin = StringIO("")

                sys.stdout = StringIO()

                try:
                    run_file(filepath)
                except Exception as e:
                    self.fail(f"Shirin '{basename}' ya gaza aiki tare da kuskure: {str(e)}")

        finally:
            sys.stdout = old_stdout
            sys.stdin = old_stdin


if __name__ == "__main__":
    unittest.main()
