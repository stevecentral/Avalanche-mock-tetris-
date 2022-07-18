# Import libraries
import pygame
import time

from Button_Stefan import Button
from GameBoard_Stefan import GameBoard, gameBoardHeight
from Shape_Stefan import Shape

# Define some colours RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
TURQUOISE = (0, 206, 209)

ALLCOLOURS = [WHITE, GREEN, RED, BLUE, YELLOW, MAGENTA, TURQUOISE, BLACK]

# ------------- INITIALIZATION ------------------
if __name__ == "__main__":
    # Set cursor
    pygame.mouse.set_cursor(*pygame.cursors.tri_left)
    # Initialize the game engine
    pygame.init()
    # sound mixer
    pygame.mixer.init()
    # Set the size of the window 800px by 600px
    size = (800, 600)
    # Set block attributes
    screen = pygame.display.set_mode(size)
    # play button
    playButton = Button(300, 200, 200, 50, "PLAY")
    # mode button
    modeButton = Button(300, 275, 200, 50, "EASY")

    # Our first shape
    shape = Shape(False)

    nextShape = Shape(False)
    gameBoard = GameBoard(WHITE, 25)
    name = ""
    pygame.display.set_caption("Avalanche - by Stefan")

    delay = 0
    slowTimeDelay = 0
    pygame.mixer.music.load('Assets/Sounds/tetristheme.wav')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
    # Whether the game has started or not
    started = False
    # Game condition
    done = False
    # Whether or not we are playing
    playing = False
    # FONTS
    myfont = pygame.font.Font('freesansbold.ttf', 30)
    HSfont = pygame.font.Font('freesansbold.ttf', 20)
    # Access the highscore files
    HSfile = open("HighScores.txt", "r")


    nameList = [0 for y in range(5)]
    scoreList = [0 for y in range(5)]
    for i in range(5):
        nameList[i] = HSfile.readline().rstrip('\n')
    for i in range(5):
        scoreList[i] = HSfile.readline().rstrip('\n')

    HSfile.close()

def checkKey():
        if event.key == pygame.K_LEFT:
            shape.moveLeft()

        elif event.key == pygame.K_RIGHT:
            shape.moveRight()

        elif event.key == pygame.K_DOWN:
            shape.rotateCCW()

        elif event.key == pygame.K_UP:
            shape.rotateCW()

        elif event.key == pygame.K_s:
            shape.moveDown()

        elif event.key == pygame.K_SPACE:
            shape.drop()
            gameBoard.score += (gameBoardHeight - shape.blockList[0].gridYPosition)

        elif event.key == pygame.K_1 and gameBoard.numSlowTime > 0:
            gameBoard.numSlowTime -= 1
            gameBoard.slowTimeOn = True

        elif event.key == pygame.K_2 and gameBoard.numSwap > 0:
            gameBoard.numSwap -= 1
            gameBoard.swapShape = True

        elif event.key == pygame.K_ESCAPE:
            pause()

        elif event.key == pygame.K_m:
            if pygame.mixer.music.get_volume() > 0:
                pygame.mixer.music.set_volume(0)
            else:
                pygame.mixer.music.set_volume(0.1)


def drawScreen():
        # Where we draw and add color
        screen.fill(BLACK)
        shape.draw(screen)
        nextShape.drawNextShape(screen)
        gameBoard.draw(screen)
        scoretext = myfont.render("Score: " + str(gameBoard.score), 1, WHITE)
        screen.blit(scoretext, (400, 10))
        linesText = myfont.render("Lines: " + str(gameBoard.numLines), 1, WHITE)
        screen.blit(linesText, (400, 270))
        levelText = myfont.render("level: " + str(gameBoard.level), 1, WHITE)
        screen.blit(levelText, (400, 320))

        # Display Power ups
        powerUpText = myfont.render("Power Ups: ", 1, WHITE)
        screen.blit(powerUpText, (50, 525))

        # display number of slow time Power ups available
        numSlowTimeText = myfont.render(" x" + str(gameBoard.numSlowTime), 1, WHITE)
        screen.blit(numSlowTimeText, (310, 525))
        slowTime_image = pygame.image.load("Assets/Pics/CLOCK (2).png")
        screen.blit(slowTime_image, (250, 515))

        # display number of swap piece Power ups available
        numSwapText = myfont.render(" x" + str(gameBoard.numSwap), 1, WHITE)
        screen.blit(numSwapText, (435, 525))
        swap_image = pygame.image.load("Assets/Pics/SWAP (2).png")
        screen.blit(swap_image, (375, 515))

        # Display next shape
        nextShapeText = myfont.render("Next: ", 1, WHITE)
        screen.blit(nextShapeText, (400, 60))
        pygame.draw.rect(screen, WHITE, [400, 110, 6*shape.blockList[0].size, 6*shape.blockList[0].size], 1)

        # Display the high score
        highScoreText = myfont.render("High Scores", 1, WHITE)
        screen.blit(highScoreText, (575,50))
        pygame.draw.rect(screen, WHITE, [575, 100, 200, 400], 1)
        for i in range(5):
            hsnametext = HSfont.render(str(nameList[i]), 1, WHITE)
            hsscoretext = HSfont.render(str(scoreList[i]), 1, WHITE)
            screen.blit(hsnametext, (580, i*25 + 125))
            screen.blit(hsscoretext, (700, i*25 + 125))
        # Display Name
        playerNameText = myfont.render("Player: " + name, 1, WHITE)
        screen.blit(playerNameText, (515, 525))
        pygame.display.flip()  # Redraws screen

# ---------- Title Screen -----------
while not playing:

    titleScreen1 = pygame.image.load("Assets/Pics/Backdrop2.png")
    titleScreen2 = pygame.image.load("Assets/Pics/Backdrop1.png")

    if not started:
        screen.blit(titleScreen2, (0, 0))
        playButton.draw(screen)  # draws our play button
        pygame.time.delay(100)
        modeButton.draw(screen)  # draws our mode button
    else:
        screen.blit(titleScreen1, (0, 0))
        enterNameText = myfont.render("Enter Your Name: ", 1, WHITE)
        nameText = myfont.render(name, 1, WHITE)
        screen.blit(enterNameText, (200, 200))
        screen.blit(nameText, (300, 250))

    pygame.display.flip()

    # ------- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            playing = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if playButton.checkHover():
                started = True
                if modeButton.string == "SPECIAL":
                    shape.specialMode = True

            if modeButton.checkHover():
                if modeButton.string == "EASY":
                    modeButton.setText("MEDIUM")
                elif modeButton.string == "MEDIUM":
                    modeButton.setText("HARD")
                elif modeButton.string == "HARD":
                    modeButton.setText("SPECIAL")
                elif modeButton.string == "SPECIAL":
                    modeButton.setText("PRACTICE")
                elif modeButton.string == "PRACTICE":
                    modeButton.setText("EASY")

        if event.type == pygame.KEYDOWN:
            if event.key >= 33 and event.key <= 126 and len(name) <= 10:
                name = name + chr(event.key) # add character to name

            if event.key == pygame.K_BACKSPACE: # removes a character from name
                    name = name[:-1]

            if event.key == pygame.K_RETURN:
                if name == "":
                    name = "Player1"
                started = False
                playing = True

# ---------- Main Game Loop -----------
def checkHighScores():
    newHighScores = False
    tempNameList = [0 for y in range(5)]
    tempScoreList = [0 for y in range(5)]

    for i in range(5):
        if gameBoard.score > int(scoreList[i]) and newHighScores == False:
            newHighScores = True
            tempScoreList[i] = gameBoard.score
            tempNameList[i] = name

        elif newHighScores == True:
            tempNameList[i] = nameList[i - 1]
            tempScoreList[i] = scoreList[i - 1]

        else:
            tempNameList[i] = nameList[i]
            tempScoreList[i] = scoreList[i]

    for i in range(5):
        scoreList[i] = tempScoreList[i]
        nameList[i] = tempNameList[i]

    # Open and write a new file
    HSfile = open("HighScores.txt", "w")
    for i in range(5):
        HSfile.write(nameList[i] + ('\n'))

    for i in range(5):
        HSfile.write(str(scoreList[i]) + ('\n'))

def pause():
    pauseText = myfont.render("Paused", 1, WHITE)
    screen.blit(pauseText, (100, 275))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return



while not done:
    # ------ Main event loop
    for event in pygame.event.get():  # For every user action (KeyPress, QUIT, etc.)
        if event.type == pygame.QUIT:  # If user event is
            done = True  # Then game is done

        elif event.type == pygame.KEYDOWN:
            checkKey()

    delay += 1
    if delay >= 10:
        shape.fall()
        delay = 0
    print(delay)

    if gameBoard.slowTimeOn:
        slowTimeDelay += 1
        if slowTimeDelay > 50:
            slowTimeDelay = 0
            gameBoard.slowTimeOn = False

    if gameBoard.swapShape:
        shape = nextShape
        nextShape = Shape(modeButton.string == "SPECIAL")
        gameBoard.swapShape = False

    # if our shape is inactive, spawn a new shape
    if shape.active == False:
        gameBoard.clearFullRows()
        delay = 0
        slowTimeDelay = 0
        shape = nextShape
        nextShape = Shape(modeButton.string == "SPECIAL")

    if gameBoard.checkLoss():
        checkHighScores()
        gameBoard = GameBoard(WHITE, shape.blockList[0].size)
        delay = 0
        slowTimeDelay = 0
        shape = Shape(modeButton.string == "SPECIAL")
        nextShape = Shape(modeButton.string == "SPECIAL")
        shape.updateGhost()


    drawScreen()

    if modeButton.string == "EASY" or modeButton.string == "SPECIAL":
        if (0.11 - gameBoard.level * 0.01 >= 0):
            time.sleep(0.11 - gameBoard.level * 0.01 + gameBoard.slowTimeOn * 0.1)

    elif modeButton.string == "MEDIUM":
        if (0.11 - gameBoard.level * 0.02 >= 0):
            time.sleep(0.11 - gameBoard.level * 0.02 + gameBoard.slowTimeOn * 0.1)

    elif modeButton.string == "HARD":
        if (0.11 - gameBoard.level * 0.03 >= 0):
            time.sleep(0.11 - gameBoard.level * 0.03 + gameBoard.slowTimeOn * 0.1)

    elif modeButton.string == "PRACTICE":
            time.sleep(0.11 + gameBoard.slowTimeOn * 0.1)
