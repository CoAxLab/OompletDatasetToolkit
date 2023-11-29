##########
# BitterBuster Candy Categorizer Script
# Originally Developed by Team HAI Fall 2022
# Angela Zhang, Constanza Tong, Ruizi Wang, Yuan Tan
#
# This script and all related assets fall under the CC BY-NC-SA 4.0 License
# All future derivations of this code should contain the above attribution
##########

### Customizable Parameters
# Function that, given the labels for a Candy, determines whether this Candy is bitter
def is_bitter(labels):
  #return labels["body"]["hue"] == "cold" and labels["pattern"]["type"] != "stripes"
  return labels["body"]["hue"] == "cold" and labels["eye"]["lash"] != "lash"

input_path = "../../Data/AnalysisData"
output_bitter_path = "../../Output/Bitter"
output_sweet_path = "../../Output/Sweet"
### End of Customizable Parameters

import argparse
import json
import os
import shutil
from util import remove_files

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-k', action="count", help='keep existing files in output folders, default off')
  args = parser.parse_args()

  keep_output_files = args.k

  if not os.path.exists(output_bitter_path):
    os.makedirs(output_bitter_path)

  if not os.path.exists(output_sweet_path):
    os.makedirs(output_sweet_path)

  # Have a flag for clearing all files in output folders
  if not keep_output_files:
    remove_files(output_bitter_path)
    remove_files(output_sweet_path)

  # Categorize all input files
  path = input_path
  for filename in os.listdir(path):
    f = os.path.join(path, filename)

    if not os.path.isfile(f):
      continue

    # Only look at json files
    if not f.endswith(".json"):
      continue

    json_filename = filename
    json_input_filepath = f

    # Load candy labels and image
    candy_labels = json.load(open(json_input_filepath))
    image_filename = candy_labels["image_filename"]
    image_input_filepath = os.path.join(path, image_filename)

    # Add to respective folder depending on bitterness categorization
    if is_bitter(candy_labels):
      shutil.copy(json_input_filepath, os.path.join(output_bitter_path, json_filename))
      shutil.copy(image_input_filepath, os.path.join(output_bitter_path, image_filename))
    else:
      shutil.copy(json_input_filepath, os.path.join(output_sweet_path, json_filename))
      shutil.copy(image_input_filepath, os.path.join(output_sweet_path, image_filename))
