# -*- coding: utf-8 -*-
import pygame
import math
import config

class Player:
    def __init__(self, x, y, color, border_color):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.radius = config.INITIAL_RADIUS
        self.mass = self.radius * self.radius
        self.speed = config.INITIAL_SPEED
        self.color = color
        self.border_color = border_color

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.radius = config.INITIAL_RADIUS
        self.mass = self.radius * self.radius
        self.speed = config.INITIAL_SPEED

    def update(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.x = max(self.radius, min(config.WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(config.HEIGHT - self.radius, self.y))

    def grow(self, food_mass):
        self.mass += food_mass
        self.radius = int(math.sqrt(self.mass))
        self.x = max(self.radius, min(config.WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(config.HEIGHT - self.radius, self.y))
        self.speed = max(config.MIN_SPEED, config.INITIAL_SPEED - self.radius // 50)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

        for i in range(8):
            angle = math.pi * 1.5 + i * (math.pi / 4)
            inner_r = self.radius + 5
            outer_r = self.radius + 12
            x1 = self.x + math.cos(angle) * inner_r
            y1 = self.y + math.sin(angle) * inner_r
            x2 = self.x + math.cos(angle) * outer_r
            y2 = self.y + math.sin(angle) * outer_r
            pygame.draw.line(surface, self.border_color, (x1, y1), (x2, y2), 3)

        pygame.draw.circle(surface, self.border_color, (int(self.x), int(self.y)), self.radius, 3)
