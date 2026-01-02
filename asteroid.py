from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event
import random
import pygame

class Asteroid(CircleShape):
    '''
    Asteroid class representing an asteroid in the game.
    Inherits from CircleShape and includes methods for drawing, updating position, and splitting into smaller asteroids.
    Args:
        x (float): Initial x-coordinate of the asteroid.
        y (float): Initial y-coordinate of the asteroid.
        radius (float): Radius of the asteroid.
    Returns:
        None
    '''
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        
    def draw(self, screen):
        '''
        Draw the asteroid's circular shape on the given screen.
        Args:
            screen (pygame.Surface): The surface to draw the asteroid on.
        Returns:
            None
        '''
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)
        
    def update(self, dt):
        '''
        Update the asteroid's position based on its velocity and time delta.
        Args:
            dt (float): Time delta in seconds.
        Returns:
            None
        '''
        self.position += (self.velocity * dt)
    
    def split(self):
        '''
        Split the asteroid into two smaller asteroids if its radius is above the minimum threshold.
        Kills the current asteroid.        
        Returns:
            None
        '''
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        random_angle = random.uniform(20, 50)
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        log_event("asteroid_split")
        asteroid1.velocity = self.velocity.rotate(random_angle) * 1.2
        asteroid2.velocity = self.velocity.rotate(random_angle * -1) * 1.2