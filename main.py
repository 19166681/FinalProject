import cv2
import os
import setuptools.dist
from pathlib import Path
from ultralytics import YOLO
from distutils.version import LooseVersion
import json

# Load the JSON file
file_path = "/Users/rovitsanthapa/Downloads/annotations/person_keypoints_default.json"

with open(file_path, "r") as f:
    data = json.load(f)

# Keep only images with id ≤ 200
data["images"] = [img for img in data["images"] if img["id"] <= 200]

# Keep only annotations related to those images
valid_image_ids = {img["id"] for img in data["images"]}
if "annotations" in data:
    data["annotations"] = [ann for ann in data["annotations"] if ann["image_id"] in valid_image_ids]

# Save the modified JSON file
new_file_path = "/Users/rovitsanthapa/Downloads/annotationsperson_keypoints_trimmed.json"
with open(new_file_path, "w") as f:
    json.dump(data, f, indent=4)

new_file_path


def load_yolo_model():
    """Load YOLOv8 model with custom weights."""
    model_path = "/Users/rovitsanthapa/Documents/GitHub/FinalProject/runs/pose/train10/weights/best.pt"  # Path to trained model
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
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Debugging frame dimensions
    print(f"Frame width: {frame_width}, Frame height: {frame_height}, FPS: {fps}")

    # Provide default frame size if invalid
    if frame_width == 0 or frame_height == 0:
        frame_width, frame_height = 640, 480  # Default frame size

    # Setup video writer for annotated output
    out_video_path = str(output_dir / "output_video.avi")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(out_video_path, fourcc, fps, (frame_width, frame_height))

    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLOv8 Pose model on the frame
        results = model(frame)

        # Extract keypoints from detections
        for detection in results:
            if hasattr(detection, 'keypoints') and detection.keypoints is not None:
                keypoints = detection.keypoints.numpy()  # Convert keypoints to NumPy
                print(f"Frame {frame_count}: Keypoints: {keypoints}")
            else:
                print(f"Frame {frame_count}: No keypoints detected.")

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

    print(f"Processed video saved at: {out_video_path}")

def save_frame(frame, output_dir, frame_count):
    """Save individual frames to the output directory."""
    frame_path = os.path.join(output_dir, f"frame_{frame_count:06d}.jpg")
    cv2.imwrite(frame_path, frame)

if __name__ == "__main__":
    # Set the video file path
    video_path = "/Users/rovitsanthapa/Desktop/university /year 3/Comp 6013 Computing Project/testVideo/IMG_7635.MOV"
    output_dir = Path("/Users/rovitsanthapa/Desktop/university /year 3/Comp 6013 Computing Project/testOutput")

    # Load YOLOv8 Pose model
    yolo_model = load_yolo_model()

    # Process video using YOLOv8 Pose
    process_video(video_path, output_dir, yolo_model)

# yolo pose train data=training.yml model=yolov8m-pose.pt epochs=200 imgsz=960 batch=8




