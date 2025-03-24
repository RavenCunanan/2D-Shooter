import pygame
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('game1\images\player.png').convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.direction = pygame.Vector2()
        self.speed = 300

        # Cooldown
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
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction  # Ensures speed is constant on diagonal movement
        self.rect.center += self.direction * self.speed * dt
        recent_keys = pygame.key.get_just_pressed()

        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()

        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = star_surf
        self.rect = self.image.get_frect(center=(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)))  # Create 20 random x and y positions for stars

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom=pos)

    def update(self, dt):
        self.rect.centery -= 800 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_surf = surf
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(random.uniform(-0.5, 0.5), 1)
        self.speed = random.randint(400, 500)
        self.rotation_speed = random.randint(40, 80)
        self.rotation = 0

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center=self.rect.center)

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center=pos)

    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index) % len(self.frames)]
        else:
            self.kill()

def collisions():
    global running, game_over

    if game_over or paused:
        return

    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if collision_sprites:
        game_over = True
        damage_sound.play()

    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
            explosion_sound.play()

def display_score():
    global score

    if not paused:  # Only update the score if the game isn't paused
        if game_over:
            score = 0  # Show score as 0 during game over
        else:
            score = (pygame.time.get_ticks() - start_time) // 10  # Calculate score based on elapsed time

        # Display the score
        text_surf = font.render(str(score), True, '#a0dee8')
        text_rect = text_surf.get_rect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
        display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(display_surface, '#a0dee8', text_rect.inflate(25, 25).move(0, -5), 5, 10)

# General setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Shooting Game")
running = True
paused = False
game_over = False
clock = pygame.time.Clock()

# Import
meteor_surf = pygame.image.load('game1\images\meteor.png').convert_alpha()
laser_surf = pygame.image.load('game1\images\laser.png').convert_alpha()
star_surf = pygame.image.load('game1\images\star.png').convert_alpha()
font = pygame.font.Font('game1\images\Oxanium-Bold.ttf', 36)
explosion_frames = [pygame.image.load(f'game1/images/explosion/{i}.png').convert_alpha() for i in range(21)]

laser_sound = pygame.mixer.Sound('game1\\audio\\laser.wav')
laser_sound.set_volume(0.2)
explosion_sound = pygame.mixer.Sound('game1\\audio\\explosion.wav')
explosion_sound.set_volume(0.2)
damage_sound = pygame.mixer.Sound('game1\\audio\\damage.ogg')
damage_sound.set_volume(0.2)
game_music = pygame.mixer.Sound('game1\\audio\\game_music.wav')
game_music.set_volume(0.2)
game_music.play()

# Sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
for i in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)

# Custom events -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

# Global score and timer setup
score = 0
start_time = pygame.time.get_ticks()

while running:
    dt = clock.tick() / 1000
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused  # Toggle pause
            if game_over and event.key == pygame.K_RETURN:  # Restart game
                # Reset all game variables (score, player, meteors, etc.)
                score = 0  # Reset score
                start_time = pygame.time.get_ticks()  # Reset the timer
                player.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
                player.can_shoot = True
                player.laser_shoot_time = 0
                meteor_sprites.empty()  # Remove all meteors
                laser_sprites.empty()   # Remove all lasers
                game_over = False  # Set game over to False when restarting
        if event.type == meteor_event:
            x, y = random.randint(0, WINDOW_WIDTH), random.randint(-200, -100)
            Meteor(meteor_surf, (x, y), (all_sprites, meteor_sprites))

    if not paused and not game_over:  # Game logic only if not paused and not game over
        all_sprites.update(dt)
        collisions()

    # Draw the game screen
    display_surface.fill('#25204f')  # Draw background
    all_sprites.draw(display_surface)
    display_score()

    if paused:
        # Display "Paused" text in the middle of the screen
        pause_text = font.render('PAUSED', True, '#a0dee8')
        pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        display_surface.blit(pause_text, pause_rect)

    if game_over:
        # Display "Game Over" and "Press Enter to Play Again"
        game_over_text = font.render('GAME OVER', True, '#a0dee8')
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50))
        display_surface.blit(game_over_text, game_over_rect)

        play_again_text = font.render('Press Enter to Play Again', True, '#a0dee8')
        play_again_rect = play_again_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50))
        display_surface.blit(play_again_text, play_again_rect)

    pygame.display.update()

pygame.quit()
