# Python-Based Candy Generation Scripts and Assets
This repository contains scripts and initial assets for Candy Generation + Bitter/Sweet classifications.
These assets were designed to be used in conjunction with the BitterBuster game; however, they can 
also be used for general visual classification studies and tasks.

## Attribution
Originally Developed by Team HAI Fall 2022
Angela Zhang, Constanza Tong, Ruizi Wang, Yuan Tan

The provided scripts and all related assets fall under the CC BY-NC-SA 4.0 License
All future derivations of this code should contain the above attribution 

## Setup
1. Set up a Python virtual environment in the root directory
```
% python -m venv venv
```
2. [Activate the virtual environment](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments) based on OS
3. Install all the requirements
```
% pip install -r requirements.txt
```

## Generate Candies
```
usage: python generate.py [-h] [-n N] [-p] [-c C] [-v] [-k] [-s S]

options:
  -h, --help  show this help message and exit
  -n N        number of candies to generate N, by default will generate all possible combinations
  -p          multiprocessing flag, default off
  -c C        max number of processes to spawn if multiprocessing, default 4
  -v          verbose, default off
  -k          keep existing files in output folder, default off
  -s S        seed value for randomly generated candies, default 0
```

## Categorize Candies
```
usage: python categorize.py [-h] [-k]

options:
  -h, --help  show this help message and exit
  -d, --def   define your 'Match' criteria
  -k          keep existing files in output folders, default off
  -i, --input name of the directory from which Oomplets will be sorted (default: Oomplets)
  -a, --any   flags Oomplets with ANY of the given defining attributes as 'Match' (default: off, must have ALL attributes)
```
