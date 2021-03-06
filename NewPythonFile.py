import pygame
import os
#import random


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


pygame.init()
size = width, height = 1024, 600
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group() #все спрайты, которые рисуются первым планом, типо игроков, коробок и т.п.
level_sprites = pygame.sprite.Group()  #тут меня только фон
vertical_borders = pygame.sprite.Group() #борды я сделал для теста пока что
horizontal_borders = pygame.sprite.Group()
platform_sprites = pygame.sprite.Group() #платформы все

class Player(pygame.sprite.Sprite):
    image = load_image("playerr.png") #player = персонаж, r = вправо направлен

    def __init__(self, x, y):
        super().__init__(all_sprites) #он у нас тут вроде добавляется в all_sprites
        Player.image = pygame.transform.scale(Player.image, (50,120)) #сделал, чтобы было не уродливо
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image) #типо по маске мы
        self.rect.x = x
        self.rect.y = y
        self.gravity = 1

class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, scale):
        base_platform = pygame.sprite.Sprite()
        base_platform.image = pygame.transform.scale(load_image('platform.png'), scale) #я типо использую только 1 вид платформы, и просто его увеличиваю/уменьшаю
        base_platform.rect = base_platform.image.get_rect()
        base_platform.rect.x, base_platform.rect.y = pos
        platform_sprites.add(base_platform)


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)

fon = pygame.sprite.Sprite()
fon.image = pygame.transform.scale(load_image('level_test_fon.jpg'), (1024, 550))
#фон, 4 платформы и игрок
fon.rect = fon.image.get_rect()
level_sprites.add(fon)
base_platform = Platform((0, 550), (1024, 50))
platform1 = Platform((24, 350), (300,25))
platform2 = Platform((700, 350), (300,25))
platform3 = Platform((370, 200), (300,25))
player = Player(600, 20)

Border(0, 0, width, 0)
Border(0, height, width, height)
Border(0, 0, 0, height)
Border(width, 0, width, height)


clock = pygame.time.Clock()
running = True
moveleft, moveright = False, False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_LEFT:
                moveleft = True
            if event.key == pygame.K_RIGHT:
                moveright = True
            if event.key == pygame.K_UP:
                player.rect.y +=1
                if pygame.sprite.spritecollideany(player, platform_sprites):
                    sprite = pygame.sprite.spritecollideany(player, platform_sprites)
                    if player.rect.y + 120 - sprite.rect.y < 2: # у нас ноги близки к верхушки платформы
                        player.gravity = -3.01
                        player.rect.y -= 1.1
                player.rect.y -= 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moveleft = False
            if event.key == pygame.K_RIGHT:
                moveright = False
    if moveleft:
        player.rect.x -= 2
        player.image = pygame.transform.scale(load_image('playerl.png'), (50, 120)) #персонаж направлен влево
        if pygame.sprite.spritecollideany(player, platform_sprites): #столкновения с платформами/борадми
            sprite = pygame.sprite.spritecollideany(player, platform_sprites)
            if player.rect.y - 120  > sprite.rect.y: #проверяем, что его ноги ниже выше платформы
                player.rect.x += 2

    if moveright:
        player.rect.x += 2
        player.image = pygame.transform.scale(load_image('playerr.png'), (50, 120))
        if pygame.sprite.spritecollideany(player, platform_sprites): #столкновения с платформами/борадми
            sprite = pygame.sprite.spritecollideany(player, platform_sprites)
            if player.rect.y - 120 > sprite.rect.y:
                player.rect.x -= 2
    player.rect.y += 1
    if not pygame.sprite.spritecollideany(player, platform_sprites): #если под ним нет поверхности
        player.rect.y -= 1
        player.rect.y += player.gravity
        player.gravity += 0.07
        while pygame.sprite.spritecollideany(player, platform_sprites):
            sprite = pygame.sprite.spritecollideany(player, platform_sprites)
            if player.rect.y < sprite.rect.y:
                player.rect.y -= 1
                player.gravity = 0
            else:
                break
    else:
        player.rect.y -= 1
        if player.gravity != 0:
            player.rect.y += player.gravity
            player.gravity += 0.07
    level_sprites.draw(screen)
    platform_sprites.draw(screen)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock = pygame.time.Clock()

pygame.quit()

