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




