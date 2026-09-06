"""Equipment artwork integrity; requires Pillow. Runs without network/API keys."""
import csv
from pathlib import Path
import unittest
from PIL import Image

ROOT = Path(__file__).resolve().parents[3] / 'templates/game/legend'

class EquipmentArtworkTests(unittest.TestCase):
    def test_every_wearable_has_exactly_one_mapping(self):
        with (ROOT/'data/items.csv').open(encoding='utf-8-sig') as f:
            expected = {int(r['id']) for r in csv.DictReader(f) if int(r['slot']) >= 0}
        with (ROOT/'data/equipment_art.csv').open(encoding='utf-8-sig') as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), len(expected))
        self.assertEqual({int(r['id']) for r in rows}, expected)
        for r in rows:
            path = (ROOT/r['path']).resolve()
            self.assertTrue(path.is_relative_to((ROOT/'assets/equipment').resolve()))
            self.assertTrue(path.is_file(), path)

    def test_normalized_transparent_sprites(self):
        paths = list((ROOT/'assets/equipment').glob('*.png'))
        self.assertEqual(len(paths), 36)
        for p in paths:
            with self.subTest(p=p.name), Image.open(p) as im:
                self.assertEqual(im.mode, 'RGBA')
                self.assertEqual(im.size, (128, 128))
                box = im.getbbox()
                self.assertIsNotNone(box)
                self.assertGreaterEqual(box[0], 8)
                self.assertGreaterEqual(box[1], 8)
                self.assertLessEqual(box[2], 120)
                self.assertLessEqual(box[3], 120)
                self.assertGreater(sum(im.getchannel('A').histogram()[1:]), 500)
                self.assertEqual(im.getpixel((0, 0))[3], 0)

    def test_sources_and_runtime_mapping(self):
        for tier in range(3):
            self.assertTrue((ROOT/f'tools/equipment-source/equipment-{tier}.png').exists())
        code = (ROOT/'src/main.zan').read_text(encoding='utf-8-sig')
        self.assertIn('equipmentArtData.At(e.definitionId)', code)
        self.assertIn('EquipmentArtPath(e)', code)

if __name__ == '__main__':
    unittest.main()

