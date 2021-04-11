import pygame

from sprite_sheet import SpriteSheet


class Entity(pygame.sprite.Sprite):

    def __init__(self, name, x, y, animation_speed=200):
        super().__init__()

        self.sprite_sheet = SpriteSheet(f'{name}.png')
        self.image = pygame.image.load('cell.png')
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)

        # vie
        self.health = 100
        self.max_health = 100

        # animation
        self.old_position = self.position
        self.current_animation_index = 0
        self.animation_speed=animation_speed
        self.cooldown = 0
        self.speed = 1

    def change_animation(self, name):
        self.current_animation = name

    def get_animation(self):
        return self.sprite_sheet.get_images(self.current_animation)

    def animation(self):
        if self.cooldown > self.animation_speed:
            self.current_animation_index += 1
            if self.current_animation_index == len(self.get_animation()):
                self.current_animation_index = 0
            self.cooldown = 0

    def teleport_to(self, target_zone):
        self.position = target_zone

    def save_location(self):
        self.old_position = self.position.copy()

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def update_health_bar(self, map_layer, screen, offset_y=5):
        bar_back_position = [self.rect.x, self.rect.y + offset_y, self.max_health/4, 2]
        pygame.draw.rect(screen, (60, 63, 60), map_layer.translate_rect(bar_back_position))
        bar_position = [self.rect.x, self.rect.y + offset_y, self.health/4, 2]
        pygame.draw.rect(screen, (111, 210, 46), map_layer.translate_rect(bar_position))

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

        self.animation()
        self.image = self.get_animation()[self.current_animation_index]
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (40, 40))
