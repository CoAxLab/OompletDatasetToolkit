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

spec_dictionary = {
  'cool_color': ['body','hue','cold'],
  'warm_color': ['body','hue','warm'],

  'sharp_shape': ['body','shape','sharp'],
  'mixed_shape': ['body','shape','mixed'],
  'round_shape': ['body','shape','round'],

  'lash': ['eye','lash','lash'],
  'nolash': ['eye','lash','nolash'],

  'wide_eyes': ['eye','distance','wide'],
  'middle_eyes': ['eye','distance','middle'],
  'narrow_eyes': ['eye','distance','narrow'],

  'short_legs': ['leg','length','short'],
  'middle_legs': ['leg','length','middle'],
  'long_legs': ['leg','length','long'],

  'feet_left': ['leg', 'orientation', 'left'],
  'feet_right': ['leg', 'orientation', 'right'],
  'feet_in': ['leg', 'orientation', 'inward'],
  'feet_out': ['leg', 'orientation', 'outward'],

  'open_mouth': ['mouth', 'openness', 'open'],
  'closed_mouth': ['mouth', 'openness', 'close'],

  'dots_pattern': ['pattern', 'type', 'dots'],
  'stripes_pattern': ['pattern', 'type', 'stripes'],

  'right_arm_down': ['right_arm', 'orientation', 'down'],
  'right_arm_up': ['right_arm', 'orientation', 'up'],

  'left_arm_down': ['left_arm', 'orientation', 'down'],
  'left_arm_up': ['left_arm', 'orientation', 'up']
}

def is_bitter(labels, list_options):
  if(len(list_options) == 1):
    try:
      specs = spec_dictionary[list_options[0]]
      return labels[specs[0]][specs[1]] == specs[2]
    except KeyError:
      print(f'{list_options[0]} is an incorrect value. Please review the list of options and try again.')
  elif(len(list_options) == 2):
    try:
      specs = spec_dictionary[list_options[0]]
      specs_two = spec_dictionary[list_options[1]]
    except KeyError:
      print(f'{list_options[0]} or {list_options[1]} is an incorrect value. Please review the list of options and try again.')
    return labels[specs[0]][specs[1]] == specs[2] and labels[specs_two[0]][specs_two[1]] == specs_two[2]
  else:
    print(f'Only using first two listed: {list_options[0]} and {list_options[1]}')
    try:
      specs = spec_dictionary[list_options[0]]
      specs_two = spec_dictionary[list_options[1]]
    except KeyError:
      print(f'{list_options[0]} or {list_options[1]} is an incorrect value. Please review the list of options and try again.')
    return labels[specs[0]][specs[1]] == specs[2] and labels[specs_two[0]][specs_two[1]] == specs_two[2]
  


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
  parser.add_argument('-d', '--define', nargs = '+', help = "list up to two attributes to define your 'Bitter' stimuli (must list one)", required = True)

  args = parser.parse_args()

  keep_output_files = args.k
  attribute_list = args.define

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
    if is_bitter(candy_labels, attribute_list):
      shutil.copy(json_input_filepath, os.path.join(output_bitter_path, json_filename))
      shutil.copy(image_input_filepath, os.path.join(output_bitter_path, image_filename))
    else:
      shutil.copy(json_input_filepath, os.path.join(output_sweet_path, json_filename))
      shutil.copy(image_input_filepath, os.path.join(output_sweet_path, image_filename))
