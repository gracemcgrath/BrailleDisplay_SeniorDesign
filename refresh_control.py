import time
import board
import pwmio
from adafruit_motor import servo
import digitalio
import ulab.numpy as np
import supervisor



#supervisor.disable_autoreload()
steps_per_rev = 4096
step_delay = 0.0009 #change this to adjust the speed of the motor

# create a PWMOut object on Pin A2.
pwm = pwmio.PWMOut(board.D2, frequency=50)

# Create a servo object, my_servo.
my_servo = servo.ContinuousServo(pwm)

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

def quarter_rev(times):
    if times == 0 : return
    elif times > 0:
        direction = "cw"
    elif time < 0:
        direction = "ccw"

    for i in range(times):
        for j in range(steps_per_rev/4):
            step_cuboid(direction)
            time.sleep(step_delay)

# step sequence for cuboid
def step_cuboid(direction):
    global step_cub_number
    if direction == "cw":
        print("its hitting cw")
        step_cub_number += 1
    elif direction == "ccw":
        print("its hitting ccw")
        step_cub_number -= 1

    step_cub_number %= len(step_sequence)
    cub_A_1.value = step_sequence[step_cub_number][0]
    cub_A_2.value = step_sequence[step_cub_number][1]
    cub_B_1.value = step_sequence[step_cub_number][2]
    cub_B_2.value = step_sequence[step_cub_number][3]

# rotate cuboid
def rotate_cuboid(next_state,current_state):
    for next_letter in next_state:
        print("spacer for next cuboid")
        nextCuboid()
        print(next_letter)
        if next_letter in char_dict:
            transition = char_dict[next_letter] - current_state
            cuboid = 0
            for times in transition:
                cuboid+=1
                print(f'cuboid {cuboid}')
                quarter_rev(times)
                nextCuboid()
                quarter_rev(times)
## I think we can add the buffer here as well --> write the text to a file
#def encodeInput(text):
#    next_state= np.array(range(3), dtype=np.uint8)
#    for letter, i in zip(text,range(len(text))):
#        if letter in char_dict:
#            next_state[i-1] = char_dict[letter]
#    np.flip(next_state,1)
#    return next_state

def nextCuboid():
    print("forward")
    my_servo.throttle = 1.0 #-1.0 to reset
    time.sleep(3.0)
    print("stop")
    my_servo.throttle = 0.0
    time.sleep(1)

step_cub_number = 0
while True:
    try:
        current_state
    except:
        current_state = char_dict['blank']
        print(current_state)
    #print([char_dict['blank'])
    #current_state = np.array([char_dict['blank'],char_dict['blank'],char_dict['blank']])
    next_state = 'dog'
    #next_state = input[::-1]
    #next_state = encodeInput(text)
    #print(next_state)
    #rotate_cuboid(next_state, current_state)
    #for i in range(5):
    #nextCuboid()
    times= -1*4
    quarter_rev(times)
    time.sleep(3.0)

