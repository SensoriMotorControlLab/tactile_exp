#!/usr/bin/env python
# -*- coding: utf-8 -*-

# based on aimingeffects code, but switched fully to Python 3
# dropping deprecated calls to scipy
# eventually will add a GUI for:
# -  easy running
# -  counter-balancing
# -  ID generation
# -  collecting demographics


from psychopy import event, visual, monitors
from psychopy.tools.coordinatetools import pol2cart, cart2pol
#from psychopy.hardware import keyboard
from pyglet.window import key
import random
import time
import scipy as sp
import numpy as np
import pandas as pd
import os
import glob
import sys


# This function choose where to start and which circle to go next randomly
def process_lists(left, right): 
    sides = [left, right]
    current_side = random.choice([0, 1])  # 0 for left, 1 for right
    
    while any(sides):  # Continue until both lists are empty
        if sides[current_side]:  # Check if the current side has elements
            circle_picked = random.choice(sides[current_side])
            sides[current_side].remove(circle_picked)
            
            # Implement logic to move cursor to circles 

            print(f"Picked {circle_picked}") # Debug Message
            
        current_side = 1 - current_side  # Switch sides
    
    print("End of trial!")


# Example usage to implement later
left_circles = ['circle_top_left', 'circle_middle_left', 'circle_bottom_left']
right_circles = ['circle_top_right', 'circle_middle_right', 'circle_bottom_right']
process_lists(left_circles, right_circles)