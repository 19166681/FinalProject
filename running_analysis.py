import json
import os
import math
import numpy as np


class RunningAnalysis:
   def __init__(self, runs_directory):

      self.runs_directory = runs_directory
      #the actual json running keypoint data for all the runs
      self.runs_data=self.load_runs()

      self.left_contact_frames = []
      self.right_contact_frames = []
      self.KEYPOINT_FOREHEAD = 0
      self.KEYPOINT_SHOULDER = 1
      self.KEYPOINT_LEFT_ELBOW = 2
      self.KEYPOINT_RIGHT_ELBOW = 3
      self.KEYPOINT_LEFT_WRIST = 4
      self.KEYPOINT_RIGHT_WRIST = 5
      self.KEYPOINT_HIP = 6
      self.KEYPOINT_RIGHT_KNEE = 7
      self.KEYPOINT_LEFT_KNEE = 8
      self.KEYPOINT_RIGHT_ANKLE = 9
      self.KEYPOINT_LEFT_ANKLE = 10
      self.KEYPOINT_RIGHT_HEEL = 11
      self.KEYPOINT_LEFT_HEEL = 12
      self.KEYPOINT_RIGHT_TOE = 13
      self.KEYPOINT_LEFT_TOE = 14





      self.bad_posture_counter = {"counter": 0, "frames": []}
      self.bad_arm_form_counter = {"counter": 0, "frames": []}
      self.footstrike_counter = {
          "frontFootStrike": 0,
          "neutralStrike": 0,
          "heelStrike": 0,
          "frames": []}
      self.bad_landing_counter = {"counter": 0, "frames": []}
      self.total_frames =0
      self.keypoints=[]
      for run in self.runs_data:
         for frame in run:
            self.keypoints.append(frame['keypoints'])
            self.total_frames += 1





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
       run_data = self.keypoints

       rheel_coords = []  # (y, x, frame)
       lheel_coords = []  # (y, x, frame)

       for i, frame_keypoints in enumerate(run_data):
           if frame_keypoints:
               try:
                   rheel_x = frame_keypoints[0][0][11][0]
                   rheel_y = frame_keypoints[0][0][11][1]

                   lheel_x = frame_keypoints[0][0][12][0]
                   lheel_y = frame_keypoints[0][0][12][1]

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
       run_data = self.keypoints

       print("\nY-values for Right Heel (keypoint 12) and Left Heel (keypoint 13):\n")

       for i, frame_keypoints in enumerate(run_data):
           if frame_keypoints and len(frame_keypoints[0][0]) >= 14:
               try:
                   rheel_y = frame_keypoints[0][0][11][1]  # Right heel Y
                   lheel_y = frame_keypoints[0][0][12][1]  # Left heel Y
                   print(f"Frame {i + 1}: Rheel_Y = {rheel_y:.4f}, Lheel_Y = {lheel_y:.4f}")
               except IndexError:
                   print(f"Frame {i + 1}: Keypoint missing, skipping.")
           else:
               print(f"Frame {i + 1}: Invalid or incomplete keypoint data.")

   #gets the lowest values of y and its corresponding x values then gets
   # mean of x value to find treadmill belt middle for the Lheel
   def get_treadmill_baseLine_forLheel(self):
       run_data = self.keypoints
       lheel_points = []  # Stores tuples of (y, x, frame_index)

       # Loop through each frame's keypoints
       for i, frame_keypoints in enumerate(run_data):
           try:
               # Index 13 corresponds to the Left Heel (Lheel)
               lheel = frame_keypoints[0][0][12]
               x, y = lheel[0], lheel[1]  # Extract x and y coordinates
               lheel_points.append((y, x, i))  # Store as (y, x, frame number)
           except (IndexError, TypeError):
               print(f"Frame {i} missing Lheel keypoint, skipping.")

       # Sorts by Y ascending  (higest Y first = lower up on the screen)
       lheel_points.sort(reverse=True)

       # Take the higest 10 Y-values and get their corresponding X and Y values
       highest_10 = lheel_points[:10]
       x_values = [x for _, x, _ in highest_10]
       y_values = [y for y, _, _ in highest_10]

       if x_values and y_values:
           mean_x = sum(x_values) / len(x_values)  # Mean of X values
           mean_y = sum(y_values) / len(y_values)  # Mean of Y values

           # Prints the 10 lowest points and their coordinates
           print("\nhighest 10 Lheel Y-values with corresponding X-values:")
           for y, x, frame in highest_10:
               #print(f"Frame {frame}: Y = {y:.2f}, X = {x:.2f}")
               i=0
           # Output the means
           print(f"\n➡️ Mean X-value of highest 10 Lheel Y-values: {mean_x:.2f}")
           print(f"➡️ Mean Y-value of highest 10 Lheel Y-values: {mean_y:.2f}")
           return mean_x, mean_y
       else:
           print("No valid Lheel data found.")
           return None, None

   def get_treadmill_baseLine_forRheel(self):
       run_data = self.keypoints
       rheel_points = []

       for i, frame_keypoints in enumerate(run_data):
           try:
               rheel = frame_keypoints[0][0][11]
               x, y = rheel[0], rheel[1]
               rheel_points.append((y, x, i))
           except (IndexError, TypeError):
               print(f"Frame {i} missing Rheel keypoint, skipping.")
       rheel_points.sort(reverse=True)
       highest_10 = rheel_points[:10]
       x_values = [x for _, x, _ in highest_10]
       y_values = [y for y, _, _ in highest_10]

       if x_values and y_values:
           mean_x = sum(x_values) / len(x_values)
           mean_y = sum(y_values) / len(y_values)

           print("\nhighest 10 Rheel Y-values with corresponding X-values:")
           for y, x, frame in highest_10:
            #print(f"Frame {frame}: Y = {y:.2f}, X = {x:.2f}")
            i=0
           print(f"\n➡️ Mean X-value of higehst 10 Rheel Y-values: {mean_x:.2f}")
           print(f"➡️ Mean Y-value of higehst 10 Rheel Y-values: {mean_y:.2f}")
           return mean_x, mean_y
       else:
           print("No valid Rheel data found.")
           return None, None



   def get_footStrike(self):
       #calls the base line funtions first then  after y valuys reaches
       #base line  it gets the y values of next 5 frames of the toes (YOMMY) and the heels
       # and compares it
       # coord works by (0,0) being top left and the more right yiu go x increases
       # when u go down y increase
       # so lets say the mean y values of the toes is higher than the heels means front foot striker
       # if lower heel striker
       # if around the same neutral foot striker
       run_data = self.keypoints
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
                       self.footstrike_counter["frontFootStrike"] += 1
                       self.footstrike_counter["frames"].append(i)
                   elif mean_heel_y > mean_toe_y:
                       print("  Strike Type: Heel strike")
                       self.footstrike_counter["heelStrike"] += 1
                       self.footstrike_counter["frames"].append(i)
                   else:
                       print("  Strike Type: Neutral strike")
                       self.footstrike_counter["neutralStrike"] += 1
                       self.footstrike_counter["frames"].append(i)

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
                       print("  Strike Type: Frontfoot strike")
                       self.footstrike_counter["frontFootStrike"] += 1
                       self.footstrike_counter["frames"].append(i)
                   elif mean_heel_y > mean_toe_y:
                       print("  Strike Type: Heel strike")
                       self.footstrike_counter["heelStrike"] += 1
                       self.footstrike_counter["frames"].append(i)
                   else:
                       print("  Strike Type: Neutral strike")
                       self.footstrike_counter["neutralStrike"] += 1
                       self.footstrike_counter["frames"].append(i)

               # Reset contact when heel lifts again
               if in_contact_L and lheel_y < lheel_baseline_y - (lheel_baseline_y * release_offset):
                   in_contact_L = False

               if in_contact_R and rheel_y < rheel_baseline_y - (rheel_baseline_y * release_offset):
                   in_contact_R = False

           except (IndexError, TypeError):
               continue



   def getPosture(self):
       run_data = self.keypoints
       print("\ngetting  Posture ")
       #works by creating a vector from the shoulder, hip and the middle of the knees
       # then checks if the angle is greater than 150 too see if good posture
       for i, frame in enumerate(run_data):
           try:
               keypoints = frame[0][0]
               shoulder = keypoints[self.KEYPOINT_SHOULDER]
               hip = keypoints[self.KEYPOINT_HIP]
               knee_L = keypoints[self.KEYPOINT_LEFT_KNEE]
               knee_R = keypoints[self.KEYPOINT_RIGHT_KNEE]
               #coord between the left and right knee
               mid_knee = (
                   (knee_L[0] + knee_R[0]) / 2,
                   (knee_L[1] + knee_R[1]) / 2
               )
               angle_deg = self.calculate_angle(shoulder, hip, mid_knee)

               if angle_deg is None:
                   print(f"Frame {i}: Could not calculate posture angle.")
                   continue

               print(f"\nFrame {i} | Posture Angle: {angle_deg:.2f}°")
               if angle_deg >= 150:
                   print("Good posture")
               else:
                   self.bad_posture_counter["counter"] += 1
                   self.bad_posture_counter["frames"].append(i)
                   print("Poor posture: Leaning forward")

           except (IndexError, TypeError):
               print(f"Frame {i}: Missing keypoints, skipping.")
   def calculate_angle(self, pointA, pointB, pointC):
       # creates vector for point a to b then b to c
       # then uses dot product formula to calculate the angle betwween the two vectors
       vec1 = (pointA[0] - pointB[0], pointA[1] - pointB[1])
       vec2 = (pointC[0] - pointB[0], pointC[1] - pointB[1])
       dot = vec1[0] * vec2[0] + vec1[1] * vec2[1]
       mag1 = math.sqrt(vec1[0] ** 2 + vec1[1] ** 2)
       mag2 = math.sqrt(vec2[0] ** 2 + vec2[1] ** 2)
       # to prevent if one of the vector is 0 when dividing
       if mag1 == 0 or mag2 == 0:
           return None

       angle_rad = math.acos(dot / (mag1 * mag2))
       return math.degrees(angle_rad)

   def getArmForm(self):
       # gets angle of elbow and check if below 110 to be considred good form
       run_data = self.keypoints
       print("\n getting Arm Angles")

       for i, frame in enumerate(run_data):
           try:
               keypoints = frame[0][0]
               shoulder = keypoints[self.KEYPOINT_SHOULDER]
               L_elbow = keypoints[self.KEYPOINT_LEFT_ELBOW]
               R_elbow = keypoints[self.KEYPOINT_RIGHT_ELBOW]
               L_wrist = keypoints[self.KEYPOINT_LEFT_WRIST]
               R_wrist = keypoints[self.KEYPOINT_RIGHT_WRIST]

               left_angle = self.calculate_angle(shoulder, L_elbow, L_wrist)
               right_angle = self.calculate_angle(shoulder, R_elbow, R_wrist)



               print(f"\nFrame {i}")

               if left_angle is not None:
                   print(f"Left Elbow Angle: {left_angle:.2f}°", end=" → ")
                   if left_angle < 110:
                       print("Good arm Form" )
                   else:
                       self.bad_arm_form_counter["counter"] += 1
                       self.bad_arm_form_counter["frames"].append(i)
                       print("Arm form Needs improvement")


               else:
                   print("Left arm angle could not be calculated.")

               if right_angle is not None:
                   print(f" Right Elbow Angle: {right_angle:.2f}°", end=" → ")
                   if left_angle < 110:
                       print("Good arm Form")
                   else:
                       self.bad_arm_form_counter["counter"] += 1
                       self.bad_arm_form_counter["frames"].append(i)
                       print("Arm form Needs improvement")



               else:
                   print(" Right arm angle could not be calculated.")
           except (IndexError, TypeError):
               print(f"Frame {i}: Missing keypoints, skipping.")

   def getFootLanding(self):
       run_data = self.keypoints
       print("\nEvaluating Foot Landing Alignment")
       print("test icles")

       # Left foot

       for i in self.left_contact_frames:
           try:
               frame = run_data[i][0][0]

               heel_x = frame[self.KEYPOINT_LEFT_HEEL][0]
               toe_x = frame[self.KEYPOINT_LEFT_TOE][0]
               mid_x = (heel_x + toe_x) / 2

               # if hip key point not avaliable uses shoulder insteaad
               hip_x = frame[self.KEYPOINT_HIP][0] if frame[self.KEYPOINT_HIP] else None
               if hip_x is None or hip_x == 0:
                   hip_x = frame[self.KEYPOINT_SHOULDER][0] if frame[self.KEYPOINT_SHOULDER] else None

               if hip_x is None:
                   print(f"Frame {i}: Hip and Shoulder keypoints missing, skippping.")
                   continue

               diff = abs(hip_x - mid_x)
               print(
                   f"\neft Foot Frame {i} | Hip X: {hip_x:.2f} | Mid-foot X: {mid_x:.2f} | Difference: {diff:.2f}")

               if diff < 200:
                   print(" Goood alignment: Hip over mid-foot.")
               elif hip_x < mid_x:
                   print("Hip too far behind foot (overstriding).")
                   self.bad_landing_counter["counter"] += 1
                   self.bad_landing_counter["frames"].append(i)
               else:
                   print("Hip too far ahead (possible brakingg).")
                   self.bad_landing_counter["counter"] += 1
                   self.bad_landing_counter["frames"].append(i)

           except (IndexError, TypeError):
               print(f"Error processing frame {i}, skipping.")

       # Right foot
       for i in self.right_contact_frames:
           try:
               frame = run_data[i][0][0]

               heel_x = frame[self.KEYPOINT_RIGHT_HEEL][0]
               toe_x = frame[self.KEYPOINT_RIGHT_TOE][0]
               mid_x = (heel_x + toe_x) / 2

               hip_x = frame[self.KEYPOINT_HIP][0] if frame[self.KEYPOINT_HIP] else None
               if hip_x is None or hip_x == 0:
                   hip_x = frame[self.KEYPOINT_SHOULDER][0] if frame[self.KEYPOINT_SHOULDER] else None

               if hip_x is None:
                   print(f"Frame {i}: Hip and Shoulder keypoints missing, skipping.")
                   continue

               diff = abs(hip_x - mid_x)
               print(
                   f"\nRight Foot Frame {i} |Hip X: {hip_x:.2f} | Mid-foot X: {mid_x:.2f} |  Difference: {diff:.2f}")

               if diff < 200:
                   print("Good alignment: Hip over mid-foot.")
               elif hip_x < mid_x:
                   print("Hip too far behind foot (overstriding).")
                   self.bad_landing_counter["counter"] += 1
                   self.bad_landing_counter["frames"].append(i)
               else:
                   print("Hip too far ahead (possible brakingg).")
                   self.bad_landing_counter["counter"] += 1
                   self.bad_landing_counter["frames"].append(i)

           except (IndexError, TypeError):
               print(f" Error processing frame {i}, skipping.")

   def analyseForm(self):
       self.getArmForm()
       self.getPosture()
       self.get_footStrike()
       self.getFootLanding()


if __name__ == "__main__":
   print("zipzap")
   runs_folder=r"data/runs"
   analysis=RunningAnalysis(runs_folder)

   #analysis.print_all_heel_y_values()
   analysis.test_function()
   #analysis.get_treadmill_baseLine_forLheel()
   #analysis.get_treadmill_baseLine_forRheel()
   #analysis.print_keypoints()
   analysis.analyseForm()
   print(analysis.bad_posture_counter["counter"])
   print(analysis.bad_arm_form_counter["counter"])
   print(analysis.bad_landing_counter["counter"])


   print("hey now  ",analysis.total_frames)




'''
index of the keypoints
 0 - 1 (forehead)
 1 - shoulder
 2 - L_elbow
 3 - R_elbow
 4 - L_wrist
 5 - R_wrist
 6 - Hip
 7 - R_knee
 8 - L_knee
 9 - R_ankle
 10 - L_ankle
 11 - R_heel
 12 - L_heel
 13- R_toe
 14- L_toe

'''


