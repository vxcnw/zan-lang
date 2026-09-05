"""Title shader baking and WebP-only, repeatable artwork import regression."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / 'templates/game/wuwei'
SCRIPT = PROJECT / 'tools/prepare_assets.py'
spec = importlib.util.spec_from_file_location('wuwei_prepare_assets', SCRIPT)
assets = importlib.util.module_from_spec(spec)
spec.loader.exec_module(assets)


def shader_alpha(r, g, b, a):
    paper = min(r, g, b) / 255
    if paper <= 0.82:
        return a
    if paper >= 0.94:
        return 0
    x = (paper - 0.82) / (0.94 - 0.82)
    return round(a * (1 - 3 * x ** 2 + 2 * x ** 3))


def is_webp(data):
    return data[:4] == b'RIFF' and data[8:12] == b'WEBP'


class PrepareAssetsTests(unittest.TestCase):
    def test_shader_formula_and_original_alpha(self):
        pixels = [(v, v, v, a) for a in (0, 1, 64, 128, 255) for v in range(256)]
        pixels += [(250, 40, 30, 255), (40, 250, 250, 128), (250, 250, 40, 255)]
        source = Image.new('RGBA', (len(pixels), 1))
        source.putdata(pixels)
        result = assets.apply_title_alpha(source)
        self.assertEqual(result.size, source.size)
        self.assertEqual(source.tobytes(), bytes(v for pixel in pixels for v in pixel))
        expected = [(r, g, b, shader_alpha(r, g, b, a)) for r, g, b, a in pixels]
        self.assertEqual(result.tobytes(), bytes(v for pixel in expected for v in pixel))

    def test_import_emits_webp_only_and_is_repeatable(self):
        scratch = ROOT / '_scratch'
        scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='wuwei-assets-', dir=scratch) as directory:
            source = Path(directory) / 'source'
            output = Path(directory) / 'output'
            source.mkdir()
            output.mkdir()
            # Larger than the icon tier: the title must not be resized.
            title = Image.new('RGBA', (2001, 2), (225, 230, 240, 128))
            title.putpixel((0, 0), (180, 30, 25, 255))
            title.save(source / 'title_calligraphy.webp', lossless=True)
            # A stale PNG from the earlier PNG era must not survive the import.
            title.save(output / 'title_calligraphy.png')
            icon = Image.new('RGBA', (2, 2), (250, 250, 250, 255))
            icon.save(source / 'icon.webp', lossless=True)
            landscape = Image.new('RGBA', (300, 2), (240, 242, 245, 255))
            landscape.save(source / 'landscape.webp', lossless=True)
            command = [sys.executable, '-B', str(SCRIPT), '--source', str(source),
                       '--output', str(output)]
            subprocess.run(command, check=True, capture_output=True)
            self.assertEqual({p.name for p in output.iterdir()},
                             {'title_calligraphy.webp', 'icon.webp', 'landscape.webp'})
            for name, original in (('title_calligraphy.webp', title),
                                   ('icon.webp', icon), ('landscape.webp', landscape)):
                data = (output / name).read_bytes()
                self.assertTrue(is_webp(data), name)
                with Image.open(output / name) as actual:
                    self.assertEqual(actual.size, original.size, name)
                    rgba = actual.convert('RGBA').tobytes()
                    if name.startswith('title'):
                        self.assertEqual(rgba, assets.apply_title_alpha(title).tobytes())
                        continue
                    for r, g, b, a in zip(rgba[0::4], rgba[1::4], rgba[2::4], rgba[3::4]):
                        for value, want in zip((r, g, b), (250, 250, 250)):
                            # Lossy WebP drift depends on the vendored libwebp
                            # build (9 measured on Pillow 12.1); real pipeline
                            # regressions flip modes or tiers and drift by tens.
                            self.assertLessEqual(abs(value - want), 12)
                        self.assertEqual(a, 255)
            first = {p.name: p.read_bytes() for p in output.iterdir()}
            subprocess.run(command, check=True, capture_output=True)
            self.assertEqual({p.name: p.read_bytes() for p in output.iterdir()}, first)

    def test_shipped_title_header_pixels_background_and_seal(self):
        path = PROJECT / 'assets/images/title_calligraphy.webp'
        self.assertTrue(is_webp(path.read_bytes()[:12]))
        with Image.open(path) as image:
            self.assertEqual(image.mode, 'RGBA')
            self.assertEqual(image.size, (1916, 821))
            rgba = image.tobytes()
            transparent = partial = seal = ink = 0
            for r, g, b, a in zip(rgba[0::4], rgba[1::4], rgba[2::4], rgba[3::4]):
                self.assertEqual(a, shader_alpha(r, g, b, 255))
                transparent += a == 0
                partial += 0 < a < 255
                if r > 100 and r > g * 2 and r > b * 2:
                    self.assertEqual(a, 255)
                    seal += 1
                ink += max(r, g, b) < 80 and a == 255
            self.assertGreater(transparent, image.width * image.height // 2)
            self.assertGreater(partial, 0)
            self.assertGreater(seal, 1000)
            self.assertGreater(ink, 10000)

    def test_shipped_images_are_webp_only(self):
        images = PROJECT / 'assets/images'
        self.assertEqual(list(images.glob('*.png')), [])
        webp = sorted(images.glob('*.webp'))
        self.assertGreater(len(webp), 300)
        total = 0
        for path in webp:
            self.assertTrue(is_webp(path.read_bytes()[:12]), path.name)
            total += path.stat().st_size
        self.assertLess(total, 40 * 1024 * 1024)


if __name__ == '__main__':
    unittest.main()
