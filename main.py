import json
import numpy as np
import cv2
import os
import setuptools.dist
from pathlib import Path
from ultralytics import YOLO
import torch
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from running_analysis import RunningAnalysis












def load_yolo_model():
   """Load YOLOv8 model with custom weights."""
   #model_path = r"C:\Users\rocke\OneDrive\Desktop\uni\comp 6032 AI\FinalProject\yolov8_models\yolov8l-pose.pt"

   model_path = r"best.pt"
 # Path to trained model

   # Uncomment the following line to use the default YOLOv8 model
   #return YOLO("/Users/rovitsanthapa/Documents/GitHub/FinalProject/yolov8n-pose.pt")
   return YOLO(model_path)


def save_keyPoint_data(keypoint_data,save_dir):
    os.makedirs(save_dir,exist_ok=True)

    run_number=1
    while os.path.exists(os.path.join(save_dir,f"run_{run_number}.json")):
        run_number+=1

    file_path =os.path.join(save_dir,f"run_{run_number}.json")
    with open(file_path, "w") as f:
        json.dump(keypoint_data,f, indent=4)

    print(f"Keypoints data Saved to {file_path}")





def process_video(video_path, output_dir, model):
   # Ensure the output directory exists
   output_dir = Path(output_dir)
   output_dir.mkdir(parents=True, exist_ok=True)


   # Open the video file
   cap = cv2.VideoCapture(video_path)
   original_rotation=cap.get(cv2.CAP_PROP_ORIENTATION_META)
   print("Video Rotation:",original_rotation)
   frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
   frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
   fps = int(cap.get(cv2.CAP_PROP_FPS))

   # Debugging frame dimensions
   #print(f"Frame width: {frame_width}, Frame height: {frame_height}, FPS: {fps}")


   # Provide default frame size if invalid
   if frame_width == 0 or frame_height == 0:
       #frame_width, frame_height = 1440, 2560
       frame_width, frame_height = 600, 600

       # Setup video writer for annotated output
   out_video_path = str(output_dir / "output_video.avi")
   fourcc = cv2.VideoWriter_fourcc(*'XVID')
   out = cv2.VideoWriter(out_video_path, fourcc, fps, (frame_width, frame_height))

   frame_count = 0
   all_keyPoints =[]

   while cap.isOpened():
       ret, frame = cap.read()
       if not ret:
           break
       if original_rotation ==90:
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
       # Run YOLOv8 Pose model on the frame
       results = model(frame)
       frame_keyPoints=[]

       # get keypoints from detections
       for detection in results:
           if hasattr(detection, 'keypoints') and detection.keypoints is not None:
               keypoints = detection.keypoints.data.cpu().numpy().tolist()  # Convert keypoints to NumPy

               frame_keyPoints.append(keypoints )
               print(f"Frame {frame_count}: Keypoints: {keypoints}")
           else:
               print(f"Frame {frame_count}: No keypoints detected.")

       all_keyPoints.append({"frame": frame_count, "keypoints": frame_keyPoints})
       # Annotate frame with pose landmarks
       annotated_frame = results[0].plot()

       # Write the annotated frame to the output video
       out.write(annotated_frame)

       # **Save the frame to the output directory**
       save_frame(annotated_frame, output_dir, frame_count)

       cv2.imshow('YOLOv8 Pose Detection', annotated_frame)
       frame_count += 1


       if cv2.waitKey(1) & 0xFF == ord('q'):
           break




   cap.release()
   out.release()
   cv2.destroyAllWindows()

   save_dir = r"data/runs"
   for filename in os.listdir(save_dir):
       file_path = os.path.join(save_dir, filename)
       if os.path.isfile(file_path):
           os.remove(file_path)


   save_keyPoint_data(all_keyPoints,save_dir)
   print(f"Processed video saved at: {out_video_path}")


def save_frame(frame, output_dir, frame_count):

   frame_path = os.path.join(output_dir, f"frame_{frame_count:06d}.jpg")
   cv2.imwrite(frame_path, frame)



def runUI():
    def select_video():
        video_path = filedialog.askopenfilename(
            title="Select a Video File",
            filetypes=[("Video Files", "*.mp4 *.avi *.mov")]
        )
        if not video_path:
            return

        output_dir = os.path.join(os.getcwd(), "data", "runs")
        model = load_yolo_model()

        process_video(video_path, output_dir, model)

        analysis = RunningAnalysis(output_dir)
        analysis.get_footStrike()
        analysis.getFootLanding()
        analysis.getPosture()
        analysis.getArmForm()
        totalFrames = analysis.total_frames
        goodPosturePercentage =1-(analysis.bad_posture_counter['counter'] / totalFrames)
        goodArmFormPercentage =1 - (analysis.bad_arm_form_counter['counter'] / totalFrames)
        goodFootLandingPercentage= 1 -(analysis.bad_landing_counter['counter'] / totalFrames)
        goodFootStrikePercentage = 1-(analysis.footstrike_counter['heelStrike'] / totalFrames)
        posture_msg = "Good posture maintained!" if goodPosturePercentage >= 0.75 else "You have bad posture in your run"
        arm_msg = " Yourr Arm form looks good!" if goodArmFormPercentage >= 0.75 else "Your arm form needs improvement"
        landing_msg = "Foot landing alignment looks good!" if goodFootLandingPercentage >= 0.75 else "Your foot is not landing under your hips"

        if goodFootStrikePercentage >= 0.75:
            front = analysis.footstrike_counter['frontFootStrike']
            neutral = analysis.footstrike_counter['neutralStrike']
            if front > neutral:
                footstrike_msg = "You are a forefoot striker"
            elif neutral > front:
                footstrike_msg = "You are a neutral striker"
            else:
                footstrike_msg = "You are a heel striker"
        else:
            footstrike_msg = "Your foot strike pattern needs improvement."
        summary = (
            f"\nYour posture score: {goodPosturePercentage*100}%"
            f"\nPosture Issues: {analysis.bad_posture_counter['counter']} frames (number of frames with bad posture )"
            f"\nYour arm form score: {goodArmFormPercentage*100}%"
            f"\nArm Form Issues: {analysis.bad_arm_form_counter['counter']} frames (number of frames with bad arm form )"
            f"\nYour for landing score: {goodFootLandingPercentage*100}%"
            f"\nLanding Issues: {analysis.bad_landing_counter['counter']} frames (number of frames with foot landing )"
            f"\nyour foot strike score: {goodFootStrikePercentage*100}% "
            f"\nFoot Strikes - Heel: {analysis.footstrike_counter['heelStrike']} | "
            f"Forefoot: {analysis.footstrike_counter['frontFootStrike']} | "
            f"Neutral: {analysis.footstrike_counter['neutralStrike']}\n\n"
            f"{posture_msg}\n{arm_msg}\n{landing_msg}\n{footstrike_msg}"
        )

        messagebox.showinfo("Analysis Complete", f"Video has been processed and analyzed.\n{summary}")


    # the gui window
    root = tk.Tk()
    root.title("Running Form Analyzer")
    root.geometry("600x400")

    label = tk.Label(root, text="Select a video to analyze running form", font=("Arial", 12))
    label.pack(pady=20)
    button = tk.Button(root, text="Select Video", command=select_video, font=("Arial", 12), bg="lightblue")
    button.pack(pady=10)

    root.mainloop()



if __name__ == "__main__":
   runUI()




   # Set the video file path
   #video_path = r"C:\Users\rocke\OneDrive\Desktop\uni\comp 6032 AI\FinalProject\data\videos\video1.mov"
   #output_dir = Path(r"C:\Users\rocke\OneDrive\Desktop\uni\comp 6032 AI\FinalProject\output")

   # Load YOLOv8 Pose model
   #yolo_model = load_yolo_model()


   # Process video using YOLOv8 Pose
   #process_video(video_path, output_dir, yolo_model)



# yolo pose train data=training.yml model=yolov8m-pose.pt epochs=200 imgsz=960 batch=8
#yolo train pose data="C:\Users\rocke\OneDrive\Desktop\uni\comp 6032 AI\FinalProject\training.yml" model="C:\Users\rocke\OneDrive\Desktop\uni\comp 6032 AI\FinalProject\yolov8_models\yolov8l-pose.pt" epochs=100 imgsz=960 device=0
#yolo train pose data="C:\Users\rocke\OneDrive\Desktop\uni\comp 6032 AI\FinalProject\trainingTreadmil.yml" model="C:\Users\rocke\OneDrive\Desktop\uni\comp 6032 AI\FinalProject\yolov8_models\yolov8l-pose.pt" epochs=50 imgsz=960 device=0




#python train.py --img 1280 --batch 16 --epochs 50 --data /Users/rovitsanthapa/Documents/GitHub/FinalProject/training.yml --weights yolov5s.pt

#python train.py --img 1280--batch 16 --epochs 100 --data /Users/rovitsanthapa/Documents/GitHub/FinalProject/training.yml --weights yolov5s.pt



