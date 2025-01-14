import torch
import cv2
import os
from pathlib import Path

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True, trust_repo='check')

#python train.py --img 640 --batch 16 --epochs 50 --data /Users/rovitsanthapa/Documents/GitHub/FinalProject/training.yml --weights yolov5s.pt

#python train.py --img 640 --batch 16 --epochs 100 --data /Users/rovitsanthapa/Documents/GitHub/FinalProject/training.yml --weights yolov5s.pt


# Set the video file path
#first path is for windows pc
#video_path = "C:/Users/rocke/OneDrive/Desktop/uni/Cristiano Ronaldo's incredible free-kick for Manchester United against Portsmouth.mp4"
#output_dir = Path("C:/Users/rocke/OneDrive/Desktop/uni/output")
#second path is for mac pc
video_path = "/Users/rovitsanthapa/Desktop/university /year 3/Comp 6013 Computing Project/testVideo/video1.mov"
output_dir = Path("/Users/rovitsanthapa/Desktop/university /year 3/Comp 6013 Computing Project/testOutput")



output_dir.mkdir(parents=True, exist_ok=True)

# Open video
cap = cv2.VideoCapture(video_path)
frame_count= 0
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Video writer to save results
out_video_path = str(output_dir / "output_video.avi")
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(out_video_path, fourcc, fps, (frame_width, frame_height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to RGB (YOLO expects RGB)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Run YOLO on frame
    results = model(frame_rgb)

    # Draw results on the frame
    annotated_frame = results.render()[0]  # Render results on the frame

    # Write frame to output video
    out.write(annotated_frame)

    # Optionally, display frame
    cv2.imshow('YOLOv5 Detection', annotated_frame)
    frame_path = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")
    cv2.imwrite(frame_path, frame)  # Save the frame as an image
    frame_count += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
print(f"Extracted {frame_count} frames to {output_dir}")
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"Processed video saved at: {out_video_path}")


if __name__ == "__main__":
    video_path
    output_dir


    yoloModel =load_yolo_model()



def load_yolo_model()

