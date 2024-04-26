"""
Name: Lucas Siemsen, Callia Yuan, Michael Yao
Date: 04/30/2024
Description: 
"""

import pygame
from collision import Collidable


class Duck:
    def __init__(self, groundheight):
        original_image = pygame.image.load('duck.png').convert_alpha() #intializing the duck sprite
        self.image = pygame.transform.scale(original_image,(60,60))
        self.rect = self.image.get_rect()
        self.rect.x = 60
        self.rect.y = groundheight-self.rect.height
        self.y_velocity = 0
        self.height = 60
        self.width = 60
        self.fell = False
        self.jumpHeight = 1200
        self.jump_time = 0
        self.dive_speed = 300
        self.underwater = False
        self.groundheight = groundheight
        self.score = 0
        self.double_score_active = False  # Flag to track double score power-up
        self.collidable = Collidable(self.image)

    def jump(self):
      if self.rect.y == self.groundheight - self.rect.height:  # Make sure the duck can only jump when it is on the ground
        self.y_velocity = -self.jumpHeight  

    def dive(self): 
      if self.rect.y == self.groundheight - self.rect.height: # Similar check as jump
        self.y_velocity = self.dive_speed  

    def fall(self):
        if self.rect.y > 0:
            if self.y_velocity > 0:
                self.y_velocity = -200 - self.jumpHeight / 3
            else:
                self.y_velocity -= 200 + self.jumpHeight / 3
            self.fell = True


    def update(self, deltaTime):
        self.y_velocity += 4400 * deltaTime  # Apply gravity
        new_y = self.rect.y + self.y_velocity * deltaTime
        # Check if the duck is below the ground
        if new_y + self.rect.height > self.groundheight:
            new_y = self.groundheight - self.rect.height  # Set the duck on the ground
            self.y_velocity = 0  # Stop vertical movement
        self.rect.y = new_y

    def draw_collision(self, collision_mask):
        self.collidable.draw(collision_mask, self.rect)
    


    def updateUnderWater(self, deltaTime):
        self.y_velocity -= -4400 * deltaTime  # Gravity effect
        self.rect.y += self.y_velocity * deltaTime
        if self.rect.y > 0:
            self.rect.y = 0
            self.underwater = False
            self.fell = False


    def draw(self, surface):  # draws the duck
        surface.blit(self.image,(self.rect.x , self.rect.y))

    def collides_with(self, rect):
    # Ensure the duck's rect is correctly set up for collision detection
        return self.rect.colliderect(rect)

