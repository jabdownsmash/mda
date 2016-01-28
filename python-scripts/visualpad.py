from p3.pad import Pad, Button, Stick
import pygame

def convertMain(x, y):
    return (int(x*60+170), int(y*60+170))

def convertC(x, y):
    return (int(x*60+370), int(y*60+170))

class VisualPad(Pad):
    def __init__(self, path):
        super().__init__(path)
        pygame.init()
        pygame.display.set_caption('Gamepad')
        self.windowSurfaceObj = pygame.display.set_mode((640, 480))
        self.fontObj = pygame.font.Font('freesansbold.ttf', 32)

        self.colorDict = {}
        self.colorDict['A'] = pygame.Color(0, 0, 0)
        self.colorDict['B'] = pygame.Color(0, 0, 0)
        self.colorDict['X'] = pygame.Color(0, 0, 0)
        self.colorDict['Y'] = pygame.Color(0, 0, 0)
        self.colorDict['L'] = pygame.Color(0, 0, 0)
        self.colorDict['R'] = pygame.Color(0, 0, 0)
        self.colorDict['Z'] = pygame.Color(0, 0, 0)

        # self.windowSurfaceObj.fill(pygame.Color(255, 255, 255))

        self.mainX = 0.5
        self.mainY = 0.5
        self.cX = 0.5
        self.cY = 0.5
        # pygame.draw.circle(self.windowSurfaceObj, (0, 255, 0), (200, 200), 30, 4)
        # pygame.draw.circle(self.windowSurfaceObj, (255, 0, 0), convert(self.mainX, self.mainY), 5)
        self.update_pygame()

    def update_pygame(self):
        self.windowSurfaceObj.fill(pygame.Color(255, 255, 255))
        yPos = 268
        xPos = 128
        spacing = 60
        # Color buttons
        for button in Button:
            if button.name in self.colorDict:
                buttonSurfaceObj = self.fontObj.render(button.name, False, self.colorDict[button.name])
                buttonRectObj = buttonSurfaceObj.get_rect()
                buttonRectObj.topleft = (xPos, yPos)
                self.windowSurfaceObj.blit(buttonSurfaceObj, buttonRectObj)

                xPos += spacing

        # Sticks
        pygame.draw.circle(self.windowSurfaceObj, (0, 255, 0), (200, 200), 30, 4)
        pygame.draw.circle(self.windowSurfaceObj, (255, 0, 0), convertMain(self.mainX, self.mainY), 5)
        pygame.draw.circle(self.windowSurfaceObj, (0, 255, 0), (400, 200), 30, 4)
        pygame.draw.circle(self.windowSurfaceObj, (255, 0, 0), convertC(self.cX, self.cY), 5)

        pygame.display.update()

    def press_button(self, button):
        super().press_button(button)
        if button.name in self.colorDict:
            self.colorDict[button.name] = pygame.Color(255, 0, 0)
        self.update_pygame()

    def release_button(self, button):
        super().release_button(button)
        if button.name in self.colorDict:
            self.colorDict[button.name] = pygame.Color(0, 0, 0)
        self.update_pygame()

    def press_trigger(self, trigger, amount):
        super().press_trigger(trigger, amount)

    def tilt_stick(self, stick, x, y):
        super().tilt_stick(stick, x, y)
        if stick.name == 'MAIN':
            self.mainX = x
            self.mainY = y
        if stick.name == 'C':
            self.cX = x
            self.cY = y

        self.update_pygame()
