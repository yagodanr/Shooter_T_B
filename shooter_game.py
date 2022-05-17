from pygame import *
from random import randint, choice
from math import cos, sin
from time import time as clocker

font.init()






class sSprite(sprite.Sprite):
    def __init__(self, kakapukaimage, x, y, speed=1, l=150, h=150):
        super().__init__()
        self.image = transform.scale(image.load(kakapukaimage), (l, h))
        self.step = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



class Player(sSprite):
    def update(self):

        
        key_pressed = key.get_pressed()

        if key_pressed[K_a] and self.rect.x>5:
            self.rect.x -= self.step
        if key_pressed[K_d] and self.rect.x<display.length-75:
            self.rect.x += self.step
    def update2(self):

        
        key_pressed1 = key.get_pressed()

        if key_pressed1[K_LEFT] and self.rect.x>5:
            self.rect.x -= self.step
        if key_pressed1[K_RIGHT] and self.rect.x<display.length-75:
            self.rect.x += self.step

class Enemy(sSprite):

    def update(self):
        if self.rect.y >= display.high-40:
            self.ran_coord()
            display.lost += 1
        self.rect.y += self.step

    def update_asteroid(self):
        if self.rect.y >= display.high-40:
            self.ran_coord()
            
        self.rect.y += self.step


    def ran_coord(self):
        self.rect.x = randint(80, display.length-80)
        self.rect.y = 0-self.step-50
        self.step = randint(1,4)   #*


class Bullet(sSprite):
    def __init__(self, kakapukaimage, x, y, left_right, angle, speed, l=150, h=150):
        super().__init__(kakapukaimage, x, y, speed, l, h)
        self.direction = left_right
        self.angle = angle
        self.coord_x = self.rect.x
        self.coord_y = self.rect.y
        if self.angle == 0:
            self.speed_x = 0
            self.speed_y = speed
        else:
            self.speed_x = abs(speed * cos(self.angle)) * self.direction
            self.speed_y = abs(speed * sin(self.angle))
    def update(self):
        self.coord_x += self.speed_x
        self.coord_y -= self.speed_y
        self.rect.x = self.coord_x
        self.rect.y = self.coord_y


length = 1280
high = 720


window = display.set_mode((length, high))


display.set_caption("Шутер")

display.length = length
display.high = high

display.lost = 0
display.got = 0

display.bullets = 0







background = transform.scale(image.load("фон серый.jpeg"), (display.length, display.high)) 






step = 13

clock = time.Clock()
FPS = 60







enemies = list()
bullets = list()
for i in range(1, 10):
    #*
    monster = Enemy("Уран 235.png", randint(80, display.length-80), -40, randint(1, 4), 80, 80)
    enemies.append(monster)

asteroids = list()
for i in range(1, 3):
    #*
    asteroid = Enemy("asteroid.png", randint(80, display.length-80), -40, randint(1, 4), 80, 120)
    asteroids.append(asteroid)



D_p = Player("Дейтерий.png", 400, display.high-150, step)
T_p = Player("Тритий.png", 200, display.high-150, step)




game = True




#
mixer.init() 
mixer.music.load("Chris Christodoulou - Risk of Rain 2 _ Risk of Rain 2 (2020).ogg") 
mixer.music.play()



font = font.SysFont("Arial", 36)

start_time = clocker()

finish = False


win = font.render("YOU WIN!", True, (255, 215, 0))
lose = font.render("YOU LOSE!", True, (255, 0, 0))

life = 150

flagafk = 0
while game:
    
    now = clocker()
    
    window.blit(background, (0, 0))

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYUP:
            if e.key == K_8: #pausa music
                mixer.music.pause()
            elif e.key == K_9:
                mixer.music.unpause()
                mixer.music.set_volume(0.5) #тише в 2 раза
    D_p.update()
    T_p.update2()
    for enemy in enemies:
        enemy.update()
    for asteroid in asteroids:
        asteroid.update_asteroid()

    got = font.render("Распалось: " + str(display.got), True, (255, 100, 0))
    lost = font.render("Пропущено: " + str(display.lost), True, (255, 100, 0))

    HP = font.render("Осталось ускорения: " + str(life), True, ((255, 100, 0)))



    for enemy in enemies:
        if sprite.collide_rect(D_p, enemy) or sprite.collide_rect(T_p, enemy):
            life -= 1
            enemy.ran_coord()
    for asteroid in asteroids:
        if sprite.collide_rect(D_p, asteroid) or sprite.collide_rect(T_p, asteroid):
            life -= 1
            asteroid.ran_coord()

    

    
    if sprite.collide_rect(D_p, T_p) and display.bullets == 0 and now > start_time+FPS*0.01:
        x = (D_p.rect.x+T_p.rect.x)/2 +30
        y = (D_p.rect.y+T_p.rect.y)/2
        for i in range(6):
            bulleter = Bullet("Ну тип нейтрон.png", x, y, choice([-1, 1]), randint(0, 40), 20, 20, 20)
            bullets.append(bulleter)
        display.bullets = 1
        start_time = clocker()
        life -= 2

    if abs(D_p.rect.x - T_p.rect.x) > 150:
        display.bullets = 0


    for bullet in bullets:
        bullet.update()
        for enemy in enemies:
            if sprite.collide_rect(bullet, enemy):
                enemy.ran_coord()


                flagafk = 1
                display.got += 5
                continue

        bullet.reset()
        

        if ((bullet.rect.x > display.length or bullet.rect.x < 0) or (bullet.rect.y < 0)) or flagafk:
            bullets.remove(bullet)
            flagafk = 0


    if display.got > 1000:
        window.blit(win, (length/2-100, high/2))


    if life <= 0 or display.lost >= 30:
        window.blit(lose, (length/2-100, high/2))
        life = 0
        D_p.rect.x = length*5
        D_p.step = 0
        T_p.rect.x = length*5
        T_p.step = 0





    
    D_p.reset()
    T_p.reset()
    for enemy in enemies:
        enemy.reset()
    for asteroid in asteroids:
        asteroid.reset()
    window.blit(got, (25, 75))
    window.blit(lost, (25, 100))
    window.blit(HP, (display.length - 400, 100))
    
    clock.tick(FPS)
    display.update() 




























window.blit(background, (0, 0))