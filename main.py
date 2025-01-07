import torch
import cv2
from pathlib import Path

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Set the video file path
video_path = "C:/Users/rocke/OneDrive/Desktop/uni/Cristiano Ronaldo's incredible free-kick for Manchester United against Portsmouth.mp4"
output_dir = Path("C:/Users/rocke/OneDrive/Desktop/uni/output")
output_dir.mkdir(parents=True, exist_ok=True)

# Open video
cap = cv2.VideoCapture(video_path)
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
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

print(f"Processed video saved at: {out_video_path}")
