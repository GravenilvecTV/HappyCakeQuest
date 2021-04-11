import pygame

from entity import Entity


class Scorpion(Entity):

    def __init__(self, x, y):
        super().__init__('scorpion', x, y)
        self.sprite_sheet.load_images('left', numbers=4, row=4)
        self.sprite_sheet.load_images('right', numbers=4, row=5)
        self.current_animation = 'right'
        self.image = self.sprite_sheet.get_images(self.current_animation)[0]
        self.cooldown_between_anim = 0
        self.projectiles = pygame.sprite.Group()

    def toggle_animation(self, group):
        if self.cooldown_between_anim > 5000:
            if self.current_animation == 'right':
                self.current_animation = 'left'
            else:
                self.current_animation = 'right'
            self.cooldown_between_anim = 0