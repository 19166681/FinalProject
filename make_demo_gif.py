"""
Run this once to generate demo.gif from the annotated output frames.
Usage: python make_demo_gif.py
Output: demo.gif in the project root (~5-8 MB, suitable for GitHub README)
"""

import glob
import os
from PIL import Image

FRAMES_DIR = "output"
OUTPUT_PATH = "demo.gif"
TARGET_WIDTH = 640
FPS = 12
MAX_FRAMES = 72  # ~6 seconds at 12 fps

frame_paths = sorted(glob.glob(os.path.join(FRAMES_DIR, "frame_*.jpg")))
if not frame_paths:
    raise FileNotFoundError(f"No frames found in '{FRAMES_DIR}/'. Run the app on a video first.")

step = max(1, len(frame_paths) // MAX_FRAMES)
selected = frame_paths[::step][:MAX_FRAMES]
print(f"Using {len(selected)} of {len(frame_paths)} frames (every {step}th)")

frames = []
for path in selected:
    img = Image.open(path).convert("RGB")
    w, h = img.size
    new_h = int(h * TARGET_WIDTH / w)
    frames.append(img.resize((TARGET_WIDTH, new_h), Image.LANCZOS))

frames[0].save(
    OUTPUT_PATH,
    save_all=True,
    append_images=frames[1:],
    duration=int(1000 / FPS),
    loop=0,
    optimize=True,
)

size_mb = os.path.getsize(OUTPUT_PATH) / 1_000_000
print(f"Saved {OUTPUT_PATH} ({size_mb:.1f} MB)")
if size_mb > 10:
    print("Warning: file is over 10 MB — GitHub may not render it inline. Try reducing MAX_FRAMES.")
