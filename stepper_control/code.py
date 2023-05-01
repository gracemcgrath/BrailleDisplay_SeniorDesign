# cuboid

import time
import board
import digitalio
import ulab.numpy as np

steps_per_rev = 4096
step_delay = 0.0009 #change this to adjust the speed of the motor
cuboid_delay = 3
char_delay = 3

revs_to_next_cub = 4096    # a guess



char_dict = {'blank': np.array((0,0,0)),
            'a': np.array((3,0,0)),
            'b': np.array((3,3,0)),
            'c': np.array((2,0,0)),
            'd': np.array((2,1,0)),
            'e': np.array((3,2,0)),
            'f': np.array((2,1,0)),
            'g': np.array((2,2,0)),
            'h': np.array((3,2,0)),
            'i': np.array((1,3,0)),
            'j': np.array((1,2,0)),
            'k': np.array((3,0,3)),
            'l': np.array((3,3,3)),
            'm': np.array((2,0,3)),
            'n': np.array((2,1,3)),
            'o': np.array((3,1,3)),
            'p': np.array((2,3,3)),
            'q': np.array((2,2,3)),
            'r': np.array((3,2,3)),
            's': np.array((1,3,3)),
            't': np.array((1,2,3)),
            'u': np.array((3,0,2)),
            'v': np.array((3,3,2)),
            'w': np.array((1,2,1)),
            'x': np.array((2,0,2)),
            'y': np.array((2,1,2)),
            'z': np.array((3,1,2))
            }

# CUBOID REFRESHER
# Define the pins connected to the stepper motor coils
cub_A_1 = digitalio.DigitalInOut(board.A0)
cub_A_2 = digitalio.DigitalInOut(board.A1)
cub_B_1 = digitalio.DigitalInOut(board.A2)
cub_B_2 = digitalio.DigitalInOut(board.A3)
# Set the pins as outputs
cub_A_1.direction = digitalio.Direction.OUTPUT
cub_A_2.direction = digitalio.Direction.OUTPUT
cub_B_1.direction = digitalio.Direction.OUTPUT
cub_B_2.direction = digitalio.Direction.OUTPUT

# LINEAR MOVEMENT
# Define the pins connected to the stepper motor coils
lin_A_1 = digitalio.DigitalInOut(board.D1)
lin_A_2 = digitalio.DigitalInOut(board.D2)
lin_B_1 = digitalio.DigitalInOut(board.D3)
lin_B_2 = digitalio.DigitalInOut(board.D4)
# Set the pins as outputs
lin_A_1.direction = digitalio.Direction.OUTPUT
lin_A_2.direction = digitalio.Direction.OUTPUT
lin_B_1.direction = digitalio.Direction.OUTPUT
lin_B_2.direction = digitalio.Direction.OUTPUT

# Define the sequence of signals to activate the stepper motor coils
step_sequence = [
    (1, 0, 0, 1),
    (1, 0, 0, 0),
    (1, 1, 0, 0),
    (0, 1, 0, 0),
    (0, 1, 1, 0),
    (0, 0, 1, 0),
    (0, 0, 1, 1),
    (0, 0, 0, 1),
]

# 90-degree rotations for cuboid
def quarter_rev(times):
    if times == 0 : return
    elif times > 0:
        direction = "cw"
    else:
        direction = "ccw"

    for i in range(times):
        for j in range(steps_per_rev/4):
            step_cuboid(direction)
            time.sleep(step_delay)

# step sequence for cuboid
def step_cuboid(direction):
    global step_cub_number
    if direction == "cw":
        step_cub_number += 1
    else:
        step_cub_number -= 1

    step_cub_number %= len(step_sequence)
    cub_A_1.value = step_sequence[step_cub_number][0]
    cub_A_2.value = step_sequence[step_cub_number][1]
    cub_B_1.value = step_sequence[step_cub_number][2]
    cub_B_2.value = step_sequence[step_cub_number][3]

# rotate cuboid
def rotate_cuboid(text,current_state):
    for letter in text:
        print(letter)
        if letter in char_dict:
            next_state = char_dict[letter] - current_state
            cuboid = 0
            for times in next_state:
                cuboid+=1
                print(f'cuboid {cuboid}')
                quarter_rev(times)
                move_refresher()
            if cuboid<3:
                move_refresher()

# step sequence for linear shaft
def step_linear(direction):
    global step_lin_number
    if direction == "cw":
        step_lin_number += 1
    else:
        step_lin_number -= 1

    step_lin_number %= len(step_sequence)
    lin_A_1.value = step_sequence[step_lin_number][0]
    lin_A_2.value = step_sequence[step_lin_number][1]
    lin_B_1.value = step_sequence[step_lin_number][2]
    lin_B_2.value = step_sequence[step_lin_number][3]

# rotate stepper to forward/backward linear shaft
def move_refresher():
    print('move_refresher')
    direction = "cw"
    for k in range(revs_to_next_cub):
        step_linear(direction)
        time.sleep(step_delay)

step_cub_number = 0
step_lin_number = 0

while True:
    current_state = char_dict['blank']
    text = 'no'
    rotate_cuboid(text, current_state)



