"""
Name: Lucas Siemsen, Callia Yuan, Michael Yao
Date: 04/30/2024
Description: 
"""

import pygame
from collision import Collidable

class Obstacle:
    obstacle_sprite = pygame.image.load("iceberg_top.png")
    obstacle_bottom_sprite = pygame.image.load("iceberg_bottom.png")
    obstacle_aspect_ratio = obstacle_sprite.get_height() / obstacle_sprite.get_width()
    obstacle_bottom_aspect_ratio = obstacle_bottom_sprite.get_height() / obstacle_bottom_sprite.get_width()
    bottom_width_ratio = obstacle_bottom_sprite.get_width() / obstacle_sprite.get_width()


    def __init__(self, x, size, groundheight):
        self.x = x
        size = (size, size * Obstacle.obstacle_aspect_ratio)
        self.sprite = pygame.transform.scale(Obstacle.obstacle_sprite, size)
        bottom_size = size[0] * Obstacle.bottom_width_ratio
        bottom_size = (bottom_size, bottom_size * Obstacle.obstacle_bottom_aspect_ratio)
        self.bottom_sprite = pygame.transform.scale(Obstacle.obstacle_bottom_sprite, bottom_size)
        self.size = size 
        self.groundheight = groundheight
        self.rect = pygame.Rect(self.x, self.groundheight - self.size[1], size[0], size[1])  # Define the rectangle
        self.bottom_rect = pygame.Rect(self.x - 3, self.groundheight - 3, bottom_size[0], bottom_size[1])
        self.collidable = Collidable(self.sprite)

    def draw(self, gameDisplay):  # Draws the obstacle
        # pygame.draw.rect(gameDisplay, obstacle_Color, (self.x, self.groundheight - self.size, self.size, self.size))
        gameDisplay.blit(self.sprite, self.rect)
        gameDisplay.blit(self.bottom_sprite, self.bottom_rect)

    def draw_collision(self, collision_mask):
        self.collidable.draw(collision_mask, self.rect)

    def update(self, deltaTime, velocity):  # update the position of the obstacle
        self.x -= velocity * deltaTime
        self.bottom_rect.left = self.x - 3
        self.rect.left = self.x  # Update the left position of the rectangle

    def checkOver(self):  # checks if the obstacle is still on the screen
        if self.x < 0:
            return True
        else:
            return False
