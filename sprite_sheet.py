import pygame


class SpriteSheet:

    def __init__(self, name):
        self.sprite_sheet = pygame.image.load(name)
        self.images = dict()

    def load_images(self, name, numbers=1, row=0):
        images = []
        for i in range(0, numbers):
            image = pygame.Surface([40, 40])
            image.blit(self.sprite_sheet, (0, 0), (i * 32, (row * 32), 32, 32))
            images.append(image)

        self.images.update({name: images})

    def get_images(self, name):
        return self.images[name]