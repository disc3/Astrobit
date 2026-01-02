import pygame
from constants import PLAYER_SPEED
# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    '''
    Base class for circular game objects.
    Inherits from pygame.sprite.Sprite and includes position, velocity, and radius attributes.
    Args:
        x (float): Initial x-coordinate of the object.
        y (float): Initial y-coordinate of the object.
        radius (float): Radius of the circular object.
    Returns:
        None
    '''
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # must override
        pass

    def update(self, dt):
        # must override
        pass
    
    def collides_with(self, other):
        '''
        Check if this CircleShape collides with another CircleShape.
        Args:
            other (CircleShape): Another CircleShape object to check collision against.
        Returns:
            bool: True if the two CircleShapes collide, False otherwise.
        '''
        return (abs(self.position.distance_to(other.position)) - abs(self.radius + other.radius)) <= 0 