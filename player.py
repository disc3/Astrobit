from circleshape import CircleShape
from shot import Shot
from constants import PLAYER_RADIUS, PLAYER_SHOOT_COOLDOWN_SECONDS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SPEED, SHOT_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT
import pygame

class Player(CircleShape):
    '''
    Player class representing the player's spaceship.
    Inherits from CircleShape and includes methods for drawing,
    updating position, rotating, moving, shooting, and boundary checking.
    Args:
        x (float): Initial x-coordinate of the player.
        y (float): Initial y-coordinate of the player.
    Returns:
        None
    '''

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown = 0

    def triangle(self):
        '''
        Calculate the vertices of the triangular representation of the player.
        Returns:
            list: A list of three pygame.Vector2 points representing the triangle vertices.
        '''
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        '''
        Draw the player's triangular shape on the given screen.
        Args:
            screen (pygame.Surface): The surface to draw the player on.
        Returns:
            None
        '''
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)
        
    def rotate(self, dt):
        '''
        Rotate the player sprite based on the time delta.
        Args:
            dt (float): Time delta in seconds.
        Returns:
            None
        '''
        self.rotation += (PLAYER_TURN_SPEED * dt)
        
    def update(self, dt):
        '''
        Update the player's state (movement, rotation, shooting) based on input and time delta.
        Args:
            dt (float): Time delta in seconds.
        Returns:
            None
        '''
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            if self.cooldown <= 0:
                self.shoot()
                self.cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        if keys[pygame.K_a]:
            self.rotate(dt * -1)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_s]:
            self.move(dt * -1)
        if keys[pygame.K_w]:
            self.move(dt)

        self.cooldown -= dt

    def move(self, dt):
        '''
        Move the player in the direction it is facing based on the time delta.
        Args:
            dt (float): Time delta in seconds.
        Returns:
            None
        '''
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector
        
    def shoot(self):
        '''
        Shoot a projectile in the direction the player is facing.
        Returns:
            None
        '''
        shot_fired = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        shot_fired.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
    
    def hits_boundary(self):
        '''
        Check if the player has hit the screen boundaries.
        Returns:
            bool: True if the player is out of bounds, False otherwise.
        '''
        return (self.position.x >= SCREEN_WIDTH or self.position.y >= SCREEN_HEIGHT 
             or self.position.x <= 0 or self.position.y <= 0)