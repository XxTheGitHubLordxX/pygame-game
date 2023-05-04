import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1510, 925
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Star Wars space shooter") #window name

BLACK = (25, 0, 51)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(0, HEIGHT//2 - 5, WIDTH, 10 )

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'hit.mp3'))
BULLET_FIRE_SOUND_TIE = pygame.mixer.Sound(os.path.join('Assets', 'tie.mp3'))
BULLET_FIRE_SOUND_WING = pygame.mixer.Sound(os.path.join('Assets', 'wing.mp3'))

HEALTH_FONT = pygame.font.SysFont('nanum gothic', 40)
WINNER_FONT = pygame.font.SysFont('nanum gothic', 100)

BULLET_VEL = 7
MAX_BULLETS = 10
FPS = 60
VEL = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 75, 100

TIE_HIT = pygame.USEREVENT + 1
WING_HIT = pygame.USEREVENT + 2

Tie_Fighter_IMAGE = pygame.image.load(
    os.path.join('Assets', 'tie.png'))
Tie_Fighter = pygame.transform.rotate(
    pygame.transform.scale(
    Tie_Fighter_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

Xwing_IMAGE = pygame.image.load(
    os.path.join('Assets', 'xwing.png'))
Xwing = pygame.transform.rotate(pygame.transform.scale(
    Xwing_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)

SPACE =pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'background.png')), (WIDTH, HEIGHT))

#drawing stuff on window
def draw_window(wing, tie, wing_bullets, tie_bullets, wing_health, tie_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, WHITE, BORDER)
    
    wing_health_text = HEALTH_FONT.render(
        "Health: " + str(wing_health), 1, WHITE)
    tie_health_text = HEALTH_FONT.render(
        "Health: " + str(tie_health), 1, WHITE)
    WIN.blit(wing_health_text, (WIDTH - wing_health_text.get_width() -10, 10))
    WIN.blit(tie_health_text, (10, 10))
    
    WIN.blit(Tie_Fighter, (tie.x, tie.y))
    WIN.blit(Xwing, (wing.x, wing.y))
    
    for bullet in wing_bullets:
        pygame.draw.rect(WIN, RED, bullet)
        
    for bullet in tie_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)    
    
    pygame.display.update()

def tie_movement(keys_pressed, tie):
    if keys_pressed[pygame.K_z] and tie.x - VEL > 0: # left
        tie.x -= VEL
    if keys_pressed[pygame.K_c] and tie.x + VEL + tie.width < WIDTH: # right
        tie.x += VEL   
    if keys_pressed[pygame.K_s] and tie.y - VEL > BORDER.y + 5: # up
        tie.y -= VEL
    if keys_pressed[pygame.K_x] and tie.y + VEL + tie.height < HEIGHT + 5: # down
        tie.y += VEL 
        
def wing_movement(keys_pressed, wing):
    if keys_pressed[pygame.K_j] and wing.x - VEL > BORDER.x: # left
        wing.x -= VEL
    if keys_pressed[pygame.K_l] and wing.x + VEL + wing.width < WIDTH: # right
        wing.x += VEL   
    if keys_pressed[pygame.K_i] and wing.y - VEL > 0: # up
        wing.y -= VEL
    if keys_pressed[pygame.K_k] and wing.y + VEL + wing.height < BORDER.y: # down
        wing.y += VEL

def handle_bullets(tie_bullets, wing_bullets, tie, wing):
    for bullet in tie_bullets:
        bullet.y -= BULLET_VEL
        if wing.colliderect(bullet):
            pygame.event.post(pygame.event.Event(WING_HIT))
            tie_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            tie_bullets.remove(bullet)
    
    for bullet in wing_bullets:
        bullet.y += BULLET_VEL
        if tie.colliderect(bullet):
            pygame.event.post(pygame.event.Event(TIE_HIT))
            wing_bullets.remove(bullet)
        elif bullet.x < 0:
            wing_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (555, 300))
    pygame.display.update()             
    pygame.time.delay(5000)
    
    
def main():
    wing = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    tie = pygame.Rect(100, 700, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    tie_bullets = []
    wing_bullets = []
    
    wing_health = 10
    tie_health = 10
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and len(tie_bullets) < MAX_BULLETS:
                   bullet = pygame.Rect(
                       tie.x + tie.width, tie.y + tie.height//2 - 2, 10, 5)
                   tie_bullets.append(bullet)
                   BULLET_FIRE_SOUND_TIE.play()
                   
                if event.key == pygame.K_o and len(wing_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        wing.x, wing.y + wing.height//2 - 2, 10, 5)
                    wing_bullets.append(bullet)
                    BULLET_FIRE_SOUND_WING.play()
                    
            if event.type == WING_HIT:
                wing_health -= 1
                BULLET_HIT_SOUND.play()
                
            if event.type == TIE_HIT:
                tie_health -= 1
                BULLET_HIT_SOUND.play()
                
        winner_text = ""
        if wing_health <= 0:
            winner_text = "Tie Fighter wins!"
            
        if tie_health <= 0:
            winner_text = "X-wing wins!"     
        
        if winner_text != "":
             draw_winner(winner_text)
             break
                     
        keys_pressed = pygame.key.get_pressed()
        tie_movement(keys_pressed, tie)
        wing_movement(keys_pressed, wing)   
        
        handle_bullets(tie_bullets, wing_bullets, tie, wing)    
        
        draw_window(wing, tie, wing_bullets, tie_bullets,
                    wing_health, tie_health)
        
    main()
  
    
if __name__ == "__main__":
    main()