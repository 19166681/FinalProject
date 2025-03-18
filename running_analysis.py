import json
import os

import numpy as np


class RunningAnalysis:
   def __init__(self, runs_directory):
      self.runs_directory = runs_directory
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
      print(f"Total Runs:  {total_numOfRuns}")
      print(f"Total Frames Analyzed:  {total_frames}")





if __name__ == "__main__":
   runs_folder=r"C:\Users\rocke\OneDrive\Desktop\uni\comp 6032 AI\FinalProject\data\runs"
   analysis=RunningAnalysis(runs_folder)
   analysis.print_keypoints()


