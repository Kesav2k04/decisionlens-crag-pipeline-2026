# scripts/make_icon.py
# Generates the DecisionLens favicon: a vintage laced football inked on
# terracotta book cloth — the visual signature of the Football Codex theme.
import os
from PIL import Image, ImageDraw

S = 256
TERRA = (188, 86, 50, 255)
PAPER = (244, 240, 229, 255)
INK = (38, 30, 18, 255)
GRID = (255, 255, 255, 16)

img = Image.new("RGBA", (S, S), TERRA)
d = ImageDraw.Draw(img)

# faint graph-paper grid, like the Fable frame
for x in range(0, S + 1, 32):
    d.line([(x, 0), (x, S)], fill=GRID, width=1)
    d.line([(0, x), (S, x)], fill=GRID, width=1)

cx, cy, r = S // 2, S // 2, 88

# paper ball with ink outline
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PAPER, outline=INK, width=6)

# vintage T-panel seams: two vertical lens seams + equator
d.ellipse([cx - 44, cy - r + 8, cx + 44, cy + r - 8], outline=INK, width=4)
d.arc([cx - r + 8, cy - 36, cx + r - 8, cy + 36], 0, 360, fill=INK, width=4)

# the lace, c. 1930 — short bar with cross stitches at top of centre panel
lace_y = cy - 46
d.line([(cx - 22, lace_y), (cx + 22, lace_y)], fill=INK, width=5)
for sx in (-14, 0, 14):
    d.line([(cx + sx - 5, lace_y - 8), (cx + sx + 5, lace_y + 8)], fill=INK, width=4)

out = os.path.join(os.path.dirname(__file__), "..", "assets", "icon.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(os.path.abspath(out))
print("wrote", os.path.abspath(out))
