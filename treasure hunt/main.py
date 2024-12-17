import random
import pygame
import time

pygame.init()

screen_width = 900
screen_height = 700
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Treasure Hunt Game")

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
pink = (255, 192, 203)

class Treasure(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        super().__init__()
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(center=(x, y))

class Ely(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("ely.png")
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect(center=(screen_width // 2, screen_height // 2))

class Good(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        super().__init__()
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect(center=(x, y))

class Bad(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("kevin.png")
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect(center=(x, y))

all_sprites = pygame.sprite.Group()
good_list = pygame.sprite.Group()
bad_list = pygame.sprite.Group()
treasure_list = pygame.sprite.Group()

ely = Ely()
all_sprites.add(ely)

good_images = ["eden.png", "mei.png"]

good_pairs = []
for i in range(30):
    x, y = random.randrange(50, screen_width - 50), random.randrange(50, screen_height - 50)
    good_item = Good(random.choice(good_images), x, y)
    treasure = Treasure("treasure1.jpg", x, y)
    
    good_list.add(good_item)
    treasure_list.add(treasure)
    all_sprites.add(good_item, treasure)
    
    good_pairs.append((good_item, treasure))

bad_pairs = []
for i in range(10):
    x, y = random.randrange(50, screen_width - 50), random.randrange(50, screen_height - 50)
    bad_item = Bad(x, y)
    treasure = Treasure("treasure2.jpg", x, y)
    
    bad_list.add(bad_item)
    treasure_list.add(treasure)
    all_sprites.add(bad_item, treasure)
    
    bad_pairs.append((bad_item, treasure))

score = 0
playing = True
clock = pygame.time.Clock()
start_time = time.time()
font = pygame.font.SysFont("Arial", 22)

while playing:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

    time_elapsed = time.time() - start_time

    if time_elapsed >= 30:
        if score >= 20:
            screen.fill("Gold")
            result_text = font.render("Lucky!", True, black)
        else:
            screen.fill(red)
            result_text = font.render("Unlucky!", True, black)
        screen.blit(result_text, (250, 40))
    else:
        screen.fill(pink)

        countdown_text = font.render(f"Time Left: {60 - int(time_elapsed)}", True, white)
        screen.blit(countdown_text, (20, 10))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and ely.rect.y > 0:
            ely.rect.y -= 5
        if keys[pygame.K_DOWN] and ely.rect.y < screen_height - 70:
            ely.rect.y += 5
        if keys[pygame.K_LEFT] and ely.rect.x > 0:
            ely.rect.x -= 5
        if keys[pygame.K_RIGHT] and ely.rect.x < screen_width - 70:
            ely.rect.x += 5

        good_hit_list = pygame.sprite.spritecollide(ely, good_list, True)
        for good_item in good_hit_list:
            for pair in good_pairs:
                if pair[0] == good_item:
                    pair[1].kill()  
                    good_pairs.remove(pair)
                    break
            score += 1

        bad_hit_list = pygame.sprite.spritecollide(ely, bad_list, True)
        for bad_item in bad_hit_list:
            for pair in bad_pairs:
                if pair[0] == bad_item:
                    pair[1].kill() 
                    bad_pairs.remove(pair)
                    break
            score -= 5
        score_text = font.render(f"Score: {score}", True, red)
        screen.blit(score_text, (20, 50))
        all_sprites.draw(screen)
    pygame.display.update()
pygame.quit()
