"""Building multi-object scene by pasting object photos onto a background"""
import random
from PIL import Image
from src import config

def overlaps(box, placed):
    """true if the box touxhes any box that is already in the scene"""
    x1, y1, x2, y2 = box
    for px1, py1, px2, py2 in placed:
        if x1 < px2 and px1 < x2 and y1 < py2 and py1 < y2:
            return True
    return False

def place_box(w, h, canvas, placed, rng, max_tries = config.max_tries):
    """Random spot for a w x h sized object that does not overlap the placed boxes or 'None' if it will not fit"""
    if w > canvas or h > canvas:
        return None
    for _ in range(max_tries):
        x1 = rng.randint(0, canvas - w)
        y1 = rng.randint(0, canvas - h)
        box = (x1, y1, x1+w, y1+h)
        if not overlaps(box, placed):
            return box
    return None

def make_scene(background_path, objects, rng, canvas = config.canvas,
               min_size = config.min_size, max_size = config.max_size,
               min_objects = config.min_objects, max_objects = config.max_objects):
    """One canvvas X canvas sized scene and its labels as a list of the class and bounding box coords"""
    scene = Image.open(background_path).convert("RGB").resize((canvas, canvas))
    n = rng.randint(min_objects, max_objects)
    picks = rng.sample(range(len(objects)), n) # n different photos so no one photo appears more than once
    placed, labels = [], []
    for i in picks:
        row = objects.iloc[i]
        photo = Image.open(row["path"]).convert("RGB")
        size = min(rng.randint(min_size, max_size), canvas) # Longest side of the pasted object
        scale = size / max(photo.size)
        w, h = round(photo.width * scale), round(photo.height * scale)
        box = place_box(w, h, canvas, placed, rng)
        if box is None:
            continue # No room left to fit the particular object, so move on
        scene.paste(photo.resize((w, h)), box[:2])
        placed.append(box)
        labels.append((int(row["yolo_class"]), box))
    return scene, labels

def yolo_lines(labels, canvas = config.canvas):
    """Labels as YOLO text lines: class x_center, y_center, width, and height all scaled from [0,1]"""
    lines = []
    for cls, (x1, y1, x2, y2) in labels:
        cx = (x1 + x2) / 2 / canvas
        cy = (y1 + y2) / 2 / canvas
        w = (x2 - x1) / canvas
        h = (y2 - y1) / canvas
        lines.append(f"{cls} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}")
    return lines           