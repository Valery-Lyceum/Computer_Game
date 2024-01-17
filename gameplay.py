import pygame
from random import randint

pygame.init()
WIDTH, HEIGHT = 800, 600
FPS = 60
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Strelyalka')
fontUI = pygame.font.Font('fonts/northrup-regular.ttf', 30)
fontItem = pygame.font.Font('fonts/better-vcr_0.ttf', 70)
imgBrick = pygame.image.load('images/oshibka_blue.jpg')
imgPlayers = [pygame.image.load('images/mouse.jpeg'),
              pygame.image.load('images/err.png')]
imgBangs = [
    pygame.image.load('images/bang1.png'),
    pygame.image.load('images/bang2.png'),
    pygame.image.load('images/bang3.png'),
    pygame.image.load('images/bang2.png'),
    pygame.image.load('images/bang1.png'), ]
sndShot = pygame.mixer.Sound('sounds/shot.wav')
sndDestroy = pygame.mixer.Sound('sounds/destroy.wav')
DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]
TILE = 32


class Player:
    def __init__(self, color, imBase, px, py, direct, keysList):
        objects.append(self)
        self.type = 'player'
        self.color = color
        self.imBase = imBase
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.moveSpeed = 2
        self.shotTimer = 0
        self.shotDelay = 60
        self.bulletSpeed = 5
        self.bulletDamage = 1
        self.isMove = False
        self.hp = 3
        self.keyLEFT = keysList[0]
        self.keyRIGHT = keysList[1]
        self.keyUP = keysList[2]
        self.keyDOWN = keysList[3]
        self.keySHOT = keysList[4]
        self.image = pygame.transform.rotate(self.imBase, -self.direct * 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.image = pygame.transform.rotate(self.imBase, -self.direct * 90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 5, self.image.get_height() - 5))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.moveSpeed = 2
        self.bulletDamage = 1
        self.bulletSpeed = 4
        self.shotDelay = 60
        oldX, oldY = self.rect.topleft
        if keys[self.keyUP] and self.rect.y - self.moveSpeed > 0:
            self.rect.y -= self.moveSpeed
            self.direct = 0
            self.isMove = True
        elif keys[self.keyRIGHT] and self.rect.x + self.moveSpeed < 770:
            self.rect.x += self.moveSpeed
            self.direct = 1
            self.isMove = True
        elif keys[self.keyDOWN] and self.rect.y + self.moveSpeed < 570:
            self.rect.y += self.moveSpeed
            self.direct = 2
            self.isMove = True
        elif keys[self.keyLEFT] and self.rect.x - self.moveSpeed > 0:
            self.rect.x -= self.moveSpeed
            self.direct = 3
            self.isMove = True
        else:
            self.isMove = False
        if keys[self.keySHOT] and self.shotTimer == 0:
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotTimer = self.shotDelay
        if self.shotTimer > 0:
            self.shotTimer -= 1
        for obj in objects:
            if obj != self and obj.type == 'block':
                if self.rect.colliderect(obj):
                    self.rect.topleft = oldX, oldY

    def draw(self):
        window.blit(self.image, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)


class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        self.parent = parent
        self.px = px
        self.py = py
        self.dx = dx
        self.dy = dy
        self.damage = damage
        bullets.append(self)
        sndShot.play()

    def update(self):
        self.px += self.dx
        self.py += self.dy
        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.type != 'bang':
                    if obj.rect.collidepoint(self.px, self.py):
                        obj.damage(self.damage)
                        bullets.remove(self)
                        Bang(self.px, self.py)
                        sndDestroy.play()
                        break

    def draw(self):
        pygame.draw.circle(window, 'yellow', (self.px, self.py), 2)


class Bang:
    def __init__(self, px, py):
        objects.append(self)
        self.type = 'bang'
        self.px, self.py = px, py
        self.frame = 0

    def update(self):
        self.frame += 0.2
        if self.frame >= 5:
            objects.remove(self)

    def draw(self):
        img = imgBangs[int(self.frame)]
        rect = img.get_rect(center=(self.px, self.py))
        window.blit(img, rect)


class Block:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'
        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1

    def update(self):
        pass

    def draw(self):
        window.blit(imgBrick, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)


bullets = []
objects = []
player1 = Player('gray', imgPlayers[0], 50, 50, 1,
                 (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
player2 = Player('red', imgPlayers[1], 700, 500, 3,
                 (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN))
for _ in range(randint(60, 100)):
    while True:
        x = randint(0, WIDTH // TILE - 1) * TILE
        y = randint(1, HEIGHT // TILE - 1) * TILE
        rect = pygame.Rect(x, y, TILE, TILE)
        fined = False
        for obj in objects:
            if rect.colliderect(obj):
                fined = True
        if not fined:
            break
    Block(x, y, TILE)
isMove = False
isWin = False
isWinEndCheck = 0
y = 0
play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
    keys = pygame.key.get_pressed()
    oldIsMove = isMove
    isMove = False
    for obj in objects:
        if obj.type == 'player':
            isMove = isMove or obj.isMove
    for bullet in bullets:
        bullet.update()
    for obj in objects:
        obj.update()
    window.fill('black')
    for bullet in bullets:
        bullet.draw()
    for obj in objects:
        obj.draw()
    i = 0
    for obj in objects:
        if obj.type == 'player':
            text = fontUI.render(str(obj.hp), 1, obj.color)
            rect = text.get_rect(center=(5 + i * 70 + TILE, 5 + 11))
            window.blit(text, rect)
            i += 1
    t = 0
    for obj in objects:
        if obj.type == 'player':
            t += 1
            playerWin = obj
    if t == 1 and not isWin and isWinEndCheck == 0:
        isWin = True
    if isWin and isWinEndCheck == 0:
        pygame.mixer.music.load('sounds/finishSong.mp3')
        pygame.mixer.music.play()
        isWinEndCheck = 1
    if t == 1 and isWin:
        text = fontItem.render(f'Win {playerWin.color}!', 1, 'white')
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        window.blit(text, rect)
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
