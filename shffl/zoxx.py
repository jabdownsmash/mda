
import sys,os
import math
import random
from PySide import QtCore, QtGui
from p3.state_manager import StateManager
from p3.state import State
from p3.memory_watcher import MemoryWatcher

class Container(QtGui.QWidget):
    def __init__(self, board, quitCB, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        quit = QtGui.QPushButton("Calibrate")
        quit.resize(75, 30)
        quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))

        QtCore.QObject.connect(quit, QtCore.SIGNAL("clicked()"),lambda:quitCB())
        # quit.show()
        # board.show()
        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(quit, 0, 0)
        gridLayout.addWidget(board, 1, 1, 2, 1)
        gridLayout.setColumnStretch(1, 10)
        self.setLayout(gridLayout)
        # self.show()

class Melee(QtGui.QWidget):
    def __init__(self, mouseCallback,closeCallback, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.rectangles = []
        self.texts = []
        self.kek = 0
        self.mcb = mouseCallback
        self.ccb = closeCallback


    def paintEvent(self,event):
        painter = QtGui.QPainter(self)

        for text in self.texts:
            painter.setPen(QtCore.Qt.white)
            painter.setFont(QtGui.QFont("Courier", 20, QtGui.QFont.Bold))
            painter.save()
            painter.translate(text[0], text[1])
            painter.drawText(self.rect(), text[2])
            painter.restore()

        for rect in self.rectangles:
            painter.setPen(QtCore.Qt.white)
            painter.setBrush(QtGui.QColor(*rect[4]))
            painter.drawRect(QtCore.QRect(rect[0], rect[1], rect[2], rect[3]))

        # painter.setPen(QtCore.Qt.NoPen)
        # painter.setBrush(QtCore.Qt.blue)
        # painter.save()
        # painter.translate(0, self.height())
        # painter.drawPie(QtCore.QRect(-35, -35, 70, 70), 0, 90 * 16)
        # painter.restore()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            x = event.pos().x()
            y = event.pos().y()
            self.mcb(x,y)
        self.update()

    def closeEvent(self, event):
        self.ccb()

def listener (state):
    pass
    # print(str(state.action_state) + " " + str(state.fastfall_velocity) + " " + str(state.vertical_velocity))
    if state.players[0].vertical_velocity < 0 and state.players[0].vertical_velocity > -state.players[0].fastfall_velocity:
        print('hey')


if __name__ == '__main__':

    if len(sys.argv) != 2:
        sys.exit('Usage: ' + sys.argv[0] + ' dolphin-home')
    home = sys.argv[1]

    state = State()
    sm = StateManager(state)

    # state.players[0].hitlag_counter_changed.append(listener)
    # state.players[0].vertical_velocity_changed.append(listener)

    locationsTxt = ''
    for i in sm.locations():
        locationsTxt += i + '\n'

    with open(home + '/MemoryWatcher/Locations.txt', 'w') as file:
        file.write(locationsTxt)

    done = False
    x1 = 0
    x2 = 100
    y1 = 0
    y2 = 0
    calibrating = 0

    def exitHandler():
        global done
        done = True

    def calibrate():
        global calibrating
        calibrating = 2

    def mouseHandler(x,y):
        global calibrating, x1, x2, y1, y2
        if calibrating == 2:
            x1 = x
            y1 = y
            calibrating -= 1
        elif calibrating == 1:
            x2 = x
            y2 = y
            calibrating -= 1

    app = QtGui.QApplication(sys.argv)
    board = Melee(mouseHandler, exitHandler)

    cont = Container(board,calibrate)
    cont.show()

    kek = [300,400,100,100,(255,0,0,100)]
    board.rectangles.append(kek)

    def listener2 (state):
        scale = (x2 - x1)/(88.47*2)
        kek[0] = state.players[0].x*scale + x1 + (x2 - x1)/2 - 50
        kek[1] = -state.players[0].y*scale - 50 + (y2 + y1)/2
        board.update()
    state.players[0].x_changed.append(listener2)
    # board.texts.append((200,350,"hello"))

    mww = MemoryWatcher(home + '/MemoryWatcher/MemoryWatcher')
    for returnValue in mww:
        if returnValue is not None:
            address, value = returnValue
            sm.handle(address,value)
        app.processEvents()
        if done:
            break

# sys.exit(app.exec_())

