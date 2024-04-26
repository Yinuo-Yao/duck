"""
Name: Lucas Siemsen, Callia Yuan, Michael Yao
Date: 04/30/2024
Description: 
"""

import pygame
from collision import Collidable

# Constants
POWERUP_DURATION = 10  # Duration of each power-up in seconds

jump_sprite = pygame.image.load("jump.png")

class Powerup:
    def _set_sprite(self, sprite):
        self.sprite = pygame.transform.scale(sprite, self.rect.size)

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.timer = 0  # Initialize the timer
        collision_surf = pygame.Surface(self.rect.size)
        collision_surf.fill((255, 255, 255, 255))
        self.collidable = Collidable(collision_surf)

    def draw(self, game_display):
        game_display.blit(self.sprite, self.rect)

    def draw_collision(self, collision_mask):
        self.collidable.draw(collision_mask, self.rect)

    def update(self, velocity):
        self.rect.x -= velocity

    def is_offscreen(self):
        return self.rect.right < 0

    def apply_effect(self, player):
        pass  # This method will be implemented by each specific power-up

    def update_timer(self, deltaTime):
        self.timer += deltaTime
        if self.timer >= POWERUP_DURATION:
            self.timer = 0  # Reset timer when duration is reached
            return True  # Indicate that the power-up duration has expired
        return False

class DoubleScorePowerup(Powerup):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)  # Gold color
        self._set_sprite(jump_sprite)

    def apply_effect(self, player):
        player.double_score_active = True

    def update_timer(self, deltaTime, player):  # Add 'player' argument here
        expired = super().update_timer(deltaTime)
        if expired:
            player.double_score_active = False
        return expired


class SpeedUpPowerup(Powerup):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)  # Green color
        self._set_sprite(jump_sprite)

    def apply_effect(self, player):
        return +30 #increase the speed by 30


class SlowDownPowerup(Powerup):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)  # Red color
        self._set_sprite(jump_sprite)

    def apply_effect(self, player):
        return -30 #decrease the speed by 30
