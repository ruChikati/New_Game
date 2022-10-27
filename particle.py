
import random

import pygame
import math


class Particle:

    def __init__(self, colour, pos, vel, size, time_to_live, game, shape='circle', width=0, shrink=False, fade=True, gravity=0):
        self.colour = colour
        self.pos = pos
        self.vel = vel
        self.size = size
        self.shape = shape
        self.game = game
        self.shrink = shrink
        self.fade = fade
        self.width = width
        self.gravity = gravity
        self.surf = pygame.Surface((2 * size, 2 * size), pygame.SRCALPHA)
        self.is_alive = True
        self.timer = time_to_live
        self.total_time = time_to_live
        match self.shape:
            case 'rect' | 'rectangle' | 'square':
                pygame.draw.rect(self.surf, self.colour, self.surf.get_rect(), self.width)
            case 'circle' | 'point' | 'dot':
                pygame.draw.circle(self.surf, self.colour, (self.size, self.size), self.size, self.width)

    def update(self, dt, vel_update=(0, 0)):
        vel_update = (vel_update[0], vel_update[1] + self.gravity)
        self.vel[0] += vel_update[0]
        self.vel[1] += vel_update[1]
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        if self.shrink:
            size = self.size * self.timer // self.total_time
        else:
            size = self.size
        if self.fade:
            self.surf.set_alpha(255 * self.timer // self.total_time)
        if not self.timer:
            self.is_alive = False
        elif self.timer > 0:
            self.timer -= 1
        self.surf = pygame.transform.scale(self.surf, (2 * size, 2 * size))
        self.game.assets.camera.render(self.surf, self.pos)


class ParticleBurst:

    def __init__(self, pos, size, amount, colours, time_to_live, particle_time_to_live, speed, game, type='burst', shape='circle', width=0, shrink=False, fade=True, gravity=0):
        self.particles = []
        self.starting_time = time_to_live
        self.time = time_to_live
        self.type = type
        self.colours = colours
        self.middle = pos
        self.particle_size = size
        self.game = game
        self.shrinks = shrink
        self.fades = fade
        self.amount = amount
        self.type = type
        self.speed = speed
        self.size = size
        self.shape = shape
        self.width = width
        self.shrink = shrink
        self.fade = fade
        self.gravity = gravity
        self.particle_time = particle_time_to_live
        if self.amount >= 0:    # if amount is negative, new particles are added every frame, else the specified amount are added at the beginning
            match type:
                case 'burst' | 'circle':
                    for i in range(amount):
                        theta = random.random() * 2 * math.pi
                        self.particles.append(Particle(random.choice(self.colours), [self.middle[0], self.middle[1]], [speed * math.cos(theta) * random.random(), speed * math.sin(theta) * random.random()], size, particle_time_to_live, self.game, shape, width, shrink, fade, gravity))
                case 'fountain' | 'pillar':
                    for i in range(amount):
                        self.particles.append(Particle(random.choice(self.colours), [self.middle[0], self.middle[1]], [(2 * random.random() - 1) * speed, -2 * speed], size, particle_time_to_live, self.game, shape, width, shrink, fade, gravity))
                # [self.middle[0], self.middle[1]], because it didn't work with just self.middle

    def update(self, dt, vel_update=(0, 0)):
        if self.time > 0:
            self.time -= 1
        for particle in self.particles:
            particle.update(dt, vel_update)
            if not particle.is_alive:
                del particle
        if self.amount < 0 and self.time:
            match self.type:
                case 'burst' | 'circle':
                    theta = random.random() * 2 * math.pi
                    self.particles.append(Particle(random.choice(self.colours), [self.middle[0], self.middle[1]], [self.speed * math.cos(theta) * random.random(), self.speed * math.sin(theta) * random.random()], self.size, self.particle_time, self.game, self.shape, self.width, self.shrink, self.fade, self.gravity))
                case 'fountain' | 'pillar':
                    self.particles.append(Particle(random.choice(self.colours), [self.middle[0], self.middle[1]], [(2 * random.random() - 1) * self.speed, -2 * self.speed], self.size, self.particle_time, self.game, self.shape, self.width, self.shrink, self.fade, self.gravity))
        if len(self.particles) > 100_000:
            for i in range(100):
                self.particles.pop(i)
