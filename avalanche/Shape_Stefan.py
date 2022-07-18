import random  # used to randomly generate a shape

import pygame

from Block_Stefan import Block, SpecialBlock
from GameBoard_Stefan import gameBoardWidth, activeBoardSquare, activeBoardColour, specialBoardSquare, \
    specialBoardImage
from GameBoard_Stefan import gameBoardHeight

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
TURQUOISE = (0, 206, 209)

ALLCOLOURS = [WHITE, GREEN, RED, BLUE, YELLOW, MAGENTA, TURQUOISE]

ZSHAPE = [[(gameBoardWidth / 2) - 1, 0], [(gameBoardWidth / 2) - 2, 0], [(gameBoardWidth / 2) - 1, 1],
          [gameBoardWidth / 2, 1]]

SSHAPE = [[(gameBoardWidth / 2) - 1, 0], [gameBoardWidth / 2, 0], [(gameBoardWidth / 2) - 2, 1],
          [(gameBoardWidth / 2) - 1, 1]]

LINESHAPE = [[(gameBoardWidth / 2) - 1, 0], [(gameBoardWidth / 2) - 2, 0], [(gameBoardWidth / 2), 0],
             [gameBoardWidth / 2 + 1, 0]]

SQUARESHAPE = [[(gameBoardWidth / 2) - 1, 0], [gameBoardWidth / 2, 0], [gameBoardWidth / 2, 1],
               [(gameBoardWidth / 2) - 1, 1]]

LSHAPE = [[(gameBoardWidth / 2) - 1, 1], [(gameBoardWidth / 2) - 1, 0], [(gameBoardWidth / 2) - 1, 2],
          [gameBoardWidth / 2, 2]]

MLSHAPE = [[gameBoardWidth / 2, 1], [gameBoardWidth / 2, 0], [gameBoardWidth / 2, 2], [(gameBoardWidth / 2) - 1, 2]]

TSHAPE = [[(gameBoardWidth / 2) - 1, 1], [(gameBoardWidth / 2) - 1, 0], [gameBoardWidth / 2, 1],
          [(gameBoardWidth / 2) - 2, 1]]

ALLSHAPES = [ZSHAPE, SSHAPE, LINESHAPE, SQUARESHAPE, LSHAPE, MLSHAPE, TSHAPE]


class Shape:
    # Constructor
    def __init__(self, special):
        self.isSpecial = special
        self.numBlock = 4
        randomNum = random.randrange(7)
        self.shape = ALLSHAPES[randomNum]
        self.colour = ALLCOLOURS[randomNum]
        randomType = random.randrange(3)
        self.blockList = []
        self.active = True

        for i in range(self.numBlock):
            if random.randrange(4) == 0 and self.isSpecial:
                self.blockList.append(SpecialBlock(self.colour, self.shape[i][0], self.shape[i][1]))
            else:
                self.blockList.append(Block(self.colour, self.shape[i][0], self.shape[i][1]))

        self.ghostDistance = 0
        self.updateGhost()

    def draw(self, screen):
        # draw ghost shape
        for i in range(self.numBlock):
            pygame.draw.rect(screen, self.blockList[i].colour, [self.blockList[i].gridXPosition * self.blockList[i].size, (self.blockList[i].gridYPosition + self.ghostDistance) * self.blockList[i].size, self.blockList[i].size - 1, self.blockList[i].size - 1], 3)

        # draw main shape
        for i in range(self.numBlock):
            self.blockList[i].draw(screen)


    def moveLeft(self):
        blocked = False


        for i in range(self.numBlock):
            if self.blockList[i].gridXPosition == 0 or activeBoardSquare[self.blockList[i].gridXPosition - 1][self.blockList[i].gridYPosition]:
                blocked = True
        if blocked == False:
            for i in range(self.numBlock):
                self.blockList[i].gridXPosition -= 1
        self.updateGhost()

    def moveRight(self):
        blocked = False
        for i in range(self.numBlock):
            if self.blockList[i].gridXPosition == gameBoardWidth - 1 or activeBoardSquare[self.blockList[i].gridXPosition + 1][self.blockList[i].gridYPosition]:
                blocked = True
        if blocked == False:
            for i in range(self.numBlock):
                self.blockList[i].gridXPosition += 1
        self.updateGhost()

    def moveDown(self):
        blocked = False  # it isn't touching the edge
        for i in range(self.numBlock):
            if self.blockList[i].gridYPosition == gameBoardHeight - 1 or activeBoardSquare[self.blockList[i].gridXPosition][self.blockList[i].gridYPosition + 1]:
                blocked = True

        if blocked == False:
            for i in range(self.numBlock):
                self.blockList[i].gridYPosition += 1
        self.updateGhost()

    def fall(self):
        for i in range(self.numBlock):
            if self.blockList[i].gridYPosition == gameBoardHeight - 1 or activeBoardSquare[self.blockList[i].gridXPosition][self.blockList[i].gridYPosition + 1]:
                self.hitBottom()

        for i in range(self.numBlock):
            if self.active:
                self.blockList[i].gridYPosition += 1
        self.updateGhost()

    def rotateCW(self):
        if self.shape:
            newBlockX = [0, 0, 0, 0]
            newBlockY = [0, 0, 0, 0]
            canRotate = True

            for i in range(self.numBlock):

                newBlockX[i] = - (self.blockList[i].gridYPosition - self.blockList[0].gridYPosition) + self.blockList[0].gridXPosition
                newBlockY[i] = (self.blockList[i].gridXPosition - self.blockList[0].gridXPosition) + self.blockList[0].gridYPosition

                if newBlockX[i] < 0 or newBlockX[i] >= gameBoardWidth - 1:
                    canRotate = False
                if newBlockY[i] < 0 or newBlockY[i] >= gameBoardHeight - 1:
                    canRotate = False
                if activeBoardSquare[newBlockX[i]][newBlockY[i]]:
                    canRotate = False

            if canRotate:
                self.blockList[i].gridXPosition = newBlockX[i]
                self.blockList[i].gridYPosition = newBlockY[i]
        self.updateGhost()

    def rotateCCW(self):
        if self.shape:
            newBlockX = [0, 0, 0, 0]
            newBlockY = [0, 0, 0, 0]
            canRotate = True
            for i in range(self.numBlock):

                newBlockX[i] = (self.blockList[i].gridYPosition - self.blockList[0].gridYPosition) + self.blockList[0].gridXPosition
                newBlockY[i] = - (self.blockList[i].gridXPosition - self.blockList[0].gridXPosition) + self.blockList[0].gridYPosition

                if newBlockX[i] < 0 or newBlockX[i] >= gameBoardWidth - 1:
                    canRotate = False
                if newBlockY[i] < 0 or newBlockY[i] >= gameBoardHeight - 1:
                    canRotate = False
                if activeBoardSquare[newBlockX[i]][newBlockY[i]]:
                    canRotate = False

            if canRotate:
                for i in range(self.numBlock):
                    self.blockList[i].gridXPosition = newBlockX[i]
                    self.blockList[i].gridYPosition = newBlockY[i]
        self.updateGhost()

    def hitBottom(self):
        for i in range(self.numBlock):
            activeBoardSquare[self.blockList[i].gridXPosition][self.blockList[i].gridYPosition] = True
            activeBoardColour[self.blockList[i].gridXPosition][self.blockList[i].gridYPosition] = self.blockList[i].colour

            if isinstance(self.blockList[i], SpecialBlock):
                specialBoardSquare[self.blockList[i].gridXPosition][self.blockList[i].gridYPosition] = self.blockList[i].type
                specialBoardImage[self.blockList[i].gridXPosition][self.blockList[i].gridYPosition] = self.blockList[i].blockImage
        self.active = False

    def drop(self):
        while self.active:
            for i in range(self.numBlock):
                if self.blockList[i].gridYPosition == gameBoardHeight - 1 or activeBoardSquare[self.blockList[i].gridXPosition][self.blockList[i].gridYPosition + 1]:
                    self.hitBottom()
            for i in range(self.numBlock):
                if self.active:
                    self.blockList[i].gridYPosition += 1

    def drawNextShape(self, screen):
        for i in range(self.numBlock):
            pygame.draw.rect(screen, self.blockList[i].colour, [self.blockList[i].gridXPosition * self.blockList[i].size + 325, self.blockList[i].gridYPosition * self.blockList[i].size  + 150,
                              self.blockList[i].size - 1, self.blockList[i].size - 1], 0)

    def updateGhost(self):
        updating = True
        d = 0
        while updating:
            for i in range(self.numBlock):
                if self.blockList[i].gridYPosition + d == gameBoardHeight - 1 or activeBoardSquare[self.blockList[i].gridXPosition][self.blockList[i].gridYPosition + d + 1] == True:
                    updating = False
                    self.ghostDistance = d
            d += 1