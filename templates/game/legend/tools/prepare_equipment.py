from pathlib import Path
from PIL import Image
import numpy as np,csv
import argparse

parser=argparse.ArgumentParser(description="Rebuild transparent equipment assets and explicit item-ID mapping")
parser.add_argument("--preview",type=Path,help="Optional contact sheet path outside the source tree")
args=parser.parse_args()

root=Path(__file__).resolve().parents[1]; out=root/'assets/equipment'; out.mkdir(exist_ok=True)
names=['sword','armor','helmet','necklace','bracelet','ring','belt','boots','gem','book','axe','staff']
for tier in range(3):
 im=Image.open(root/'tools/equipment-source'/f'equipment-{tier}.png').convert('RGB')
 for k,name in enumerate(names):
  x,y=k%4,k//4
  a=np.array(im.crop((x*im.width//4,y*im.height//3,(x+1)*im.width//4,(y+1)*im.height//3)))
  # Chroma matte from magenta dominance; preserve black metal and fine chains.
  f=a.astype(float); mask=(f[:,:,0]>f[:,:,1]*1.55+28)&(f[:,:,2]>f[:,:,1]*1.4+28)
  # Reject small disconnected scraps from neighboring cells, keeping thin chains intact.
  seen=mask.copy(); components=[]; h,w=mask.shape
  for yy,xx in zip(*np.where(~mask)):
   if seen[yy,xx]:continue
   pending=[(int(yy),int(xx))];seen[yy,xx]=True;component=[]
   while pending:
    py,px=pending.pop();component.append((py,px))
    for ny,nx in ((py-1,px),(py+1,px),(py,px-1),(py,px+1)):
     if 0<=ny<h and 0<=nx<w and not seen[ny,nx]:seen[ny,nx]=True;pending.append((ny,nx))
   components.append(component)
  threshold=max(35,max(map(len,components))*0.005)
  for c in components:
   if len(c)<threshold:
    for yy,xx in c:mask[yy,xx]=True
  rgba=np.dstack([a,np.where(mask,0,255).astype('uint8')]); sprite=Image.fromarray(rgba)
  box=sprite.getbbox(); sprite=sprite.crop(box); sprite.thumbnail((112,112),Image.Resampling.LANCZOS)
  canvas=Image.new('RGBA',(128,128));canvas.alpha_composite(sprite,((128-sprite.width)//2,(128-sprite.height)//2))
  canvas.save(out/f'{name}-{tier}.png')
rows=list(csv.DictReader((root/'data/items.csv').open(encoding='utf-8-sig')))
slot={0:'sword',1:'armor',2:'helmet',3:'necklace',4:'bracelet',5:'bracelet',6:'ring',7:'ring',8:'belt',9:'boots',10:'gem',11:'book'}
with (root/'data/equipment_art.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.writer(f);w.writerow(['id','path'])
 for r in rows:
  if int(r['slot'])<0:continue
  name=slot[int(r['slot'])]; lv=int(r['min_level']); tier=0 if lv<25 else 1 if lv<45 else 2
  if int(r['slot'])==0:
   if '斧' in r['name']:name='axe'
   elif '杖' in r['name'] or int(r['magic_max'])>int(r['attack_max']):name='staff'
  w.writerow([r['id'],f'assets/equipment/{name}-{tier}.png'])
(root/'assets/equipment/README.md').write_text('''# Equipment icon set

36 generated icons, 12 families × 3 visual tiers. Created with the locally configured Image2 API; no credentials are included. These are template artwork, not extracted originals or 732 unique item illustrations.

`data/equipment_art.csv` maps each wearable item ID explicitly to its PNG. Runtime rendering must use this mapping, not slot modulo or screenshot crops. Tier appearance is illustrative, not an equipment quality indicator. Coefficient, quality and enhancement remain independent gameplay fields.

All PNGs are 128×128 RGBA, normalized to a 112px content box. Original 4×3 sheets used a magenta chroma background, removed before reduction. Review on dark backgrounds when replacing assets.
''',encoding='utf-8')
# Dark-background art contact sheet for verification.
preview=Image.new('RGB',(12*100,3*100),(24,31,41))
for t in range(3):
 for i,n in enumerate(names):
  icon=Image.open(out/f'{n}-{t}.png');icon.thumbnail((96,96));preview.paste(icon,(i*100,t*100),icon)
if args.preview:
 args.preview.parent.mkdir(parents=True,exist_ok=True)
 preview.save(args.preview)
