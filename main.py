import pygame
import random
import math
from pygame import mixer
count =0
# intialize the pygame
pygame.init()

# Background Sound
mixer.music.load('backmusic.mp3')
mixer.music.play(-1)  # we pit -1 to play it in a loop

score = 0
# Adding Text
font = pygame.font.Font('freesansbold.ttf', 22)
textX = 600
textY = 10


def show_score(x, y):
    score1 = font.render("SCORE : " + str(score), True, (0, 190, 0))
    Screen.blit(score1, (x, y))


# game over text font
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_is_over():
    over_txt = over_font.render("GAME OVER", True, (255, 255, 255))
    Screen.blit(over_txt, (200, 250))


# create the screen
Screen = pygame.display.set_mode((800, 600))

# Background
back_img = pygame.image.load('2799006.png')
back_img = pygame.transform.scale(back_img, (800, 600))

# Title and icon
pygame.display.set_caption("Space Turminator KSR")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#  Player
player_img = pygame.image.load('startup (2).png')
enemy_img = pygame.transform.scale(player_img, (90, 90))
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0


def Player(x, y):
    Screen.blit(player_img, (x, y))


# Enemy
enemy_img = pygame.image.load('ufo.png')
enemy_img = pygame.transform.scale(enemy_img, (75, 75))

enemyX = random.randint(0, 750)
enemyY = random.randint(50, 150)

enemyX_change = 0.5
enemyY_change = 40


def enemy(x, y):
    Screen.blit(enemy_img, (x, y))


# Astroid
astro_img = pygame.image.load('asteroid.png')


def Astro():
    Screen.blit(astro_img, (700, 100))
    Screen.blit(astro_img, (100, 200))
    Screen.blit(astro_img, (500, 300))
    Screen.blit(astro_img, (50, 500))


#  planet
planet_img = pygame.image.load('jupiter.png')
planet_img = pygame.transform.scale(planet_img, (90, 90))

# bullet
bullet_img = pygame.image.load('bullet.png')
bullet_img = pygame.transform.scale(bullet_img, (20, 20))  # resize bullet
angle = 45.5
bullet_img = pygame.transform.rotate(bullet_img, angle)  # rotate imgae
bullet_state = "ready"

bulletX = 0
bulletY = 0

bulletX_change = 0
bulletY_change = 1


# ready -> it is the state when we cant see the bullet
# fire-> it is the state when we can see the bullet
def bullet_fire(x, y):
    global bullet_state
    bullet_state = "fire"
    Screen.blit(bullet_img, (x + 16, y + 10))


def planet():
    Screen.blit(planet_img, (5, 10))


# is collision
def collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance <= 50:
        return True
    else:
        return False


def game_over_collision(enemyX, enemyY, playerX, playerY):
    distance = math.sqrt(math.pow(enemyX - playerX, 2) + math.pow(enemyY - playerY, 2))
    if distance <= 50:
        return True
    else:
        return False


# to hold and exit the screen
running = True

while running:
    # RGB screen background colour
    Screen.fill((0, 0, 0))

    # Background Image
    Screen.blit(back_img, (0, 0))
    planet()
    Astro()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('mixkit-retro-arcade-casino-notification-211.wav')
                    bullet_sound.play()
                    bulletY = playerY
                    bulletX = playerX
                    bullet_fire(bulletX, bulletY)

            if event.key == pygame.K_LEFT:
                playerX_change = -0.3

            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3

            if event.key == pygame.K_UP:
                playerY_change = -0.3

            if event.key == pygame.K_DOWN:
                playerY_change = 0.3

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    playerX += playerX_change
    playerY += playerY_change
    # checking boundries for player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # enemy movement
    enemyX += enemyX_change
    # checking boundries for  enemy
    if enemyX <= 0:
        enemyX_change = 0.5
        enemyY += enemyY_change  # to shift enemy down when it hit the boundry
    elif enemyX >= 736:
        enemyY += enemyY_change  # to shift enemy down when it hit the boundry
        enemyX_change = -0.5

    # Bullet moovement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        bullet_fire(bulletX, bulletY)
        bulletY -= bulletY_change

    # is collision
    col = collision(enemyX, enemyY, bulletX, bulletY)
    if col:
        col_sound = mixer.Sound('mixkit-arcade-retro-changing-tab-206.wav')
        col_sound.play()
        bulletY = playerY
        bullet_state = "ready"
        score += 1

        enemyX = random.randint(0, 735)
        enemyY = random.randint(50, 150)

    show_score(textX, textY)

    khatam = game_over_collision(enemyX, enemyY, playerX, playerY)
    if khatam:
        enemyY = 20000
        count = 1
    if count == 1:
        game_is_over()

    enemy(enemyX, enemyY)
    Player(playerX, playerY)

    # Need to update contuinously
    pygame.display.update()
