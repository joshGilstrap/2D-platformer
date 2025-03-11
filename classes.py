import pygame
from settings import *

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=BLUE):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        

class Token(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=PURPLE, value=10):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.value = value


class Hazard(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=GREY, direction="up"):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.direction = direction
        if direction == "up":
            pygame.draw.polygon(self.image, color, ([self.width // 2, 0],
                                                    [0, self.height],
                                                    [self.width, self.height]))
        elif direction == "down":
            pygame.draw.polygon(self.image, color, ([self.width // 2, self.height],
                                                    [0, 0],
                                                    [self.width, 0]))
        elif direction == "left":
            pygame.draw.polygon(self.image, color, ([0, 0],
                                                    [self.width, self.height // 2],
                                                    [0, self.height]))