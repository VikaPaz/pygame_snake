import pygame as pg
from random import randrange as rd
import sys
import os

res = 600
size = 50

x, y = 100, 100
vx, vy = 0, 0
pos_snake = [(x, y)]
len_snake = 1

restrictions = {'w': False, 's': True, 'a': True, 'd': True}
fps = 60
speed = 10
count = 0
count_apple, speed_apple, num_apple = 0, 10, 2

apple = (rd(size, res - size, size), rd(size, res - size, size))
score = 0
with open('record.txt', 'r') as mapFile:
    record = mapFile.read()

pg.init()
screen = pg.display.set_mode([res, res])

font_score = pg.font.SysFont('Arial', 26, bold=True)
font_record = pg.font.SysFont('Arial', 26, bold=True)
font_end = pg.font.SysFont('Arial', 45, bold=True)

img_skin = pg.image.load('skin.png').convert()
img_headS = pg.image.load('head.png').convert()
img_headD = pg.transform.rotate(img_headS, 90)
img_headA = pg.transform.rotate(img_headS, -90)
img_headW = pg.transform.rotate(img_headS, 180)
img_head = img_headS

img_apple = pg.image.load('apple2.png').convert()

eating_sound = pg.mixer.Sound("apple.mp3")
eating_sound.set_volume(0.5)
game_over_sound = pg.mixer.Sound('game_over.mp3')
game_over_sound.set_volume(1)


def exit_game():
    global flag
    key = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        elif key[pg.K_SPACE]:
            flag = False
            game()
            break


def drawing():
    global screen, size, pos_snake, img_skin, img_apple, count_apple, speed_apple, num_apple
    [screen.blit(img_skin, (i, j)) for i, j in pos_snake]
    screen.blit(img_head, pos_snake[-1])

    count_apple += 1
    if count_apple % speed_apple == 0:
        if num_apple < 9:
            num_apple += 1
    img_apple = pg.image.load(f'apple{num_apple}.png').convert()
    screen.blit(img_apple, apple)


def movement():
    global x, y, vx, vy, size, pos_snake, len_snake, count, speed
    count += 1
    if count % speed == 0:
        x += vx * size
        y += vy * size
        pos_snake.append((x, y))
        pos_snake = pos_snake[-len_snake:]


def eating():
    global pos_snake, apple, len_snake, size, res, score, num_apple, count_apple, sound_eating
    if pos_snake[-1] == apple:
        while apple in pos_snake:
            apple = (rd(size, res - size, size), rd(size, res - size, size))
        count_apple = 0
        num_apple = 2
        len_snake += 1
        score += 1
        eating_sound.play()


def game_over():
    global res, size, x, y, flag, game_over
    if x < 0 or x > res - size or y < 0 or y > res - size or \
            len(pos_snake) != len(set(pos_snake)):
        flag = False
        game_over_sound.play()
        while True:
            render_end = font_end.render('GAME OVER', True, pg.Color('red'))
            render_end1 = font_end.render('press SPACE to RESTART play', True, pg.Color('green'))
            screen.blit(render_end, (res // 2 - 100, res // 3))
            screen.blit(render_end1, (res // 2 - 270, res // 3 + 50))
            pg.display.flip()
            exit_game()


def controls():
    global vx, vy, restrictions, img_head
    key = pg.key.get_pressed()
    if key[pg.K_w]:
        if restrictions['w']:
            vx, vy = 0, -1
            restrictions = {'w': False, 's': False, 'a': True, 'd': True}
            img_head = img_headW
    elif key[pg.K_s]:
        if restrictions['s']:
            vx, vy = 0, 1
            restrictions = {'w': False, 's': False, 'a': True, 'd': True}
            img_head = img_headS
    elif key[pg.K_a]:
        if restrictions['a']:
            vx, vy = -1, 0
            restrictions = {'w': True, 's': True, 'a': False, 'd': False}
            img_head = img_headA
    elif key[pg.K_d]:
        if restrictions['d']:
            vx, vy = 1, 0
            restrictions = {'w': True, 's': True, 'a': False, 'd': False}
            img_head = img_headD


def show_score():
    render_score = font_score.render(f'SCORE: {score}', True, pg.Color('red'))
    screen.blit(render_score, (5, 5))


def show_record():
    global record
    if score > int(record):
        with open('record.txt', 'w') as mapFile:
            record = mapFile.write(str(score))
        with open('record.txt', 'r') as mapFile:
            record = mapFile.read()
    render_score = font_score.render(f'RECORD: {record}', True,
                                     pg.Color('orange'))
    screen.blit(render_score, (5, 50))


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pg.image.load(fullname)
    return image


FPS = 50


def terminate():
    pg.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Исспользуйте кнопки w a s d для управления"
                  ]

    fon = pg.transform.scale(load_image('head1.png'), (res, res))
    screen.blit(fon, (0, 0))
    font = pg.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pg.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


flag = False


def game():
    global flag, x, y, vx, vy, pos_snake, len_snake, restrictions
    x, y = 100, 100
    vx, vy = 0, 0
    pos_snake = [(x, y)]
    len_snake = 1

    restrictions = {'w': False, 's': True, 'a': True, 'd': True}

    while not flag:
        start_screen()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            elif event.type == pg.KEYDOWN or \
                    event.type == pg.MOUSEBUTTONDOWN:
                flag = True
        pg.display.flip()

    clock = pg.time.Clock()
    while flag:
        screen.fill(pg.Color('black'))
        show_record()
        drawing()
        movement()
        eating()
        controls()
        game_over()
        show_score()

        pg.display.flip()
        clock.tick(fps)
        exit_game()


game()
