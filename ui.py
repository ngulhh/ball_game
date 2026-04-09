# -*- coding: utf-8 -*-
import pygame
import config

class Button:
    def __init__(self, x, y, w, h, text, color=(50, 100, 200), hover_color=(80, 130, 220)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.hovered = False

    def draw(self, surface):
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (100, 100, 100), self.rect, 2, border_radius=10)
        font = pygame.font.Font(None, 40)
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def create_menu_buttons():
    start_btn = Button(config.WIDTH // 2 - 80, config.HEIGHT // 2 - 30, 160, 60, "START")
    sound_btn = Button(config.WIDTH // 2 - 80, config.HEIGHT // 2 + 50, 160, 50, "Sound: OFF")
    return start_btn, sound_btn

def draw_background(surface):
    bg = pygame.Surface((config.WIDTH, config.HEIGHT))
    for y in range(config.HEIGHT):
        color_value = int(5 + (y / config.HEIGHT) * 20)
        bg.set_at((0, y), (color_value, color_value, color_value + 5))
    surface.blit(bg, (0, 0))
    return bg

def draw_game_over(screen):
    font = pygame.font.Font(None, 72)
    text = font.render("Game Failed", True, (255, 0, 0))
    text_rect = text.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2))
    screen.blit(text, text_rect)

    font_small = pygame.font.Font(None, 36)
    hint = font_small.render("Press R to Menu  |  ESC to Quit", True, (200, 200, 200))
    hint_rect = hint.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2 + 50))
    screen.blit(hint, hint_rect)
