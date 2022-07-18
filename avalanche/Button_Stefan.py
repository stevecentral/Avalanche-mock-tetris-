import random

import pygame


class Button():
    def __init__(self, x, y, width, height, string):
        self.isHovering = False
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.string = string
        self.text = pygame.font.Font('freesansbold.ttf', 20).render(self.string, 1, (255, 255, 255))

    # Draws button
    def draw(self, screen):
        randomColour = (random.randrange(255), random.randrange(255), random.randrange(255))

        pygame.draw.rect(screen, (255, 0, 0), [self.x, self.y, self.width, self.height], 3)
        screen.blit(self.text, (self.x + self.width / 2 - 6.1 * len(self.string), self.y + self.height / 2 - 10))
        if self.checkHover():
            pygame.draw.rect(screen, randomColour, [self.x, self.y, self.width, self.height], 10)
            screen.blit(self.text, (self.x + self.width / 2 - 6.1 * len(self.string), self.y + self.height / 2 - 10))

    def checkHover(self):
        if self.x < pygame.mouse.get_pos()[0] < self.x + self.width and self.y < pygame.mouse.get_pos()[1] < self.y + self.height:
            return True
        else:
            return False

    def setText(self, newText):
        self.string = newText
        self.text = pygame.font.Font('freesansbold.ttf', 20).render(self.string, 1, (255, 255, 255))
