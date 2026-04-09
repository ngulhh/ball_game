# -*- coding: utf-8 -*-
import pygame
import random
import math
import config

class FoodBall:
    def __init__(self, exclude_positions):
        self.radius = random.randint(config.FOOD_RADIUS_MIN, config.FOOD_RADIUS_MAX)
        while True:
            self.x = random.randint(self.radius, config.WIDTH - self.radius)
            self.y = random.randint(self.radius, config.HEIGHT - self.radius)
            dist_ok = True
            for pos in exclude_positions:
                dist = math.sqrt((self.x - pos[0]) ** 2 + (self.y - pos[1]) ** 2)
                if dist < config.SAFE_RADIUS:
                    dist_ok = False
                    break
            if dist_ok:
                break
        self.mass = self.radius * self.radius
        self.vx = random.uniform(-config.FOOD_SPEED, config.FOOD_SPEED)
        self.vy = random.uniform(-config.FOOD_SPEED, config.FOOD_SPEED)

        colors = [
            (255, 100, 100), (100, 255, 100), (100, 100, 255),
            (255, 255, 100), (255, 100, 255), (100, 255, 255),
            (255, 150, 100), (150, 100, 255), (200, 100, 150),
            (100, 200, 150), (150, 150, 200), (255, 200, 100)
        ]
        self.color = random.choice(colors)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x - self.radius < 0 or self.x + self.radius > config.WIDTH:
            self.vx = -self.vx
            self.x = max(self.radius, min(config.WIDTH - self.radius, self.x))
        if self.y - self.radius < 0 or self.y + self.radius > config.HEIGHT:
            self.vy = -self.vy
            self.y = max(self.radius, min(config.HEIGHT - self.radius, self.y))

    def draw(self, surface):
        pygame.draw.circle(surface, self.color,
                          (int(self.x), int(self.y)), self.radius)

    def check_collision(self, ball_x, ball_y, ball_radius):
        distance = math.sqrt((self.x - ball_x) ** 2 + (self.y - ball_y) ** 2)
        return distance < ball_radius + self.radius
