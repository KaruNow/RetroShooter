from pygame import *
from random import *
from time import time as timer

#классы
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size1, size2, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size1, size2))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= (self.speed)*1.5
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += (self.speed)*1.5
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10, 30, -15)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

lost = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 400)
            self.rect.y = 0
            lost += 1

class Aster(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(80, 400)
            self.rect.y = 0
            
#окно
window = display.set_mode((700, 500))
display.set_caption('Galaxy(шутер)')

#картинка
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

#групы
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()

#спрайты
player = Player('rocket.png', 300, 430, 65, 65, 5)
    
for i in range(1, 5):
    x = Enemy('ufo.png', randint(0, 600), 20, 65, 65, randint(1,3))
    monsters.add(x)

for q in range(1, 4):
    a = Aster('asteroid.png', randint(0, 600), 20, 65, 65, randint(1,2))
    asteroids.add(a)

#текст
font.init()
font = font.SysFont("Arial", 30)
win = font.render('ТЫ ВЫЙГРАЛ!', True, (255, 165, 0))
lose = font.render('ХАХАХ ЛОХ!', True, (255, 165, 0))
#музыка
mixer.init()
mixer.music.load('space.ogg')
fire_sound = mixer.Sound('fire.ogg')
mixer.music.play()

#частота кадров
FPS = 60
clock = time.Clock()

#счётчики
score = 0
lost = 0
lives = 120
#для игрового цикла
num_fire = 0
rel_time = False
run = True
finish = False
#цмкл
while run:

    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:

                if num_fire < 12 and rel_time == False:
                    fire_sound.play()
                    player.fire()
                    num_fire += 1
                
                if num_fire >= 12 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    #выигрыш
    if finish != True:
        window.blit(background, (0,0))

        q = font.render('Убито:' + str(score), True, (255, 165, 0))
        e = font.render('Пропущенно:' + str(lost), True, (255, 165, 0))
        h = font.render('HP:' + str(lives), True, (20, 250, 50))
        window.blit(q, (25, 25))
        window.blit(e, (25, 60))
        window.blit(h, (500, 60))

        monsters.draw(window)
        monsters.update()

        asteroids.draw(window)
        asteroids.update()

        bullets.draw(window)
        bullets.update()

        player.update()
        player.reset()

        if sprite.spritecollide(player, monsters, False):
            if lives < 0:
                finish = True
                window.blit(lose, (225, 200))
            else:
                lives -= 1
            
        if sprite.spritecollide(player, asteroids, False):
            if lives < 0:
                finish = True
                window.blit(lose, (225, 200))
            else:
                lives -= 1

        if sprite.groupcollide(monsters, bullets, True, True):
            score += 1
            x1 = Enemy('ufo.png', randint(0, 600), 0, 65, 65, 1)
            monsters.add(x1)

        if score == 30:
            finish = True
            window.blit(win, (225, 200))
        
        if lost == 20:
            finish = True
            window.blit(lose, (225, 200))

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 2:
                per = font.render('ЩА 5 СЕК...', True, (255, 165, 0))
                window.blit(per, (280, 450))
            
            else:
                num_fire = 0
                rel_time = False

    #обновление
    display.update()
    clock.tick(FPS)