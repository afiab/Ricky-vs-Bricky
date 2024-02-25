import pygame
import os

# window
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 500 # pixel width, height
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #create the screen
pygame.display.set_caption("Ritchie vs Bricky") # set title of the window

BORDER = pygame.Rect(SCREEN_WIDTH//2 - 5, 0, 10, SCREEN_HEIGHT)

WHITE = (255,255,255) # pass in rgb vals as a tuple
BLACK = (0,0,0)
RED = (255,0,0)
ORANGE = (255, 200, 0)

FPS = 60 # Frames per second
VEL = 5 # Velocity
BRICK_VEL = 7 # Velocity of bricks
MAX_BRICKS = 3 # Maximum amt of bricks per player

# sprites: Ritchie and Bricky
IMAGE_WIDTH, IMAGE_HEIGHT = 536/3,458/3

RITCHIE_HIT = pygame.USEREVENT+1 #create a user event
BRICKY_HIT = pygame.USEREVENT+2 #create a user event, +1 and +2 distinguish events

RITCHIE_IMAGE = pygame.image.load(os.path.join('Assets', 'ritchie.png')) # ritchie
RITCHIE_IMAGE = pygame.transform.scale(RITCHIE_IMAGE, (IMAGE_WIDTH, IMAGE_HEIGHT)) #resize to size specified
BRICKY_IMAGE = pygame.image.load(os.path.join('Assets', 'bricky.png')) # bricky
BRICKY_IMAGE = pygame.transform.scale(BRICKY_IMAGE, (IMAGE_WIDTH, IMAGE_HEIGHT)) #resize to size specified

def draw_window(ritchie, bricky, ritchie_bricks, bricky_bricks):
    #updates the window
    WIN.fill(WHITE) # fill the window with White
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(RITCHIE_IMAGE, (ritchie.x,ritchie.y)) # image, coords
    WIN.blit(BRICKY_IMAGE, (bricky.x,bricky.y)) # image, coords

    for brick in ritchie_bricks:
        pygame.draw.rect(WIN, ORANGE, brick)

    for brick in bricky_bricks:
        pygame.draw.rect(WIN, RED, brick)

    pygame.display.update() # continuously update the display

def ritchie_handle_movement(keys_pressed, ritchie):
    if keys_pressed[pygame.K_a] and ritchie.x-VEL>0: # LEFT
        ritchie.x -= VEL 
    if keys_pressed[pygame.K_d] and ritchie.x+VEL+ritchie.width<BORDER.x: # RIGHT
        ritchie.x += VEL 
    if keys_pressed[pygame.K_w] and ritchie.y-VEL>0: # UP
        ritchie.y -= VEL 
    if keys_pressed[pygame.K_s] and ritchie.y+VEL+ritchie.height<SCREEN_HEIGHT: # DOWN
        ritchie.y += VEL 

def bricky_handle_movement(keys_pressed, bricky):
    if keys_pressed[pygame.K_LEFT] and bricky.x-VEL>BORDER.x+BORDER.width: # LEFT
        bricky.x -= VEL 
    if keys_pressed[pygame.K_RIGHT] and bricky.x+VEL+bricky.width<SCREEN_WIDTH: # RIGHT
        bricky.x += VEL 
    if keys_pressed[pygame.K_UP] and bricky.y-VEL>0: # UP
        bricky.y -= VEL 
    if keys_pressed[pygame.K_DOWN] and bricky.y+VEL+bricky.height<SCREEN_HEIGHT: # DOWN
        bricky.y += VEL 

def handle_bricks(ritchie_bricks, bricky_bricks, ritchie, bricky):
    for brick in ritchie_bricks:
        brick.x+=BRICK_VEL
        if bricky.colliderect(brick):
            pygame.event.post(pygame.event.Event(BRICKY_HIT))
            ritchie_bricks.remove(brick)
        elif brick.x > SCREEN_WIDTH:
            bricky_bricks.remove(brick)
    for brick in bricky_bricks:
        brick.x-=BRICK_VEL
        if ritchie.colliderect(brick):
            pygame.event.post(pygame.event.Event(RITCHIE_HIT))
            bricky_bricks.remove(brick)
        elif brick.x < 0:
            ritchie_bricks.remove(brick)

def main():
    ritchie = pygame.Rect(100, 300, IMAGE_WIDTH, IMAGE_HEIGHT)
    bricky = pygame.Rect(700, 300, IMAGE_WIDTH, IMAGE_HEIGHT)

    ritchie_bricks = []
    bricky_bricks = []

    clock = pygame.time.Clock() # to help do FPS
    run = True
    while run:
        clock.tick(FPS) # control the Frame Rate
        for event in pygame.event.get(): # loop through all the events
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(ritchie_bricks)<MAX_BRICKS: #ritchie
                    brick = pygame.Rect(ritchie.x+ritchie.width, ritchie.y+ritchie.height//2-2, 10, 5)
                    ritchie_bricks.append(brick)
                if event.key == pygame.K_RCTRL and len(bricky_bricks)<MAX_BRICKS: #bricky
                    brick = pygame.Rect(bricky.x, bricky.y+bricky.height//2-2, 10, 5)
                    bricky_bricks.append(brick)

        keys_pressed = pygame.key.get_pressed() #tell us currently pressed keys
        ritchie_handle_movement(keys_pressed, ritchie) #movement for ritchie
        bricky_handle_movement(keys_pressed, bricky) #movement for bricky

        handle_bricks(ritchie_bricks, bricky_bricks, ritchie, bricky)

        draw_window(ritchie, bricky, ritchie_bricks, bricky_bricks)

    pygame.quit()

if __name__ == "__main__":
    main() # only run file directly