import pygame as p
import random
import math

p.init()

# screen
screen = p.display.set_mode((800, 600))

# Title
p.display.set_caption("Egg-Catcher")
icon = p.image.load("egg.png")
p.display.set_icon(icon)

# Score
score = 0
font = p.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
# level
level = 1
# Hiscore
with open("hiscore.txt", "r") as f:
    hiscore = f.read()

# end
end = 0
# Game over text
overfont = p.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_text = overfont.render("GAME OVER", True, (255, 255, 255))
    text = font.render("Score : " + str(score), True, (255, 255, 255))
    hitext = font.render("HiScore : " + str(hiscore), True, (255, 255, 255))
    screen.blit(over_text, (150, 250))
    screen.blit(text, (300, 350))
    screen.blit(hitext, (350, 400))


def show_score(x, y, a, b):
    global score_s
    score_s = font.render("Score : " + str(score) + "  HiScore : " + str(hiscore), True, (255, 255, 255))
    lvl = font.render("Level : " + str(level), True, (255, 255, 255))
    screen.blit(score_s, (x, y))
    screen.blit(lvl, (a, b))


# bomb
bomb_img = []
bomb_X = []
bomb_Y = []
bombY_change = []
num = 2

for a in range(num):
    bomb_img.append(p.image.load("bomb.png"))
    bomb_X.append(random.randint(0, 700))
    bomb_Y.append(random.randint(10, 200))
    bombY_change.append(.25)


def bomb(x, y, a):
    screen.blit(bomb_img[a], (x, y))


# egg
egg_img = []
egg_X = []
egg_Y = []
eggY_change = []
no = 4

for i in range(no):
    egg_img.append(p.image.load("egg.png"))
    egg_X.append(random.randint(0, 700))
    egg_Y.append(random.randint(10, 200))
    eggY_change.append(.25)


def egg(x, y, i):
    screen.blit(egg_img[i], (x, y))


# basket
basket_img = p.image.load("basket.png")
bas_X = 370
bas_Y = 480
basX_change = 0
bas_Y_change = 0


def isCollision(eX, eY, bX, bY):
    dis = math.sqrt(math.pow((eX - bX), 2) + (math.pow((eY - bY), 2)))
    if dis <= 20:
        return True
    else:
        return False


run = True

while run:
    screen.fill((0, 0, 0))
    for event in p.event.get():

        if event.type == p.QUIT:
            run = False
        if event.type == p.KEYDOWN:
            press = True
            if event.key == p.K_ESCAPE:
                run = False
            if event.key == p.K_RIGHT:
                basX_change = .25

            if event.key == p.K_LEFT:
                basX_change = -.25

        if event.type == p.KEYUP:
            if event.key == p.K_LEFT or event.key == p.K_RIGHT:
                basX_change = 0
            # print('released')
    bas_X += basX_change

    # bomb movement
    for a in range(num):
        coll = isCollision(bomb_X[a], bomb_Y[a], bas_X, bas_Y)


        if coll:
            #bomb_Y[a]=2000
            if score > int(hiscore):
                hiscore = score
                with open("hiscore.txt", "w")as f:
                    f.write(str(hiscore))
            end = 1
            break
            #game_over_text()
        else:
            bomb_Y[a] += bombY_change[a]
            if bomb_Y[a] > 500:
                bomb_X[a] = random.randint(0, 700)
                bomb_Y[a] = random.randint(0, 10)
            bomb(bomb_X[a], bomb_Y[a], a)

    # egg movement
    for i in range(no):
        if end == 1:
            break
        egg_Y[i] += eggY_change[i]

        collision = isCollision(egg_X[i], egg_Y[i], bas_X, bas_Y)
        if collision:
            score += 1
            # print(score)
            egg_X[i] = random.randint(0, 700)
            egg_Y[i] = random.randint(0, 10)

        if egg_Y[i] > 500:
            egg_X[i] = random.randint(0, 700)
            egg_Y[i] = random.randint(0, 10)

        egg(egg_X[i], egg_Y[i], i)

    # checking for bounderies
    if end == 1:
        game_over_text()
    if bas_X <= 0:
        bas_X = 0
    elif bas_X >= 736:  # image size is 64x64(size consation)
        bas_X = 736

    screen.blit(basket_img, (bas_X - 16, bas_Y))
    show_score(textX, textY, 10, 50)
    p.display.update()
