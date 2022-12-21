
import pygame

import input
import particle

class Entity:

    def __init__(self, x, y, w, h, name, img, game):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y, w, h)
        self.name = name
        self.img = img
        self.game = game
        self.action = 'idle'
        self.vel = [0, 0]

    def update(self):
        collision_directions, amount_moved = self.move(self.game.assets.worlds.get_active_world().level.collision_mesh, self.game.dt)
        if collision_directions['down'] or collision_directions['up']:
            self.vel[1] = 0
        if collision_directions['right'] or collision_directions['left']:
            self.vel[0] = 0
        self.game.assets.camera.render(self.img, (self.x, self.y))

    def move(self, tiles, dt):
        collision_directions = {'up': False, 'down': False, 'left': False, 'right': False}
        orig_x, orig_y = self.rect.x / 1, self.rect.y / 1
        self.rect.x += self.vel[0] * dt
        collision_tiles = [tile for tile in tiles if self.rect.colliderect(tile)]
        for tile in collision_tiles:
            if self.vel[0] > 0:
                self.rect.x = tile.x - self.w
                collision_directions['right'] = True
            elif self.vel[0] < 0:
                self.rect.x = tile.right
                collision_directions['left'] = True
        self.rect.y += self.vel[1] * dt
        collision_tiles = [tile for tile in tiles if self.rect.colliderect(tile)]
        for tile in collision_tiles:
            if self.vel[1] > 0:
                self.rect.y = tile.y - self.h
                collision_directions['down'] = True
            elif self.vel[1] < 0:
                self.rect.y = tile.bottom
                collision_directions['up'] = True
        self.y, self.x = self.rect.y, self.rect.x
        amount_moved = [self.x - orig_x, self.y - orig_y]
        return collision_directions, amount_moved


class Player(Entity):

    def __init__(self, x, y, w, h, img, game, gravity=0):
        super().__init__(x, y, w, h, 'player', img, game)
        self.anims = {anim.split(self.name)[-1]: self.game.assets.anims.anims[anim] for anim in self.game.assets.anims.anims if self.name in anim}
        self.gravity = gravity
        self.vel_cap = 20
        self.speed = 2

    def update(self):
        raw_movement_directions = {'down': False, 'up': False, 'left': False, 'right': False}
        for event in self.game.last_input:
            if event.type == input.KEYHOLD:
                match event.key:
                    case input.S:
                        self.vel[1] += self.speed
                        raw_movement_directions['down'] = True
                    case input.W:
                        self.vel[1] -= self.speed
                        raw_movement_directions['up'] = True
                    case input.A:
                        self.vel[0] -= self.speed
                        raw_movement_directions['left'] = True
                    case input.D:
                        self.vel[0] += self.speed
                        raw_movement_directions['right'] = True
                    case input.RETURN:
                        self.x, self.y = 0, 0
                        self.rect.x, self.rect.y = 0, 0
                        self.vel = [0, 0]
        if self.vel[0] > self.vel_cap:
            self.vel[0] = self.vel_cap
        if self.vel[1] > self.vel_cap:
            self.vel[1] = self.vel_cap
        if self.vel[0] < -self.vel_cap:
            self.vel[0] = -self.vel_cap
        if self.vel[1] < -self.vel_cap:
            self.vel[1] = -self.vel_cap
        self.vel[1] += self.gravity

        collision_directions, amount_move = self.move(self.game.assets.worlds.get_active_world().level.collision_mesh, self.game.dt)
        amount_move[0] = int(amount_move[0])
        amount_move[1] = int(amount_move[1])

        if amount_move[1] < 0:
            self.game.particles.append(particle.ParticleBurst((self.x + self.w // 2, self.y + self.h // 2), 7, 50, ((255, 250, 250), (255, 255, 240), (245, 245, 245), (255, 255, 255), (254, 222, 23)), 80, 80, (0, -self.speed), self.game, type='|', shape='rect', fade=True, spread=0.2))
        if amount_move[1] > 0:
            self.game.particles.append(particle.ParticleBurst((self.x + self.w // 2, self.y + self.h // 2), 7, 50, ((255, 250, 250), (255, 255, 240), (245, 245, 245), (255, 255, 255), (254, 222, 23)), 80, 80, (0, self.speed), self.game, type='|', shape='rect', fade=True, spread=0.2))
        if amount_move[0] < 0:
            self.game.particles.append(particle.ParticleBurst((self.x + self.w // 2, self.y + self.h // 2), 7, 50, ((255, 250, 250), (255, 255, 240), (245, 245, 245), (255, 255, 255), (254, 222, 23)), 80, 80, (-self.speed, 0), self.game, type='-', shape='rect', fade=True, spread=0.2))
        if amount_move[0] > 0 :
            self.game.particles.append(particle.ParticleBurst((self.x + self.w // 2, self.y + self.h // 2), 7, 50, ((255, 250, 250), (255, 255, 240), (245, 245, 245), (255, 255, 255), (254, 222, 23)), 80, 80, (self.speed, 0), self.game, type='-', shape='rect', fade=True, spread=0.2))

        if collision_directions['down'] or collision_directions['up']:
            self.vel[1] = 0
        if collision_directions['right'] or collision_directions['left']:
            self.vel[0] = 0

        # if self.vel[0] > 0:
        #     self.vel[0] -= 1
        # elif self.vel[0] < 0:
        #     self.vel[0] += 1
        # if self.vel[1] > 0:
        #     self.vel[1] -= 1
        # elif self.vel[1] < 0:
        #     self.vel[1] += 1

        self.anims[self.action].play(self.game.dt)
        self.anims[self.action].render_main((self.x, self.y))
