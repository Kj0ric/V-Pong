# Import the module
import pygame
import random

# Define game constants
SCREEN_WIDTH = 800 #pixels
SCREEN_HEIGHT = 600

GAME_SPEED = 60 #frames per second

BALL_SIZE = 20
BALL_SPEED_X = random.choice([-1, 1])
BALL_SPEED_Y = random.choice([-1, 1])
BALL_POS = [(SCREEN_WIDTH - BALL_SIZE) // 2, (SCREEN_HEIGHT - BALL_SIZE) // 2]

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_SPEED = 8
PADDLE_POS_TOP = [(SCREEN_WIDTH - PADDLE_HEIGHT) // 2, 0]
PADDLE_POS_BOT = [(SCREEN_WIDTH - PADDLE_HEIGHT) // 2, SCREEN_HEIGHT - PADDLE_WIDTH]

clock = pygame.time.Clock()

def MainGameLoop():
    
    screen = InitializeScreen()
    ball, redPaddle, greenPaddle = InitializeGameObjects()
    
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Fill the screen with a color
        screen.fill((0, 0, 0))
        
        # Draw the objects
        pygame.draw.rect(screen, (255, 0, 0), redPaddle)
        pygame.draw.rect(screen, (0, 255, 0), greenPaddle)
        pygame.draw.rect(screen, (0, 0, 255), ball)
        
        # Move the ball
        ball.move_ip(BALL_SPEED_X, BALL_SPEED_Y)
        # Move the paddle
        KeyBinds(redPaddle, greenPaddle)
        
        # Collision
        HandleCollision(ball, redPaddle, greenPaddle)
        
        # Update the display
        pygame.display.flip()
        
        clock.tick(60)

    # Quit pygame
    pygame.quit()
    
def InitializeScreen():    

    print(pygame.version.ver)

    # Initialize the module
    try:
        pygame.init()
    except ImportError:
        pass

    # Setting window dimensions
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    return screen

def InitializeGameObjects():
    # Create the ball object
    ball = pygame.Rect(BALL_POS[0], BALL_POS[1], BALL_SIZE, BALL_SIZE)
    
    # Create the paddle objects
    redPaddle = pygame.Rect(PADDLE_POS_TOP[0], PADDLE_POS_TOP[1], PADDLE_HEIGHT, PADDLE_WIDTH)
    greenPaddle = pygame.Rect(PADDLE_POS_BOT[0], PADDLE_POS_BOT[1], PADDLE_HEIGHT, PADDLE_WIDTH)
    
    return ball, redPaddle, greenPaddle

def HandleCollision(ball, redPaddle, greenPaddle):
    # Between ball and paddles
    if ball.colliderect(redPaddle) or ball.colliderect(greenPaddle):
        BALL_SPEED_Y *= -1
    
    # Between ball and walls
    if ball.left < 0 or ball.right > SCREEN_WIDTH: # X coord of left and right side of the ball
        BALL_SPEED_X *= -1
    
def KeyBinds(redPaddle, greenPaddle):
        # Move the paddles
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            redPaddle.move_ip(-PADDLE_SPEED, 0)
        if keys[pygame.K_d]:
            redPaddle.move_ip(PADDLE_SPEED, 0)
        if keys[pygame.K_LEFT]:
            greenPaddle.move_ip(-PADDLE_SPEED, 0)
        if keys[pygame.K_RIGHT]:
            greenPaddle.move_ip(PADDLE_SPEED, 0)
        
# Main

MainGameLoop()