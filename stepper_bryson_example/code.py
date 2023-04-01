# stepper_bryson_ex

import time
import board
import digitalio

steps_per_rev = 200  # change this to match your motor's steps per revolution
delay = 0.05 #change this to adjust the speed of the motor

# ORIGINAL
# Define the pins connected to the stepper motor coils
coil_A_1_pin = digitalio.DigitalInOut(board.A0)
coil_A_2_pin = digitalio.DigitalInOut(board.A1)
coil_B_1_pin = digitalio.DigitalInOut(board.A2)
coil_B_2_pin = digitalio.DigitalInOut(board.A3)

# Set the pins as outputs
coil_A_1_pin.direction = digitalio.Direction.OUTPUT
coil_A_2_pin.direction = digitalio.Direction.OUTPUT
coil_B_1_pin.direction = digitalio.Direction.OUTPUT
coil_B_2_pin.direction = digitalio.Direction.OUTPUT

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

# Function to make one step in a given direction
def step(direction):
    global step_number
    if direction == "forward":
        step_number += 1
    else:
        step_number -= 1

#     if step_number%10==0: print(step_number)
    step_number %= len(step_sequence)
    coil_A_1_pin.value = step_sequence[step_number][0]
    coil_A_2_pin.value = step_sequence[step_number][1]
    coil_B_1_pin.value = step_sequence[step_number][2]
    coil_B_2_pin.value = step_sequence[step_number][3]

step_number = 0
direction = "forward"

# Make the stepper motor move 100 steps in one direction
for i in range(4096):
    step(direction)
    time.sleep(delay)

# Change direction and make the stepper motor move 100 steps in the opposite direction
# direction = "backward"
# for i in range(32*16):
#     step(direction)
#     time.sleep(delay)
