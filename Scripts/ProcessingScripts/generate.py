##########
# BitterBuster Candy Generator Script
# Originally Developed by Team HAI Fall 2022
# Angela Zhang, Constanza Tong, Ruizi Wang, Yuan Tan
#
# This script and all related assets fall under the CC BY-NC-SA 4.0 License
# All future derivations of this code should contain the above attribution
##########
import argparse
import json
import os
import time
import numpy as np
import cv2 as cv
import multiprocessing as mp
from util import remove_files
from multiprocessing import Pool
### Customizable Parameters
# Path to directory for each component
left_arm_path = "../../Data/InputData/Left_Arms_2x(280x280)"

right_arm_path = "../../Data/InputData/Right_Arms_2x(280x280)"
body_path = "../../Data/InputData/Body_2x(840x840)"
eyes_path = "../../Data/InputData/Eyes_2x(480x240)"
legs_path = "../../Data/InputData/Legs_2x(480x500)"
mouth_path = "../../Data/InputData/Mouth_2x(400x240)"
pattern_path = "../../Data/InputData/Pattern_2x(840x840)"
all_paths = [left_arm_path, right_arm_path, body_path, eyes_path, legs_path, mouth_path, pattern_path]

# Label names for each component
left_arm_labels = ["side", "orientation"]
right_arm_labels = ["side", "orientation"]
body_labels = ["hue", "shape"]
eye_labels = ["lash", "distance"]
leg_labels = ["length", "orientation"]
mouth_labels = ["openness"]
pattern_labels = ["type"]
all_labels = [left_arm_labels, right_arm_labels, body_labels, eye_labels, leg_labels, mouth_labels, pattern_labels]

# Position of center of each component in the final image (y, x)
left_arm_pos = (580, 150)
right_arm_pos = (580, 1162)
body_pos = (560, 656)
eye_pos = (520, 656)
leg_pos = (1080, 656)
mouth_pos = (650, 656)
pattern_pos = (560, 656)
all_pos = [left_arm_pos, right_arm_pos, body_pos, eye_pos, leg_pos, mouth_pos, pattern_pos]

# Dimensions of output image in (y, x, # channels)
output_size = (1400, 1312, 4)
basePath = os.path.dirname(os.path.dirname(os.getcwd()))
output_path = os.path.join(basePath, 'Output', 'Oomplets')
### End of Customizable Parameters

### Start of main functionality


## Helper Functions
def get_indices(image_pos, image_size):
  """
    Given the central image position and the image's size, 
    returns the indices of where this image starts and ends
    Arguments:
      image_pos: position (y, x) of the image
      image_size: size (height, width) of the image
    Returns:
      (start_y, end_y, start_x, end_x) indices of where the image should go
  """

  start_y = image_pos[0] - (image_size[0] // 2)
  end_y = image_pos[0] + (image_size[0] // 2) + (1 if image_size[0] % 2 != 0 else 0)
  start_x = image_pos[1] - (image_size[1] // 2)
  end_x = image_pos[1] + (image_size[1] // 2) + (1 if image_size[1] % 2 != 0 else 0)
  return (start_y, end_y, start_x, end_x)

def overlay(paired_pixel):
  """
    Given an interweaving pair of two pixels, overlays the new pixel on top 
    of the old (original) one
    Arguments:
      paired_pixel: an interweaving array that contains
        [orig_r, new_r, orig_g, new_g, orig_b, new_b, orig_a, new_a]
        Can be parsed into RGBA values for the new and original pixels
    Returns:
      Resulting pixel of overlaying the new pixel on top of the old one
  """

  orig_pixel = paired_pixel[::2]
  new_pixel = paired_pixel[1::2]

  if (new_pixel[3] == 0): 
    return orig_pixel
  return new_pixel

def burn(paired_pixel):
  """
    Given an interweaving pair of two pixels, burns the new pixel on top 
    of the old (original) one
    Arguments:
      paired_pixel: an interweaving array that contains
        [orig_r, new_r, orig_g, new_g, orig_b, new_b, orig_a, new_a]
        Can be parsed into RGBA values for the new and original pixels
    Returns:
      Resulting pixel of burning the new pixel on top of the old one
  """

  orig_pixel = paired_pixel[::2]
  new_pixel = paired_pixel[1::2]

  # Skip transparent pixels
  if (orig_pixel[3] == 0 or new_pixel[3] == 0): 
    return orig_pixel

  ret_pixel = [0, 0, 0, orig_pixel[3]]
  ret_pixel[0] = int(orig_pixel[0] * new_pixel[0] / 255)
  ret_pixel[1] = int(orig_pixel[1] * new_pixel[1] / 255)
  ret_pixel[2] = int(orig_pixel[2] * new_pixel[2] / 255)
  return ret_pixel

def draw_component(img, comp, comp_pos, apply_burn=False):
  """
    Given the overall image and a component, adds the component to the overall image
    Arguments:
      img: a numpy array of the overall image
      comp: a struct
        "labels": a struct containing the component labels
        "image": a numpy array containing the component image
      comp_pos: a tuple (y, x) of where the component should go
      apply_burn: whether to burn the component on top of the image. On False, will simply overlay (replace) any pixels underneath
    Returns:
      The labels of the component that was added
  """

  # Draw a body first
  comp_labels = comp["labels"]
  comp_image = comp["image"]
  
  # Get body image position
  (start_y, end_y, start_x, end_x) = get_indices(comp_pos, comp_image.shape)

  orig_shape = comp_image.shape
  flattened_shape = (orig_shape[0] * orig_shape[1], orig_shape[2])
  stacked_flattened_shape = (orig_shape[0] * orig_shape[1], orig_shape[2] * 2)

  curr_image = img[start_y:end_y, start_x:end_x].reshape(flattened_shape)
  comp_image = comp_image.reshape(flattened_shape)

  comp_image = np.dstack([curr_image, comp_image]).reshape(stacked_flattened_shape)

  if apply_burn:
    comp_image = np.array(list(map(burn, comp_image))).reshape(orig_shape)
  else:
    comp_image = np.array(list(map(overlay, comp_image))).reshape(orig_shape)

  img[start_y:end_y, start_x:end_x] = comp_image

  return comp_labels

def generate_candy(i):
  """
    Given an index, generates a candy
    Arguments:
      i: an index into the global combinations array defining which components to use in the constructed
  """

  if verbose:
    tic = time.perf_counter()

  img = np.full(output_size, 0)

  (left_arm_index, right_arm_index, body_index, eye_index, legs_index, mouth_index, pattern_index) = combinations[i]

  # Draw a base first
  left_arm_comp_labels = draw_component(img, left_arms[left_arm_index], left_arm_pos)
  leg_comp_labels = draw_component(img, legs[legs_index], leg_pos)
  body_comp_labels = draw_component(img, bodies[body_index], body_pos)

  # Apply pattern next
  pattern_comp_labels = draw_component(img, patterns[pattern_index], pattern_pos, True)
  
  # Place everything else
  right_arm_comp_labels = draw_component(img, right_arms[right_arm_index], right_arm_pos)
  eye_comp_labels = draw_component(img, eyes[eye_index], eye_pos)
  mouth_comp_labels = draw_component(img, mouths[mouth_index], mouth_pos)

  # Write image png file
  filename = f"oomplet_{str(i)}"
  image_filename = f"{filename}.png"
  image_path = os.path.join(output_path, image_filename)
  cv.imwrite(image_path, img)

  # Write label json file
  labels = {
    "image_filename": image_filename,
    "body": body_comp_labels,
    "eye": eye_comp_labels,
    "left_arm": left_arm_comp_labels,
    "leg": leg_comp_labels,
    "mouth": mouth_comp_labels,
    "pattern": pattern_comp_labels,
    "right_arm": right_arm_comp_labels,
  }
  json_object = json.dumps(labels, indent=4)

  json_filename = f"{filename}.json"
  json_path = os.path.join(output_path, json_filename)
  with open(json_path, "w") as outfile:
    outfile.write(json_object)

  if verbose:
    toc = time.perf_counter()
    print(f"Created oomplet_{i} in {toc - tic:0.4f} seconds")

def load_components():
  """
    Loads all of the components in the Components folder based on 
    the arguments defined at the top of this script
    Returns:
      An array of arrays of each type of component
  """
  all_components = []
  for i in range(len(all_paths)):
    path = all_paths[i]
    labels = all_labels[i]
    components = []

    if not os.path.exists(path):
      raise Exception(f"Unable to load components from path {path}")

    for filename in os.listdir(path):
      f = os.path.join(path, filename)
      
      # only read png files
      if not os.path.isfile(f):
        continue

      if not f.endswith(".png"):
        continue

      img = cv.imread(f, cv.IMREAD_UNCHANGED)

      # parse labels from the png name
      img_labels = filename[0:filename.find(".png")].split(',')[1:-1]
      assert(len(img_labels) == len(labels))
      
      comp_labels = {}
      for j in range(len(labels)):
        comp_labels[labels[j]] = img_labels[j]

      components.append({"labels": comp_labels, "image": img})

    all_components.append(components)
  return all_components

## End Helper Functions

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-n', type=int, help='number of oomplets to generate')
parser.add_argument('-p', action="count", help='multiprocessing flag, default off')
parser.add_argument('-c', type=int, help='max number of processes to spawn if multiprocessing, default 4', default=4)
parser.add_argument('-v', action="count", help='verbose, default off')
parser.add_argument('-k', action="count", help='keep existing files in output folder, default off')
parser.add_argument('-s', type=int, help='seed value for randomly generated oomplets', default=0)
args = parser.parse_args()

# Load all components
all_components = load_components()
[left_arms, right_arms, bodies, eyes, legs, mouths, patterns] = all_components

component_indices = [np.array(range(len(comp))) for comp in all_components]
combinations = np.array(np.meshgrid(*component_indices)).T.reshape(-1,len(component_indices))

verbose = args.v
parallel = args.p
max_workers = args.c
if args.n == None:
  num_candies = len(combinations)
else:
  num_candies = args.n
keep_output_files = args.k
seed = args.s

np.random.seed(seed)
np.random.shuffle(combinations)

if __name__ == '__main__':
  if not os.path.exists(output_path):
    os.makedirs(output_path)

  if not keep_output_files:
    remove_files(output_path)

  overall_tic = time.perf_counter()

  if parallel:
    # Begins multi-processing to allow parallel generation of candies
    num_workers = min(mp.cpu_count(), max_workers)

    if verbose:
      print(f"Multi-processing: using {num_workers} processes")

    with Pool(processes=num_workers) as pool:
      pool.map(generate_candy, range(num_candies))
  else:
    if verbose:
      print(f"Sequential")

    for i in range(num_candies):
      generate_candy(i)

  overall_toc = time.perf_counter()
  print(f"Generated {num_candies} oomplets in {overall_toc - overall_tic:0.4f} seconds")
