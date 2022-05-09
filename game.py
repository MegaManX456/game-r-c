
import pygame
from sys import exit
import math
import random
pygame.init()
screen = pygame.display.set_mode((800,600))
w,h = screen.get_size()
clock = pygame.time.Clock()

score = 0
font = pygame.font.Font(None,30)
def debug(info,y = 10,x = 10):
    display_surf = pygame.display.get_surface()
    debug_surf = font.render(str(info),True,'White')
    debug_rect = debug_surf.get_rect(topleft = (x,y))
    display_surf.blit(debug_surf,debug_rect)

def collisions(square,enemies,bullets):
    score = 0
    for bullet in bullets:
        if pygame.sprite.spritecollide(bullet,enemies,True):
            bullet.kill()
            score += 1
    for enemy in enemies:
        if pygame.sprite.spritecollide(enemy,square,False):
            square.sprite.lives -= 1
    return score


class Square(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.mouse_pos = pygame.mouse.get_pos()
        self.image = pygame.Surface((10,10))
        self.image.fill('blue')
        self.rect = self.image.get_rect(center = (w//2,h//2))
        self.speed = 3
        self.lives = 5
    def shoot(self,mousepos):
        return Bullet(self.rect.centerx,self.rect.centery,mousepos)
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            self.speed = 1
        else:
            self.speed = 3
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.x < w:
            self.rect.x += self.speed
        if keys[pygame.K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.y < h:
            self.rect.y += self.speed
    def update(self):
        self.move()


class Bullet(pygame.sprite.Sprite):
    def __init__(self,playerx,playery,mouse_pos):
        super().__init__()
        self.x = playerx
        self.y = playery
        self.image = pygame.Surface((5,5))
        self.image.fill('red')
        self.rect = self.image.get_rect(center = (self.x,self.y))
        self.mouse_pos = mouse_pos
        self.speed = 10
        self.direction = pygame.math.Vector2(self.x - mouse_pos[0],self.y - mouse_pos[1]).normalize()
        self.newpos = [self.x,self.y]
        
    def move(self):
        self.newpos[0] -= self.direction.x * self.speed
        self.newpos[1] -= self.direction.y * self.speed
        self.rect.centerx = self.newpos[0]
        self.rect.centery = self.newpos[1]
    def update(self):
        self.move()
        if self.rect.x > w or self.rect.x < 0 or self.rect.y > h or self.rect.y < 0:
            self.kill()
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.Surface((20,20))
        self.image.fill('brown')
        self.rect = self.image.get_rect(center = pos)
        self.speed = 1
        self.direction = [0,0]
        self.newpos = [self.rect.x,self.rect.y]
    def move(self,target,enemies):
        self.direction = pygame.math.Vector2(self.rect.x - target[0],self.rect.y - target[1])
        if self.direction != [0,0]:
            self.direction = self.direction.normalize()
            self.newpos[0] -= self.direction[0] * self.speed 
            self.newpos[1] -= self.direction[1] * self.speed 
            # self.rect.topleft = self.newpos
        for enemy in enemies:
            if enemy is self:
                continue
            if pygame.sprite.collide_rect(self,enemy):
                self.direction.x = self.newpos[0] - enemy.newpos[0]
                self.direction.y = self.newpos[1] - enemy.newpos[1]
                self.direction = self.direction.normalize()
                self.newpos[0] += self.direction.x * 2
                self.newpos[1] += self.direction.y * 2
        self.rect.topleft = self.newpos

    def update(self,target,enemies):
        self.move(target,enemies)
    


square = Square()
square_gr = pygame.sprite.GroupSingle(square)

enemy_gr = pygame.sprite.Group()

bullet_gr = pygame.sprite.Group()

while True:
    clock.tick(60)
    screen.fill('grey')
    mouse_pos = pygame.mouse.get_pos()
    pygame.draw.line(screen,'green',square.rect.center,mouse_pos)
    if len(enemy_gr) <= 10 and random.randint(1,30)== 15:
        spawnside = random.choice(('left','right','top','bottom'))
        if spawnside == 'left':
            enemy_gr.add(Enemy((random.randint(0,50),random.randint(0,h))))
        if spawnside == 'right':
            enemy_gr.add(Enemy((random.randint(w-50,w),random.randint(0,h))))
        if spawnside == 'top':
            enemy_gr.add(Enemy((random.randint(0,w),random.randint(0,50))))
        if spawnside == 'bottom':
            enemy_gr.add(Enemy((random.randint(0,w),random.randint(h-50,h))))
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            bullet_gr.add(square.shoot(mouse_pos))
    
    score_font = font.render(str(score),True,'black')
    score_rect = score_font.get_rect(topright = (w-20,20))
    screen.blit(score_font,score_rect)

    lives_font = font.render(str(f'Lives: {square.lives}'),True,'black')
    lives_rect = lives_font.get_rect(topleft = (20,20))
    screen.blit(lives_font,lives_rect)

    square_gr.draw(screen)
    square_gr.update()

    bullet_gr.draw(screen)
    bullet_gr.update()

    enemy_gr.draw(screen)
    enemy_gr.update(square.rect.center,enemy_gr)

    score += collisions(square_gr,enemy_gr,bullet_gr)

    pygame.display.update()