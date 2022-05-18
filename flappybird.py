import pygame 
import sys
import random
#setup
pygame.init()
screen_w, screen_h = 600,500
screen = pygame.display.set_mode((screen_w,screen_h))
clock = pygame.time.Clock()
font = pygame.font.Font(None,70)

#####

#bird
class Bird(pygame.sprite.Sprite):
    def __init__(self,y):
        super().__init__()
        self.image = pygame.Surface((25,25))
        self.image.fill('yellow')
        self.rect = self.image.get_rect(center = (screen_w//3,y))
        self.x = screen_w//2
        self.vel = 0.5
        self.score = 0
        self.falling_speed = 0
        self.is_alive = True

    def falling(self):
        if self.falling_speed > 15:
            self.falling_speed = 15
        self.rect.y += self.falling_speed + 0.5* self.vel
        self.falling_speed += self.vel
    def jump(self):
        self.falling_speed = -8

    def update(self):
        self.falling()

#pipe
class PipeGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
    def custom_draw(self,screen):
        for sprite in self.sprites():
            screen.blit(sprite.top_pipe_image,sprite.top_pipe_rect.topleft)
            screen.blit(sprite.bot_pipe_image,sprite.bot_pipe_rect.topleft)

class Pipes(pygame.sprite.Sprite):
    speed = 2
    def __init__(self,y):
        super().__init__()
        self.weight = 40
        self.height = 800
        self.offset = 120

        self.top_pipe_image = pygame.Surface((self.weight,self.height))
        self.top_pipe_image.fill('green')
        self.top_pipe_rect = self.top_pipe_image.get_rect(bottomleft = (screen_w,y))

        self.bot_pipe_image = pygame.Surface((self.weight,self.height))
        self.bot_pipe_image.fill('green')
        self.bot_pipe_rect = self.bot_pipe_image.get_rect(topleft = (screen_w, self.top_pipe_rect.bottom + self.offset))
        
        self.score_given = False
    def update(self,bird):
        self.top_pipe_rect.x -= self.speed
        self.bot_pipe_rect.x -= self.speed
        if bird.rect.left > self.top_pipe_rect.right and not self.score_given:
            bird.score += 1
            self.score_given = True
        if self.top_pipe_rect.right < 0:
            self.kill()
    
def testcollide(bird,pipes):
    for pipe in pipes:
        if bird.rect.colliderect(pipe.top_pipe_rect) or bird.rect.colliderect(pipe.bot_pipe_rect)\
            or bird.rect.bottom < 0 or bird.rect.top > screen_h:
            Pipes.speed = 2
            bird.is_alive = False
            return True
        
        


#main
def main():
    running = True
    #instance
    bird = Bird(screen_h//2)
    bird_group = pygame.sprite.GroupSingle()
    bird_group.add(bird)

    pipes_group = PipeGroup()
    ####
    pipe_spawn_time = 2000
    pipe_last_spawn = 0
    while running:
        clock.tick(60)
        current_time = pygame.time.get_ticks()

        #spawn pipes
        if current_time - pipe_last_spawn > pipe_spawn_time:
            pipes_group.add(Pipes(random.randint(80,300)))
            pipe_last_spawn = current_time
        if pipe_spawn_time >1200:
            pipe_spawn_time -= 0.1
        #check collide
        if bird.is_alive == True:
            screen.fill('cyan')

            bird_group.update()
            bird_group.draw(screen)
            
            pipes_group.custom_draw(screen)
            pipes_group.update(bird)

            scorefont = font.render(f'{bird.score}',True,'red')
            scorerect = scorefont.get_rect(topleft = (10,10))
            screen.blit(scorefont,scorerect)
            
            testcollide(bird,pipes_group)
                
        


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
                if event.key == pygame.K_r:
                    running = False

        
        pygame.display.flip()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    main()