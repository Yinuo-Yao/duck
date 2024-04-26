import pygame

class Collidable:
    def __init__(self, surface):
        self.mask = pygame.mask.from_surface(surface)

    def draw(self, collision_surf, rect):
        collision_surf.draw(self.mask, rect.topleft)


def collides(mask1, mask2):
    return mask1.overlap(mask2, (0, 0)) is not None
