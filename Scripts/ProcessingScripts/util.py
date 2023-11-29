
##########
# BitterBuster Candy Generator Utility Functions
# Originally Developed by Team HAI Fall 2022
# Angela Zhang, Constanza Tong, Ruizi Wang, Yuan Tan
#
# This script and all related assets fall under the CC BY-NC-SA 4.0 License
# All future derivations of this code should contain the above attribution
##########

import os

## Various utility functions that are used across both scripts
def remove_files(path):
  """
    Removes all files from the given input path
    Arguments:
      path: string of the directory to remove all files from
  """

  for filename in os.listdir(path):
    f = os.path.join(path, filename)

    if not os.path.isfile(f):
      continue
    
    os.remove(f)
