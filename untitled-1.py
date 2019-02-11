import pygame
import os


# import random


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


def load_level(filename):
    file = open(filename, 'r')
    elements = file.read()
    elements = elements.split('\n')
    for element in elements:
        element = element.split('-')
        type = element[0]
        if type == 'Platform':
            element = element[1].split()
            pos = (int(element[0]), int(element[1]))
            scale = (int(element[2]), int(element[3]))
            Platform((pos), (scale), element[4])
        if type == 'Background':
            name = element[1]
            Background = pygame.sprite.Sprite()
            Background.image = pygame.transform.scale(load_image(name), (1024, 550))
            Background.rect = Background.image.get_rect()
            level_sprites.add(Background)


pygame.init()
change = 0
size = width, height = 1024, 600
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()  # все спрайты, которые рисуются первым планом, типо игроков, коробок и т.п.
level_sprites = pygame.sprite.Group()  # тут меня только фон
platform_sprites = pygame.sprite.Group()  # платформы все
guns_sprites = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    image = load_image("player.png")  # player = персонаж, r = вправо направлен

    def __init__(self, columns, rows, x, y):
        super().__init__(all_sprites)  # он у нас тут вроде добавляется в all_sprites
        Player.image = pygame.transform.scale(Player.image, (50, 120))  # сделал, чтобы было не уродливо
        self.frames = [] # надо сделать 2 списка под спрайты ходьбы в обе стороны
        self.cut_sheet(Player.image, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame] 
        self.rect = self.rect.move(x, y)        
        self.mask = pygame.mask.from_surface(self.image) #типо по маске мы
        self.rect.x = x
        self.rect.y = y
        self.gravity = 1
        self.mask = pygame.mask.from_surface(self.image)  # типо по маске мы
        self.moveleft = False
        self.moveright = False
        self.jump = False
        self.drop = False
        self.side = 'Right'
        self.gravity_velocity = 0.07  # скорость, с которой растет скорость падения

    def players_move(self):
        if self.jump:
            player.rect.y += 1
            if pygame.sprite.spritecollideany(player, platform_sprites):
                sprite = pygame.sprite.spritecollideany(player, platform_sprites)
                if player.rect.y + 120 - sprite.rect.y < 2:  # у нас ноги близки к верхушки платформы
                    player.gravity = -5
                    player.rect.y -= 1
            player.rect.y -= 1
            self.jump = False
        if self.moveright:
            if change % 10 == 0: # смена изображения на каждый 10 раз
                player.update()
            change += 1            
            player.rect.x += 2
            if self.side == 'Left':
                player.image = pygame.transform.flip(player.image, True, False)
                self.side = 'Right'
            if pygame.sprite.spritecollideany(player, platform_sprites):  # столкновения с платформами/борадми
                sprite = pygame.sprite.spritecollideany(player, platform_sprites)
                if player.rect.y - 120 > sprite.rect.y and self.gravity > 0:
                    player.rect.x -= 2
        if self.moveleft:
            if change % 10 == 0:
                player.update()
            change += 1            
            player.rect.x -= 2
            if self.side == 'Right':
                player.image = pygame.transform.flip(player.image, True, False)  # персонаж направлен влево
                self.side = 'Left'
            if pygame.sprite.spritecollideany(player, platform_sprites):  # столкновения с платформами/борадми
                sprite = pygame.sprite.spritecollideany(player, platform_sprites)
                if player.rect.y - 120 > sprite.rect.y and self.gravity > 0:  # проверяем, что его ноги ниже выше платформы
                    player.rect.x += 2
        if self.drop:
            player.rect.y += 2
            self.drop = False
        if self.gravity >= 0:  # если он падает
            self.rect.y += 1
            if not pygame.sprite.spritecollideany(self, platform_sprites):  # если под ним нет поверхности
                self.rect.y -= 1
                self.rect.y += self.gravity
                self.gravity += self.gravity_velocity
                while pygame.sprite.spritecollideany(self, platform_sprites):  # вдруг появилась поверхность
                    self.rect.y -= 1
                    self.gravity = 0
            else:
                sprite = pygame.sprite.spritecollideany(self, platform_sprites)  # есть поверхность
                if self.rect.y + 119 <= sprite.rect.y:  # наши ножки выше этой поверхности
                    self.rect.y -= 1
                else:  # наши ножки ниже этой поверхности
                    self.rect.y -= 1
                    self.rect.y += self.gravity
                    self.gravity += self.gravity_velocity
                    if pygame.sprite.spritecollideany(self, platform_sprites) and self.rect.y + 120 - sprite.rect.y < 2:
                        while pygame.sprite.spritecollideany(self, platform_sprites):
                            self.rect.y -= 1
                            self.gravity = 0
        else:
            self.rect.y += self.gravity
            self.gravity += self.gravity_velocity
        
    def cut_sheet(self, sheet, columns, rows):
            self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                    sheet.get_height() // rows)
            for j in range(rows):
                for i in range(columns):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames.append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))
    
    def update(self): #добавить проверку направления движения
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
    
    
class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, scale, filename):
        base_platform = pygame.sprite.Sprite()
        base_platform.image = pygame.transform.scale(load_image(filename), scale)  # платформа и её размеры
        base_platform.rect = base_platform.image.get_rect()
        base_platform.rect.x, base_platform.rect.y = pos
        platform_sprites.add(base_platform)


class Pistol(pygame.sprite.Sprite):
    def __init__(self, player):
        self.pistol = pygame.sprite.Sprite()
        self.pistol.image = pygame.transform.scale(load_image('guns/pistol.png'), (40, 25))
        self.pistol.rect = self.pistol.image.get_rect()
        self.pistol.rect.x, self.pistol.rect.y = player.rect.x + 10, player.rect.y + 30
        self.player = player
        self.side = 'Right'
        guns_sprites.add(self.pistol)

    def update(self):
        if self.player.side == 'Right':
            if self.side == 'Left':
                self.pistol.image = pygame.transform.flip(self.pistol.image, True, False)
                self.side = 'Right'
            self.pistol.rect.x, self.pistol.rect.y = self.player.rect.x + 25, self.player.rect.y + 50
        elif self.player.side == 'Left':
            if self.side == 'Right':
                self.pistol.image = pygame.transform.flip(self.pistol.image, True, False)
                self.side = 'Left'
            self.pistol.rect.x, self.pistol.rect.y = self.player.rect.x - 10, self.player.rect.y + 50


player = Player(600, 20)
pistol = Pistol(player)
load_level('level1.txt')
clock = pygame.time.Clock()
running = True
moveleft, moveright, jump = False, False, False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.moveleft = True
            if event.key == pygame.K_RIGHT:
                player.moveright = True
            if event.key == pygame.K_UP:
                player.jump = True
            if event.key == pygame.K_DOWN:
                player.drop = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.moveleft = False
            if event.key == pygame.K_RIGHT:
                player.moveright = False
    player.players_move()
    pistol.update()
    level_sprites.draw(screen)
    platform_sprites.draw(screen)
    all_sprites.draw(screen)
    guns_sprites.draw(screen)
    pygame.display.flip()
    clock = pygame.time.Clock()

pygame.quit()