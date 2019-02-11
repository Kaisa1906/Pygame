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
size = width, height = 1024, 600
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()  # все спрайты, которые рисуются первым планом, типо игроков, коробок и т.п.
level_sprites = pygame.sprite.Group()  # тут меня только фон
platform_sprites = pygame.sprite.Group()  # платформы все
guns_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    image = load_image("player.png")  # player = персонаж, r = вправо направлен

    def __init__(self, x, y, gun):
        super().__init__(all_sprites)  # он у нас тут вроде добавляется в all_sprites
        Player.image = pygame.transform.scale(Player.image, (50, 120))  # сделал, чтобы было не уродливо
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)  # типо по маске мы
        self.rect.x = x
        self.rect.y = y
        self.gravity = 1
        self.moveleft = False
        self.moveright = False
        self.jump = False
        self.drop = False
        self.shoot = False
        self.side = 'Right'
        self.gravity_velocity = 0.07  # скорость, с которой растет скорость падения
        if gun == 'Pistol':
            weapon = Pistol(self)
            self.weapon = weapon
        elif gun == 'ak47':
            weapon = Gun(self)
            self.weapon = weapon
        elif gun == 'awp':
            weapon = Snipe(self)
            self.weapon = weapon
        elif gun == 'mp5':
            weapon = Mp5(self)
            self.weapon = weapon

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
            player.rect.x += 2
            if self.side == 'Left':
                player.image = pygame.transform.flip(player.image, True, False)
                self.side = 'Right'
            if pygame.sprite.spritecollideany(player, platform_sprites):  # столкновения с платформами/борадми
                sprite = pygame.sprite.spritecollideany(player, platform_sprites)
                if player.rect.y - 120 > sprite.rect.y and self.gravity > 0:
                    player.rect.x -= 2
        if self.moveleft:
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

        if self.shoot == True:
            self.weapon.shot()


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
        self.pistol.rect.x, self.pistol.rect.y = player.rect.x + 35, player.rect.y + 45
        self.player = player
        self.side = 'Right'
        guns_sprites.add(self.pistol)

    def update(self):
        if self.player.side == 'Right':
            if self.side == 'Left':
                self.pistol.image = pygame.transform.flip(self.pistol.image, True, False)
                self.side = 'Right'
            self.pistol.rect.x, self.pistol.rect.y = self.player.rect.x + 35, self.player.rect.y + 45
        elif self.player.side == 'Left':
            if self.side == 'Right':
                self.pistol.image = pygame.transform.flip(self.pistol.image, True, False)
                self.side = 'Left'
            self.pistol.rect.x, self.pistol.rect.y = self.player.rect.x - 25, self.player.rect.y + 45


class Gun(pygame.sprite.Sprite):
    def __init__(self, player):
        self.Gun = pygame.sprite.Sprite()
        self.Gun.image = pygame.transform.scale(load_image('guns/ak47.png'), (80, 30))
        self.Gun.rect = self.Gun.image.get_rect()
        self.Gun.rect.x, self.Gun.rect.y = player.rect.x, player.rect.y + 50
        self.player = player
        self.side = 'Right'
        guns_sprites.add(self.Gun)

    def update(self):
        if self.player.side == 'Right':
            if self.side == 'Left':
                self.Gun.image = pygame.transform.flip(self.Gun.image, True, False)
                self.side = 'Right'
            self.Gun.rect.x, self.Gun.rect.y = self.player.rect.x, self.player.rect.y + 50
        elif self.player.side == 'Left':
            if self.side == 'Right':
                self.Gun.image = pygame.transform.flip(self.Gun.image, True, False)
                self.side = 'Left'
            self.Gun.rect.x, self.Gun.rect.y = self.player.rect.x - 30, self.player.rect.y + 50


class Snipe(pygame.sprite.Sprite):
    def __init__(self, player):
        self.Snipe = pygame.sprite.Sprite()
        self.Snipe.image = pygame.transform.scale(load_image('guns/awp.png'), (125, 25))
        self.Snipe.rect = self.Snipe.image.get_rect()
        self.Snipe.rect.x, self.Snipe.rect.y = player.rect.x - 5, player.rect.y + 40
        self.player = player
        self.side = 'Right'
        guns_sprites.add(self.Snipe)

    def update(self):
        if self.player.side == 'Right':
            if self.side == 'Left':
                self.Snipe.image = pygame.transform.flip(self.Snipe.image, True, False)
                self.side = 'Right'
            self.Snipe.rect.x, self.Snipe.rect.y = self.player.rect.x - 5, self.player.rect.y + 40
        elif self.player.side == 'Left':
            if self.side == 'Right':
                self.Snipe.image = pygame.transform.flip(self.Snipe.image, True, False)
                self.side = 'Left'
            self.Snipe.rect.x, self.Snipe.rect.y = self.player.rect.x - 70, self.player.rect.y + 40


class Mp5(pygame.sprite.Sprite):
    def __init__(self, player):
        self.Mp5 = pygame.sprite.Sprite()
        self.Mp5.image = pygame.transform.scale(load_image('guns/mp5.png'), (75, 30))
        self.Mp5.rect = self.Mp5.image.get_rect()
        self.Mp5.rect.x, self.Mp5.rect.y = player.rect.x, player.rect.y + 40
        self.player = player
        self.side = 'Right'
        self.bullets = []
        guns_sprites.add(self.Mp5)
        self.kd = 0

    def update(self):
        if self.player.side == 'Right':
            if self.side == 'Left':
                self.Mp5.image = pygame.transform.flip(self.Mp5.image, True, False)
                self.side = 'Right'
            self.Mp5.rect.x, self.Mp5.rect.y = self.player.rect.x, self.player.rect.y + 40
        elif self.player.side == 'Left':
            if self.side == 'Right':
                self.Mp5.image = pygame.transform.flip(self.Mp5.image, True, False)
                self.side = 'Left'
            self.Mp5.rect.x, self.Mp5.rect.y = self.player.rect.x - 20, self.player.rect.y + 40

    def shot(self):
        if self.kd == 0:
            self.bullet = Minibullet(self.side, self.Mp5.rect.x, self.Mp5.rect.y)
            self.bullets.append(self.bullet)
            self.kd = 10

class Minibullet(pygame.sprite.Sprite):
    def __init__(self, side, x, y):
        self.side = side
        self.bullet = pygame.sprite.Sprite()
        self.bullet.image = pygame.transform.scale(load_image('guns/Minibullet.png'), (20, 5))
        if side == 'Left':
            self.bullet.image = pygame.transform.flip(self.bullet.image, True, False)
        self.bullet.rect = self.bullet.image.get_rect()
        self.bullet.rect.x, self.bullet.rect.y = x + 75, y
        self.velocity = 3
        bullet_sprites.add(self.bullet)

    def update(self):
        if self.side == 'Right':
            self.bullet.rect.x += self.velocity
        else:
            self.bullet.rect.x -= self.velocity
        if pygame.sprite.spritecollideany(self.bullet, platform_sprites):
            self.bullet.kill()
player = Player(600, 20, 'mp5')
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
            if event.key == pygame.K_m:
                player.shoot = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.moveleft = False
            if event.key == pygame.K_RIGHT:
                player.moveright = False
            if event.key == pygame.K_m:
                player.shoot = False
    if player.weapon.kd != 0:
        player.weapon.kd -= 1
    player.players_move()
    player.weapon.update()
    if player.weapon.bullets != []:
        for k in player.weapon.bullets:
            k.update()
    level_sprites.draw(screen)
    platform_sprites.draw(screen)
    all_sprites.draw(screen)
    guns_sprites.draw(screen)
    bullet_sprites.draw(screen)
    pygame.display.flip()
    clock = pygame.time.Clock()

pygame.quit()
