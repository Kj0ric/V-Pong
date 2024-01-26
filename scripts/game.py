# Import the module
import pygame
import random

# Initialize the module
try:
    pygame.init()
except ImportError:
    pass

# Define game constants
SCREEN_WIDTH = 800 #pixels
SCREEN_HEIGHT = 600

GAME_SPEED = 60 #frames per second

BALL_SIZE = 15
BALL_SPEED_X = random.choice([-4, 4])
BALL_SPEED_Y = random.choice([-4, 4])
BALL_POS = [(SCREEN_WIDTH - BALL_SIZE) // 2, (SCREEN_HEIGHT - BALL_SIZE) // 2]

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_SPEED = 8
PADDLE_POS_TOP = [(SCREEN_WIDTH - PADDLE_HEIGHT) // 2, 0]
PADDLE_POS_BOT = [(SCREEN_WIDTH - PADDLE_HEIGHT) // 2, SCREEN_HEIGHT - PADDLE_WIDTH]

clock = pygame.time.Clock()

scoreRed = 0
scoreGreen = 0

font = pygame.font.Font(None, 50)   
menuFont = pygame.font.Font(None, 50)
LARGE_FONT = pygame.font.Font(None, 100)

def DrawEverything(screen, ball, redPaddle, greenPaddle):
    screen.fill((0, 0, 0))
    
    pygame.draw.rect(screen, (255, 0, 0), redPaddle)
    pygame.draw.rect(screen, (0, 255, 0), greenPaddle)
    pygame.draw.rect(screen, (0, 0, 255), ball)
    
    # Render the scores
    scoreRedSurface = font.render(f"R: {scoreRed}", True, (255, 0, 0))  # Red color
    scoreGreenSurface = font.render(f"G: {scoreGreen}", True, (0, 255, 0))  # Green color

    # Make the scores slightly transparent
    scoreRedSurface.set_alpha(128)  # 50% transparent
    scoreGreenSurface.set_alpha(128)  # 50% transparent

    # Calculate the positions of the scores
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2
    scoreRedPos = (center_x - scoreRedSurface.get_width() - 10, center_y - scoreRedSurface.get_height() // 2)
    scoreGreenPos = (center_x + 10, center_y - scoreGreenSurface.get_height() // 2)

    # Draw the scores
    screen.blit(scoreRedSurface, scoreRedPos)
    screen.blit(scoreGreenSurface, scoreGreenPos)
    
    
def MainGameLoop(screen, ball, redPaddle, greenPaddle):
    StartMenu(screen)
    paused = False
    while True:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
        
        if paused:
            # Take a screenshot of the game screen
            background = pygame.Surface(screen.get_size())
            background.fill((0, 0, 0))
            
            # Draw pause indicator
            label = LARGE_FONT.render("PAUSED", 1, (255, 255, 255))
            
            screen.blit(background, (0, 0))  
            screen.blit(label, ((SCREEN_WIDTH - label.get_width()) // 2, (SCREEN_HEIGHT - label.get_height()) // 2))
            pygame.display.update()
        
        if not paused: 
            # Update the display
            pygame.display.flip()
            clock.tick(80)
            
            # Draw the objects
            DrawEverything(screen, ball, redPaddle, greenPaddle)
            
            # Move the ball
            ball.move_ip(BALL_SPEED_X, BALL_SPEED_Y)
            
            # Move the paddle
            KeyBinds(redPaddle, greenPaddle)                        

            # Check if a player has scored
            if HandleCollision(screen, ball, redPaddle, greenPaddle):
                # A player has scored
                pygame.time.delay(500) # wait 500 milliseconds
                ResetGame(ball, redPaddle, greenPaddle)

def KeyBinds(redPaddle, greenPaddle):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        redPaddle.x -= PADDLE_SPEED  # Move the red paddle up
    if keys[pygame.K_d]:
        redPaddle.x += PADDLE_SPEED  # Move the red paddle down
    if keys[pygame.K_LEFT]:
        greenPaddle.x -= PADDLE_SPEED  # Move the green paddle up
    if keys[pygame.K_RIGHT]:
        greenPaddle.x += PADDLE_SPEED  # Move the green paddle down
    
def InitializeScreen():    
    # Setting window dimensions
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    return screen

def InitializeGameObjects():
    # Create the ball object
    ball = pygame.Rect(BALL_POS[0], BALL_POS[1], BALL_SIZE, BALL_SIZE)
    
    # Create the paddle objects
    redPaddle =   pygame.Rect(PADDLE_POS_TOP[0], PADDLE_POS_TOP[1], PADDLE_HEIGHT, PADDLE_WIDTH)
    greenPaddle = pygame.Rect(PADDLE_POS_BOT[0], PADDLE_POS_BOT[1], PADDLE_HEIGHT, PADDLE_WIDTH)
    
    return ball, redPaddle, greenPaddle

def HandleCollision(screen, ball, redPaddle, greenPaddle):
    global BALL_SPEED_X, BALL_SPEED_Y, scoreRed, scoreGreen
    # Check for collision with paddles
    if ball.colliderect(redPaddle) or ball.colliderect(greenPaddle):
        # Reverse the x direction of the ball
        BALL_SPEED_Y *= -1

    # Check for collision with walls
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        # Reverse the y direction of the ball
        BALL_SPEED_X *= -1

    # Check if a player has scored
    if ball.top <= 0:  # Ball hit the ceiling of the screen
        scoreGreen += 1  
        pygame.display.flip()
        return True
    elif ball.bottom > SCREEN_HEIGHT:  # Ball hit the bottom of the screen
        scoreRed += 1  # Increment the score of the red player
        pygame.display.flip()
        return True

    return False  # No player has scored
    
        
def StartMenu(screen):
    # Take a screenshot of the game screen
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))

    label1 = LARGE_FONT.render("V-PONG", 1, (0, 0, 255))
    label2 = menuFont.render("Press SPACE to start", 1, (255, 255, 255))
    label3 = menuFont.render("Press ESC to pause", 1, (255, 255, 255))
    
    while True:
        screen.blit(background, (0, 0))  
        screen.blit(label1, ((SCREEN_WIDTH - label1.get_width()) // 2, (SCREEN_HEIGHT - label1.get_height()) // 2 - 40))
        screen.blit(label2, ((SCREEN_WIDTH - label2.get_width()) // 2, (SCREEN_HEIGHT - label2.get_height()) // 2 + 40))
        screen.blit(label3, ((SCREEN_WIDTH - label3.get_width()) // 2, (SCREEN_HEIGHT - label3.get_height()) // 2 + 80))
        pygame.display.update()
        
        for event in pygame.event.get():
            # Quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            # Start the game 
            if event.type == pygame.KEYDOWN: # If a key is pressed
                if event.key == pygame.K_SPACE: # If the key is space                    
                    return

def ResetGame(ball, redPaddle, greenPaddle):
    # Reset the positions of the paddles and the ball
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    redPaddle.topleft = PADDLE_POS_TOP
    greenPaddle.topleft = PADDLE_POS_BOT
    
    global BALL_SPEED_X, BALL_SPEED_Y
    BALL_SPEED_X *= random.choice([-1, 1])
    BALL_SPEED_Y *= random.choice([-1, 1])
    
# Main game loop
screen = InitializeScreen()
ball, redPaddle, greenPaddle = InitializeGameObjects()
MainGameLoop(screen, ball, redPaddle, greenPaddle)