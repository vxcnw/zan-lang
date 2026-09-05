"""Build reviewed Image2 extraction plates into straight-alpha runtime sprites.

Authoring only: Python + Pillow. No API calls or credentials. Run from any cwd.
The color key is deliberately limited to the magenta extraction plates described
in monster-art.json; it is not a general-purpose background remover.
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'tools/monster-art.json'
SOURCES = ROOT / 'assets/generated/monster-sources'


def remove_matte(image):
    """Unmix magenta edge spill; preserve non-magenta subject colors verbatim."""
    result = image.convert('RGBA')
    pixels = []
    for r, g, b, old_alpha in result.getdata():
        spill = min(r, b) - g
        if spill >= 150:
            pixels.append((0, 0, 0, 0))
        elif spill > 18:
            # C = alpha*foreground + (1-alpha)*(255,0,255).
            alpha = (255 - spill) / 255
            pixels.append((max(0, round((r - spill) / alpha)),
                           min(255, round(g / alpha)),
                           max(0, round((b - spill) / alpha)),
                           round(old_alpha * alpha)))
        else:
            pixels.append((r, g, b, old_alpha))
    result.putdata(pixels)
    return result


def sprite_from_cell(plate, asset, size=256):
    col, row = asset['cell'] % 3, asset['cell'] // 3
    box = asset.get('crop', [col * 512, row * 512, (col+1)*512, (row+1)*512])
    cutout = remove_matte(plate.crop(box))
    bounds = cutout.getbbox()
    if not bounds:
        raise ValueError(f"Empty sprite: {asset['name']}")
    if min(bounds[0], bounds[1], cutout.width-bounds[2], cutout.height-bounds[3]) < 4:
        raise ValueError(f"Sprite touches cell edge: {asset['name']}; review plate/crop")
    cutout = cutout.crop(bounds)
    cutout.thumbnail((size-32, size-32), Image.Resampling.LANCZOS)
    # Lanczos ringing can reintroduce chroma at high-contrast edges.
    cutout = remove_matte(cutout)
    # Shared baseline 240/256; keep a clean 16px padding around all silhouettes.
    sprite = Image.new('RGBA', (size, size))
    sprite.alpha_composite(cutout, ((size-cutout.width)//2, size-16-cutout.height))
    return sprite


def prepare(manifest_path=MANIFEST, source_dir=SOURCES, output_root=ROOT):
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    plates = {}
    for asset in manifest['assets']:
        source = source_dir / asset['sheet']
        if asset['sheet'] not in plates:
            expected = manifest.get('source_sha256', {}).get(asset['sheet'])
            if expected and hashlib.sha256(source.read_bytes()).hexdigest() != expected:
                raise ValueError(f'Source checksum changed: {source.name}')
            plate = Image.open(source).convert('RGB')
            if plate.size != tuple(manifest['source_size']):
                raise ValueError(f'Unexpected source dimensions: {source.name}')
            plates[asset['sheet']] = plate
        sprite = sprite_from_cell(plates[asset['sheet']], asset, manifest['runtime_size'])
        target = output_root / asset['path']
        target.parent.mkdir(parents=True, exist_ok=True)
        sprite.save(target, optimize=True)
    return manifest


def contact_sheet(manifest, output, root=ROOT):
    cols, tw, th = 6, 224, 250
    sheet = Image.new('RGB', (cols*tw, 64+6*th), '#151e27')
    draw = ImageDraw.Draw(sheet)
    font_path = Path('C:/Windows/Fonts/msyh.ttc')
    if not font_path.exists():
        raise ValueError('Contact sheet needs a CJK font at C:/Windows/Fonts/msyh.ttc')
    font = ImageFont.truetype(str(font_path), 17)
    title = ImageFont.truetype(str(font_path), 25)
    draw.text((24, 16), '传奇放置  /  怪物素材库 · 36 种外形', font=title, fill='#ead6ac')
    for i, asset in enumerate(manifest['assets']):
        x, y = (i%cols)*tw, 64+(i//cols)*th
        draw.rounded_rectangle((x+6,y+6,x+tw-6,y+th-6), radius=8, fill='#1e2a35')
        sprite = Image.open(root/asset['path']).convert('RGBA')
        sprite.thumbnail((196,196), Image.Resampling.LANCZOS)
        sheet.paste(sprite, (x+(tw-sprite.width)//2,y+8), sprite)
        text = f"{asset['picture']:02d}  {asset['name']}"
        draw.text((x+tw//2,y+216), text, anchor='mm', font=font, fill='#e4d8bd')
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=SOURCES)
    parser.add_argument('--output-root', type=Path, default=ROOT)
    parser.add_argument('--preview', type=Path, help='Optional contact sheet (put throwaway previews in _scratch)')
    args = parser.parse_args()
    manifest = prepare(source_dir=args.source, output_root=args.output_root)
    if args.preview:
        contact_sheet(manifest, args.preview, args.output_root)
    print(f"Prepared {len(manifest['assets'])} unique RGBA monster sprites")
