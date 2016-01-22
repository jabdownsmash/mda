
import sys, os, json, pickle
import struct
from p3.melee import Melee
from p3.addr import AddressObjects
from sknn.mlp import Regressor, Layer
import numpy as np
from sklearn.preprocessing import StandardScaler

acceptedInputs = [
    "player1ActionState",
    # "player1Percent",
    # "player1JumpsUsed",
    # "player1InAir",
    # "player1X",
    # "player1Y",
    # "player1Facing",
    # "player1GroundVelocityX",
    # "player1AirVelocityX",
    # "player1AirVelocityY",
    # "player1AttackVelocityX",
    # "player1AttackVelocityY",

    "player2ActionState",
    # "player2Percent",
    # "player2JumpsUsed",
    # "player2InAir",
    # "player2X",
    # "player2Y",
    # "player2Facing",
    # "player2GroundVelocityX",
    # "player2AirVelocityX",
    # "player2AirVelocityY",
    # "player2AttackVelocityX",
    # "player2AttackVelocityY",
]

acceptedOutputs = [
    "controller2A",
    "controller2B",
    "controller2X",
    "controller2Y",
    "controller2DigitalL",
    "controller2DigitalR",
    "controller2AnalogR",
    "controller2AnalogL",
    "controller2Z",
    "controller2ControlX",
    "controller2ControlY",
    "controller2CX",
    "controller2CY",
]

gameState = [0 for i in acceptedInputs]
controllerState = [0 for i in acceptedOutputs]

def listener (evName, value,inputs,outputs):
    global gameState,controllerState
    if type(value) is bool:
        value = 1 if value else 0
    if evName in acceptedInputs:
        gameState[acceptedInputs.index(evName)] = value
    if evName in acceptedOutputs:
        controllerState[acceptedOutputs.index(evName)] = value
    if evName == "globalFrameCounter":
        inputs.append(gameState)
        outputs.append(controllerState)
        gameState = [i for i in gameState]
        controllerState = [i for i in controllerState]
    # if evName == "controller1ControlX":
    #     print(value)

if __name__ == '__main__':

    AddressObjects.init()

    if len(sys.argv) < 2:
        sys.exit('Usage: ' + sys.argv[0] + ' savepath (outputpath)')
    path = sys.argv[1]

    formattedReplay = []

    for path in sys.argv[1:]:
        replay = json.load( open( path, "r" ) )

        for name, val in replay:
            formattedReplay.append([name,val])

    melee = Melee()

    # gameState = [0 for i in acceptedInputs]
    # controllerState = [0 for i in acceptedOutputs]
    inputs = []
    outputs = []

    melee.listen(formattedReplay,lambda x, y: listener(x,y, inputs,outputs))

    # with open(sys.argv[2], 'w') as outfile:     
    #     json.dump(inputs + outputs, outfile)    
    nn = Regressor(     
    layers=[         
    # Layer("Sigmoid",units=100),         
    Layer("Sigmoid", units=200),         
    Layer("Linear")], learning_rate=0.02, n_iter=80)

    inScaler = StandardScaler()
    npin = np.array(inputs)
    inScaler.fit(npin)
    npout = np.array(outputs)
    # print(insc)
    # for i in inScaler.transform(npin):
    #     print(i)
    nn.fit(inScaler.transform(npin),npout)
    pickle.dump((acceptedInputs,nn), open('nn4.pkl', 'wb'))
    # print(nn.predict(i for i in inputs[10]))
    # for i in inputs:
    #     print(nn.predict(np.array([i]))[0][9])
        # print(nn.predict(np.array([inputs[2]]))[0][0])
    print(len(inputs))
    print(len(outputs))
