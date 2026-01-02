import pygame
import sys
from logger import log_state, log_event
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, ASTEROID_MAX_RADIUS, ASTEROID_MIN_RADIUS
from player import Player
from shot import Shot
from asteroid import Asteroid
from asteroidfield import AsteroidField

def main():
    '''
    Main function to run the Asteroids game.
    Initializes the game, handles the game loop, updates game objects,
    checks for collisions, and manages the score.
    Args:
        None
    Returns:
        None
    '''
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    gameclock = pygame.time.Clock()
    dt = 0
    score = 0
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    while True:
        log_state()
        dt = gameclock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        screen.fill("black")
        for player_update in updatable:
            player_update.update(dt=dt)
        
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                end_game("player_hit", score)
            if player.hits_boundary():
                end_game("window_boundary_hit", score)
        for asteroid in asteroids:
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    shot.kill()
                    gained_points = gain_points(asteroid)
                    score += int(gained_points)
                    print(f"Score: {score} points (+{gained_points})")
                    asteroid.split()
        show_score(screen, score)

        for player_draw in drawable:
            player_draw.draw(screen=screen)
        pygame.display.flip()
        

def end_game(message, score):
     '''
     Handle end of game scenario.
     Args:
            message (str): The reason for game termination.
            score (int): The final score of the player.
     Returns:
        None
     '''
     log_event(message)
     print("Game over")
     print(f"Score: {score} points")
     sys.exit()

def gain_points(asteroid):
    '''
    Gain points based on asteroid size. Smaller asteroids give more points.
    Args:
        asteroid (Asteroid): The asteroid that was destroyed.
    Returns:
        int: Points gained from destroying the asteroid.
    '''
    range = (ASTEROID_MAX_RADIUS - ASTEROID_MIN_RADIUS) / 10
    points = (ASTEROID_MAX_RADIUS - asteroid.radius) // range
    points = max(1, points)
    points = int(points * 10)
    return points
    
def show_score(screen, score):
    '''
    Display the current score on the game screen.
    Args:
        screen (pygame.Surface): The surface to draw the score on.
        score (int): The current score of the player.
    Returns:
        None
    '''
    font = pygame.font.Font('freesansbold.ttf', 16)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
if __name__ == "__main__":
    main()
