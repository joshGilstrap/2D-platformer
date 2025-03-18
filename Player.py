import pygame
from settings import *
from Projectile import Projectile

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.speed = 5
        self.jump_height = 15
        self.gravity = 1
        self.acceleration = 0.5
        self.max_speed = 10
        self.facing_direction = "right"
        self.score = 0
        
        self.x_vel = 0
        self.y_vel = 0
        self.is_jumping = False
        self.has_double_jumped = False
        
        self.is_wall_sliding = False
        self.wall_direction = None
        self.on_platform = False
        
        self.health = 3
        self.dead = False
        self.is_damaged = False
        self.invincibility_timeframe = 60
        self.invincibility_timer = 60
        
        self.projectile_max = 5
        self.can_fire = True
        self.fire_timer = 15
        self.fire_threshold = 15
    
    def handle_wall_collisions(self, walls):
        self.is_wall_sliding = False
        wall_collisions = pygame.sprite.spritecollide(self, walls, False)
        for wall in wall_collisions:
            collide_left = self.rect.right > wall.rect.left and self.rect.left > wall.rect.left
            collide_right = self.rect.left < wall.rect.right and self.rect.right > wall.rect.right
            collide_top = self.rect.bottom > wall.rect.top and self.rect.top < wall.rect.top -25
            collide_bottom = self.rect.top < wall.rect.bottom and self.rect.bottom > wall.rect.bottom
            if self.x_vel < 0 and collide_right and not collide_top and not collide_bottom:
                self.rect.left = wall.rect.right
                self.x_vel *= -1
                self.x_vel = 0
                self.is_wall_sliding = True
                self.wall_direction = 'left'
                self.facing_direction = "left"
            if self.x_vel > 0 and collide_left and not collide_top and not collide_bottom:
                self.rect.right = wall.rect.left
                self.x_vel *= -1
                self.x_vel = 0
                self.is_wall_sliding = True
                self.wall_direction = 'right'
                self.facing_direction = "right"
            if self.y_vel > 0 and collide_top and not collide_bottom:
                self.y_vel *= -1
                self.y_vel = 0
                self.rect.bottom = wall.rect.top
                self.is_jumping = False 
                self.has_double_jumped = False
                self.on_platform = True
            if self.y_vel < 0 and collide_bottom and not self.is_wall_sliding:
                self.y_vel *= -1
                self.y_vel = 0
                self.rect.top = wall.rect.bottom
                self.is_jumping = True
                self.has_double_jumped = True
                self.on_platform = False
            
            if self.on_platform:
                self.is_wall_sliding = False
            
            if self.is_wall_sliding:
                if self.y_vel > 0:
                    self.y_vel = 2
            
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    if self.wall_direction == 'left':
                        self.x_vel = self.jump_height // 2
                    elif self.wall_direction == 'right':
                        self.x_vel = -self.jump_height // 2
                    self.y_vel = -self.jump_height
                    self.is_jumping = True
                    self.has_double_jumped = False
                    self.on_platform = False
    
    def handle_enemy_collisions(self, enemies):
        enemy_collisions = pygame.sprite.spritecollide(self, enemies, False)
        for enemy in enemy_collisions:
            collide_left = self.rect.right > enemy.rect.left and abs(self.rect.right - enemy.rect.right) < self.width and self.rect.x > enemy.rect.x
            collide_right = self.rect.left < enemy.rect.right and abs(self.rect.left - enemy.rect.left) < self.width and self.rect.x < enemy.rect.x
            collide_top = self.rect.bottom > enemy.rect.top and abs(self.rect.top - enemy.rect.top) < self.height
            collide_bottom = self.rect.top < enemy.rect.bottom and abs(self.rect.bottom - enemy.rect.bottom) < self.height
            if collide_right and self.y_vel == 0:
                self.x_vel = -self.jump_height // 2
                if self.invincibility_timer >= self.invincibility_timeframe:
                    self.handle_damage()
            if collide_left and self.y_vel == 0:
                self.x_vel = self.jump_height // 2
                if self.invincibility_timer >= self.invincibility_timeframe:
                    self.handle_damage()
            if self.y_vel > 0 and collide_top:
                if self.x_vel == 0:
                    self.x_vel = 0
                elif self.facing_direction == 'left':
                    self.x_vel = -self.jump_height // 2
                elif self.facing_direction == 'right':
                    self.x_vel = self.jump_height // 2
                self.y_vel = -self.jump_height
                self.is_jumping = True
                self.has_double_jumped = False
                self.on_platform = False
                enemy.squished = True
                self.score += 10
    
    def handle_hazard_collisions(self, hazards):
        hazard_collisions = pygame.sprite.spritecollide(self, hazards, False)
        for hazard in hazard_collisions:
            true_collision = False
            if abs(self.rect.right - hazard.rect.right) < self.width and self.rect.left < hazard.rect.left:
                if self.on_platform:
                    self.x_vel = -self.jump_height // 1.5
                    true_collision = True
                else:
                    self.x_vel = self.jump_height // 1.5
                    true_collision = True
            elif abs(self.rect.left - hazard.rect.left) < self.width and self.rect.left > hazard.rect.left:
                if self.on_platform:
                    self.x_vel = self.jump_height // 1.5
                    true_collision = True
                else:
                    self.x_vel = -self.jump_height // 1.5
                    true_collision = True
            
            if true_collision and not self.is_damaged:
                if self.invincibility_timer >= self.invincibility_timeframe:
                    self.handle_damage()
                
                if hazard.direction == 'down':
                    self.y_vel = self.jump_height
                else:
                    self.y_vel = -self.jump_height
                self.is_jumping = True
                self.has_double_jumped = False
                self.on_platform = False
    
    def handle_damage(self):
        if not self.is_damaged:
            self.health -= 1
            if self.health < 0:
                self.dead = True
            
            self.invincibility_timer = 0
    
    def invincibility(self):
        if self.invincibility_timer < self.invincibility_timeframe and not self.is_damaged:
            self.is_damaged = True
            self.invincibility_timer += 1
        else:
            self.is_damaged = False
    
    def draw(self):
        if self.is_damaged:
            if self.invincibility_timer % 5 == 0:
                self.image.fill(GREEN)
            else:
                self.image.fill(WHITE)

    def update(self, walls, enemies, tokens, hazards, projectiles, level_width, level_height):
        self.invincibility()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_vel -= self.acceleration
            if self.x_vel < -self.max_speed:
                self.x_vel = -self.max_speed
            self.facing_direction = "left"
        elif keys[pygame.K_RIGHT]:
            self.x_vel += self.acceleration
            if self.x_vel > self.max_speed:
                self.x_vel = self.max_speed
            self.facing_direction = "right"
        else:
            if self.x_vel > 0:
                self.x_vel -= self.acceleration
                if self.x_vel < 0:
                    self.x_vel = 0
            elif self.x_vel < 0:
                self.x_vel += self.acceleration
                if self.x_vel > 0:
                    self.x_vel = 0
        if keys[pygame.K_f] and len(projectiles) <= self.projectile_max and self.fire_timer >= self.fire_threshold:
            self.fire_timer = 0
            direction = -1
            if self.facing_direction == "right":
                direction = 1
            projectiles.add(Projectile(self.rect.centerx, self.rect.centery, 10, 5, direction, 12))
        
        if self.fire_timer < self.fire_threshold:
            self.fire_timer += 1
        
        self.handle_wall_collisions(walls)
        
        self.handle_enemy_collisions(enemies)
        
        token_collisions = pygame.sprite.spritecollide(self, tokens, False)
        for token in token_collisions:
            self.score += token.value
            token.kill()
        
        self.handle_hazard_collisions(hazards)
        
        self.y_vel += self.gravity
        if self.y_vel > 20:
            self.y_vel = 20
        
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
        
        if self.rect.y >= level_height + self.height:
            self.dead = True
        
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > level_width - self.width:
            self.rect.x = level_width - self.width