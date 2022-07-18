# Our block class
import random
import pygame

SPECIALBLOCKS = ["bomb", "clock", "swap", "poison"]


class Block:
    # Block class constructor
    def __init__(self, colour, gridXPosition, gridYPosition):
        self.colour = colour  # set colour
        self.gridXPosition = int(gridXPosition)  # set position
        self.gridYPosition = int(gridYPosition)
        self.size = 25  # set size

    def draw(self, screen):
        # Draw a rectangle to represent block
        pygame.draw.rect(screen, self.colour,
                         [self.gridXPosition * self.size, self.gridYPosition * self.size, self.size - 1, self.size - 1], 0)


class SpecialBlock(Block):
    bombImage = pygame.image.load("Assets/Pics/Bomb.png")
    clockImage = pygame.image.load("Assets/Pics/clock.png")
    swapImage = pygame.image.load("Assets/Pics/swap.png")
    poisonImage = pygame.image.load("Assets/Pics/PoisonBlock.png")


    def __init__(self, colour, gridXPosition, gridYPosition):
        super().__init__(colour, gridXPosition, gridYPosition)
        ranNum = random.randrange(len(SPECIALBLOCKS))
        self.type = SPECIALBLOCKS[random.randrange(len(SPECIALBLOCKS))]
        self.typeCheck()


    def draw(self, screen):
        # Draw a rectangle to represent block
        pygame.draw.rect(screen, self.colour, [self.gridXPosition * self.size, self.gridYPosition * self.size, self.size - 1, self.size - 1], 0)
        screen.blit(self.blockImage, (self.gridXPosition * self.size, self.gridYPosition * self.size))


    def typeCheck(self):
        if self.type == "bomb":
            self.blockImage = SpecialBlock.bombImage
        elif self.type == "clock":
            self.blockImage = SpecialBlock.clockImage
        elif self.type == "swap":
            self.blockImage = SpecialBlock.swapImage
        elif self.type == "poison":
            self.blockImage = SpecialBlock.poisonImage
