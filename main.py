import pygame
import random


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('game1\images\player.png').convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        self.direction = pygame.Vector2()
        self.speed=300

        #cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed() 
        self.direction.x= int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y= int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction=self.direction.normalize() if self.direction else self.direction #ensures speed is constant on diagonal movement
        self.rect.center += self.direction * self.speed * dt
        recent_keys = pygame.key.get_just_pressed()

        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
        
        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = star_surf
        self.rect = self.image.get_frect(center = (random.randint(0,WINDOW_WIDTH),random.randint(0,WINDOW_HEIGHT))) #create 20 random x and y positions for stars

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom=pos)
    
    def update(self,dt):
        self.rect.centery -=800 *dt
        if self.rect.bottom < 0: 
            self.kill() 

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.orignal_surf = surf
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(random.uniform(-0.5, 0.5),1)
        self.speed = random.randint(400,500)
        self.rotation_speed = random.randint(40,80)
        self.rotation = 0
    
    def update(self,dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.orignal_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

def collisions():
    global running

    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if collision_sprites:
        print(collision_sprites[0])
        running=False
    
    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser,meteor_sprites,True)
        if collided_sprites:
            laser.kill()

def display_score():
    current_time = pygame.time.get_ticks() // 10
    text_surf=font.render(str(current_time), True, '#a0dee8')
    text_rect = text_surf.get_rect(midbottom=(WINDOW_WIDTH /2, WINDOW_HEIGHT - 50))
    display_surface.blit(text_surf,text_rect)
    pygame.draw.rect(display_surface, '#a0dee8', text_rect.inflate(25,25).move(0,-5),5,10)



#general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT=1280,720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Shooting Game")
running = True
clock = pygame.time.Clock()

# import
meteor_surf=pygame.image.load('game1\images\meteor.png').convert_alpha()
laser_surf=pygame.image.load('game1\images\laser.png').convert_alpha()
star_surf = pygame.image.load('game1\images\star.png').convert_alpha()
font = pygame.font.Font('game1\images\Oxanium-Bold.ttf', 36)


# sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
for i in range(20):
    Star(all_sprites,star_surf)
player=Player(all_sprites)

# custom events -> meteor event

meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event,500)

test_rect = pygame.FRect(0,0,300,600)

while running:
    dt=clock.tick() /1000
    # event loop
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type == meteor_event:
            x,y = random.randint(0,WINDOW_WIDTH), random.randint(-200,-100)
            Meteor(meteor_surf, (x,y), (all_sprites, meteor_sprites))
    #update
    all_sprites.update(dt)
    collisions()
    
    #draw the game
    display_surface.fill('#25204f') #draw background
    all_sprites.draw(display_surface)
    display_score()

    # test collision
    pygame.display.update()
    
pygame.quit()
