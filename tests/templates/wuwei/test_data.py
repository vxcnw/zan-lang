"""Cross-table integrity checks for the maintained Wuwei balancing sheets."""
import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / 'templates/game/wuwei/data'


def table(name):
    with (DATA / (name + '.csv')).open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


class WuweiDataTests(unittest.TestCase):
    def test_original_content_counts(self):
        for name, count in [('realms', 9), ('maps', 29), ('enemies', 69), ('recipes', 108), ('skills', 10), ('quests', 21), ('sects', 2)]:
            self.assertEqual(len(table(name)), count, name)

    def test_unique_keys(self):
        for path in DATA.glob('*.csv'):
            rows = table(path.stem)
            if rows and 'id' in rows[0]:
                ids = [row['id'] for row in rows]
                self.assertEqual(len(ids), len(set(ids)), path.name)

    def test_map_enemy_ranges(self):
        enemies = table('enemies')
        for area in table('maps'):
            start, count = int(area['first_enemy']), int(area['enemy_count'])
            self.assertGreater(count, 0)
            self.assertEqual(len(enemies[start:start + count]), count)
            for enemy in enemies[start:start + count]:
                self.assertEqual(enemy['map'], area['id'])
                self.assertGreater(float(enemy['hp']), 0)
                self.assertGreater(float(enemy['interval']), 0)

    def test_recipe_references(self):
        items = {row['id'] for row in table('items')}
        recipes = {row['id'] for row in table('recipes')}
        for recipe in table('recipes'):
            self.assertIn(recipe['result'], items, recipe['id'])
            self.assertGreater(float(recipe['duration']), 0, recipe['id'])
        for cost in table('ingredients'):
            self.assertIn(cost['recipe'], recipes)
            self.assertIn(cost['item'], items | {'stones'})
            self.assertGreater(int(cost['count']), 0)

    def test_breakthrough_and_market_references(self):
        items = {row['id'] for row in table('items')}
        pills = {row['pill'] for row in table('maps') if row['pill']}
        for realm in table('realms')[:-1]:
            self.assertIn(realm['pill'], pills)
            self.assertIn(realm['pill'], items)
        for offer in table('market'):
            self.assertIn(offer['id'], items)
            self.assertGreater(float(offer['price']), 0)


if __name__ == '__main__':
    unittest.main()
