
import sys, os, json
from p3.melee import Melee
from p3.addr import AddressObjects
from p3.mw import MemoryWatcher

inGame = False
toSave = []
preData = {}
saveNum = 0

player1Stocks = 3
player2Stocks = 3

def watcher (home):
    global inGame
    mww = MemoryWatcher(home + '/MemoryWatcher/MemoryWatcher')
    for address, value in mww:
        for name, pv in AddressObjects.get_by_address(address).parse_string(value):
            if name == "player1Stocks":
                player1Stocks = pv
                # print(value)
            if name == "player2Stocks":
                player2Stocks = pv
                # print(value)
            if name in ["player1Character","player2Character","stageID"]:
                preData[address] = value
        if inGame:
            toSave.append([address,value])
        yield (address, value)

def listener (name, value):
    pass
    # global inGame
    # if name[:5] == "contr":
    #     print(name,value)
    # if inGame:
    #     toSave.append([name,value])

    #     print(ao.name, " ", value)

def menuCallback(event, gameState):
    global inGame, toSave, saveNum
    # print("menu " + str(event.value))
    if event.value == 13 and inGame == False:
        inGame = True;
        toSave = []
        print('starting record')
    elif event.value != 13 and inGame == True:
    # elif event.value != 13 and inGame == True and (player1Stocks == 0 or player2Stocks == 0):
        inGame = False
        pathName = sys.argv[2] + str(saveNum) + ".json"
        while(os.path.exists(pathName)):
            saveNum += 1
            pathName = sys.argv[2] + str(saveNum) + ".json"
        # pickle.dump( toSave, open( pathName, "wb" ) )
        # toSave.insert(0, {
        #     'stage':gameState["stageID"],
        #     "player1":gameState["player1Character"],
        #     "player2":gameState["player2Character"]})
        preDataList = []
        for key, value in preData.items():
            preDataList.append((key,value))
        with open(pathName, 'w') as outfile:
            json.dump(preDataList + toSave, outfile)
        saveNum += 1
        print('ended record ' + pathName)
        # print(gameState)

if __name__ == '__main__':
    AddressObjects.init()

    if len(sys.argv) != 3:
        sys.exit('Usage: ' + sys.argv[0] + ' dolphin-home savepath')
    home = sys.argv[1]

    # if not os.path.exists(home + '/MemoryWatcher/Locations.txt'):
    with open(home + '/MemoryWatcher/Locations.txt', 'w') as file:
        file.write(AddressObjects.locations_txt)

    melee = Melee()

    melee.add_listener("currentMenu",menuCallback)
    melee.listen(watcher(home),listener)