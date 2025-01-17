import torch
import cv2
import os
from pathlib import Path


def load_yolo_model():
    model_path="/Users/rovitsanthapa/Documents/GitHub/FinalProject/yolov5/runs/train/exp18/weights/best.pt"
    # Load YOLOv5 model
    return torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, trust_repo='check')
    #return torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True, trust_repo='check')



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

        # Convert frame to RGB for YOLO
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Run YOLO model on the frame
        results = model(frame_rgb)

        # Extract bounding box data
        detections = results.pred[0].cpu().numpy()  # Convert to NumPy for easier processing
        for det in detections:
            x1, y1, x2, y2, conf, class_id = det
            class_name = model.names[int(class_id)]  # Get class name from model
            print(f"Frame {frame_count}: Class={class_name}, Confidence={conf:.2f}, "
                  f"BBox=({x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f})")

        # Render results on the frame
        annotated_frame = results.render()[0]

        # Write the annotated frame to the output video
        out.write(annotated_frame)

        # Extract frames to images
        save_frame(frame, output_dir, frame_count)

        # Optionally display the frame
        cv2.imshow('YOLOv5 Detection', annotated_frame)
        frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print(f"Processed video saved at: {out_video_path}")
    print(f"Extracted {frame_count} frames to {output_dir}")

def save_frame(frame, output_dir, frame_count):

    frame_path = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")
    cv2.imwrite(frame_path, frame)


if __name__ == "__main__":
    # Set the video file path
    #first path is for windows pc
    #video_path = "C:/Users/rocke/OneDrive/Desktop/uni/Cristiano Ronaldo's incredible free-kick for Manchester United against Portsmouth.mp4"
    #output_dir = Path("C:/Users/rocke/OneDrive/Desktop/uni/output")
    #second path is for mac pc
    video_path = "/Users/rovitsanthapa/Desktop/university /year 3/Comp 6013 Computing Project/testVideo/video2.mov"
    output_dir = Path("/Users/rovitsanthapa/Desktop/university /year 3/Comp 6013 Computing Project/testOutput")


    yolo_model = load_yolo_model()

    class_names= ['goalPost', 'Person', 'sports ball', 'ballMark']

    # Process video
    process_video(video_path, output_dir, yolo_model)


    #python train.py --img 1280 --batch 16 --epochs 50 --data /Users/rovitsanthapa/Documents/GitHub/FinalProject/training.yml --weights yolov5s.pt

    #python train.py --img 1280--batch 16 --epochs 100 --data /Users/rovitsanthapa/Documents/GitHub/FinalProject/training.yml --weights yolov5s.pt


