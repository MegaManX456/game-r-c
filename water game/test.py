from sys import exit
import pygame as pg
import random

pg.init()

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)

running = True
fps = 40
screen_w,screen_h = 800,600
screen = pg.display.set_mode((screen_w,screen_h))
gamefps = pg.time.Clock()

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((40,40))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = screen_w/2
        self.rect.y = screen_h/2
        self.speed = 5
    def get_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_d] and self.rect.right < screen_w:
            self.rect.x += self.speed
        if keys[pg.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pg.K_s]:
            self.rect.y += self.speed
        if keys[pg.K_w]:
            self.rect.y -= self.speed
    def shoot(self):
        return Bullet(player.rect.centerx,player.rect.centery)
    def update(self):
        self.get_input()
        self.shoot()

    
class Object(pg.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pg.Surface((60,60))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_falling = 3

    def update(self):
        self.rect.y += self.speed_falling
        if self.rect.y > screen_h:
            self.kill()
        
class Bullet(pg.sprite.Sprite):
    def __init__(self,player_x,player_y):
        super().__init__()
        self.image = pg.Surface((10,10))
        self.image.fill(blue)
        self.rect = self.image.get_rect(x = player_x,y = player_y)
        self.speed = 30
    def destroy_object(self,obj_group):
        hit = pg.sprite.spritecollideany(self,obj_group)
        if hit:
            self.kill()
            hit.kill()
                
    def update(self,obj_group):
        self.destroy_object(obj_group)
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
    
player = Player()
player_group = pg.sprite.Group()
player_group.add(player)

bullet_group = pg.sprite.Group()

object_group = pg.sprite.Group()

#main
while running:

    gamefps.tick(fps)
    screen.fill((10,10,10))

    #spawn objects
    if random.randint(0,30) == 15:
        object_sprite = Object(random.randrange(screen_h),0)
        if pg.sprite.spritecollideany(object_sprite,object_group) == None :
            object_group.add(object_sprite)

    #collision of obj and player
    if pg.sprite.spritecollideany(player, object_group):
        pg.quit()
        exit()


    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                bullet_group.add(player.shoot())
    
    bullet_group.draw(screen)
    bullet_group.update(object_group)

    player_group.draw(screen)   
    player_group.update()

    object_group.draw(screen)
    object_group.update()
        
    pg.display.flip()