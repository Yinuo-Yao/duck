"""
Name: Lucas Siemsen, Callia Yuan, Michael Yao
Date: 04/30/2024
Description: 
"""

import pygame
import random
from duck import Duck
from obstacle import Obstacle
from powerup import Powerup, DoubleScorePowerup, SpeedUpPowerup, SlowDownPowerup
from collision import collides

# Initialize Pygame
pygame.init()

# Initializing game
size = width, height = 800, 520

figma_width = 1280
ratio = width / figma_width

def from_figma_coords(coords):
    return (int(coords[0] * ratio), int(coords[1] * ratio))


gameDisplay = pygame.display.set_mode(size)
Ground_height = from_figma_coords((147.14 + 285, 0))[0]
velocity = 300
Min_Gap = 300
Max_Gap = 600
Obstacles = []
Powerups = []
powerupSpeed = 1
game_over = False
initializing = True
running = False  # Set to True when "Play" button is clicked
obstacles_passed = 0  # Counter to track the number of obstacles passed
powerup_spawn_timer = random.randint(5, 15)  # Initial random timer between 5 and 15 seconds

# Create instances
duck = Duck(Ground_height)



def make_grad_rect(top_col, bot_col, w, h):
    grad = pygame.Surface((2, 2))
    pygame.draw.line(grad, top_col, (0, 0), (1, 0))
    pygame.draw.line(grad, bot_col, (0, 1), (1, 1))
    grad = pygame.transform.smoothscale(grad, (w, h))
    return grad


top_col, bot_col = "#A1D3D7BF", "#408094BF"
full_grad_rect = make_grad_rect(top_col, bot_col, width, height)
ground_draw_height = from_figma_coords((0, 417))[1]
water_rect = make_grad_rect(top_col, bot_col, width, height - ground_draw_height)

water_rect.set_alpha(191)

def load_sprite(name, pos, res=2):
    sprite = pygame.image.load(name)
    new_size = sprite.get_rect().size
    new_size = (new_size[0] // res, new_size[1] // res)
    new_size = from_figma_coords(new_size)
    sprite = pygame.transform.smoothscale(sprite, new_size)

    rect = sprite.get_rect()
    rect.topleft = from_figma_coords(pos)
    return sprite, rect

play_button, play_button_rect = load_sprite("play_button.png", (497, 338), 1)
quit_button, quit_button_rect = load_sprite("quit.png", (610, 465), 2)

# Function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Gameover Screen
def show_game_over_screen():
    game_over_screen = True
    while game_over_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_pos):
                    return 'restart'
        gameDisplay.blit(full_grad_rect, (0, 0))
        # Display Game Over text
        draw_text('Game Over', title_font, (255, 0, 0), gameDisplay, width//2 - 100, height//4)
        draw_text(f'Final Score: {duck.score}', title_font, (0, 0, 0), gameDisplay, width//2 - 100, height//2 - 50)
        
        # Draw Restart Button
        restart_button = pygame.Rect(width//2 - 100, height//2 + 100, 200, 50)
        pygame.draw.rect(gameDisplay, (0, 200, 0), restart_button)
        draw_text('Restart', button_font, (255, 255, 255), gameDisplay, width//2 - 45, height//2 + 110)
        
        pygame.display.update()

# Main game loop
while initializing:
    # print("Initialization loop running")
    gameDisplay.blit(full_grad_rect, (0, 0))

    # Draw title
    title_font = pygame.font.SysFont(None, 48)
    draw_text('Duck Run', title_font, (0, 0, 0), gameDisplay, width//2 - 80, height//4)

    # Draw buttons
    gameDisplay.blit(play_button, play_button_rect)
    gameDisplay.blit(quit_button, quit_button_rect)

    # Draw text on buttons
    button_font = pygame.font.SysFont(None, 30)

    # Event handling for initialization screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            initializing = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if play_button_rect.collidepoint(mouse_pos):
                initializing = False
                running = True  # Start the game loop
                print("Game loop started")
            elif quit_button_rect.collidepoint(mouse_pos):
                initializing = False
                game_over = True

    pygame.display.update()

duck_collision_mask = pygame.mask.Mask((width, height), False)
obstacle_collision_mask = pygame.mask.Mask((width, height), False)
powerup_collision_mask = pygame.mask.Mask((width, height), False)

# Main game loop
lastFrame = pygame.time.get_ticks()  # Initialize lastFrame
while running:
    duck_collision_mask.clear()
    obstacle_collision_mask.clear()
    powerup_collision_mask.clear()

    # print("Game loop running")
    t = pygame.time.get_ticks()
    deltaTime = (t - lastFrame) / 1000.0
    lastFrame = t

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:  # Ensure this is a keyboard event before checking keys
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                # Check if the bottom of the duck is at ground level
                if duck.rect.bottom == Ground_height:
                    duck.jump()
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                # Similar check for diving
                if duck.rect.bottom == Ground_height:
                    duck.dive()


    gameDisplay.fill((255, 255, 255))  # White background

    if duck.underwater == False:
        duck.update(deltaTime)
    else:
        duck.updateUnderWater(deltaTime)

    # Draw duck
    duck.draw(gameDisplay)
    duck.draw_collision(duck_collision_mask)

    # Draw ground
    # pygame.draw.rect(gameDisplay, (159, 198, 238), (0, Ground_height, width, height - Ground_height))
    gameDisplay.blit(water_rect, (0, ground_draw_height))

    # Generate obstacles
    if len(Obstacles) == 0 or width - Obstacles[-1].x > Min_Gap:
        obstacle = Obstacle(width, random.randint(30, 50), Ground_height)
        Obstacles.append(obstacle)

    # Update and draw obstacles
    for obstacle in Obstacles:
        obstacle.update(deltaTime, velocity)  # Pass velocity here
        obstacle.draw(gameDisplay)
        obstacle.draw_collision(obstacle_collision_mask)

        if obstacle.x < -obstacle.size[0]:  # Adjusted condition
            Obstacles.remove(obstacle)
            obstacles_passed += 1
            if obstacles_passed % 10 == 0:  # Check if 10 obstacles have been passed
                velocity += 30  # Increase velocity by 30

            if duck.double_score_active:  # Check if double score power-up is active
                duck.score += 2  # Double the score accumulation
            else:
                duck.score += 1  # Regular score accumulation

    if collides(duck_collision_mask, obstacle_collision_mask):
        action = show_game_over_screen()
        if action == 'restart':
            # Reset game state
            duck = Duck(Ground_height)  # Reset the duck
            Obstacles = []  # Clear obstacles
            Powerups = []  # Clear powerups
            velocity = 300  # Reset velocity
            obstacles_passed = 0  # Reset obstacles passed
            duck.score = 0  # Reset score
            running = True  # Restart the game
        else:
            running = False
        continue

    # Update the power-up spawn timer
    powerup_spawn_timer -= deltaTime
    if powerup_spawn_timer <= 0:
        # Spawn a new power-up
        powerup_type = random.choice([DoubleScorePowerup, SpeedUpPowerup, SlowDownPowerup])
        powerup = powerup_type(width, Ground_height - 150, 20, 20)
        Powerups.append(powerup)
        # Reset the timer for the next power-up spawn
        powerup_spawn_timer = random.randint(5, 15)

    # Generate power-ups
    if random.random() < 0.0005:
        powerup_type = random.choice([DoubleScorePowerup, SpeedUpPowerup, SlowDownPowerup])
        powerup_y = Ground_height - 150  # Adjust y-coordinate
        powerup = powerup_type(width, powerup_y, 20, 20)  # Spawn power-up higher
        Powerups.append(powerup)

    # Update and draw power-ups
    for powerup in Powerups:
        powerup.update(powerupSpeed)
        powerup.draw(gameDisplay)
        powerup.draw_collision(powerup_collision_mask)

        if duck.collides_with(powerup.rect):
            powerup.apply_effect(duck)
            Powerups.remove(powerup)
        if powerup.rect.x < 0:
            Powerups.remove(powerup)

    if isinstance(Powerup, DoubleScorePowerup):  # Check if it's a DoubleScorePowerup
        if powerup.update_timer(deltaTime, duck):  # Pass the 'duck' player instance
            Powerups.remove(powerup)  # Remove the power-up if its duration has expired


        # Update the power-up timer for DoubleScorePowerup
        if isinstance(Powerup, DoubleScorePowerup):
            if powerup.update_timer(deltaTime):
                # If the power-up duration expires, remove its effect from the duck
                duck.double_score_active = False

    # Draw score
    font = pygame.font.SysFont(None, 30)
    text = font.render("Score: " + str(duck.score), True, (0, 0, 0))
    gameDisplay.blit(text, (10, 10))

    pygame.display.update()

# Quit Pygame
pygame.quit()
