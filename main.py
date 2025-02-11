import pygame
import random

#general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT=1280,720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Shooting Game")
running = True
clock = pygame.time.Clock()

# plain surface
surf = pygame.Surface((100,200))
surf.fill('orange')
x=100

#importing an image
player_surf=pygame.image.load('game1\images\player.png').convert_alpha() #convert_alpha for higher frame rate
player_rect=player_surf.get_frect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
player_direction=pygame.math.Vector2()
player_speed=300

star_surf=pygame.image.load('game1\images\star.png').convert_alpha()
star_positions=[(random.randint(0,WINDOW_WIDTH),random.randint(0,WINDOW_HEIGHT)) for i in range(20)] #create 20 random x and y positions for stars

meteor_surf=pygame.image.load('game1\images\meteor.png').convert_alpha()
meteor_rect=meteor_surf.get_frect(center=((WINDOW_WIDTH/2,WINDOW_HEIGHT/2)))

laser_surf=pygame.image.load('game1\images\laser.png').convert_alpha()
laser_rect=meteor_surf.get_frect(bottomleft=((20,WINDOW_HEIGHT-20)))


while running:
    dt=clock.tick() /1000
    # event loop
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    #   if event.type==pygame.KEYDOWN and event.key==pygame.K_1:
    #      print(1)
    #   if event.type==pygame.MOUSEMOTION:
    #      player_rect.center = event.pos

    #input
   #print(pygame.mouse.get_rel())
    keys=pygame.key.get_pressed()
   
    player_direction.x= int(keys[pygame.K_d]) - int(keys[pygame.K_a])
    player_direction.y= int(keys[pygame.K_s]) - int(keys[pygame.K_w])
    player_direction=player_direction.normalize() if player_direction else player_direction #ensures speed is constant on diagonal movement
 
    player_rect.center += player_direction * player_speed * dt

    recent_keys = pygame.key.get_just_pressed()
    if recent_keys[pygame.K_SPACE]:
        print("Fire Laser")
   
    #draw the game
    display_surface.fill('darkseagreen') #draw background
    for pos in star_positions: #create 20 stars in random position
        display_surface.blit(star_surf, pos )
    
    
    display_surface.blit(player_surf,(player_rect)) #draw player
    display_surface.blit(meteor_surf,(meteor_rect))
    display_surface.blit(laser_surf,(laser_rect))


    pygame.display.update()


pygame.quit()
