import os



def load_level(filename):
    filename = 'data/' + filename
    file = open(filename, 'r')
    elements = file.read()
    elements = elements.split('\n')
    for element in elements:
        element = element.split('-')
        type = element[0]
        if type == 'Platform':
            element = element[1].split()
            pos = (element[1], element[2])
            scale = (element[3], element[4])
            Platform((pos), (scale))
        if type == 'Player':
            element = element[1].split()
            Player(element[0], element[1])
        if type == 'Background':
            name = element[1]
            Background = pygame.sprite.Sprite()
            Background.image = pygame.transform.scale(load_image(name), (1024, 550))
            Background.rect = Background.image.get_rect()
            level_sprites.add(Background)

load_level('level1.txt')
