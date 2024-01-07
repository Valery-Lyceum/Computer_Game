import pygame as pg
from random import choice, randrange


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
        while True:
            screen.blit(surface, (0, 0))
            surface.fill(pg.Color('black'))
            [num_column.draw() for num_column in nums_columns]
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.flip()
            clock.tick(60)


WIDTH, HEIGHT = 1600, 900
FONT_SIZE = 40

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
surface = pg.Surface((WIDTH, HEIGHT))
clock = pg.time.Clock()
nums = "0123456789"
font = pg.font.Font('northrup-regular.ttf', FONT_SIZE)
green_nums = [font.render(char, True, (40, randrange(160, 256), 40)) for char in nums]
nums_columns = [NumsColumn(x, randrange(-HEIGHT, 0)) for x in range(0, WIDTH, FONT_SIZE)]
st = Start()