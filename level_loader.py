import pygame
import json
from Player import Player
from Enemy import Enemy
from classes import Wall, Token, Hazard

levels = []
level_data = None
with open('levels.json', 'r') as f:
    level_data = json.load(f)

def load_level(level):
    walls = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    tokens = pygame.sprite.Group()
    hazards = pygame.sprite.Group()
    player = None
    
    for obj in level:
        if obj == "walls":
            for wall in level[obj]:
                walls.add(Wall(wall['x'], wall['y'], wall['width'], wall['height']))
        elif obj == 'player':
            for value in level[obj]:
                player = Player(value['x'], value['y'], value['width'], value['height'])
        elif obj == 'enemies':
            for enemy in level[obj]:
                enemies.add(Enemy(enemy['x'], enemy['y'], enemy['width'], enemy['height'], enemy['speed'], enemy['dir'], enemy['color']))
        elif obj == 'tokens':
            for token in level[obj]:
                tokens.add(Token(token['x'], token['y'], token['width'], token['height'], token['color'], token['value']))
        elif obj == 'hazards':
            for hazard in level[obj]:
                hazards.add(Hazard(hazard['x'], hazard['y'], hazard['width'], hazard['height'], hazard['color'], hazard['direction']))
    total_level_width = level['level_width']
    total_level_height = level['level_height']
    print(total_level_width, total_level_height)
    
    return walls, enemies, tokens, hazards, player, total_level_width, total_level_height

def load_all_levels(filename):
    global levels
    
    levels = []
    for level in level_data['levels']:
        walls, enemies, tokens, hazards, player, total_level_width, total_level_height = load_level(level)
        levels.append({
            "name": level["name"],
            "index": level["index"],
            "walls": walls,
            "enemies": enemies,
            "tokens": tokens,
            "hazards": hazards,
            "player": player,
            "total_level_width": total_level_width,
            "total_level_height": total_level_height
        })
    return levels

def load_single_level(index):
    level = level_data['levels'][index]
    walls, enemies, tokens, hazards, player, total_level_width, total_level_height = load_level(level)
    return walls, enemies, tokens, hazards, player, total_level_width, total_level_height
    