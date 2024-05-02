##########
# BitterBuster Candy Categorizer Script
# Originally Developed by Team HAI Fall 2022
# Angela Zhang, Constanza Tong, Ruizi Wang, Yuan Tan
#
# This script and all related assets fall under the CC BY-NC-SA 4.0 License
# All future derivations of this code should contain the above attribution
##########

### Customizable Parameters
# Function that, given the attribute specifications, determines whether this Oomplet matches the criteria, and sorts it correctly

spec_dictionary = {
  'color_cool': ['body','hue','cold'],
  'color_warm': ['body','hue','warm'],

  'shape_sharp': ['body','shape','sharp'],
  'shape_mixed': ['body','shape','mixed'],
  'shape_round': ['body','shape','round'],

  'lash_yes': ['eye','lash','lash'],
  'lash_no': ['eye','lash','nolash'],

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
  
def isMatch(labels, providedOpts, lookForAny):
  for option in providedOpts:
    try:
      specs = spec_dictionary[option]
    except KeyError:
      print(f'{option} is not a valid option. Please revise according to the documentation, and try again!')
    if not lookForAny and labels[specs[0]][specs[1]] != specs[2]:
      return False
    elif lookForAny and labels[specs[0]][specs[1]] == specs[2]:
      return True
  return not lookForAny


### End of Customizable Parameters

import argparse
import json
import os
import shutil
from util import remove_files
import datetime

basePath = os.path.dirname(os.path.dirname(os.getcwd()))

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-k', action="count", help='keep existing files in output folders, default off')
  parser.add_argument('-i', '--input', default='Oomplets', help='name of the directory from which Oomplets will be sorted')
  parser.add_argument('-d', '--def', nargs = '+', help = "list attributes to define which Oomplets are a Match (must list one), separated using space", required = True)
  parser.add_argument('-a', '--any', action="store_true", help= 'indicates that Oomplets with ANY of defining attributes will be placed in the Match group')
  
  args = parser.parse_args()

  keep_output_files = args.k
  inDirectory = args.input
  attribute_list = args.define
  searchForAny = args.any

  ts = datetime.datetime.now()

  input_path = os.path.join(basePath, 'Output', inDirectory)
  output_bitter_path = os.path.join(basePath, 'Output', f'Match_{str(ts.hour)}-{str(ts.minute)}-{str(ts.second)}-{str(ts.microsecond)}')
  output_sweet_path = os.path.join(basePath, 'Output', f'NoMatch_{str(ts.hour)}-{str(ts.minute)}-{str(ts.second)}-{str(ts.microsecond)}')

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
    if isMatch(candy_labels, attribute_list, searchForAny):
      shutil.copy(json_input_filepath, os.path.join(output_bitter_path, json_filename))
      shutil.copy(image_input_filepath, os.path.join(output_bitter_path, image_filename))
    else:
      shutil.copy(json_input_filepath, os.path.join(output_sweet_path, json_filename))
      shutil.copy(image_input_filepath, os.path.join(output_sweet_path, image_filename))
