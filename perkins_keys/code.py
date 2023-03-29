# code.py
'''
Build: combo_dot_braille
Inspo: https://learn.adafruit.com/circuitpython-essentials/circuitpython-hid-keyboard-and-mouse
type speed: https://stackoverflow.com/questions/22505698/what-is-a-typical-keypress-duration
Keycodes: https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/keycode.html

AS OF 0314:
- Implemented a catch-logic for keys that do not exist in char_dict instead of a placeholder
- Implemented DEL, SPACE, and ENTER keys and it's working

NEXT:
- indicators
- assume edge cases
'''
import board
import time
import ulab.numpy as np
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

import neopixel

# braille-dot no. are connected to D-pin with the same no.
# pins to use on the KB2040
keypress_pins = [# characters
                 board.D1, board.D2, board.D3,
                 board.D4, board.D5, board.D6,
                 # delete, space, enter
                 board.D7, board.D8, board.D9]

# setup onboard led, for debugging purposes
pixel = neopixel.NeoPixel(board.NEOPIXEL,1)

char_dict = { (1,):         (Keycode.A,),
              (1,2):        (Keycode.B,),
              (1,4):        (Keycode.C,),
              (1,4,5):      (Keycode.D,),
              (1,5):        (Keycode.E,),
              (1,2,4):      (Keycode.F,),
              (1,2,4,5):    (Keycode.G,),
              (1,2,5):      (Keycode.H,),
              (2,4):        (Keycode.I,),
              (2,4,5):      (Keycode.J,),
              (1,3):        (Keycode.K,),
              (1,2,3):      (Keycode.L,),
              (1,3,4):      (Keycode.M,),
              (1,3,4,5):    (Keycode.N,),
              (1,3,5):      (Keycode.O,),
              (1,2,3,4):    (Keycode.P,),
              (1,2,3,4,5):  (Keycode.Q,),
              (1,2,3,5):    (Keycode.R,),
              (2,3,4):      (Keycode.S,),
              (2,3,4,5):    (Keycode.T,),
              (1,3,6):      (Keycode.U,),
              (1,2,3,6):    (Keycode.V,),
              (2,4,5,6):    (Keycode.W,),
              (1,3,4,6):    (Keycode.X,),
              (1,3,4,5,6):  (Keycode.Y,),
              (1,3,5,6):    (Keycode.Z,),

              (2,5,6):      (Keycode.PERIOD,),
              (2,):         (Keycode.COMMA,),
              (3,):         (Keycode.QUOTE,),
              (3,5,6):      (Keycode.SHIFT, Keycode.QUOTE), # double quotation marks
              (2,3):        (Keycode.SEMICOLON,),
              (2,5):        (Keycode.SHIFT, Keycode.SEMICOLON),

              (2,3,5):      (Keycode.SHIFT, Keycode.ONE),   # Exclamation point
              (2,3,5,6):    (Keycode.SHIFT, Keycode.NINE),  # Parentheses

              (3,6):        (Keycode.MINUS,),
              (2,3,4,6):    'the',
              (1,2,4,6):    'ed',
              (1,4,6):      'sh',
              (1,2,3,4,6):  'and',
              (1,2,3,5,6):  'of',
              (2,3,4,5,6):  'with',
              (1,6):        'ch',
              (3,4,6):      'ing',
              (3,4):        'st',
              (2,6):        'en',
              (3,5):        'in',
              (1,5,6):      'wh',
              (1,2,6):      'gh',
              (1,2,3,4,5,6):'for',
              (3,4,5):      'ar',
              (1,4,5,6):    'th',
              (2,4,6):      'ow',
              (1,2,4,5,6):  'er',
            # indicators
#               (4,):         '<PH>',     # accent prefix
#               (5,):         '<PH>',     # contraction
#               (6,):         '<PH>',     # uppercase prefix
#               (5,6):        '<PH>',     # letter prefix
              (3,4,5,6):    '<PH>',     # number prefix
#               (4,5):        '<PH>',     # currency prefix
#               (4,5,6):      '<PH>',     # contraction

            # non-braille, non-character keys
              (7,):         (Keycode.BACKSPACE,),
              (8,):         (Keycode.SPACE,),
              (9,):         (Keycode.ENTER,)
             }

# to avoid a race condition if the program gets run
# as soon as the kb2040 gets plugged in''''''''''''''''''
time.sleep(1)

# instantiate keyboard device, following US layout
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

# make all pin object inputs PULL-UP
pin_array = []
for pin in keypress_pins:
    key_pin = digitalio.DigitalInOut(pin)
    key_pin.direction = digitalio.Direction.INPUT
    key_pin.pull = digitalio.Pull.UP
    pin_array.append(key_pin)

# now that everything is set...
print('~~~~~ combo_dot_braille ~~~~~')
pixel.fill((255,255,0))
time.sleep(2)

# maximum difference between two ground pins to be considered for the same braille character
tol = 0.005

pixel.fill((0,0,0))

# main loop
while True:
    # if pin is grounded, record tuple(pin, time of grounding)
    gnd_pin_time = [(i+1,time.monotonic()) for i,pin in enumerate(pin_array) if not pin.value]

    if len(gnd_pin_time) >= 1:
        # sort tuples in ascending time
        gnd_pin_time.sort(key=lambda tup: tup[1])

        # unpack tuple to a list of pin indices and a list of time
        gnd_pin, gnd_time = [i for i, time in gnd_pin_time], [time for i, time in gnd_pin_time]

        # get difference between two consecutive ground times
        gnd_time_diff = np.diff(np.array(gnd_time))
        print(f'gnd_time_diff = {gnd_time_diff}')
        len_gnd_time_diff = len(gnd_time_diff)

        i = 0
        keys_pressed = [gnd_pin[i]]
        while i < len_gnd_time_diff:
            if gnd_time_diff[i] <= tol:
                keys_pressed.append(gnd_pin[i+1])
            i+=1

        char_dict_key = tuple(sorted(keys_pressed))
        if char_dict_key in char_dict:      # avoid errors from absent dict keys
            char_dict_value = char_dict[char_dict_key]
            if isinstance(char_dict_value, str):    # if contraction/word
                keyboard_layout.write(char_dict_value)
            else:                                   # rest are tuples of length >=1
                keyboard.press(*char_dict_value)

        keyboard.release_all()
        time.sleep(0.12)    # inside the 'if' so 'while' can catch the keypresses @ any time

