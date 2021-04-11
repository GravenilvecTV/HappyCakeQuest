import pygame
import pytmx
import pyscroll

from entity import Entity
from player import Player
from scorpion import Scorpion


class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode((1080, 720))
        pygame.display.set_caption("HappyCakeQuest")

        # charger la carte
        tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 2.8

        # le group avec la map
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=3)

        # recuperer le point de spawn du joueur
        self.spawn_point = tmx_data.get_object_by_name('player_spawn')

        self.monsters = pygame.sprite.Group()

        win_point = tmx_data.get_object_by_name('win')
        self.win_rect = pygame.Rect(win_point.x, win_point.y, win_point.width, win_point.height)

        # charger le joueur
        self.player = Player(self.spawn_point.x, self.spawn_point.y)
        self.group.add(self.player)

        # charger les blocks de collisions
        self.walls = []
        self.void = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.rect.Rect(
                    obj.x, obj.y, obj.width, obj.height
                ))
            if obj.type == "void":
                self.void.append(pygame.rect.Rect(
                    obj.x, obj.y, obj.width, obj.height
                ))
            if obj.type == "monster":
                scorpion = Scorpion(obj.x, obj.y)
                self.monsters.add(scorpion)

        self.group.add(self.monsters)

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')

    def update(self):
        self.group.update()

        # collision
        for sprite in self.group.sprites():

            # murs
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

            # collision
            if type(sprite) is Player:
                if self.player.feet.collidelist(self.void) > -1:
                    sprite.teleport_to([self.spawn_point.x, self.spawn_point.y])
                elif self.player.feet.colliderect(self.win_rect):
                    print("Gagné !")

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:

            # actualisation de la carte
            self.player.save_location()
            self.handle_input()
            self.update()

            self.group.center(self.player.rect)
            self.group.draw(self.screen)

            self.player.cooldown += clock.get_time()
            self.player.update_health_bar(self.map_layer, self.screen, -3)

            for monster in self.monsters:
                monster.cooldown += clock.get_time()
                monster.cooldown_between_anim += clock.get_time()
                monster.update_health_bar(self.map_layer, self.screen)
                monster.toggle_animation(self.group)

            # actualiser l'ecran
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(120)
        pygame.quit()


if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()
