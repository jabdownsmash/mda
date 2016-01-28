import sys, os, json
from p3.melee import Melee
from p3.addr import AddressObjects
from p3.mw import MemoryWatcher
from p3.pad import Pad,Button,Stick
import numpy as np
import pickle
from clear_inputs import clear
from visualpad import VisualPad

inGame = False
toSave = []
preData = {}
saveNum = 0

player1Stocks = 3
player2Stocks = 3

def press (button, value, pad):
    if value > .5:
        pad.press_button(button)
    else:
        pad.release_button(button)

def trunc(value):
    return (max(min(value,1),-1) + 1)/2

def listener (evName, value,acceptedInputs,nnGameState,nn,pad):
    # global nnGameState, acceptedInputs
    if evName in acceptedInputs:
        nnGameState[acceptedInputs.index(evName)] = value
    if evName == "globalFrameCounter":
        output = nn.predict(np.array([nnGameState]))[0]
        press(Button.A,output[0],pad)
        press(Button.B,output[1],pad)
        press(Button.X,output[2],pad)
        press(Button.Y,output[3],pad)
        press(Button.L,output[4],pad)
        press(Button.R,output[5],pad)
        press(Button.Z,output[8],pad)


        pad.tilt_stick(Stick.MAIN,trunc(output[9]),trunc(output[10]))
        pad.tilt_stick(Stick.C,trunc(output[11]),trunc(output[12]))


if __name__ == '__main__':
    global acceptedInputs
    AddressObjects.init()

    if len(sys.argv) != 3:
        sys.exit('Usage: ' + sys.argv[0] + ' dolphin-home savepath')
    home = sys.argv[1]

    with open(home + '/MemoryWatcher/Locations.txt', 'w') as file:
        file.write(AddressObjects.locations_txt)

    acceptedInputs, nn = pickle.load( open( sys.argv[2], "rb" ) )

    nnGameState = [0 for i in acceptedInputs]

    # print()
    melee = Melee()

    mww = MemoryWatcher(home + '/MemoryWatcher/MemoryWatcher')
    pad = VisualPad(home + '/Pipes/pipe')
    try:
        melee.listen(mww,lambda x, y: listener(x,y,acceptedInputs,nnGameState,nn,pad))
    except KeyboardInterrupt:
        # Set controller to neutral
        clear(pad)
        sys.exit()