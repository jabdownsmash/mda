import sys
from p3.pad import Pad,Button,Trigger,Stick

def clear(pad):
    for button in Button:
        pad.release_button(button)
    for trigger in Trigger:
        pad.press_trigger(trigger, 0)
    for stick in Stick:
        pad.tilt_stick(stick, 0.5, 0.5)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Usage: ' + sys.argv[0] + ' dolphin-home')
    home = sys.argv[1]
    pad = Pad(home + '/Pipes/pipe')
    clear(pad)