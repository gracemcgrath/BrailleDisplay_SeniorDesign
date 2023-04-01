# perkins_keys
# boot.py

import usb_hid
import usb_cdc

usb_cdc.disable()
print('~perkins_keys~')

# This is only one example of a gamepad descriptor, and may not suit your needs.
BRAILLE_REPORT_DESCRIPTOR = bytes((
    0x05, 0x41,        # Usage Page (Braille)
    0x09, 0x01,        # Usage (Braille Display)
    0xA1, 0x01,        # Collection (Application)
    0x09, 0x00, 0x02,  #     Usage (Braille Buttons)
    0x1A, 0x01, 0x02,  #     Usage Minimum (Braille Keyboard Dot 1)
    0x2A, 0x08, 0x02,  #     Usage Minimum (Braille Keyboard Dot 8)
    0x75, 0x01,        #     Report Size (1)
    0x95, 0x08,        #     Report Count (8)
    0x15, 0x00,        #     Logical Minimum (0)
    0x25, 0x01,        #     Logical Maximum (1)
    0x81, 0x02,        #     Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0xC0,              # End Collection
))
print('~~report descriptor good')
braille = usb_hid.Device(
    report_descriptor=BRAILLE_REPORT_DESCRIPTOR,
    usage_page=0x41,           # Braille
    usage=0x01,                # Braille Display
    report_ids=(0,),           # report_descriptor does not dpecify a report ID
    in_report_lengths=(1,),    # This braille display sends 1 byte = 8 bits, 1 bit for each braille-dot
    out_report_lengths=(0,),   # It does not receive any reports.
)
print('~~~device setup good')
usb_hid.enable((braille,))
print('~~~~enable good')
