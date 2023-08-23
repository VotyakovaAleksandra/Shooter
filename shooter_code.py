from pygame import *
from random import randint
timer1 =  time.Clock()
font.init()
window = display.set_mode((800,500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'),(800,500))
#переменные
lost = 0
lost_max = 3
score = 0
class GameSprite(sprite.Sprite):
    def __init__(self,picture,speed,x,y,width,hight):
        sprite.Sprite.__init__(self)
        self.width = width
        self.hight = hight
        self.image = transform.scale(image.load(picture),(self.width,self.hight))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def show1(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def move(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_RIGHT] and self.rect.x < 740:
            self.rect.x += self.speed
        if key_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
    def bullet1(self):
        bul = Bullet('bullet.png',6,(self.rect.x + self.width//2 - 7.5),(self.rect.y - self.hight),15,20)
        buls.add(bul)

class Ufo(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            global lost
            self.rect.y = -50
            self.rect.x = randint(0,740)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0 :
            self.kill()

player = Player('rocket.png',8,370,430,45,65)
monsters = sprite.Group()
for i in range(1,6):
    ufo = Ufo('ufo.png',2,randint(0,740),-50,60,40)
    monsters.add(ufo)
buls = sprite.Group()

finish = False
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #    fire_sound.play()
                player.bullet1()
    
    if not finish:
     
        window.blit(background,(0,0))
        player.move()
        monsters.update()
        buls.update()
        player.show1()
        monsters.draw(window)
        buls.draw(window)
        
        collides = sprite.groupcollide(buls,monsters,True,True) 
        for a in collides:
            score += 1
            ufo = Ufo('ufo.png',2,randint(0,740),0,60,40)
            monsters.add(ufo)

        if sprite.spritecollide(player,monsters,False) or lost >= lost_max:
            lost += 1
            finish = True
            font2 = font.SysFont('Arial', 45)
            text_lose = font2.render('YOU LOSE WITH SCORE : '+ str(score),True,(255,0,0))
            window.blit(text_lose,(260,100))

    
        if score >= 25: 
            finish = True
            font3 = font.SysFont('Arial',45)
            winner = font3.render('YOU WIN WITH SCORE : '+ str(score),True,(254, 236, 0))
            window.blit(winner,(260,100))

        font1 = font.SysFont('Arial', 25)
        text_score = font1.render('Счет: '+ str(score),True,(255,255,255))
        window.blit(text_score,(10,10))

        lose_ = font.SysFont('Arial', 25)
        lose_ = font1.render('Пропущенно: '+ str(lost),True,(255,255,255)) 
        window.blit(lose_,(10,35)) 

        display.update()
        timer1.tick(40)
