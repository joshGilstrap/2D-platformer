import pygame
from settings import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, direction, speed=7, color=YELLOW):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.direction = direction
        self.speed = speed
        self.time_alive = 0
        self.alive_threshold = 120
    
    def update(self, walls, enemies, projectiles):
        self.rect.x += self.speed * self.direction
        if self.time_alive >= self.alive_threshold:
            projectiles.remove(self)
            self.kill()
        
        wall_collisions = pygame.sprite.spritecollide(self, walls, False)
        if wall_collisions:
            projectiles.remove(self)
            self.kill()
        
        # enemy_collisions = pygame.sprite.spritecollide(self, enemies, False)
        # if enemy_collisions:
        #     projectiles.remove(self)
        #     self.kill()
            
        self.time_alive += 1