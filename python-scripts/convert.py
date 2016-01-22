
import sys, pickle,os, json
from p3.melee import Melee
from p3.addr import AddressObjects
import msgpack, struct

inGame = False
toSave = []
saveNum = 0
names = []

def listener (evName, value,gameState,rows):
    # gameState[evName] = value
    if evName not in names:
        names.append(evName)
    if evName not in ["frameCount","globalFrameCounter"]:
        rows.append((names.index(evName),value))
    # print(value)
    # if(evName == 'player1Y'):
        # print(value)
    # if(evName == "globalFrameCounter" or ('player2Stocks' in gameState and gameState['player2Stocks'] > 0)):

if __name__ == '__main__':

    gameState = {}
    rows = []

    if len(sys.argv) < 2:
        sys.exit('Usage: ' + sys.argv[0] + ' savepath (outputpath)')
    path = sys.argv[1]


    # inputs = pickle.load( open( path, "rb" ) )
    inputs = json.load( (open( path, "r" )) )
    # print(inputs)

    for x in inputs:
        rows.append((x[0], hex(x[1])[2:]))

    if len(sys.argv) >= 3:
        outputPath = sys.argv[2]
        # outputPath2 = sys.argv[2] + ".mp"
        with open(outputPath, 'w') as outfile:
            # pickle.dump(rows, outfile)
            json.dump(rows, outfile)
            # msgpack.dump(rows,outfile)
        # with open(outputPath2, 'wb') as outfile2:
