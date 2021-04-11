import pygame

from entity import Entity


class Player(Entity):

    def __init__(self, x, y):
        super().__init__('player', x, y)

        # charger animations du sprite
        self.sprite_sheet.load_images('right', numbers=5, row=0)
        self.sprite_sheet.load_images('left', numbers=5, row=1)
        self.current_animation = 'left'
        self.image = self.sprite_sheet.get_images(self.current_animation)[0]

    def move_right(self):
        self.position[0] += self.speed

    def move_left(self):
        self.position[0] -= self.speed

    def move_down(self):
        self.position[1] += self.speed

    def move_up(self):
        self.position[1] -= self.speed

    def teleport_to(self, target_zone):
        self.position = target_zone