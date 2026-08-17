from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "themes"))
sys.path.insert(0, str(ROOT / "lab" / "reverse"))

from signal_style import palette, profile  # noqa: E402
from reverse_score import score  # noqa: E402


class TestSignalHelpers(unittest.TestCase):
    def test_palette_is_copy(self):
        a = palette()
        b = palette()
        a["primary"] = "#000000"
        self.assertNotEqual(a["primary"], b["primary"])

    def test_profile_is_copy(self):
        a = profile("paper")
        b = profile("paper")
        a["font_size"] = 99
        self.assertNotEqual(a["font_size"], b["font_size"])

    def test_reverse_score_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "a.png"
            arr = np.zeros((80, 120, 3), dtype=np.uint8) + 255
            arr[20:60, 50:70] = 0
            Image.fromarray(arr).save(p)
            result = score(p, p)
            self.assertAlmostEqual(result["total"], 1.0, places=6)


if __name__ == "__main__":
    unittest.main()
