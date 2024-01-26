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
MAX_BALL_SPEED = 35

BALL_SIZE = 15
BALL_SPEED_X = random.choice([-8, 8])
BALL_SPEED_Y = random.choice([-8, 8])
BALL_POS = [(SCREEN_WIDTH - BALL_SIZE) // 2, (SCREEN_HEIGHT - BALL_SIZE) // 2]

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_SPEED = 14
PADDLE_POS_TOP = [(SCREEN_WIDTH - PADDLE_HEIGHT) // 2, 0]
PADDLE_POS_BOT = [(SCREEN_WIDTH - PADDLE_HEIGHT) // 2, SCREEN_HEIGHT - PADDLE_WIDTH]

clock = pygame.time.Clock()
timePassed = 0

scoreRed = 0
scoreGreen = 0

font = pygame.font.Font(None, 50)   
menuFont = pygame.font.Font(None, 30)
LARGE_FONT = pygame.font.Font(None, 100)

def DrawEverything(screen, ball, redPaddle, greenPaddle):
    global scoreRed, scoreGreen
    screen.fill((0, 0, 0))
    
    pygame.draw.rect(screen, (255, 0, 0), redPaddle)
    pygame.draw.rect(screen, (0, 255, 0), greenPaddle)
    pygame.draw.rect(screen, (0, 0, 255), ball)
    
    draw_dashed_line(screen, (255, 255, 255), (0, SCREEN_HEIGHT // 2), (SCREEN_WIDTH, SCREEN_HEIGHT // 2))
    
    # Render the scores
    scoreRedSurface = font.render(f"R: {scoreRed}", True, (255, 0, 0))  # Red color
    scoreGreenSurface = font.render(f"G: {scoreGreen}", True, (0, 255, 0))  # Green color

    # Make the scores slightly transparent
    scoreRedSurface.set_alpha(128)  # 50% transparent
    scoreGreenSurface.set_alpha(128)  # 50% transparent

    # Calculate the positions of the scores
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2
    
    # Get the rectangles that enclose the scores
    scoreRedRect = scoreRedSurface.get_rect()
    scoreGreenRect = scoreGreenSurface.get_rect()
    
    # Calculate the positions of the scores so that they are centered
    scoreRedPos = (center_x - scoreRedRect.width // 2, center_y - 30 - scoreRedRect.height // 2)
    scoreGreenPos = (center_x - scoreGreenRect.width // 2, center_y + 30 - scoreGreenRect.height // 2)

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
            
            # Draw the objects
            DrawEverything(screen, ball, redPaddle, greenPaddle)
            
            # Move the ball in an accelerated fashion 
            global timePassed
            dt = clock.tick(60) / 1000  # Time passed since last tick in seconds.
            timePassed += dt
            
            global BALL_SPEED_X, BALL_SPEED_Y
            if timePassed > 10:
                BALL_SPEED_X = min(BALL_SPEED_X + 2 if BALL_SPEED_X > 0 else BALL_SPEED_X - 2, MAX_BALL_SPEED)
                BALL_SPEED_Y = min(BALL_SPEED_Y + 2 if BALL_SPEED_Y > 0 else BALL_SPEED_Y - 2, MAX_BALL_SPEED)
                timePassed = 0
                
            ball.move_ip(BALL_SPEED_X, BALL_SPEED_Y)
            
            # Move the paddle
            KeyBinds(redPaddle, greenPaddle)                        

            # Check if a player has scored
            if HandleCollision(screen, ball, redPaddle, greenPaddle):
                # A player has scored
                pygame.time.delay(500) # wait 500 milliseconds
                ResetBallSpeed()
                ResetGame(ball, redPaddle, greenPaddle)
                
                        
            pygame.display.flip()
            clock.tick(60)

def draw_dashed_line(surface, color, start_pos, end_pos, width=1, dash_length=5):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length
    
    if (x1 == x2):
        ycoords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
        xcoords = [x1] * len(ycoords)
    else: 
        xcoords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
        ycoords = [y1] * len(xcoords)
        
    next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
    last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
    for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
        pygame.draw.line(surface, color, (x1, y1), (x2, y2), width)

def ResetBallSpeed():
    global BALL_SPEED_X, BALL_SPEED_Y
    BALL_SPEED_X = random.choice([-8, 8])
    BALL_SPEED_Y = random.choice([-8, 8])

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
        # Reverse the y direction of the ball
        BALL_SPEED_Y *= -1

    # Check for collision with walls
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        # Reverse the x direction of the ball
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
    # Load the screenshot image
    #background = pygame.image.load('screenshot.png')

    # Take a screenshot of the game screen
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))

    label1 = LARGE_FONT.render("V-PONG", 1, (0, 0, 255))
    label2 = menuFont.render("Press SPACE to start", 1, (255, 255, 255))
    label3 = menuFont.render("Press ESC to pause", 1, (255, 255, 255))
    
    # Render the player controls text
    controls_text = "Player 1: A/D keys"
    controls_text2 = "Player 2: Left/Right arrows"
    label4 = menuFont.render(controls_text, 1, (255, 0, 0))
    label5 = menuFont.render(controls_text2, 1, (0, 255, 0))
    
    while True:
        screen.blit(background, (0, 0))  
        screen.blit(label1, ((SCREEN_WIDTH - label1.get_width()) // 2, (SCREEN_HEIGHT - label1.get_height()) // 2 - 40))
        screen.blit(label2, ((SCREEN_WIDTH - label2.get_width()) // 2, (SCREEN_HEIGHT - label2.get_height()) // 2 + 40))
        screen.blit(label3, ((SCREEN_WIDTH - label3.get_width()) // 2, (SCREEN_HEIGHT - label3.get_height()) // 2 + 80))
        # Display the player controls text
        screen.blit(label4, ((SCREEN_WIDTH - label4.get_width()) // 2, (SCREEN_HEIGHT - label4.get_height()) // 2 + 120))
        screen.blit(label5, ((SCREEN_WIDTH - label5.get_width()) // 2, (SCREEN_HEIGHT - label5.get_height()) // 2 + 160))
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