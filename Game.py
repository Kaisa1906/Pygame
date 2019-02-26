import pygame
import os
from random import choice

mus = None


def music(sound, where):
    global mus
    mus = where
    pygame.mixer.music.stop()
    pygame.mixer.music.load(sound)
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)


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


def finaly_menu(l1):
    global running
    fon = pygame.sprite.Sprite()
    fon.image = pygame.transform.scale(load_image('temn.png'), (1024, 600))
    fon.rect = fon.image.get_rect()
    fon.rect.x, fon.rect.y = 0, 0
    all_sprites.add(fon)
    guns_sprites.empty()
    won = pygame.sprite.Sprite()
    if l1 == 0:
        won.image = pygame.transform.scale(load_image('player1_won.png'), (400, 80))
    else:
        won.image = pygame.transform.scale(load_image('player2_won.png'), (400, 80))
    won.rect = won.image.get_rect()
    won.rect.x, won.rect.y = 300, 200
    lish.add(won)
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                run = False
        level_sprites.draw(screen)
        platform_sprites.draw(screen)
        all_sprites.draw(screen)
        bullet1_sprites.draw(screen)
        bullet2_sprites.draw(screen)
        box_sprites.draw(screen)
        numbers_sprites.draw(screen)
        guns_sprites.draw(screen)
        all_sprites.draw(screen)
        lish.draw(screen)
        pygame.display.flip()


def how_to_play():
    global running
    fon = pygame.sprite.Sprite()
    fon.image = pygame.transform.scale(load_image('level_test_fon.jpg'), (1024, 600))
    fon.rect = fon.image.get_rect()
    fon.rect.x, fon.rect.y = 0, 0
    level_sprites.add(fon)
    button = pygame.sprite.Sprite()
    button.image = pygame.transform.scale(load_image('main_window/teach.png'), (800, 500))
    button.rect = button.image.get_rect()
    button.rect.x, button.rect.y = 100, 50
    buttons2 = pygame.sprite.Group()
    buttons2.add(button)
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                run = False
        level_sprites.draw(screen)
        buttons2.draw(screen)
        pygame.display.flip()
    return started_menu()


def chose_level():
    global running
    Maps(200, 50, 'level1.png')
    Maps(200, 225, 'level2.png')
    Maps(200, 400, 'level3.png')
    level_sprites.empty()
    button_sprites.empty()
    fon = pygame.sprite.Sprite()
    fon.image = pygame.transform.scale(load_image('level_test_fon.jpg'), (1024, 600))
    Buttons(800, 50, 'back.png', 'back', (70, 70))
    fon.rect = fon.image.get_rect()
    fon.rect.x, fon.rect.y = 0, 0
    level_sprites.add(fon)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                point = Fake(pygame.mouse.get_pos())
                if pygame.sprite.spritecollideany(point, maps_sprites):
                    map = pygame.sprite.spritecollideany(point, maps_sprites)
                    point.kill()
                    name = map.clicked()
                    return name
                if pygame.sprite.spritecollideany(point, button_sprites):
                    button = pygame.sprite.spritecollideany(point, button_sprites)
                    need = button.click()
                    if need == 'back':
                        return started_menu()

        level_sprites.draw(screen)
        button_sprites.draw(screen)
        maps_sprites.draw(screen)
        pygame.display.flip()
    return


def started_menu():
    global running
    if not running:
        return
    if mus != 'menu':
        music(choice(music_for_menu), 'menu')
    button_sprites.empty()
    fon = pygame.sprite.Sprite()
    fon.image = pygame.transform.scale(load_image('level_test_fon.jpg'), (1024, 600))
    fon.rect = fon.image.get_rect()
    fon.rect.x, fon.rect.y = 0, 0
    fonov = pygame.sprite.Group()
    fonov.add(fon)
    fake = pygame.sprite.Group()

    Buttons(400, 200, 'play_1.png', "Game")
    Buttons(375, 400, 'how_to_play.png', "how_to_play", (300, 75))
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                point = Fake(pygame.mouse.get_pos())
                if pygame.sprite.spritecollideany(point, button_sprites):
                    button = pygame.sprite.spritecollideany(point, button_sprites)
                    point.kill()
                    if button.click() == 'Game':
                        return chose_level()
                    elif button.click() == 'how_to_play':
                        return how_to_play()

        fonov.draw(screen)
        button_sprites.draw(screen)
        pygame.display.flip()
    return


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
            Background.image = pygame.transform.scale(load_image(name), (1024, 600))
            Background.rect = Background.image.get_rect()
            level_sprites.add(Background)


pygame.init()
pygame.mixer.init()
# Music time
music_for_fight = []
music_for_menu = []
music_for_fight.append('data/music/1.wav')
music_for_menu.append('data/music/9.wav')
music_for_menu.append('data/music/14.wav')
music_for_fight.append('data/music/15.wav')
music_for_menu.append('data/music/17.wav')
music_for_menu.append('data/music/18.wav')
music_for_menu.append('data/music/19.wav')
minibullet = pygame.mixer.Sound('data/music/minibullet.wav')
pistol = pygame.mixer.Sound('data/music/pistol.wav')
new_weapon = pygame.mixer.Sound('data/music/new_weapon.wav')
gun = pygame.mixer.Sound('data/music/sniper.wav')
sniper = pygame.mixer.Sound('data/music/gun.wav')
died = pygame.mixer.Sound('data/music/died.wav')

size = width, height = 1024, 600
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()  # âñå ñïðàéòû, êîòîðûå ðèñóþòñÿ ïåðâûì ïëàíîì, òèïî èãðîêîâ, êîðîáîê è ò.ï.
level_sprites = pygame.sprite.Group()  # òóò ìåíÿ òîëüêî ôîí
platform_sprites = pygame.sprite.Group()  # ïëàòôîðìû âñå
guns_sprites = pygame.sprite.Group()
bullet1_sprites = pygame.sprite.Group()
bullet2_sprites = pygame.sprite.Group()
box_sprites = pygame.sprite.Group()
numbers_sprites = pygame.sprite.Group()
button_sprites = pygame.sprite.Group()
fake = pygame.sprite.Group()
maps_sprites = pygame.sprite.Group()
lish = pygame.sprite.Group()
icons = pygame.sprite.Group()
players1 = pygame.sprite.Group()
players2 = pygame.sprite.Group()
numbers = [load_image('fortable/0.png'), load_image('fortable/1.png'), load_image('fortable/2.png'),
           load_image('fortable/3.png'),
           load_image('fortable/4.png'), load_image('fortable/5.png'), load_image('fortable/6.png'),
           load_image('fortable/7.png'),
           load_image('fortable/8.png'), load_image('fortable/9.png'), load_image('fortable/nolimit.png')]


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, gun, image, columns, rows, pl, side='Right'):
        if pl == 'player1':
            super().__init__(players1)
        else:
            super().__init__(players2)
        self.pl = pl
        self.frames = []
        self.respawn = 600
        self.cut_sheet(load_image(image), columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.pos = x, y
        self.rect.x = x
        self.rect.y = y
        self.gravity = 1
        self.count = 0
        self.Transformed = False
        self.moveleft = False
        self.moveright = False
        self.jump = False
        self.drop = False
        self.shoot = False
        self.die = False
        self.side = side
        if self.side == 'Left':
            self.image = pygame.transform.flip(self.image, True, False)
        self.gun = gun
        self.ammo = -1
        self.velocityx = 0
        self.gravity_velocity = 0.07
        self.lives = 5
        if gun == 'Pistol':
            self.weapon = Pistol(self)
        elif gun == 'ak47':
            self.weapon = Gun(self)
            self.ammo = self.weapon.ammo
        elif gun == 'awp':
            self.weapon = Snipe(self)
            self.ammo = self.weapon.ammo
        elif gun == 'mp5':
            self.weapon = Mp5(self)
            self.ammo = self.weapon.ammo
        elif gun == 'shotgun':
            self.weapon = ShotGun(self)
            self.ammo = self.weapon.ammo

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def players_move(self):
        if self.respawn != 0:
            self.respawn -= 1
        if self.jump:
            self.rect.y += 1
            if pygame.sprite.spritecollideany(self, platform_sprites):
                sprite = pygame.sprite.spritecollideany(self, platform_sprites)
                if self.rect.y + 120 - sprite.rect.y <= 3:
                    self.gravity = -5
                    self.rect.y -= 1
            self.rect.y -= 1
            self.jump = False
        if self.drop:
            self.rect.y += 5
            self.drop = False
        if self.shoot:
            self.weapon.shot()

        if self.moveright:
            self.rect.x += 2
            if self.side == 'Left':
                if self.side == 'Left':
                    if self.count % 10 == 0:
                        self.update()
                    self.count = (self.count + 1) % 20
                self.Transformed = False
                self.image = pygame.transform.flip(self.image, True, False)
                self.side = 'Right'
            else:
                if self.count % 10 == 0:
                    self.update()
                self.count = (self.count + 1) % 20
        if self.moveleft:
            self.rect.x -= 2
            if self.side == 'Right':
                if self.count % 10 == 0:
                    self.update()
                self.count = (self.count + 1) % 20
                self.image = pygame.transform.flip(self.image, True, False)
                self.Transformed = True  # Ð¿ÐµÑÑÐ¾Ð½Ð°Ð¶ Ð½Ð°Ð¿ÑÐ°Ð²Ð»ÐµÐ½ Ð²Ð»ÐµÐ²Ð¾
                self.side = 'Left'
            else:
                if self.count % 10 == 0:
                    self.update()
                    self.Transformed = False
                if not self.Transformed:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.Transformed = True
                self.count = (self.count + 1) % 20

        if self.gravity >= 0:

            if pygame.sprite.spritecollideany(self, platform_sprites):
                sprite = pygame.sprite.spritecollideany(self, platform_sprites)
                if self.rect.y + 120 - sprite.rect.y <= 3 and self.gravity > 0:
                    self.rect.y = sprite.rect.y - 120

            self.rect.y += 1
            if not pygame.sprite.spritecollideany(self, platform_sprites):
                if self.gravity <= 3:
                    self.gravity += self.gravity_velocity
                self.rect.y += self.gravity
            else:
                sprite = pygame.sprite.spritecollideany(self, platform_sprites)
                if self.rect.y + 120 - sprite.rect.y > 3:
                    if self.gravity <= 3:
                        self.gravity += self.gravity_velocity
                    self.rect.y += self.gravity
                elif self.gravity > 0:
                    self.gravity = 0
            self.rect.y -= 1
        else:
            self.rect.y += self.gravity
            self.gravity += self.gravity_velocity

        self.rect.x -= self.velocityx

        if abs(self.velocityx) < 1:
            self.velocityx = 0

        if self.velocityx > 0:
            self.velocityx -= 0.2
        elif self.velocityx < 0:
            self.velocityx += 0.2
        if self.rect.y > 1024 and not self.die:
            self.die = True
            pygame.mixer.Sound.play(died)

        if self.rect.y > 1300:
            self.rect.x, self.rect.y = choice(range(900)), self.pos[1]
            self.lives -= 1
            self.respawn = 600
            self.swap_weapon(gun=False, death=True)
            self.die = False

        if pygame.sprite.spritecollideany(self, box_sprites):
            box = pygame.sprite.spritecollideany(self, box_sprites)
            self.swap_weapon(box)
            box.kill()

        if self.ammo == 0:
            self.swap_weapon(gun=False)
            self.ammo = self.weapon.ammo

    def swap_weapon(self, box=False, gun=True, death=False):
        if not death:
            pygame.mixer.Sound.play(new_weapon)
        self.weapon.kill()
        if not gun:
            self.weapon = Pistol(self)
        else:
            gun = box.gun
        if box != False:
            box.dostav = True
            self.weapon.kill()
            if gun == 'mp5':
                self.weapon = Mp5(self)
            if gun == 'awp':
                self.weapon = Snipe(self)
            if gun == 'ak47':
                self.weapon = Gun(self)
            elif gun == 'shotgun':
                self.weapon = ShotGun(self)
            self.gun = gun
            box.rect.x = 0
            box.rect.y = -150
        self.ammo = self.weapon.ammo
        self.weapon.kd = 60


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, scale, filename):
        base_platform = pygame.sprite.Sprite()
        base_platform.image = pygame.transform.scale(load_image(filename), scale)  # ïëàòôîðìà è å¸ ðàçìåðû
        base_platform.rect = base_platform.image.get_rect()
        base_platform.rect.x, base_platform.rect.y = pos
        platform_sprites.add(base_platform)


class Buttons(pygame.sprite.Sprite):
    def __init__(self, x, y, filename, purpose, scale=False):
        super().__init__(button_sprites)
        self.but = filename
        self.purpose = purpose
        self.name = 'main_window/' + filename
        self.x, self.y = x, y
        if not scale:
            scale = (250, 120)
        self.image = pygame.transform.scale(load_image(self.name), scale)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

    def click(self):
        return self.purpose


class Maps(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        super().__init__(maps_sprites)
        self.filename = filename
        self.image = pygame.transform.scale(load_image(filename), (300, 150))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def clicked(self):
        return self.filename


class Fake(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('main_window/' + 'play_1.png'), (1, 1))

    def __init__(self, pos):
        super().__init__(fake)
        self.image = Fake.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos


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
        super().__init__(guns_sprites)
        self.image = pygame.transform.scale(load_image('guns/pistol.png'), (40, 25))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = player.rect.x + 35, player.rect.y + 45
        self.player = player
        self.side = 'Right'
        self.kd = 0
        self.ammo = -1

    def update(self):
        if self.player.side == 'Right':
            if self.side == 'Left':
                self.image = pygame.transform.flip(self.image, True, False)
                self.side = 'Right'
            self.rect.x, self.rect.y = self.player.rect.x + 35, self.player.rect.y + 45
        elif self.player.side == 'Left':
            if self.side == 'Right':
                self.image = pygame.transform.flip(self.image, True, False)
                self.side = 'Left'
            self.rect.x, self.rect.y = self.player.rect.x - 25, self.player.rect.y + 45

    def shot(self):
        if self.kd == 0:
            pygame.mixer.Sound.play(pistol)
            self.bullet = Minibullet(self.side, self.rect.x, self.rect.y, 'Pistol', self.player.pl)
            if self.player.pl == 'player1':
                bullet1_sprites.add(self.bullet)
            else:
                bullet2_sprites.add(self.bullet)
            self.kd = 100


class Gun(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__(guns_sprites)
        self.image = pygame.transform.scale(load_image('guns/ak47.png'), (80, 30))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = player.rect.x, player.rect.y + 50
        self.player = player
        self.side = 'Right'
        self.kd = 0
        self.ammo = 15

    def update(self):
        if self.player.side == 'Right':
            if self.side == 'Left':
                self.image = pygame.transform.flip(self.image, True, False)
                self.side = 'Right'
            self.rect.x, self.rect.y = self.player.rect.x, self.player.rect.y + 50
        elif self.player.side == 'Left':
            if self.side == 'Right':
                self.image = pygame.transform.flip(self.image, True, False)
                self.side = 'Left'
            self.rect.x, self.rect.y = self.player.rect.x - 30, self.player.rect.y + 50

    def shot(self):
        if self.kd == 0:
            pygame.mixer.Sound.play(gun)
            self.bullet = Mediumbullet(self.side, self.rect.x, self.rect.y,  self.player.pl)
            if self.player.pl == 'player1':
                bullet1_sprites.add(self.bullet)
            else:
                bullet2_sprites.add(self.bullet)
            self.kd = 60
            self.player.ammo -= 1


class Snipe(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__(guns_sprites)
        self.image = pygame.transform.scale(load_image('guns/awp.png'), (125, 25))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = player.rect.x - 5, player.rect.y + 40
        self.player = player
        self.side = 'Right'
        self.kd = 0
        self.ammo = 5

    def update(self):
        if self.player.side == 'Right':
            if self.side == 'Left':
                self.image = pygame.transform.flip(self.image, True, False)
                self.side = 'Right'
            self.rect.x, self.rect.y = self.player.rect.x - 5, self.player.rect.y + 40
        elif self.player.side == 'Left':
            if self.side == 'Right':
                self.image = pygame.transform.flip(self.image, True, False)
                self.side = 'Left'
            self.rect.x, self.rect.y = self.player.rect.x - 70, self.player.rect.y + 40

    def shot(self):
        if self.kd == 0:
            pygame.mixer.Sound.play(sniper)
            self.bullet = SniperBullet(self.side, self.rect.x, self.rect.y, self.player.pl)
            if self.player.pl == 'player1':
                bullet1_sprites.add(self.bullet)
            else:
                bullet2_sprites.add(self.bullet)
            self.kd = 175
            self.player.ammo -= 1


class Mp5(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__(guns_sprites)
        self.image = pygame.transform.scale(load_image('guns/mp5.png'), (75, 30))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = player.rect.x, player.rect.y + 40
        self.player = player
        self.side = 'Right'
        self.ammo = 30
        self.kd = 0

    def update(self):
        if self.player.side == 'Right':
            if self.side == 'Left':
                self.image = pygame.transform.flip(self.image, True, False)
                self.side = 'Right'
            self.rect.x, self.rect.y = self.player.rect.x, self.player.rect.y + 40
        elif self.player.side == 'Left':
            if self.side == 'Right':
                self.image = pygame.transform.flip(self.image, True, False)
                self.side = 'Left'
            self.rect.x, self.rect.y = self.player.rect.x - 20, self.player.rect.y + 40

    def shot(self):
        if self.kd == 0:
            self.bullet = Minibullet(self.side, self.rect.x, self.rect.y, 'mp5', self.player.pl)
            if self.player.pl == 'player1':
                bullet1_sprites.add(self.bullet)
            else:
                bullet2_sprites.add(self.bullet)
            pygame.mixer.Sound.play(minibullet)
            self.kd = 35
            self.player.ammo -= 1

class ShotGun(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__(guns_sprites)
        self.image = pygame.transform.scale(load_image('guns/shotgun.png'), (125, 25))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = player.rect.x - 5, player.rect.y + 60
        self.player = player
        self.side = 'Right'
        self.kd = 0
        self.ammo = 7

    def update(self):
        if self.player.side == 'Right':
            if self.side == 'Left':
                self.image = pygame.transform.flip(self.image, True, False)
                self.side = 'Right'
            self.rect.x, self.rect.y = self.player.rect.x - 5, self.player.rect.y + 60
        elif self.player.side == 'Left':
            if self.side == 'Right':
                self.image = pygame.transform.flip(self.image, True, False)
                self.side = 'Left'
            self.rect.x, self.rect.y = self.player.rect.x - 70, self.player.rect.y + 60

    def shot(self):
        if self.kd == 0:
            pygame.mixer.Sound.play(sniper)
            self.bullet1 = ShotGunBullet(self.side, self.rect.x, self.rect.y, self.player.pl, 10)
            self.bullet2 = ShotGunBullet(self.side, self.rect.x, self.rect.y, self.player.pl)
            self.bullet3 = ShotGunBullet(self.side, self.rect.x, self.rect.y, self.player.pl, -10)
            if self.player.pl == 'player1':
                bullet1_sprites.add(self.bullet1, self.bullet2, self.bullet3)
            else:
                bullet2_sprites.add(self.bullet1, self.bullet2, self.bullet3)
            self.kd = 130
            self.player.ammo -= 1

class Minibullet(pygame.sprite.Sprite):
    def __init__(self, side, x, y, gun, pl):
        if pl == 'player1':
            super().__init__(bullet1_sprites)
        else:
            super().__init__(bullet2_sprites)
        self.side = side
        self.pl = pl
        self.image = pygame.transform.scale(load_image('guns/Minibullet.png'), (20, 5))
        if side == 'Left':
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        if gun == 'mp5' and self.side == 'Right':
            self.rect.x, self.rect.y = x + 70, y + 5
        if gun == 'mp5' and self.side == 'Left':
            self.rect.x, self.rect.y = x - 5, y + 5
        if gun == 'Pistol' and self.side == 'Right':
            self.rect.x, self.rect.y = x + 35, y + 5
        if gun == 'Pistol' and self.side == 'Left':
            self.rect.x, self.rect.y = x - 5, y + 5
        self.velocity = 3
        if gun == 'Pistol':
            self.streight = 12
        else:
            self.streight = 10
        if self.pl == 'player1':
            self.grop = players2
        else:
            self.grop = players1

    def update(self):
        if self.side == 'Right':
            self.rect.x += self.velocity
        else:
            self.rect.x -= self.velocity
        if pygame.sprite.spritecollideany(self, platform_sprites):
            self.kill()
        if self.rect.x > 2000 or self.rect.x < -500:
            self.kill()
        if pygame.sprite.spritecollideany(self, self.grop):
            hero = pygame.sprite.spritecollideany(self, self.grop)
            if self.side == 'Right' and hero.respawn == 0:
                hero.velocityx -= self.streight
            elif hero.respawn == 0:
                hero.velocityx += self.streight
            self.kill()


class Mediumbullet(pygame.sprite.Sprite):
    def __init__(self, side, x, y, pl):
        if pl == 'player1':
            super().__init__(bullet1_sprites)
        else:
            super().__init__(bullet2_sprites)
        self.side = side
        self.pl = pl
        self.image = pygame.transform.scale(load_image('guns/MediumBullet.png'), (25, 6))
        if side == 'Left':
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        if self.side == 'Right':
            self.rect.x, self.rect.y = x + 85, y
        if self.side == 'Left':
            self.rect.x, self.rect.y = x - 5, y
        self.velocity = 5
        self.streight = 13
        if self.pl == 'player1':
            self.grop = players2
        else:
            self.grop = players1

    def update(self):
        if self.side == 'Right':
            self.rect.x += self.velocity
        else:
            self.rect.x -= self.velocity
        if pygame.sprite.spritecollideany(self, platform_sprites):
            self.kill()
        if self.rect.x > 2000 or self.rect.x < -500:
            self.kill()
        if pygame.sprite.spritecollideany(self, self.grop):
            hero = pygame.sprite.spritecollideany(self, self.grop)
            if self.side == 'Right' and hero.respawn == 0:
                hero.velocityx -= self.streight
            elif hero.respawn == 0:
                hero.velocityx += self.streight
            self.kill()


class SniperBullet(pygame.sprite.Sprite):
    def __init__(self, side, x, y, pl):
        if pl == 'player1':
            super().__init__(bullet1_sprites)
        else:
            super().__init__(bullet2_sprites)
        self.side = side
        self.pl = pl
        self.image = pygame.transform.scale(load_image('guns/SniperBullet.png'), (30, 7))
        if side == 'Left':
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        if self.side == 'Right':
            self.rect.x, self.rect.y = x + 85, y
        if self.side == 'Left':
            self.rect.x, self.rect.y = x - 5, y
        self.velocity = 10
        self.streight = 16
        if self.pl == 'player1':
            self.grop = players2
        else:
            self.grop = players1


    def update(self):
        if self.side == 'Right':
            self.rect.x += self.velocity
        else:
            self.rect.x -= self.velocity
        if pygame.sprite.spritecollideany(self, platform_sprites):
            self.kill()
        if self.rect.x > 2000 or self.rect.x < -500:
            self.kill()
        if pygame.sprite.spritecollideany(self, self.grop):
            hero = pygame.sprite.spritecollideany(self, self.grop)
            if self.side == 'Right' and hero.respawn == 0:
                hero.velocityx -= self.streight
            elif hero.respawn == 0:
                hero.velocityx += self.streight
            self.kill()

class ShotGunBullet(pygame.sprite.Sprite):
    def __init__(self, side, x, y, pl, rot=0):
        if pl == 'player1':
            super().__init__(bullet1_sprites)
        else:
            super().__init__(bullet2_sprites)
        self.side = side
        self.rot = rot
        self.pl = pl
        self.image = pygame.transform.scale(load_image('guns/MediumBullet.png'), (25, 6))
        if side == 'Left':
            self.image = pygame.transform.flip(self.image, True, False)
        self.image = pygame.transform.rotate(self.image, self.rot)
        self.rect = self.image.get_rect()
        if self.side == 'Right':
            self.rect.x, self.rect.y = x + 85, y
        if self.side == 'Left':
            self.rect.x, self.rect.y = x - 5, y
        self.velocity = 5
        self.streight = 5
        if self.pl == 'player1':
            self.grop = players2
        else:
            self.grop = players1

    def update(self):
        if self.side == 'Right':
            self.rect.x += self.velocity
            if self.rot > 0:
                self.rect.y -= 2
            elif self.rot < 0:
                self.rect.y += 2
        else:
            self.rect.x -= self.velocity
            if self.rot > 0:
                self.rect.y += 2
            elif self.rot < 0:
                self.rect.y -= 2

        if pygame.sprite.spritecollideany(self, platform_sprites):
            self.kill()
        if self.rect.x > 2000 or self.rect.x < -500:
            self.kill()
        if pygame.sprite.spritecollideany(self, self.grop):
            hero = pygame.sprite.spritecollideany(self, self.grop)
            if self.side == 'Right' and hero.respawn == 0:
                hero.velocityx -= self.streight
            elif hero.respawn == 0:
                hero.velocityx += self.streight
            self.kill()

class BoxWithGun(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(box_sprites)
        self.image = pygame.transform.scale(load_image('box.png'), (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = choice(range(1, 964))
        self.rect.y = 0
        self.velo = 1
        self.dostav = False
        self.gun = choice(['ak47', 'awp', 'mp5', 'shotgun'])

    def update(self):
        if not pygame.sprite.spritecollideany(self, platform_sprites):
            self.rect.y += self.velo
        if self.rect.x == 0:
            self.velo = 0


running = True
filename = started_menu()

while running:
    if mus != 'fight':
        pygame.mixer.music.stop()
        music(choice(music_for_fight), 'fight')
    all_sprites.empty()  # âñå ñïðàéòû, êîòîðûå ðèñóþòñÿ ïåðâûì ïëàíîì, òèïî èãðîêîâ, êîðîáîê è ò.ï.
    level_sprites.empty()  # òóò ìåíÿ òîëüêî ôîí
    platform_sprites.empty()  # ïëàòôîðìû âñå
    guns_sprites.empty()
    bullet1_sprites.empty()
    bullet2_sprites.empty()
    box_sprites.empty()
    numbers_sprites.empty()
    button_sprites.empty()
    players1.empty()
    players2.empty()
    fake.empty()
    icons.empty()
    icon1 = pygame.sprite.Sprite()
    icon1.image = pygame.transform.scale(load_image('icon_p1.png'), (45, 60))
    icon1.rect = icon1.image.get_rect()
    icon1.rect.x, icon1.rect.y = 20, 20
    icons.add(icon1)
    icon2 = pygame.sprite.Sprite()
    icon2.image = pygame.transform.scale(load_image('icon_p2.png'), (50, 60))
    icon2.rect = icon2.image.get_rect()
    icon2.rect.x, icon2.rect.y = width - 190, 20
    icons.add(icon2)
    boxes = []
    player = Player(900, 20, 'Pistol', 'player1.png', 4, 1, 'player1', side='Left')  # Pistol, ak47, awp, mp5
    player2 = Player(100, 20, 'Pistol', 'player2.png', 2, 1, 'player2')
    if filename == 'level3.png':
        t2 = Table((0, 0), player2, 'table1.png')
        t1 = Table((width - 210, 0), player, 'table1.png')
    else:
        t2 = Table((0, 0), player2, 'table.png')
        t1 = Table((width - 210, 0), player, 'table.png')
    filename = filename.split('.')[0]
    load_level('data/' + filename + '.txt')
    time = 0
    clock = pygame.time.Clock()
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
        bullet1_sprites.update()
        bullet2_sprites.update()
        if player2.weapon.kd != 0:
            player2.weapon.kd -= 1
        player2.players_move()
        player2.weapon.update()
        if time % 1500 == 0:
            box = BoxWithGun()
            boxes.append(box)
        t1.update()
        t2.update()
        level_sprites.draw(screen)
        platform_sprites.draw(screen)
        all_sprites.draw(screen)
        bullet1_sprites.draw(screen)
        bullet2_sprites.draw(screen)
        box_sprites.draw(screen)
        numbers_sprites.draw(screen)
        icons.draw(screen)
        players1.draw(screen)
        players2.draw(screen)
        guns_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(300)
        for k in boxes:
            k.update()
        clock = pygame.time.Clock()
        if player.lives == 0 or player2.lives == 0:
            finaly_menu(player.lives)
            filename = started_menu()
            break