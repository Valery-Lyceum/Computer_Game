import pygame as pg
from random import choice, randrange
from gameplay import GameProcess

class Num:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.value = choice(green_nums)
        self.interval = randrange(5, 30)

    def draw(self):
        frames = pg.time.get_ticks()
        if not frames % self.interval:
            self.value = choice(green_nums)
        self.y = self.y + self.speed if self.y < HEIGHT else -FONT_SIZE
        surface.blit(self.value, (self.x, self.y))


class NumsColumn:
    def __init__(self, x, y):
        self.column_height = randrange(8, 24)
        self.speed = randrange(3, 7)
        self.nums = [Num(x, i, self.speed) for i in range(y, y - FONT_SIZE * self.column_height, -FONT_SIZE)]

    def draw(self):
        [num.draw() for i, num in enumerate(self.nums)]


class Start:
    def __init__(self):
        pg.mixer.music.load('sounds/xpSong.mp3')
        pg.mixer.music.play()
        self.play = True
        self.timer = 0
        self.select = 0
        while self.play:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.play = False
                    pg.mixer.music.stop()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        self.select -= 1
                    elif event.key == pg.K_DOWN:
                        self.select += 1
                    elif event.key in (pg.K_SPACE, pg.K_RETURN):
                        if items[self.select] == 'Exit':
                            self.play = False
                            pg.mixer.music.stop()
                        if items[self.select] == 'Start':
                            self.play = False
                            pg.mixer.music.stop()
                            gmprcs = GameProcess()
                    self.select = self.select % len(items)
            self.timer += 1
            screen.blit(surface, (0, 0))
            surface.fill(pg.Color('black'))
            [num_column.draw() for num_column in nums_columns]
            for i in range(len(items)):
                if i == self.select and self.timer % 30 < 15:
                    text = fontItemSelect.render(items[i], 0, 'white')
                else:
                    text = fontItem.render(items[i], 0, 'gray')
                rect = text.get_rect(center=(WIDTH // 2, 400 + 70 * i))
                screen.blit(text, rect)
            pg.display.flip()
            clock.tick(60)



WIDTH, HEIGHT = 1600, 900
FONT_SIZE = 40
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
surface = pg.Surface((WIDTH, HEIGHT))
clock = pg.time.Clock()
nums = "0123456789"
font = pg.font.Font('fonts/northrup-regular.ttf', FONT_SIZE)
green_nums = [font.render(char, True, (40, randrange(160, 256), 40)) for char in nums]
nums_columns = [NumsColumn(x, randrange(-HEIGHT, 0)) for x in range(0, WIDTH, FONT_SIZE)]
fontItem = pg.font.Font('fonts/better-vcr_0.ttf', 50)
fontItemSelect = pg.font.Font('fonts/better-vcr_0.ttf', 60)
items = ['Start', 'Exit']
st = Start()
