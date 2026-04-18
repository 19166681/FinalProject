import cv2
import argparse
import json
import os
from collections import defaultdict
from pathlib import Path
import numpy as np
from tqdm import tqdm






# Number of keypoints (adjust based on your dataset)
numOfKpts = 2
kptsInfo = numOfKpts * 3


# Paths
COCO_JSON_FILE = r"C:\Users\rocke\Downloads\task_treadmill_annotations_2025_03_20_15_42_10_coco keypoints 1.0\annotations\person_keypoints_default.json"
YOLO_SAVE_DIR = r"C:\Users\rocke\OneDrive\Desktop\test data\train\labels"


def convert_bbox_to_yolo(size, box):
   """Convert bounding box format from COCO to YOLO."""
   dw = 1.0 / size[0]
   dh = 1.0 / size[1]
   x = box[0] + box[2] / 2.0
   y = box[1] + box[3] / 2.0
   w = box[2]
   h = box[3]
   return round(x * dw, 6), round(y * dh, 6), round(w * dw, 6), round(h * dh, 6)


def convert_keypoints2_list(keypoints, img_width, img_height):
   """Convert COCO keypoints to YOLO format."""
   xiaoshu = 10 ** 6
   arry_x = np.zeros([numOfKpts, 1])
   arry_y = np.zeros([numOfKpts, 1])
   arry_v = np.zeros([numOfKpts, 1])


   for i in range(numOfKpts):
       arry_x[i, 0] = int((keypoints[i * 3] / img_width) * xiaoshu) / xiaoshu
       arry_y[i, 0] = int((keypoints[i * 3 + 1] / img_height) * xiaoshu) / xiaoshu
       arry_v[i, 0] = keypoints[i * 3 + 2]


   list_1 = []
   for i in range(numOfKpts):
       list_1.append(float(arry_x[i, 0].item()))
       list_1.append(float(arry_y[i, 0].item()))
       list_1.append(float(arry_v[i, 0].item()))


   return list_1




def main(root_dir, json_file):
   """Convert COCO keypoint annotations to YOLO format."""


   # Load COCO JSON
   data = json.load(open(json_file, "r"))


   # Ensure necessary directories exist
   labels_dir = os.path.join(root_dir, "train")
   os.makedirs(labels_dir, exist_ok=True)


   # Save class names
   id_map = {}
   classes_txt = os.path.join(root_dir, "classes.txt")
   with open(classes_txt, "w") as f:
       for i, category in enumerate(data["categories"]):
           f.write(f"{category['name']}\n")
           id_map[category["id"]] = i


   images = {str(x["id"]): x for x in data["images"]}
   imgToAnns = defaultdict(list)
   for ann in data["annotations"]:
       imgToAnns[ann["image_id"]].append(ann)


   list_file = open(os.path.join(root_dir, "train.txt"), "w")


   # Process each image and its annotations
   for img_id, anns in tqdm(imgToAnns.items(), desc=f"Processing {json_file}"):
       img = images[str(img_id)]
       h, w, filename = img["height"], img["width"], img["file_name"]


       bboxes = []
       for ann in anns:
           # Convert bounding box
           box = np.array(ann["bbox"], dtype=np.float64)
           box[:2] += box[2:] / 2  # Convert top-left to center
           box[[0, 2]] /= w
           box[[1, 3]] /= h
           if box[2] <= 0 or box[3] <= 0:
               continue


           # Convert keypoints
           keypoints = ann["keypoints"]
           keypoints_list = convert_keypoints2_list(keypoints, w, h)


           # Assign class ID
           cls = id_map[ann["category_id"]]
           box = [cls] + box.tolist() + keypoints_list
           if box not in bboxes:
               bboxes.append(box)


       # Save labels in YOLO format
       txt_filename = os.path.join(labels_dir, f"{Path(filename).stem}.txt")
       with open(txt_filename, "w") as file:
           for i in range(len(bboxes)):
               line = (*(bboxes[i]),)
               file.write(("%g " * len(line)).rstrip() % line + "\n")


       list_file.write(f"./images/train/{filename}\n")


   list_file.close()
   print(f"\n✅ Conversion complete! Labels saved in: {labels_dir}")


def rename_all_yolo_labels(directory):
    """
    Renames all .txt files in the directory (except 'classes.txt') to a sequential format:
    frame_000000.txt, frame_000001.txt, ...
    """
    # Get only .txt files, excluding 'classes.txt'
    txt_files = [
        f for f in os.listdir(directory)
        if f.endswith(".txt") and f.lower() != "classes.txt"
    ]

    # Sort files by original name (just to keep consistent order)
    txt_files.sort()

    # Rename each file
    for i, old_name in enumerate(txt_files):
        new_name = f"frame_{i:06d}.txt"
        old_path = os.path.join(directory, old_name)
        new_path = os.path.join(directory, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed: {old_name} → {new_name}")


def rename_all_images(directory, image_extensions=(".jpg", ".jpeg", ".png","webp")):
    """
    Renames all image files in the directory to a sequential format:
    frame_000000.jpg, frame_000001.jpg, ...

    Supported image extensions are configurable.
    """
    # Get only image files with supported extensions
    image_files = [
        f for f in os.listdir(directory)
        if f.lower().endswith(image_extensions)
    ]

    # Sort files by name to keep order consistent
    image_files.sort()

    for i, old_name in enumerate(image_files):
        ext = os.path.splitext(old_name)[1].lower()  # preserve original extension
        new_name = f"frame_{i:06d}{ext}"
        old_path = os.path.join(directory, old_name)
        new_path = os.path.join(directory, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed: {old_name} → {new_name}")

if __name__ == "__main__":
   print("Parsing and creating directories...")
   print(f"Input JSON: {COCO_JSON_FILE}")
   print(f"Output YOLO labels: {YOLO_SAVE_DIR}")

   #rename_all_yolo_labels(r'C:\Users\rocke\OneDrive\Desktop\test data\train\labels\train')
   rename_all_images(r"C:\Users\rocke\Downloads\treadmill_images")
   #main(YOLO_SAVE_DIR, COCO_JSON_FILE)


