import json
import numpy as np
import cv2
import os
import setuptools.dist
from pathlib import Path
from ultralytics import YOLO
import torch

from PIL import Image, ExifTags


def load_yolo_model():
    """Load YOLOv8 model with custom weights."""
    #model_path = r"C:\Users\rocke\OneDrive\Desktop\uni\comp 6032 AI\FinalProject\yolov8_models\yolov8l-pose.pt"

    model_path = r"C:\Users\rocke\OneDrive\Desktop\uni\comp 6032 AI\FinalProject\runs\pose\train2\weights\best.pt"
    # Path to trained model

    # Uncomment the following line to use the default YOLOv8 model
    #return YOLO("/Users/rovitsanthapa/Documents/GitHub/FinalProject/yolov8n-pose.pt")
    return YOLO(model_path)


def process_video(video_path, output_dir, model):
    """Process a video and save the output with YOLO detections."""
    # Ensure the output directory exists
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    original_rotation = cap.get(cv2.CAP_PROP_ORIENTATION_META)
    print("Video Rotation:", original_rotation)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Debugging frame dimensions
    print(f"Frame width: {frame_width}, Frame height: {frame_height}, FPS: {fps}")

    all_keyPoints = []

    # Provide default frame size if invalid
    if frame_width == 0 or frame_height == 0:
        #frame_width, frame_height = 1440, 2560   # Default frame size
        frame_width, frame_height = 600, 600

        # Setup video writer for annotated output
    out_video_path = str(output_dir / "output_video.avi")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(out_video_path, fourcc, fps, (frame_width, frame_height))

    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if original_rotation == 90:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        # Run YOLOv8 Pose model on the frame
        results = model(frame)

        frame_keyPoints = []

        # Extract keypoints from detections
        for detection in results:
            if hasattr(detection, 'keypoints') and detection.keypoints is not None:

                keypoints = detection.keypoints.numpy()  # Convert keypoints to NumPy
                frame_keyPoints.append(keypoints)
                print(f"Frame {frame_count}: Keypoints: {keypoints}")
            else:
                print(f"Frame {frame_count}: No keypoints detected.")

        all_keyPoints.append({"frame": frame_count, "keypoints": frame_keyPoints})
        # Annotate frame with pose landmarks
        annotated_frame = results[0].plot()

        # Write the annotated frame to the output video
        out.write(annotated_frame)

        # **Save the frame to the output directory**
        save_frame(annotated_frame, output_dir, frame_count)  # <-- Call this function

        # Optionally display the frame
        cv2.imshow('YOLOv8 Pose Detection', annotated_frame)
        frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    save_keyPoint_data(all_keyPoints, r"C:\Users\rocke\OneDrive\Desktop\uni\comp 6032 AI\FinalProject\data\runs")

    print(f"Processed video saved at: {out_video_path}")


def save_frame(frame, output_dir, frame_count):
    """Save individual frames to the output directory."""
    frame_path = os.path.join(output_dir, f"frame_{frame_count:06d}.jpg")
    cv2.imwrite(frame_path, frame)


if __name__ == "__main__":
    # Set the video file path
    video_path = r"C:\Users\rocke\OneDrive\Desktop\uni\comp 6032 AI\FinalProject\data\videos\video4.mov"
    output_dir = Path(r"C:\Users\rocke\OneDrive\Desktop\uni\comp 6032 AI\FinalProject\output")

    # Load YOLOv8 Pose model
    yolo_model = load_yolo_model()

    # Process video using YOLOv8 Pose
    process_video(video_path, output_dir, yolo_model)


# yolo pose train data=training.yml model=yolov8m-pose.pt epochs=200 imgsz=960 batch=8
#yolo train pose data="C:\Users\rocke\OneDrive\Desktop\uni\comp 6032 AI\FinalProject\training.yml" model="C:\Users\rocke\OneDrive\Desktop\uni\comp 6032 AI\FinalProject\yolov8_models\yolov8l-pose.pt" epochs=100 imgsz=960 device=0


def save_keyPoint_data(keyPoint_data, save_dir):
    os.makedirs(save_dir, exist_ok=True)

    run_number = 1
    while os.path.exists(os.path.join(save_dir, f"run_{run_number}.json")):
        run_number += 1

    file_path = os.path.join(save_dir, f"run_{run_number}.json")
    with open(file_path, "w") as f:
        json.dump(run_number, f, indent=4)

    print(f"Keypoints data Saved to {file_path}")

#python train.py --img 1280 --batch 16 --epochs 50 --data /Users/rovitsanthapa/Documents/GitHub/FinalProject/training.yml --weights yolov5s.pt

#python train.py --img 1280--batch 16 --epochs 100 --data /Users/rovitsanthapa/Documents/GitHub/FinalProject/training.yml --weights yolov5s.pt
