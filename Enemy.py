import pygame
from settings import *
from classes import Token

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed, direction, color=RED):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.gravity = 1
        self.direction = direction
        self.squished = False
        self.health = 2
        
        self.x_vel = 0
        self.y_vel = 0
        self.knockback_speed = 20
        
    
    def update(self, walls, tokens, hazards, projectiles):
        if self.squished:
            tokens.add(Token(self.rect.x + self.width // 4, self.rect.y + self.height // 4, 25, 25))
            self.kill()
        wall_collisions = pygame.sprite.spritecollide(self, walls, False)
        for wall in wall_collisions:
            if self.rect.left < wall.rect.right and self.rect.right > wall.rect.right and abs(self.rect.right - wall.rect.right) < self.width:
                self.rect.left = wall.rect.right
                self.direction *= -1
            if self.rect.right > wall.rect.left and self.rect.left < wall.rect.left and abs(self.rect.left - wall.rect.left) < self.width:
                self.rect.right = wall.rect.left
                self.direction *= -1
            if self.y_vel > 0 and self.rect.bottom > wall.rect.top:
                self.y_vel *= -1
                self.y_vel = 0
                self.rect.bottom = wall.rect.top
                
        hazard_collisions = pygame.sprite.spritecollide(self, hazards, False)
        for hazard in hazard_collisions:
            if self.rect.left < hazard.rect.right and self.rect.left > hazard.rect.left:
                self.rect.left = hazard.rect.right
            if self.rect.right > hazard.rect.left and self.rect.right < hazard.rect.right:
                self.rect.right = hazard.rect.left
            self.direction *= -1
        
        self.x_vel = self.speed * self.direction
        self.y_vel += self.gravity
        if self.y_vel > 20:
            self.y_vel = 20
        
        projectile_collisions = pygame.sprite.spritecollide(self, projectiles, False)
        for projectile in projectile_collisions:
            if self.rect.right > projectile.rect.left and self.rect.left < projectile.rect.left:
                self.x_vel = -self.knockback_speed
            else:
                self.x_vel = self.knockback_speed
            if self.health > 0:
                self.health -= 1
            else:
                self.squished = True
            projectile.time_alive = projectile.alive_threshold
        
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel