#Go Corona Go - a fun game developed using PyGame

import pygame
import random
import sys
import math
import time

from pygame import display, event
from pygame import mixer

# initialize pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))

running = True

# background
background = pygame.image.load('background1.jpeg')
intro_background = pygame.image.load('intro_bg3.jpg')

# background music
mixer.music.load('back_music.wav')
mixer.music.play(-1)

# caption and icon
pygame.display.set_caption("GO CORONA!")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# colours
bright_red = (250, 0, 0)
red = (200, 0, 0)
bright_green = (0,250,0)
green = (0,200, 0)

# sanitiser
player_img = pygame.image.load('sanitiser.png')
player_X = 368
player_Y = 500
playerX_change = 0

# corona
corona_img = []
corona_X = []
corona_Y = []
coronaX_change = []
coronaY_change = []
num_of_virus = 6

for i in range(num_of_virus):
    corona_img.append(pygame.image.load('corona.png'))
    corona_X.append(random.randint(0, 736))
    corona_Y.append(random.randint(50, 150))
    coronaX_change.append(2)
    coronaY_change.append(40)

# water
water_img = []
water_X = []
water_Y = []
waterX_change = []
waterY_change = []
water_state = []
num_of_drops = 5

for j in range(num_of_drops):
    water_img.append(pygame.image.load('water.png'))
    water_X.append(0)
    water_Y.append(480)
    waterX_change.append(0)
    waterY_change.append(3)
    water_state.append('ready')

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
max_scores=[0]

textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


# button
def button(msg, x, y, w, h, ic, ac, action = None):
    global running, score_value
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    small_text = pygame.font.Font('freesansbold.ttf', 20)

    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == 'play':
                running = True
                for i in range(num_of_virus):
                    corona_X[i] = (random.randint(0, 736))
                    corona_Y[i] = (random.randint(50, 150))
                player_X = 368
                player_Y = 500
                score_value = 0
                game_loop()
            elif action == 'quit':
                pygame.quit()
                quit()

    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))
    text = small_text.render(msg, True, (0, 0, 0))
    screen.blit(text, (x + (w/2) - 22, y + (h/2) - 10))


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        screen.fill((255, 255, 255))
        screen.blit(intro_background, (0, -100))
        name = over_font.render("GO CORONA!", True, (0, 0, 0))
        tiny_text = pygame.font.Font('freesansbold.ttf', 20)
        by_name = tiny_text.render("By Abitha Rao", True, (0, 0, 0))
        screen.blit(name, (200, 50))
        screen.blit(by_name, (340, 500))

        small_text = pygame.font.Font('freesansbold.ttf', 20)

        button("PLAY", 150, 450, 100, 50, bright_green, green, action = 'play')
        button("QUIT", 550, 450, 100, 50, bright_red, red, action= 'quit')

        pygame.display.update()


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (0, 0, 0))
    max_score = font.render("Max Score : " + str(max_scores[0]), True, (0, 0, 0))
    screen.blit(score, (x, y))
    screen.blit(max_score, (x, y+40))


def game_over_text():
    over_text = over_font.render("GAME OVER!", True, (0, 0, 0))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(player_img, (x, y))


def corona(x, y, i):
    screen.blit(corona_img[i], (x, y))


def spray(x, y, j):
    global water_state
    water_state[j] = 'spray'
    screen.blit(water_img[j], (x - 10, y + 10))


def isCollision(corona_X, corona_Y, water_X, water_Y):
    dist = math.sqrt((math.pow(corona_X - water_X, 2)) + (math.pow(corona_Y - water_Y, 2)))
    if dist <= 27:
        return True
    else:
        return False


def game_loop():
    global player_X, playerX_change, player_Y, score_value, running, corona_X, corona_Y
    while running:

        screen.fill((0, 0, 0))
        # background image
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                running = False
                if score_value > max_scores[0]:
                    max_scores.clear()
                    max_scores.append(score_value)
                game_intro()

            # keystrokes
             if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -2
                if event.key == pygame.K_RIGHT:
                    playerX_change = 2
                if event.key == pygame.K_SPACE:
                    for j in range(num_of_drops):
                        if water_state[j] == 'ready':
                            water_sound = mixer.Sound('shoot.wav')
                            water_sound.play()
                            water_X[j] = player_X
                            spray(water_X[j], water_Y[j], j)

             if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        player_X += playerX_change

        if player_X <= 0:
             player_X = 0
        elif player_X >= 736:
             player_X = 736

        #corona movement
        for i in range(num_of_virus):

            # game over
            if corona_Y[i]  > 440:
                for j in range(num_of_virus):
                    corona_Y[j] = 1000
                game_over_text()
                player_X = 368
                player_Y = 500
                if score_value > max_scores[0]:
                    max_scores.clear()
                    max_scores.append(score_value)
                break

            corona_X[i] += coronaX_change[i]
            if corona_X[i] <= 0:
                coronaX_change[i] = 3
                corona_Y[i] += coronaY_change[i]
            elif corona_X[i] >= 736:
                coronaX_change[i] = -3
                corona_Y[i] += coronaY_change[i]

            # collision:
            for j in range(num_of_drops):
                collision = isCollision(corona_X[i], corona_Y[i], water_X[j], water_Y[j])
                if collision:
                    explosion_sound = mixer.Sound('explosion.wav')
                    explosion_sound.play()
                    water_Y[j] = 480
                    water_state[j] = 'ready'
                    score_value += 1
                    corona_X[i] = random.randint(0, 736)
                    corona_Y[i] = random.randint(50, 150)

            corona(corona_X[i], corona_Y[i], i)

        # spray movement
        for j in range(num_of_drops):
            if water_Y[j] <= 0:
                water_Y[j] = 480
                water_state[j] = 'ready'
            if water_state[j] is 'spray':
                spray(water_X[j], water_Y[j], j)
                water_Y[j] -= waterY_change[j]

        player(player_X, player_Y)

        show_score(textX, textY)
        pygame.display.update()

game_intro()