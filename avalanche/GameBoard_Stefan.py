import random

import pygame

BLACK = (0, 0, 0)

gameBoardWidth = 12  # Width of board in blocks
gameBoardHeight = 20  # Height of board in blocks
anim = [0 for y in range(11)]
pygame.init()
linesound = pygame.mixer.Sound("Assets/Sounds/clearline.wav")
linesound.set_volume(0.05)

activeBoardSquare = [[0 for y in range(gameBoardHeight)] for x in range(gameBoardWidth)]

activeBoardColour = [[0 for y in range(gameBoardHeight)] for x in range(gameBoardWidth)]

specialBoardSquare = [[0 for y in range(gameBoardHeight)] for x in range(gameBoardWidth)]

specialBoardImage = [[0 for y in range(gameBoardHeight)] for x in range(gameBoardWidth)]

# Gameboard class
class GameBoard():
    def __init__(self, colour, blockSize):
        self.bordercolour = colour
        self.score = 0
        self.numLines = 0
        self.lineToNextLevel = 0
        self.level = 1
        self.numSlowTime = 0
        self.slowTimeOn = False
        self.numSwap = 0
        self.swapShape = False
        self.blockSize = blockSize
        self.animTimer = 0
        for i in range(gameBoardWidth):
            for j in range(gameBoardHeight):
                activeBoardSquare[i][j] = False
                activeBoardColour[i][j] = (0, 0, 0)

        for i in range(len(anim)):
            anim[i] = pygame.image.load("Assets/Pics/anim_" + str(i) + ".png")

    def draw(self, screen):
        screen.blit(anim[self.animTimer], (300, 0))
        pygame.draw.rect(screen, self.bordercolour, [0, 0, gameBoardWidth * self.blockSize, gameBoardHeight * self.blockSize], 1)

        for i in range(gameBoardWidth):
            for j in range(gameBoardHeight):
                if activeBoardSquare[i][j]:
                    if specialBoardSquare[i][j]:
                        pygame.draw.rect(screen, activeBoardColour[i][j], [i*self.blockSize, j*self.blockSize, self.blockSize - 1, self.blockSize - 1], 0)
                        screen.blit(specialBoardImage[i][j], (i * self.blockSize, j * self.blockSize))
                    else:
                        pygame.draw.rect(screen, activeBoardColour[i][j], [i*self.blockSize, j*self.blockSize, self.blockSize - 1, self.blockSize - 1], 0)

        self.animTimer += 1
        if self.animTimer >= 11:
            self.animTimer = 0

    def checkLoss(self):
        for i in range(gameBoardWidth):
            if activeBoardSquare[i][0] == True:
                return True

        return False

    def checkLine(self, rowNum):  # checks if the line is active of not
        matching = True
        matchColour = activeBoardColour[0][rowNum]
        for i in range(gameBoardWidth):
            if activeBoardColour[i][rowNum] != matchColour:
                matching = False
            if activeBoardSquare[i][rowNum] == False:
                return False

        if matching:
            self.score += 10000
            self.numSlowTime += 5
            self.numSwap += 5
        return True

    def clearFullRows(self):  # eliminates the line under by making the row under inactive
        for j in range(gameBoardHeight):
            if self.checkLine(j):
                linesound.play()
                self.score += 100
                self.numLines += 1
                self.lineToNextLevel += 1
                if self.lineToNextLevel == 10:
                    self.level += 1
                    self.numSlowTime += 1
                    self.numSwap += 1
                    self.lineToNextLevel = 0
                for k in range(j, 1, - 1):
                    for i in range(gameBoardWidth):
                        if k == j:
                            if specialBoardSquare[i][k] == "Clock":
                                self.numSlowTime += 1

                            elif specialBoardSquare[i][k] == "Swap":
                                self.numSwap += 1

                            elif specialBoardSquare[i][k] == "bomb":
                                for x in range(i - 1, i + 2):
                                    for y in range(gameBoardHeight):
                                        if 0 < x < gameBoardWidth - 1:
                                            activeBoardSquare[x][y] = False
                                            specialBoardSquare[x][y] = ""
                                            activeBoardColour[x][y] = BLACK
                                            specialBoardImage[x][y] = 0

                        activeBoardSquare[i][k] = activeBoardSquare[i][k - 1]
                        activeBoardColour[i][k] = activeBoardColour[i][k - 1]

                for r in range(gameBoardWidth):
                    activeBoardSquare[r][0] = False
                    activeBoardColour[r][0] = BLACK
                self.infect()

    def infect(self):
        tempSpecialSpot = specialBoardSquare
        for i in range(gameBoardWidth):
            for j in range(gameBoardHeight):
                if specialBoardSquare[i][j] == "poison":
                    if i > 0:
                        if activeBoardSquare[i - 1][j] and random.randrange(3) == 0:
                            tempSpecialSpot[i - 1][j] = "poison"
                            specialBoardImage[i - 1][j] = pygame.image.load("Assets/Pics/PoisonBlock.png")

                    if i < gameBoardWidth - 1:
                        if activeBoardSquare[i + 1][j] and random.randrange(3) == 0:
                            tempSpecialSpot[i + 1][j] = "poison"
                            specialBoardImage[i + 1][j] = pygame.image.load("Assets/Pics/PoisonBlock.png")

                    if j > 0:
                        if activeBoardSquare[i][j - 1] and random.randrange(3) == 0:
                            tempSpecialSpot[i][j - 1] = "poison"
                            specialBoardImage[i][j - 1] = pygame.image.load("Assets/Pics/PoisonBlock.png")

                    if j < gameBoardHeight - 1:
                        if activeBoardSquare[i][j + 1] and random.randrange(3) == 0:
                            tempSpecialSpot[i][j + 1] = "poison"
                            specialBoardImage[i][j + 1] = pygame.image.load("Assets/Pics/PoisonBlock.png")

        for i in range(gameBoardWidth):
            for j in range(gameBoardHeight):
                specialBoardSquare[i][j] = tempSpecialSpot[i][j]