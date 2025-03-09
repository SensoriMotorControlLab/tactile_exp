from psychopy import visual, event, core, monitors
import random
import time
import numpy as np
import pandas as pd

# Ask for participant number
participant_number = input("Enter participant ID: ")

# Number of trials
num_trials = 5

# Initialize monitor settings based on experiment_v2.py
monitor = monitors.Monitor(name='exp_monitor', distance=100)
monitor.setSizePix([1680, 1050])
monitor.setWidth(43.3)  # cm

# Initialize experiment window
win = visual.Window(size=[1680, 1050], fullscr=True, units='cm', monitor=monitor, color=[-1, -1, -1])

# Circle settings
circle_sizes = [0.4, 0.6, 0.8]  # Small, Medium, Large
vertical_spacing = 3  # cm (adjust as needed)
horizontal_offset = 6  # cm from center

# Define circle positions
left_positions = [[-horizontal_offset, vertical_spacing],
                  [-horizontal_offset, 0],
                  [-horizontal_offset, -vertical_spacing]]
right_positions = [[horizontal_offset, vertical_spacing],
                   [horizontal_offset, 0],
                   [horizontal_offset, -vertical_spacing]]

# Randomize circle sizes
random.shuffle(circle_sizes)
left_sizes = circle_sizes.copy()
random.shuffle(circle_sizes)
right_sizes = circle_sizes.copy()

# Create circles
circles = []
for i, pos in enumerate(left_positions + right_positions):
    size = left_sizes[i] if i < 3 else right_sizes[i - 3]
    circle = visual.Circle(win, radius=size, pos=pos, fillColor='white', lineColor='white')
    circles.append(circle)

# Initialize mouse and cursor
mouse = event.Mouse(visible=True, win=win)
cursor = visual.Circle(win, radius=0.2, fillColor='blue', lineColor='blue')

def draw_all(path_lines=[]):
    """Draw all circles, path lines, and cursor, then update the window."""
    for circle in circles:
        circle.draw()
    for line in path_lines:
        line.draw()
    cursor.pos = mouse.getPos()
    cursor.draw()
    win.flip()

def reset_circles():
    """Reset all circles to white after a trial."""
    for circle in circles:
        circle.fillColor = 'white'

def run_trial():
    visited = set()
    movement_distances = []
    prev_pos = None
    sides = [left_positions.copy(), right_positions.copy()]
    current_side = random.choice([0, 1])
    trial_start_time = time.time()
    timestamp_data = []
    path_lines = []
    
    draw_all()  # Ensure initial drawing
    
    while any(sides):
        if 'escape' in event.getKeys():  # Allow exit
            win.close()
            core.quit()
            return
        
        if sides[current_side]:
            target = random.choice(sides[current_side])
            sides[current_side].remove(target)
            
            for circle in circles:
                if list(circle.pos) == target:
                    circle.fillColor = 'red'  # Mark as selected
            
            draw_all(path_lines)
            
            waiting = True
            segment_points = []
            while waiting:
                if 'escape' in event.getKeys():  # Allow exit
                    win.close()
                    core.quit()
                    return
                
                pos = mouse.getPos()
                segment_points.append(pos)
                cursor.pos = pos
                
                for circle in circles:
                    if circle.contains(mouse):
                        if list(circle.pos) == target and tuple(target) not in visited:
                            visited.add(tuple(target))
                            timestamp_data.append(time.time() - trial_start_time)
                            
                            if prev_pos is not None:
                                dist = np.linalg.norm(np.array(prev_pos) - np.array(target))
                                movement_distances.append(dist)
                                path_lines.append(visual.ShapeStim(win, vertices=segment_points, closeShape=False, lineColor='blue'))
                            prev_pos = target
                            
                            circle.fillColor = 'green'  # Mark as visited
                            waiting = False
                            draw_all(path_lines)
                            break
            
            current_side = 1 - current_side  # Switch sides
    
    trial_end_time = time.time()
    trial_duration = trial_end_time - trial_start_time
    
    print(f"Trial completed in {trial_duration:.2f} seconds")
    
    reset_circles()  # Reset circles after each trial
    
    return trial_duration, movement_distances, timestamp_data

# Run multiple trials
all_data = []
for trial in range(num_trials):
    print(f"Starting trial {trial + 1} of {num_trials}")
    trial_duration, movement_distances, timestamp_data = run_trial()
    
    for i in range(len(timestamp_data)):
        all_data.append([participant_number, trial + 1, timestamp_data[i], movement_distances[i] if i < len(movement_distances) else np.nan])

# Save all trials to CSV
columns = ['Participant ID', 'Trial', 'Timestamp', 'Movement Distance']
df = pd.DataFrame(all_data, columns=columns)
df.to_csv(f'participant_{participant_number}_trial_data.csv', index=False)

# Close window
win.close()
core.quit()
