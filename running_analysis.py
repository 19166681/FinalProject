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
      run_data=self.get_all_keypoints()
      # i and frame_keypoints are the varibhles that change in the for loop
      #i is just the varble that goes up by 1 for the index of the frames
      # frame_keypoints is the frames keypoints data duuuh so thier should be 15
      #frame_keypoints[0][0][x][z]
      #x is the keypoint so if i make x 15 it will give the 15th (left toe) keypoint data
      #z is the keypoint dat so 0 will be the x coord, 1 will be the y coord , 2 wil be the confidence score
      frameOfthelowestRheel=0
      frameOfthelowestLheel = 0
      lowest_Yvalue_ofRheel=20000
      lowest_Yvalue_ofLheel = 20000
      for i, frame_keypoints in enumerate(run_data):
         print(f"i am pissing bruv "+ str(frame_keypoints[0][0][0][0]) )
         print(f"Frame {i + 1} Keypoints Data: {frame_keypoints}")
         if frame_keypoints[0][0][12][0] < lowest_Yvalue_ofRheel:
            lowest_Yvalue_ofRheel = frame_keypoints[0][0][12][1]
            frameOfthelowestRheel=i
         if frame_keypoints[0][0][13][0] < lowest_Yvalue_ofLheel:
            lowest_Yvalue_ofRheel = frame_keypoints[0][0][13][1]
            frameOfthelowestLheel=i
         if frame_keypoints:  # Ensure it's not empty
            print(f"First Keypoint of Frame {i + 1}: {frame_keypoints[0]}")
      print("frame of lowest Rheel" , str(frameOfthelowestRheel))
      print("frame of lowest Rheel", str(frameOfthelowestLheel))


'''for run in run_data:
        print("the whole keypoint data : " , run)
        if run[0] is not None:
           print("hi   " , run["keypoints"][0])
'''

if __name__ == "__main__":
   runs_folder=r"C:\Users\rocke\OneDrive\Desktop\uni\comp 6032 AI\FinalProject\data\runs"
   analysis=RunningAnalysis(runs_folder)
   analysis.get_all_keypoints()
   analysis.test_function()
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

