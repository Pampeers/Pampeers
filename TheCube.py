import pygame
import random

pygame.init()
pygame.font.init()

#Screen
WIDTH, HEIGHT = 1920, 1080 #Screen sizes(In pixels) P.S. You can write here sizes of your screen
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Cube")

#Font
f1 = pygame.font.SysFont('Comic Sans MS', 36)
f2 = pygame.font.SysFont('Comic Sans MS', 50)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (200, 0, 255)

#Other properties
win_count = 20 #The number of points to win
spawn_height = 210 #As higher the lower spawn of coins and mobs
#Chances
monster_chance = 150 #As higher the smaller chance
monster2_chance = 350 #As higher the smaller chance
coin_chance = 200 #As higher the smaller chance


#Variables
count = 0

#Blocks properties
BLOCK_WIDTH, BLOCK_HEIGHT = 150, 150 #Blocks sizes


#Hero properties
HERO_WIDTH, HERO_HEIGHT = 50, 50 #Hero sizes
HERO_X, HERO_Y = WIDTH // 2, HEIGHT - BLOCK_HEIGHT - HERO_HEIGHT #Hero spawnpoint
HERO_VEL = 5 #Hero movement speed
JUMP_VEL = 15 #Jump speed(max jump height depends on the jump speed)
GRAVITY = 0.5 #Fall speed

# Monsters properties
MONSTER_WIDTH, MONSTER_HEIGHT = 30, 30
MONSTER_VEL = 3

#Monster lvl2 properties
MONSTER2_WIDTH, MONSTER2_HEIGHT = 50, 50
MONSTER2_VEL = 5

# Coin properties
COIN_WIDTH, COIN_HEIGHT = 20, 20
COIN_VEL = 2

# Images
HERO_IMAGE = pygame.Surface((HERO_WIDTH, HERO_HEIGHT))
HERO_IMAGE.fill(YELLOW)

MONSTER_IMAGE = pygame.Surface((MONSTER_WIDTH, MONSTER_HEIGHT))
MONSTER_IMAGE.fill(RED)

MONSTER2_IMAGE = pygame.Surface((MONSTER2_WIDTH, MONSTER2_HEIGHT))
MONSTER2_IMAGE.fill(PURPLE)

COIN_IMAGE = pygame.Surface((COIN_WIDTH, COIN_HEIGHT))
COIN_IMAGE.fill(WHITE)



# Classes
class Hero:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, HERO_WIDTH, HERO_HEIGHT)
        self.vel_y = 0
        self.jumping = False


    def move(self, dx, dy):
        #Move
        if 0 <= self.rect.x + dx <= WIDTH - HERO_WIDTH:
            self.rect.x += dx
            #Check block collision
            for block in blocks:
                if self.rect.colliderect(block.rect):
                    if dx > 0:
                        dx = 0
                        self.rect.right = block.rect.left
                    elif dx < 0:
                        dx = 0
                        self.rect.left = block.rect.right
        self.rect.y += dy
        


    def jump(self):
        if not self.jumping:
            self.vel_y = -JUMP_VEL
            self.jumping = True
            

    def update(self):
        global on_ground
        #Jumping
        if self.jumping:
            self.vel_y += GRAVITY
            self.rect.y += self.vel_y
            if self.rect.y >= HEIGHT - HERO_HEIGHT:
                self.rect.y = HEIGHT - HERO_HEIGHT
                self.vel_y = 0
                self.jumping = False

        #Gravity
        on_ground = False
        for block in blocks:
            if hero.rect.colliderect(block.rect):
                if block.rect.top <= hero.rect.bottom:
                    on_ground = True
        if on_ground == False:
            if self.jumping == False:
                self.vel_y += GRAVITY
                self.rect.y += self.vel_y

        #Check blocks collision
        for block in blocks:
            if  hero.rect.colliderect(block.rect):
                if hero.vel_y > 0:
                    hero.rect.bottom = block.rect.top
                    hero.vel_y = 0
                    hero.jumping = False
                if hero.vel_y < 0:
                    hero.rect.top = block.rect.bottom
                    hero.vel_y = 0
            


                


class Monster:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)

    def update(self):
        self.rect.x -= MONSTER_VEL

class Monster2:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, MONSTER2_WIDTH, MONSTER2_HEIGHT)

    def update(self):
        self.rect.x -= MONSTER2_VEL

class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, COIN_WIDTH, COIN_HEIGHT)

    def update(self):
        self.rect.x -= COIN_VEL

class Block:
    def __init__(self, x, y, height):
        self.rect = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)

# Draw function
def draw_window(hero, monsters, monsters2, coins, blocks, count):
    WIN.fill(BLACK)
    pygame.draw.rect(WIN, WHITE, hero.rect)

    for monster in monsters:
        pygame.draw.rect(WIN, RED, monster.rect)
    
    for monster2 in monsters2:
        pygame.draw.rect(WIN, PURPLE, monster2.rect)

    for coin in coins:
        pygame.draw.rect(WIN, YELLOW, coin.rect)

    for block in blocks:
        pygame.draw.rect(WIN, GREEN, block.rect)
        
    #COUNT
    count = str(count)
    coins_tx = f1.render(count, True,
                  WHITE)
    WIN.blit(coins_tx, (10, 5))

blocks = []
for i in range(0, WIDTH, BLOCK_WIDTH):
    block_type = random.choice(["block", "gap"])
    if block_type == "block":
        blocks.append(Block(i, HEIGHT - BLOCK_HEIGHT, BLOCK_HEIGHT)) 
    else:
        blocks.append(Block(i, HEIGHT - 0.6*BLOCK_HEIGHT, BLOCK_HEIGHT)) 

# Hero creating
hero = Hero(HERO_X, HERO_Y)

# Monster creating
monsters = []

# Monster lvl2 creating
monsters2 = []

# Coin creating
coins = []

#Run game
clock = pygame.time.Clock()

run = True
while run:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                hero.jump()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        hero.move(-HERO_VEL, 0)
    if keys[pygame.K_d]:
        hero.move(HERO_VEL, 0)
    elif keys[pygame.K_LEFT]:
        hero.move(-HERO_VEL, 0)
    elif keys[pygame.K_RIGHT]:
        hero.move(HERO_VEL, 0)

    # Monster generation
    if random.randint(0, monster_chance) < 2:
        monsters.append(Monster(WIDTH, random.randint(spawn_height, HEIGHT - 1.1*BLOCK_HEIGHT)))

    # Monster lvl2 generation
    if random.randint(0, monster2_chance) < 2:
        monsters2.append(Monster2(WIDTH, random.randint(spawn_height, HEIGHT - 1.2*BLOCK_HEIGHT)))

    # Coin generation
    if random.randint(0, coin_chance) < 2:
        coins.append(Coin(WIDTH, random.randint(spawn_height, HEIGHT - 1.1*BLOCK_HEIGHT)))

    # Monster update
    for monster in monsters:
        monster.update()
    for monster2 in monsters2:
        monster2.update()

    # Coin update
    for coin in coins:
        coin.update()

    # Check collision(Monsters with Hero)
    for monster in monsters:
        if hero.rect.colliderect(monster.rect):
            monsters.remove(monster)
            if finish == False:
                count -= 1
                if count < 0:
                        count = 0

    for monster2 in monsters2:
        if hero.rect.colliderect(monster2.rect):
            monsters2.remove(monster2)
            if finish == False:
                count -= 3
                if count < 0:
                    count = 0

    # Check collision(Hero with coins)
    for coin in coins:
        if hero.rect.colliderect(coin.rect):
            coins.remove(coin)
            count += 1

    finish = False
    #FINISH GAME
    def finish():
        global HERO_VEL, MONSTER_VEL, MONSTER2_VEL, COIN_VEL, GRAVITY, JUMP_VEL
        if count >= win_count:
            finish = True
            #WIN TEXT
            win_tx = f2.render('You won!', True, GREEN)
            WIN.blit(win_tx, (0.45*WIDTH, 0.45*HEIGHT))
            #OFF
            HERO_VEL = 0
            MONSTER_VEL = 0
            MONSTER2_VEL = 0
            COIN_VEL = 0
            GRAVITY = 0
            JUMP_VEL = 0
            hero.rect.x = 0.5*WIDTH
            hero.rect.y = 0.4*HEIGHT

    hero.update()

    draw_window(hero, monsters, monsters2, coins, blocks, count)

    finish()

    pygame.display.update()

pygame.quit()
