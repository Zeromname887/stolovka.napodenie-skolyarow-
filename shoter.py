from pygame import *
from random import randint

mixer.init()
mixer.music.load("fonovye-zvuki-v-stolovoj.mp3")
mixer.music.play()

fire_sound = mixer.Sound("polet-i-vtykanie-noja-v-plot.mp3")

font.init()

font1 = font.Font(None, 80)
win = font1.render("YOU WIN!", True, (255, 255, 255))
lose = font1.render("YOU LOSE!!!!!", True, (180, 0, 0))

font2 = font.Font(None, 36)

img_back = "stolovka.jpg"
img_hero = "leg.jpg"
img_bullet = "kotletka.png"
img_enemy = "sholnik.png"

score = 0
goal = 250
lost = 0
max_lost = 5

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
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
            self.rect.x -= self.speed

        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed

        if keys[K_DOWN] and self.rect.x < win_height -80:
            self.rect.y += self.speed

        if keys[K_RIGHT] and self.rect.x < win_wight-80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx-7, self.rect.top, 20,  25, 25)
        bullets.add(bullet)
        bullet = Bullet(img_bullet, self.rect.centerx-50, self.rect.top, 20,  25, 25)
        bullets.add(bullet)
        bullet = Bullet(img_bullet, self.rect.centerx+50, self.rect.top, 20,  25, 25)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(20, win_wight - 80)
            self.rect.y = -40
            lost = lost + 1 

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <-10:
            self.kill


win_wight = 750
win_height = 550
display.set_caption("Ctolovka. Napodenie shkolyarow!")
window = display.set_mode((win_wight, win_height))
background = transform.scale(image.load(img_back), (win_wight, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 10):
    monster = Enemy(img_enemy, randint(5, win_wight - 80), -40, 80, 50, randint(1, 3))
    monsters.add(monster)

bullets = sprite.Group()

finish = True
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
    
    if finish:
        window.blit(background, (0,0))

        text = font2.render("Грустных школьников(: " + str(score), 1, (155, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Веселых школьников): " + str(lost), 1, (155, 255, 255))
        window.blit(text_lose, (10, 50))

        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint (5, win_wight - 80), -40, 80, 50, randint (1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = False
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = False
            window.blit(win, (200, 200))

    else:
        finish = True
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()

        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(5, win_wight - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
    display.update()
    time.delay(50)