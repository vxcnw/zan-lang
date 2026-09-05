"""Remove the audited flat matte/shadow from the temporary reference monster.

This is NOT a client extraction or a general-purpose sprite/background remover.
The pinned input digest prevents silently applying its colour key to other art.
Run from any directory; needs Pillow. Runtime game needs no Python.
"""
from pathlib import Path
import hashlib
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'assets/reference/monster.png'
OUTPUT = ROOT / 'assets/processed/monster.png'


def clean(source: Image.Image) -> Image.Image:
    rgba = source.convert('RGBA')
    result = rgba.copy()
    pixels = result.load()
    # Audited cool-blue matte varies from the baked shadow to the background.
    dark, delta = (18, 23, 31), (11, 15, 20)
    norm = sum(c*c for c in delta)
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = pixels[x, y]
            rgb = (r, g, b)
            t = max(0, min(1, sum((rgb[i]-dark[i])*delta[i] for i in range(3))/norm))
            distance = sum((rgb[i]-dark[i]-t*delta[i])**2 for i in range(3))
            if distance <= 12:
                pixels[x, y] = (0, 0, 0, 0)
    return result


def main():
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if digest != '9bd7709574d1086cf3a63680bc13801154073c703c1fb53075f8ca223bf7c9ec':
        raise SystemExit('Reference monster changed: review matte colours before regenerating')
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(SOURCE) as image:
        clean(image).save(OUTPUT)
    print(OUTPUT)


if __name__ == '__main__':
    main()
