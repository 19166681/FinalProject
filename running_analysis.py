import json
import os

import numpy as np


class RunningAnalysis:
   def __init__(self, runs_directory):

      self.runs_directory = runs_directory
      #the actual json running keypoint data for all the runs
      self.runs_data=self.load_runs()


   def load_runs(self):
      runs=[]
      for filename in sorted(os.listdir(self.runs_directory)):
        if filename.endswith('.json'):
           file_path = os.path.join(self.runs_directory, filename)
           with open(file_path, 'r') as file:
              data = json.load(file)
              runs.append(data)
      return runs

   def get_run(self,run_number):
      #get key points of the specifed number
      if 1<=run_number<= len(self.runs_data):
         return self.runs_data[run_number-1]
      else:
         print('Invalid run number')
         return None



   def get_all_keypoints(self):
      print("adadadadad")
      keypoints=[]
      for run in self.runs_data:
         for frame in run:
            keypoints.append(frame['keypoints'])
      return keypoints

   def print_keypoints(self):
      total_numOfRuns=len(self.runs_data)
      total_frames= sum(len(run) for run in self.runs_data)

      total_keypoints=0
      keypoints_per_frame=[]
      #loops through the WHAT gosh
      for run in self.runs_data:
         for frame in run:
            if 'keypoints' in frame:
               num_keypoints = len(frame['keypoints'])
               total_keypoints += num_keypoints
               keypoints_per_frame.append(num_keypoints)



      print(f"Total Runs:  {total_numOfRuns}")
      print(f"Total Frames Analyzed:  {total_frames}")
      print(f"Total Keypoints detected : {total_keypoints}")

      if self.runs_data:
         latest_run=self.runs_data[-1]
         print(f"agggghh")
         for i,frame in enumerate(latest_run):
            print(f'Frame {i+1} : {frame["keypoints"]}')

   def test_function(self):
       run_data = self.get_all_keypoints()

       rheel_coords = []  # (y, x, frame)
       lheel_coords = []  # (y, x, frame)

       for i, frame_keypoints in enumerate(run_data):
           if frame_keypoints:
               try:
                   rheel_x = frame_keypoints[0][0][12][0]
                   rheel_y = frame_keypoints[0][0][12][1]

                   lheel_x = frame_keypoints[0][0][13][0]
                   lheel_y = frame_keypoints[0][0][13][1]

                   rheel_coords.append((rheel_y, rheel_x, i))
                   lheel_coords.append((lheel_y, lheel_x, i))

               except IndexError:
                   print(f"Frame {i} is missing keypoints, skipping.")

       # Sort by Y value (index 0)
       rheel_coords.sort()
       lheel_coords.sort()

       top_5_lowest_rheel = rheel_coords[:5]
       top_5_highest_rheel = rheel_coords[-5:][::-1]

       top_5_lowest_lheel = lheel_coords[:5]
       top_5_highest_lheel = lheel_coords[-5:][::-1]

       print("\nTop 5 Lowest Y-values for Right Heel (Rheel):")
       for y, x, frame in top_5_lowest_rheel:
           print(f"Frame {frame} | X: {x} | Y: {y}")

       print("\nTop 5 Highest Y-values for Right Heel (Rheel):")
       for y, x, frame in top_5_highest_rheel:
           print(f"Frame {frame} | X: {x} | Y: {y}")

       print("\nTop 5 Lowest Y-values for Left Heel (Lheel):")
       for y, x, frame in top_5_lowest_lheel:
           print(f"Frame {frame} | X: {x} | Y: {y}")

       print("\nTop 5 Highest Y-values for Left Heel (Lheel):")
       for y, x, frame in top_5_highest_lheel:
           print(f"Frame {frame} | X: {x} | Y: {y}")

       # i and frame_keypoints are the varibhles that change in the for loop
       # i is just the varble that goes up by 1 for the index of the frames
       # frame_keypoints is the frames keypoints data duuuh so thier should be 15
       # frame_keypoints[0][0][x][z]
       # x is the keypoint so if i make x 15 it will give the 15th (left toe) keypoint data
       # z is the keypoint dat so 0 will be the x coord, 1 will be the y coord , 2 wil be the confidence score

    #def finding_baseLine(self):

   def print_all_heel_y_values(self):
       run_data = self.get_all_keypoints()

       print("\nY-values for Right Heel (keypoint 12) and Left Heel (keypoint 13):\n")

       for i, frame_keypoints in enumerate(run_data):
           if frame_keypoints and len(frame_keypoints[0][0]) >= 14:
               try:
                   rheel_y = frame_keypoints[0][0][12][1]  # Right heel Y
                   lheel_y = frame_keypoints[0][0][13][1]  # Left heel Y
                   print(f"Frame {i + 1}: Rheel_Y = {rheel_y:.4f}, Lheel_Y = {lheel_y:.4f}")
               except IndexError:
                   print(f"Frame {i + 1}: Keypoint missing, skipping.")
           else:
               print(f"Frame {i + 1}: Invalid or incomplete keypoint data.")

   #gets the lowest values of y and its corresponding x values then gets
   # mean of x value to find treadmill belt middle for the Lheel
   def get_treadmill_baseLine_forLheel(self):
       run_data = self.get_all_keypoints()
       lheel_points = []  # Stores tuples of (y, x, frame_index)

       # Loop through each frame's keypoints
       for i, frame_keypoints in enumerate(run_data):
           try:
               # Index 13 corresponds to the Left Heel (Lheel)
               lheel = frame_keypoints[0][0][13]
               x, y = lheel[0], lheel[1]  # Extract x and y coordinates
               lheel_points.append((y, x, i))  # Store as (y, x, frame number)
           except (IndexError, TypeError):
               print(f"Frame {i} missing Lheel keypoint, skipping.")

       # Sorts by Y ascending  (lowest Y first = highest up on the screen)
       lheel_points.sort()

       # Take the lowest 10 Y-values and get their corresponding X and Y values
       lowest_10 = lheel_points[:10]
       x_values = [x for _, x, _ in lowest_10]
       y_values = [y for y, _, _ in lowest_10]

       if x_values and y_values:
           mean_x = sum(x_values) / len(x_values)  # Mean of X values
           mean_y = sum(y_values) / len(y_values)  # Mean of Y values

           # Print the 10 lowest points and their coordinates
           print("\nLowest 10 Lheel Y-values with corresponding X-values:")
           for y, x, frame in lowest_10:
               print(f"Frame {frame}: Y = {y:.2f}, X = {x:.2f}")

           # Output the means
           print(f"\n➡️ Mean X-value of lowest 10 Lheel Y-values: {mean_x:.2f}")
           print(f"➡️ Mean Y-value of lowest 10 Lheel Y-values: {mean_y:.2f}")
       else:
           print("No valid Lheel data found.")

   def get_treadmill_baseLine_forRheel(self):
       run_data = self.get_all_keypoints()
       rheel_points = []

       for i, frame_keypoints in enumerate(run_data):
           try:
               rheel = frame_keypoints[0][0][12]
               x, y = rheel[0], rheel[1]
               rheel_points.append((y, x, i))
           except (IndexError, TypeError):
               print(f"Frame {i} missing Rheel keypoint, skipping.")

       rheel_points.sort()
       lowest_10 = rheel_points[:10]
       x_values = [x for _, x, _ in lowest_10]
       y_values = [y for y, _, _ in lowest_10]

       if x_values and y_values:
           mean_x = sum(x_values) / len(x_values)
           mean_y = sum(y_values) / len(y_values)

           print("\nLowest 10 Rheel Y-values with corresponding X-values:")
           for y, x, frame in lowest_10:
               print(f"Frame {frame}: Y = {y:.2f}, X = {x:.2f}")

           print(f"\n➡️ Mean X-value of lowest 10 Rheel Y-values: {mean_x:.2f}")
           print(f"➡️ Mean Y-value of lowest 10 Rheel Y-values: {mean_y:.2f}")
       else:
           print("No valid Rheel data found.")

   def get_footStrike(self):
       #calls the base line funtions first then  after y valuys reaches
       #base line  it gets the y values of next 5 frames of the toes (YOMMY) and the heels
       # and compares it
       # coord works by (0,0) being top left and the more right yiu go x increases
       # when u go down y increase
       # so lets say the mean y values of the toes is higher than the heels means front foot striker
       # if lower heel striker
       # if around the same neutral foot striker
       run_data = self.get_all_keypoints()
       lheel_baseline_x, lheel_baseline_y = self.get_treadmill_baseLine_forLheel()
       rheel_baseline_x, rheel_baseline_y = self.get_treadmill_baseLine_forRheel()



       tolerance_ratio = 0.05
       tolerance_y_L = lheel_baseline_y * tolerance_ratio
       tolerance_y_R = rheel_baseline_y * tolerance_ratio

       release_offset = 0.09

       in_contact_L = False
       in_contact_R = False


       # gets the contact frame and goes back 2 frames and gets the 5 ahead of it
       for i in range(2, len(run_data) - 2):
           try:
               frame = run_data[i][0][0]
               lheel_y = frame[self.KEYPOINT_LEFT_HEEL][1]
               rheel_y = frame[self.KEYPOINT_RIGHT_HEEL][1]

               lheel_touch = abs(lheel_y - (lheel_baseline_y + 10)) < tolerance_y_L
               rheel_touch = abs(rheel_y - (rheel_baseline_y + 10)) < tolerance_y_R

               # LEFT FOOT CONTACT
               if lheel_touch and not in_contact_L:
                   in_contact_L = True
                   print(f"\n Left Foot Contact Detected at Frame {i}")
                   self.left_contact_frames.append(i+2)
                   heel_y_vals = []
                   toe_y_vals = []

                   for j in range(i - 2, i + 3):
                       future_frame = run_data[j][0][0]
                       heel_y_vals.append(future_frame[self.KEYPOINT_LEFT_HEEL][1])
                       toe_y_vals.append(future_frame[self.KEYPOINT_LEFT_TOE][1])

                   mean_heel_y = sum(heel_y_vals) / len(heel_y_vals)
                   mean_toe_y = sum(toe_y_vals) / len(toe_y_vals)

                   print(f"  LHeel Y-avg: {mean_heel_y:.2f}, LToe Y-avg: {mean_toe_y:.2f}")
                   if mean_toe_y > mean_heel_y + 75:
                       print("  Strike Type: Frontfoot strike")
                   elif mean_heel_y > mean_toe_y:
                       print("  Strike Type: Heel strike")
                   else:
                       print("  Strike Type: Neutral strike")

               # RIGHT FOOT CONTACT
               if rheel_touch and not in_contact_R:
                   in_contact_R = True
                   print(f"\n Right Foot Contact Detected at Frame {i}")
                   self.right_contact_frames.append(i+2)
                   heel_y_vals = []
                   toe_y_vals = []

                   for j in range(i - 2, i + 3):
                       future_frame = run_data[j][0][0]
                       heel_y_vals.append(future_frame[self.KEYPOINT_RIGHT_HEEL][1])
                       toe_y_vals.append(future_frame[self.KEYPOINT_RIGHT_TOE][1])

                   mean_heel_y = sum(heel_y_vals) / len(heel_y_vals)
                   mean_toe_y = sum(toe_y_vals) / len(toe_y_vals)

                   print(f"  RHeel Y-avg: {mean_heel_y:.2f}, RToe Y-avg: {mean_toe_y:.2f}")
                   if mean_toe_y > mean_heel_y + 75:
                       print("Strike Type: Frontfoot strike")
                   elif mean_heel_y > mean_toe_y:
                       print(" Strike Type: Heel strike")
                   else:
                       print(" Strike Type: Neutral strike")

               # Reset contact when heel lifts again
               if in_contact_L and lheel_y < lheel_baseline_y - (lheel_baseline_y * release_offset):
                   in_contact_L = False

               if in_contact_R and rheel_y < rheel_baseline_y - (rheel_baseline_y * release_offset):
                   in_contact_R = False

           except (IndexError, TypeError):
               continue

 def correctPosture(self):
       run_data = self.get_all_keypoints()
       print("\ngetting  Posture ")
       #works by creating a line from the shoulder, hip and the middle of the knees
       # then checks if the angle is greater than 150 too see if good posture


if __name__ == "__main__":
   runs_folder=r"C:\Users\rocke\OneDrive\Desktop\uni\comp 6032 AI\FinalProject\data\runs"
   analysis=RunningAnalysis(runs_folder)
   analysis.get_all_keypoints()
   analysis.print_all_heel_y_values()
   analysis.test_function()
   analysis.get_treadmill_baseLine_forLheel()
   analysis.get_treadmill_baseLine_forRheel()
   #analysis.print_keypoints()




'''
 1 - 1
 2 - shoulder
 3 - L_elbow
 4 - R_elbow
 5 - L_wrist
 6 - R_wrist
 7 - Hip
 8 - R_knee
 9 - L_knee
 10 - R_ankle
 11 - L_ankle
 12 - R_heel
 13 - L_heel
 14- R_toe
 15- L_toe

'''

