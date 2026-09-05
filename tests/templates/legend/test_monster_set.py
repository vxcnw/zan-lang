"""Offline artwork gate: table coverage, source integrity, alpha and reproducibility."""
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest
from PIL import Image

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3] / 'templates/game/legend'
SPEC = importlib.util.spec_from_file_location('prepare_monsters', ROOT/'tools/prepare_monsters.py')
PREP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREP)


def rows(name):
    with (ROOT/'data'/name).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


class MonsterSetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT/'tools/monster-art.json').read_text(encoding='utf-8'))
        cls.art = {int(r['id']): r for r in rows('monster_art.csv')}

    def test_all_monsters_bosses_and_encounters_resolve(self):
        self.assertEqual(len(self.art), 36)
        self.assertEqual(len(rows('monster_art.csv')), len(self.art))
        for name in ('monsters.csv', 'bosses.csv', 'encounter_art.csv'):
            for row in rows(name):
                with self.subTest(table=name, row=row['id']):
                    self.assertIn(int(row['picture']), self.art)
        self.assertEqual({r['id'] for r in rows('encounter_art.csv')},
                         {r['id'] for r in rows('encounters.csv')})
        self.assertEqual({a['picture'] for a in self.manifest['assets']}, set(self.art))

    def test_sources_are_reviewed_and_checksummed(self):
        sources = {a['sheet'] for a in self.manifest['assets']}
        self.assertEqual(len(sources), 6)
        self.assertEqual(set(self.manifest['source_sha256']), sources)
        for source in sources:
            path = PREP.SOURCES/source
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                             self.manifest['source_sha256'][source])

    def test_all_sprites_are_unique_clean_rgba_with_shared_baseline(self):
        hashes = set()
        for key, row in self.art.items():
            with self.subTest(picture=key, name=row['name']), Image.open(ROOT/row['path']) as im:
                self.assertEqual(im.mode, 'RGBA')
                self.assertEqual(im.size, (256,256))
                hashes.add(hashlib.sha256(im.tobytes()).hexdigest())
                alpha = im.getchannel('A')
                bounds = alpha.getbbox()
                self.assertIsNotNone(bounds)
                self.assertGreaterEqual(bounds[0], 16)
                self.assertGreaterEqual(bounds[1], 16)
                self.assertLessEqual(bounds[2], 240)
                self.assertEqual(bounds[3], 240)
                pixels = list(im.getdata())
                self.assertGreater(sum(p[3]==0 for p in pixels), len(pixels)*.35)
                self.assertGreater(sum(p[3]>240 for p in pixels), len(pixels)*.08)
                # High-alpha pink matte must never survive edge processing.
                self.assertFalse(any(min(r,b)-g > 40 and a > 180 for r,g,b,a in pixels))
        self.assertEqual(len(hashes), 36, 'Repeated placeholder artwork')

    def test_runtime_images_are_reproducible(self):
        plates = {}
        for asset in self.manifest['assets']:
            with self.subTest(picture=asset['picture']):
                if asset['sheet'] not in plates:
                    plates[asset['sheet']] = Image.open(PREP.SOURCES/asset['sheet']).convert('RGB')
                result = PREP.sprite_from_cell(plates[asset['sheet']], asset)
                with Image.open(ROOT/asset['path']) as output:
                    self.assertEqual(result.tobytes(), output.tobytes())
                self.assertEqual(self.art[asset['picture']]['path'], asset['path'])

    def test_key_does_not_destroy_neutral_fur_or_warm_armor(self):
        colors = [(235,231,220,255), (110,72,34,255), (48,85,101,255), (23,23,23,255)]
        source = Image.new('RGBA', (len(colors),1)); source.putdata(colors)
        self.assertEqual(list(PREP.remove_matte(source).getdata()), colors)
        key = Image.new('RGB', (2,1)); key.putdata([(255,0,255), (180,0,180)])
        self.assertEqual(list(PREP.remove_matte(key).getchannel('A').getdata()), [0,0])


if __name__ == '__main__':
    unittest.main()
