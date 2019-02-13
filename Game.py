import pygame
import os
from random import choice


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
box_sprites = pygame.sprite.Group()
numbers_sprites = pygame.sprite.Group()
time = 0
boxes = []
numbers = [load_image('fortable/0.png'), load_image('fortable/1.png'), load_image('fortable/2.png'),load_image('fortable/3.png'),
           load_image('fortable/4.png'), load_image('fortable/5.png'), load_image('fortable/6.png'), load_image('fortable/7.png'),
           load_image('fortable/8.png'), load_image('fortable/9.png'), load_image('fortable/nolimit.png')]


class Player(pygame.sprite.Sprite):
    image = load_image("player.png")  # player = персонаж, r = вправо направлен

    def __init__(self, x, y, gun, side='Right'):
        super().__init__(all_sprites)  # он у нас тут вроде добавляется в all_sprites
        Player.image = pygame.transform.scale(Player.image, (50, 120))  # сделал, чтобы было не уродливо
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.pos = x, y
        self.rect.x = x
        self.rect.y = y
        self.gravity = 1
        self.moveleft = False
        self.moveright = False
        self.jump = False
        self.drop = False
        self.shoot = False
        self.side = side
        if self.side == 'Left':
            self.image = pygame.transform.flip(self.image, True, False)
        self.gun = gun
        self.ammo = -1
        self.bullets = []
        self.velocityx = 0
        self.gravity_velocity = 0.07  # скорость, с которой растет скорость падения
        self.lives = 5
        if gun == 'Pistol':
            self.weapon = Pistol(self)
        elif gun == 'ak47':
            self.weapon = Gun(self)
        elif gun == 'awp':
            self.weapon = Snipe(self)
        elif gun == 'mp5':
            self.weapon = Mp5(self)

    def players_move(self):
        if self.jump:
            self.rect.y += 1
            if pygame.sprite.spritecollideany(self, platform_sprites):
                sprite = pygame.sprite.spritecollideany(self, platform_sprites)
                if self.rect.y + 120 - sprite.rect.y < 5:  # у нас ноги близки к верхушки платформы
                    self.gravity = -5
                    self.rect.y -= 1
            self.rect.y -= 1
            self.jump = False
        if self.moveright:
            self.rect.x += 2
            if self.side == 'Left':
                self.image = pygame.transform.flip(self.image, True, False)
                self.side = 'Right'
            if pygame.sprite.spritecollideany(self, platform_sprites):  # столкновения с платформами/борадми
                sprite = pygame.sprite.spritecollideany(self, platform_sprites)
                if self.rect.y - 120 > sprite.rect.y and self.gravity > 0:
                    self.rect.x -= 2
        if self.moveleft:
            self.rect.x -= 2
            if self.side == 'Right':
                self.image = pygame.transform.flip(self.image, True, False)  # персонаж направлен влево
                self.side = 'Left'
            if pygame.sprite.spritecollideany(self, platform_sprites):  # столкновения с платформами/борадми
                sprite = pygame.sprite.spritecollideany(self, platform_sprites)
                if self.rect.y - 120 > sprite.rect.y and self.gravity > 0:  # проверяем, что его ноги ниже выше платформы
                    self.rect.x += 2
        if self.drop:
            self.rect.y += 2
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

        if self.shoot:
            self.weapon.shot()

        self.rect.x -= self.velocityx

        if abs(self.velocityx) < 1:
            self.velocityx = 0

        if self.velocityx > 0:
            self.velocityx -= 0.2
        elif self.velocityx < 0:
            self.velocityx += 0.2

        if self.rect.y > 1300:
            self.rect.x, self.rect.y = choice(range(900)), self.pos[1]
            self.lives -= 1
            self.swap_weapon(gun=False)

        if pygame.sprite.spritecollideany(self, box_sprites):
            box = pygame.sprite.spritecollideany(self, box_sprites)
            self.swap_weapon(box)

        if self.ammo == 0:
            self.swap_weapon(gun=False)
            self.ammo = self.weapon.ammo

    def swap_weapon(self, box=False, gun=True):
        self.weapon.gun.kill()
        if not gun:
            self.weapon = Pistol(self)
        else:
            gun = box.gun
        if box != False:
            box.dostav = True
            self.weapon.gun.kill()
            if gun == 'mp5':
                self.weapon = Mp5(self)
            if gun == 'awp':
                self.weapon = Snipe(self)
            if gun == 'ak47':
                self.weapon = Gun(self)
            self.gun = gun
            box.rect.x = 0
            box.rect.y = -40
        self.ammo = self.weapon.ammo
        self.weapon.kd = 60


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, scale, filename):
        base_platform = pygame.sprite.Sprite()
        base_platform.image = pygame.transform.scale(load_image(filename), scale)  # платформа и её размеры
        base_platform.rect = base_platform.image.get_rect()
        base_platform.rect.x, base_platform.rect.y = pos
        platform_sprites.add(base_platform)


class Table(pygame.sprite.Sprite):
    def __init__(self, pos, gamer, nameoftable):
        table = pygame.sprite.Sprite()
        table.image = pygame.transform.scale(load_image('fortable/' + nameoftable), (210, 100))
        table.rect = table.image.get_rect()
        table.rect.x, table.rect.y = pos
        self.player = gamer
        ammo = pygame.sprite.Sprite()
        ammo.image = pygame.transform.scale(load_image('fortable/ammo.png'), (70, 15))
        ammo.rect = ammo.image.get_rect()
        self.ammo = self.player.ammo
        ammo.rect.x, ammo.rect.y = pos[0] + 90, pos[1] + 30
        numbers_sprites.add(ammo)

        lives = pygame.sprite.Sprite()
        lives.image = pygame.transform.scale(load_image('fortable/lives.png'), (50, 20))
        lives.rect = lives.image.get_rect()
        lives.rect.x, lives.rect.y = pos[0] + 110, pos[1] + 60
        numbers_sprites.add(lives)
        self.ammo1 = pygame.sprite.Sprite()
        self.ammo2 = pygame.sprite.Sprite()

        if len(str(self.player.ammo)) == 1 and player.ammo != -1:
            self.ammo1.image = pygame.transform.scale(numbers[0], (0, 0))
            self.ammo1.rect = self.ammo1.image.get_rect()
            self.ammo2.image = pygame.transform.scale(numbers[self.player.ammo], (15, 17))
            self.ammo2.rect = self.ammo2.image.get_rect()
            self.ammo2.rect.x, self.ammo2.rect.y = pos[0] + 185, pos[1] + 30
        elif len(str(self.player.ammo)) == 2 and player.ammo != -1:
            self.ammo1.image = pygame.transform.scale(numbers[int(str(self.player.ammo)[0])], (15, 17))
            self.ammo1.rect = self.ammo1.image.get_rect()
            self.ammo1.rect.x, self.ammo1.rect.y = pos[0] + 165, pos[1] + 30
            self.ammo2.image = pygame.transform.scale(numbers[int(str(self.player.ammo)[1])], (15, 17))
            self.ammo2.rect = self.ammo2.image.get_rect()
            self.ammo2.rect.x, self.ammo2.rect.y = pos[0] + 185, pos[1] + 30
        elif self.player.ammo == -1:
            self.ammo1.image = pygame.transform.scale(numbers[1], (0, 0))
            self.ammo1.rect = self.ammo1.image.get_rect()
            self.ammo2.image = pygame.transform.scale(numbers[10], (20, 23))
            self.ammo2.rect = self.ammo2.image.get_rect()
            self.ammo2.rect.x, self.ammo2.rect.y = pos[0] + 165, pos[1] + 25

        numbers_sprites.add(self.ammo1, self.ammo2)

        self.x = pos[0]
        self.y = pos[1]
        self.number = player.lives
        all_sprites.add(table)
        self.lives = pygame.sprite.Sprite()
        self.lives.image = pygame.transform.scale(numbers[int(str(self.player.lives))], (15, 17))
        self.lives.rect = self.lives.image.get_rect()
        self.lives.rect.x = pos[0] + 170
        self.lives.rect.y = pos[1] + 65
        numbers_sprites.add(self.lives)

    def update(self):
        if self.number != self.player.lives and self.player.lives >= 0:
            self.lives.image = pygame.transform.scale(numbers[int(str(self.player.lives))], (15, 17))
            self.lives.rect = self.lives.image.get_rect()
            self.lives.rect.x = self.x + 170
            self.lives.rect.y = self.y + 65
            self.number = self.player.lives
        if self.ammo != self.player.ammo:
            if len(str(abs(self.player.ammo))) == 1 and self.player.ammo >= 0:
                self.ammo1.image = pygame.transform.scale(numbers[1], (0, 0))
                self.ammo1.rect = self.ammo1.image.get_rect()
                self.ammo2.image = pygame.transform.scale(numbers[self.player.ammo], (15, 17))
                self.ammo2.rect = self.ammo2.image.get_rect()
                self.ammo2.rect.x, self.ammo2.rect.y = self.x + 165, self.y + 30
            elif len(str(abs(self.player.ammo))) == 2:
                self.ammo1.image = pygame.transform.scale(numbers[int(str(self.player.ammo)[0])],
                                                          (15, 17))
                self.ammo1.rect = self.ammo1.image.get_rect()
                self.ammo1.rect.x, self.ammo1.rect.y = self.x + 165, self.y + 30
                self.ammo2.image = pygame.transform.scale(numbers[int(str(self.player.ammo)[1])],
                                                          (15, 17))
                self.ammo2.rect = self.ammo2.image.get_rect()
                self.ammo2.rect.x, self.ammo2.rect.y = self.x + 185, self.y + 30
            else:
                self.ammo1.image = pygame.transform.scale(numbers[1], (0, 0))
                self.ammo1.rect = self.ammo1.image.get_rect()
                self.ammo2.image = pygame.transform.scale(numbers[10], (20, 23))
                self.ammo2.rect = self.ammo2.image.get_rect()
                self.ammo2.rect.x, self.ammo2.rect.y = self.x + 165, self.y + 25
            self.ammo = self.player.ammo


class Pistol(pygame.sprite.Sprite):
    def __init__(self, player):
        self.gun = pygame.sprite.Sprite()
        self.gun.image = pygame.transform.scale(load_image('guns/pistol.png'), (40, 25))
        self.gun.rect = self.gun.image.get_rect()
        self.gun.rect.x, self.gun.rect.y = player.rect.x + 35, player.rect.y + 45
        self.player = player
        self.side = 'Right'
        self.kd = 0
        self.ammo = -1
        guns_sprites.add(self.gun)

    def update(self):
        if self.player.side == 'Right':
            if self.side == 'Left':
                self.gun.image = pygame.transform.flip(self.gun.image, True, False)
                self.side = 'Right'
            self.gun.rect.x, self.gun.rect.y = self.player.rect.x + 35, self.player.rect.y + 45
        elif self.player.side == 'Left':
            if self.side == 'Right':
                self.gun.image = pygame.transform.flip(self.gun.image, True, False)
                self.side = 'Left'
            self.gun.rect.x, self.gun.rect.y = self.player.rect.x - 25, self.player.rect.y + 45

    def shot(self):
        if self.kd == 0:
            self.bullet = Minibullet(self.side, self.gun.rect.x, self.gun.rect.y, 'Pistol')
            self.player.bullets.append(self.bullet)
            self.kd = 100


class Gun(pygame.sprite.Sprite):
    def __init__(self, player):
        self.gun = pygame.sprite.Sprite()
        self.gun.image = pygame.transform.scale(load_image('guns/ak47.png'), (80, 30))
        self.gun.rect = self.gun.image.get_rect()
        self.gun.rect.x, self.gun.rect.y = player.rect.x, player.rect.y + 50
        self.player = player
        self.side = 'Right'
        self.kd = 0
        self.ammo = 15
        guns_sprites.add(self.gun)

    def update(self):
        if self.player.side == 'Right':
            if self.side == 'Left':
                self.gun.image = pygame.transform.flip(self.gun.image, True, False)
                self.side = 'Right'
            self.gun.rect.x, self.gun.rect.y = self.player.rect.x, self.player.rect.y + 50
        elif self.player.side == 'Left':
            if self.side == 'Right':
                self.gun.image = pygame.transform.flip(self.gun.image, True, False)
                self.side = 'Left'
            self.gun.rect.x, self.gun.rect.y = self.player.rect.x - 30, self.player.rect.y + 50

    def shot(self):
        if self.kd == 0:
            self.bullet = Mediumbullet(self.side, self.gun.rect.x, self.gun.rect.y)
            self.player.bullets.append(self.bullet)
            self.kd = 70
            self.player.ammo -= 1


class Snipe(pygame.sprite.Sprite):
    def __init__(self, player):
        self.gun = pygame.sprite.Sprite()
        self.gun.image = pygame.transform.scale(load_image('guns/awp.png'), (125, 25))
        self.gun.rect = self.gun.image.get_rect()
        self.gun.rect.x, self.gun.rect.y = player.rect.x - 5, player.rect.y + 40
        self.player = player
        self.side = 'Right'
        self.kd = 0
        self.ammo = 5
        guns_sprites.add(self.gun)

    def update(self):
        if self.player.side == 'Right':
            if self.side == 'Left':
                self.gun.image = pygame.transform.flip(self.gun.image, True, False)
                self.side = 'Right'
            self.gun.rect.x, self.gun.rect.y = self.player.rect.x - 5, self.player.rect.y + 40
        elif self.player.side == 'Left':
            if self.side == 'Right':
                self.gun.image = pygame.transform.flip(self.gun.image, True, False)
                self.side = 'Left'
            self.gun.rect.x, self.gun.rect.y = self.player.rect.x - 70, self.player.rect.y + 40

    def shot(self):
        if self.kd == 0:
            self.bullet = SniperBullet(self.side, self.gun.rect.x, self.gun.rect.y)
            self.player.bullets.append(self.bullet)
            self.kd = 175
            self.player.ammo -= 1


class Mp5(pygame.sprite.Sprite):
    def __init__(self, player):
        self.gun = pygame.sprite.Sprite()
        self.gun.image = pygame.transform.scale(load_image('guns/mp5.png'), (75, 30))
        self.gun.rect = self.gun.image.get_rect()
        self.gun.rect.x, self.gun.rect.y = player.rect.x, player.rect.y + 40
        self.player = player
        self.side = 'Right'
        self.ammo = 30
        guns_sprites.add(self.gun)
        self.kd = 0

    def update(self):
        if self.player.side == 'Right':
            if self.side == 'Left':
                self.gun.image = pygame.transform.flip(self.gun.image, True, False)
                self.side = 'Right'
            self.gun.rect.x, self.gun.rect.y = self.player.rect.x, self.player.rect.y + 40
        elif self.player.side == 'Left':
            if self.side == 'Right':
                self.gun.image = pygame.transform.flip(self.gun.image, True, False)
                self.side = 'Left'
            self.gun.rect.x, self.gun.rect.y = self.player.rect.x - 20, self.player.rect.y + 40

    def shot(self):
        if self.kd == 0:
            self.bullet = Minibullet(self.side, self.gun.rect.x, self.gun.rect.y, 'mp5')
            self.player.bullets.append(self.bullet)
            self.kd = 35
            self.player.ammo -= 1


class Minibullet(pygame.sprite.Sprite):
    def __init__(self, side, x, y, gun):
        self.side = side
        self.bullet = pygame.sprite.Sprite()
        self.bullet.image = pygame.transform.scale(load_image('guns/Minibullet.png'), (20, 5))
        if side == 'Left':
            self.bullet.image = pygame.transform.flip(self.bullet.image, True, False)
        self.bullet.rect = self.bullet.image.get_rect()
        if gun == 'mp5' and self.side == 'Right':
            self.bullet.rect.x, self.bullet.rect.y = x + 70, y + 5
        if gun == 'mp5' and self.side == 'Left':
            self.bullet.rect.x, self.bullet.rect.y = x - 5, y + 5
        if gun == 'Pistol' and self.side == 'Right':
            self.bullet.rect.x, self.bullet.rect.y = x + 35, y + 5
        if gun == 'Pistol' and self.side == 'Left':
            self.bullet.rect.x, self.bullet.rect.y = x - 5, y + 5
        self.velocity = 3
        bullet_sprites.add(self.bullet)
        if gun == 'Pistol':
            self.streight = 10
        else:
            self.streight = 8

    def update(self):
        if self.side == 'Right':
            self.bullet.rect.x += self.velocity
        else:
            self.bullet.rect.x -= self.velocity
        if pygame.sprite.spritecollideany(self.bullet, platform_sprites):
            self.velocity = 0
            self.bullet.rect.x = 0
            self.bullet.rect.y = -100
        if self.bullet.rect.x > 2000 or self.bullet.rect.x < -500:
            self.velocity = 0
            self.bullet.rect.x = 0
            self.bullet.rect.y = -100
        if pygame.sprite.spritecollideany(self.bullet, all_sprites):
            hero = pygame.sprite.spritecollideany(self.bullet, all_sprites)
            if self.side == 'Right':
                hero.velocityx = -self.streight
            else:
                hero.velocityx = self.streight
            self.velocity = 0
            self.bullet.rect.x = 0
            self.bullet.rect.y = -100


class Mediumbullet(pygame.sprite.Sprite):
    def __init__(self, side, x, y):
        self.side = side
        self.bullet = pygame.sprite.Sprite()
        self.bullet.image = pygame.transform.scale(load_image('guns/MediumBullet.png'), (25, 6))
        if side == 'Left':
            self.bullet.image = pygame.transform.flip(self.bullet.image, True, False)
        self.bullet.rect = self.bullet.image.get_rect()
        if self.side == 'Right':
            self.bullet.rect.x, self.bullet.rect.y = x + 65, y
        if self.side == 'Left':
            self.bullet.rect.x, self.bullet.rect.y = x - 5, y
        self.velocity = 5
        bullet_sprites.add(self.bullet)
        self.streight = 11

    def update(self):
        if self.side == 'Right':
            self.bullet.rect.x += self.velocity
        else:
            self.bullet.rect.x -= self.velocity
        if pygame.sprite.spritecollideany(self.bullet, platform_sprites):
            self.velocity = 0
            self.bullet.rect.x = 0
            self.bullet.rect.y = -100
        if self.bullet.rect.x > 2000 or self.bullet.rect.x < -500:
            self.velocity = 0
            self.bullet.rect.x = 0
            self.bullet.rect.y = -100
        if pygame.sprite.spritecollideany(self.bullet, all_sprites):
            hero = pygame.sprite.spritecollideany(self.bullet, all_sprites)
            if self.side == 'Right':
                hero.velocityx = -self.streight
            else:
                hero.velocityx = self.streight
            self.velocity = 0
            self.bullet.rect.x = 0
            self.bullet.rect.y = -100


class SniperBullet(pygame.sprite.Sprite):
    def __init__(self, side, x, y):
        self.side = side
        self.bullet = pygame.sprite.Sprite()
        self.bullet.image = pygame.transform.scale(load_image('guns/SniperBullet.png'), (30, 7))
        if side == 'Left':
            self.bullet.image = pygame.transform.flip(self.bullet.image, True, False)
        self.bullet.rect = self.bullet.image.get_rect()
        if self.side == 'Right':
            self.bullet.rect.x, self.bullet.rect.y = x + 65, y
        if self.side == 'Left':
            self.bullet.rect.x, self.bullet.rect.y = x - 5, y
        self.velocity = 10
        bullet_sprites.add(self.bullet)
        self.streight = 14

    def update(self):
        if self.side == 'Right':
            self.bullet.rect.x += self.velocity
        else:
            self.bullet.rect.x -= self.velocity
        if pygame.sprite.spritecollideany(self.bullet, platform_sprites):
            self.velocity = 0
            self.bullet.rect.x = 0
            self.bullet.rect.y = -100
        if self.bullet.rect.x > 2000 or self.bullet.rect.x < -500:
            self.velocity = 0
            self.bullet.rect.x = 0
            self.bullet.rect.y = -100
        if pygame.sprite.spritecollideany(self.bullet, all_sprites):
            hero = pygame.sprite.spritecollideany(self.bullet, all_sprites)
            if self.side == 'Right':
                hero.velocityx = -self.streight
            else:
                hero.velocityx = self.streight
            self.velocity = 0
            self.bullet.rect.x = 0
            self.bullet.rect.y = -100


class BoxWithGun(pygame.sprite.Sprite):
    def __init__(self):
        self.box = pygame.sprite.Sprite()
        self.box.image = pygame.transform.scale(load_image('box.png'), (40, 40))
        self.box.rect = self.box.image.get_rect()
        self.box.rect.x = choice(range(1, 964))
        self.box.rect.y = 0
        self.velo = 1
        self.dostav = False
        self.box.gun = choice(['ak47', 'awp', 'mp5'])
        box_sprites.add(self.box)

    def update(self):
        if not pygame.sprite.spritecollideany(self.box, platform_sprites):
            self.box.rect.y += self.velo
        if self.box.rect.x == 0:
            self.velo = 0


player = Player(900, 20, 'Pistol', 'Left')  # Pistol, ak47, awp, mp5
player2 = Player(100, 20, 'Pistol')
t2 = Table((0, 0), player2, 'table.png')
t1 = Table((width - 210, 0), player, 'table.png')
load_level('level1.txt')
clock = pygame.time.Clock()
running = True
while running:
    time += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Player 1
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
            # Player 2
            if event.key == pygame.K_w:
                player2.jump = True
            if event.key == pygame.K_d:
                player2.moveright = True
            if event.key == pygame.K_a:
                player2.moveleft = True
            if event.key == pygame.K_s:
                player2.drop = True
            if event.key == pygame.K_g:
                player2.shoot = True
        if event.type == pygame.KEYUP:
            # Player 1
            if event.key == pygame.K_LEFT:
                player.moveleft = False
            if event.key == pygame.K_RIGHT:
                player.moveright = False
            if event.key == pygame.K_m:
                player.shoot = False
            # Player 2
            if event.key == pygame.K_a:
                player2.moveleft = False
            if event.key == pygame.K_d:
                player2.moveright = False
            if event.key == pygame.K_g:
                player2.shoot = False

    if player.weapon.kd != 0:
        player.weapon.kd -= 1
    player.players_move()
    player.weapon.update()
    if player.bullets != []:
        for k in player.bullets:
            k.update()
    if player2.weapon.kd != 0:
        player2.weapon.kd -= 1
    player2.players_move()
    player2.weapon.update()
    if player2.bullets != []:
        for k in player2.bullets:
            k.update()
    if time % 3000 == 0:
        box = BoxWithGun()
        boxes.append(box)
    t1.update()
    t2.update()
    level_sprites.draw(screen)
    platform_sprites.draw(screen)
    all_sprites.draw(screen)
    guns_sprites.draw(screen)
    bullet_sprites.draw(screen)
    box_sprites.draw(screen)
    numbers_sprites.draw(screen)
    pygame.display.flip()
    for k in boxes:
        k.update()
    clock = pygame.time.Clock()

pygame.quit()
