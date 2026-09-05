"""Regression for the audited temporary monster matte (Pillow, no client needed)."""
import importlib.util
from pathlib import Path
import sys
import unittest
from PIL import Image

sys.dont_write_bytecode = True
GAME = Path(__file__).resolve().parents[3] / 'templates/game/legend'
spec = importlib.util.spec_from_file_location('prepare_monster', GAME / 'tools/prepare_monster.py')
prepare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepare)


class MonsterArtworkTests(unittest.TestCase):
    def test_output_is_reproducible(self):
        with Image.open(prepare.SOURCE) as source, Image.open(prepare.OUTPUT) as result:
            self.assertEqual(result.mode, 'RGBA')
            self.assertEqual(result.size, source.size)
            self.assertEqual(result.tobytes(), prepare.clean(source).tobytes())

    def test_matte_and_baked_shadow_are_transparent(self):
        with Image.open(prepare.OUTPUT) as image:
            pixels = list(image.getdata())
            self.assertGreater(sum(p[3] == 0 for p in pixels), len(pixels) * .60)
            self.assertGreater(sum(p[3] == 255 for p in pixels), len(pixels) * .20)
            self.assertTrue(all(p[:3] not in [(29,38,51), (18,23,31)] for p in pixels if p[3]))
            self.assertEqual(image.getpixel((0,0))[3], 0)
            self.assertEqual(image.getpixel((150,100))[3], 0)

    def test_character_warm_pixels_survive(self):
        with Image.open(prepare.SOURCE) as source, Image.open(prepare.OUTPUT) as result:
            for original, actual in zip(source.convert('RGBA').getdata(), result.getdata()):
                if original[0] > original[2] + 10:
                    self.assertEqual(original, actual)


if __name__ == '__main__':
    unittest.main()
