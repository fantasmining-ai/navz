"""Ensambla la hoja de poses y el GIF a partir de simulaciones/_frames/. Requiere Pillow."""
import os, glob
from PIL import Image, ImageDraw
raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fr = os.path.join(raiz, 'simulaciones', '_frames'); out = os.path.join(raiz, 'simulaciones')
poses = sorted(glob.glob(os.path.join(fr, 'pose_*.png')))
w, h, cols = 420, 390, 4; rows = (len(poses) + cols - 1) // cols
hoja = Image.new('RGB', (cols * w, rows * h), (20, 22, 26)); d = ImageDraw.Draw(hoja)
for i, f in enumerate(poses):
    im = Image.open(f).convert('RGB').resize((w, h)); x, y = (i % cols) * w, (i // cols) * h
    hoja.paste(im, (x, y)); d.rectangle((x, y, x + w, y + 22), fill=(0, 0, 0))
    d.text((x + 8, y + 5), os.path.basename(f)[5:-4], fill=(230, 240, 250))
hoja.save(os.path.join(out, 'poses.jpg'), quality=88)
anim = sorted(glob.glob(os.path.join(fr, 'anim_*.png')))
frames = [Image.open(f).convert('RGB').resize((336, 312)).convert('P', palette=Image.ADAPTIVE, colors=64) for f in anim]
frames[0].save(os.path.join(out, 'movimiento_cuello.gif'), save_all=True, append_images=frames[1:], duration=60, loop=0, optimize=True)
print('poses', len(poses), 'frames', len(anim))
