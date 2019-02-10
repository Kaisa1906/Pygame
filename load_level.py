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