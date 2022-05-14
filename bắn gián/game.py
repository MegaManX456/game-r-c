
import pygame
from sys import exit
import math
import random
pygame.init()
screen = pygame.display.set_mode((800,600))
w,h = screen.get_size()
clock = pygame.time.Clock()

#methods
def rot_center(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)
    return rotated_image, new_rect

def to_angle(point1,point2):
    angle = math.degrees(math.atan2(-(point2[0] - point1[0]), -(point2[1] - point1[1])))
    return angle
###

def collisions(square,enemies,bullets):
    score = 0
    for bullet in bullets:
        for enemy in enemies:
            if bullet.rect.colliderect(enemy.hitbox):
                enemy.kill()
                bullet.kill()
                score += 1

    for enemy in enemies:
        if enemy.hitbox.colliderect(square.sprite) and not square.sprite.is_invincible:
            square.sprite.last_hit = pygame.time.get_ticks()
            square.sprite.lives -= 1
            square.sprite.is_invincible = True
    current_time = pygame.time.get_ticks()
    if current_time - square.sprite.last_hit > square.sprite.invincible_time:
        square.sprite.is_invincible = False
        square.sprite.last_hit = current_time
    return score


class Square(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.mouse_pos = pygame.mouse.get_pos()
        self.image = pygame.image.load('hooman.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(50,70))
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect(center = (w//2,h//2))
        self.speed = 3
        self.lives = 3
        self.invincible_time = 1000
        self.is_alive = True
        self.is_invincible = False
        self.last_hit = 0
        self.cooldown = 100
        self.lastshoot = 0
    def shoot(self,mousepos,bullets):
        mouse = pygame.mouse.get_pressed()
        if mousepos[0] >= self.rect.centerx:
            shooting_point = (self.rect.right,self.rect.centery)
        else:
            shooting_point = (self.rect.left,self.rect.centery)
        currenttime = pygame.time.get_ticks()
        if mouse[0] and currenttime - self.lastshoot > self.cooldown:
            self.lastshoot = currenttime 
            bullets.add(Bullet(shooting_point[0],shooting_point[1],mousepos))
        else:
            pass
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

        
    def update(self,mousepos,bullets):
        # pygame.draw.rect(screen,'red',self.rect,2)
        self.move()
        self.shoot(mousepos,bullets)
        if self.lives < 0:
            self.is_alive = False


class Bullet(pygame.sprite.Sprite):
    def __init__(self,playerx,playery,mouse_pos):
        super().__init__()
        self.x = playerx
        self.y = playery
        self.image = pygame.image.load('bullet.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(10,10))
        self.image.set_colorkey('white')
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
        self.image = pygame.image.load('cockcroach1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(120,120))
        self.first_image = self.image
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect.inflate(-50,-20)
        self.speed = 1
        self.direction = [0,0]
        self.newpos = [self.rect.centerx,self.rect.centery]
    def move(self,target,enemies):
        self.direction = pygame.math.Vector2(self.rect.centerx - target[0],self.rect.centery - target[1])
        self.image = self.first_image
        angle = to_angle(self.rect.center,target)
        self.image,self.rect = rot_center(self.image,angle,self.rect.centerx,self.rect.centery)

        if self.direction != [0,0]:
            self.direction = self.direction.normalize()
            
            self.newpos[0] -= self.direction[0] * self.speed 
            self.newpos[1] -= self.direction[1] * self.speed 
        for enemy in enemies:
            if enemy is self:
                continue
            if self.hitbox.colliderect(enemy.hitbox):
                self.direction.x = self.newpos[0] - enemy.newpos[0]
                self.direction.y = self.newpos[1] - enemy.newpos[1]
                self.direction = self.direction.normalize()
                self.newpos[0] += self.direction.x * 2
                self.newpos[1] += self.direction.y * 2
        self.hitbox.center = self.newpos
        self.rect.center = self.hitbox.center

    def update(self,target,enemies):
        # pygame.draw.rect(screen,'red',self.hitbox,5)
        self.move(target,enemies)
    

def game():
    bg = pygame.image.load('map.png')
    bg = pygame.transform.scale(bg,(800,1600))
    font = pygame.font.Font(None,50)
    score = 0
    running = True
    square = Square()
    square_gr = pygame.sprite.GroupSingle(square)

    enemy_gr = pygame.sprite.Group()

    bullet_gr = pygame.sprite.Group()

    while running:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
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
        
        if square.is_alive:
            screen.blit(bg,(0,0))
            square_gr.draw(screen)
            # pygame.draw.line(screen,'green',square.rect.center,mouse_pos)

            square_gr.update(mouse_pos,bullet_gr)

            bullet_gr.draw(screen)
            bullet_gr.update()

            enemy_gr.draw(screen)
            enemy_gr.update(square.rect.center,enemy_gr)

            score += collisions(square_gr,enemy_gr,bullet_gr)

            score_font = font.render(str(score),True,'white')
            score_rect = score_font.get_rect(topright = (w-20,20))
            screen.blit(score_font,score_rect)

            lives_font = font.render(str(f'Lives: {square.lives}'),True,'white')
            lives_rect = lives_font.get_rect(topleft = (20,20))
            screen.blit(lives_font,lives_rect)

        else:
            
            font = pygame.font.Font(None,100)
            death_font = font.render(str('YOU DIE'),True,'red')
            death_rect = death_font.get_rect(center = (w//2,h//2))
            screen.blit(death_font,death_rect)
            running = False
        pygame.display.update()
game()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game()
        