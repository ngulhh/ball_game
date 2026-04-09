# -*- coding: utf-8 -*-
"""
Ball Eat Game - 主程序
双人吃球游戏，支持两个玩家各自控制
玩家1: WASD 或 方向键
玩家2: 数字键盘 1(左) 2(下) 3(右) 5(上)
"""
import pygame
import math

import config
import food_ball
import player
import music
import ui

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption(config.TITLE)

music_player = music.MusicPlayer()
start_button, sound_button = ui.create_menu_buttons()

food_balls = []
player1 = player.Player(config.PLAYER1_START_X, config.PLAYER1_START_Y,
                        config.PLAYER1_COLOR, config.PLAYER1_BORDER_COLOR)
player2 = player.Player(config.PLAYER2_START_X, config.PLAYER2_START_Y,
                        config.PLAYER2_COLOR, config.PLAYER2_BORDER_COLOR)

game_state = "menu"
game_over = False
player1_alive = True
player2_alive = True
clock = pygame.time.Clock()
running = True

def spawn_food():
    global food_balls
    exclude = [(player1.x, player1.y), (player2.x, player2.y)]
    food_balls = [food_ball.FoodBall(exclude) for _ in range(config.FOOD_COUNT)]

def start_game():
    global game_state, game_over, player1_alive, player2_alive
    spawn_food()
    player1.reset()
    player2.reset()
    player1_alive = True
    player2_alive = True
    game_over = False
    game_state = "playing"

def check_player_eat_food(p):
    global food_balls
    to_remove = []
    for food in food_balls:
        if food.check_collision(p.x, p.y, p.radius):
            if p.radius > food.radius:
                p.grow(food.mass)
                to_remove.append(food)
            else:
                return True
    for f in to_remove:
        food_balls.remove(f)
    return False

def check_players_collision():
    global game_over, player1_alive, player2_alive
    if not player1_alive or not player2_alive:
        return
    dist = math.sqrt((player1.x - player2.x) ** 2 + (player1.y - player2.y) ** 2)
    if dist < player1.radius + player2.radius:
        if player1.radius > player2.radius:
            player1.grow(player2.mass)
            player2_alive = False
        elif player2.radius > player1.radius:
            player2.grow(player1.mass)
            player1_alive = False
        else:
            game_over = True

while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "menu":
                if start_button.is_clicked(mouse_pos):
                    start_game()
                elif sound_button.is_clicked(mouse_pos):
                    music_player.toggle()
                    sound_button.text = "Sound: ON" if music_player.enabled else "Sound: OFF"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_over:
                    game_state = "menu"
                elif game_state == "playing":
                    game_state = "menu"
                else:
                    running = False
            elif event.key == pygame.K_r:
                if game_over:
                    start_game()

    if game_state == "menu":
        ui.draw_background(screen)
        start_button.check_hover(mouse_pos)
        sound_button.check_hover(mouse_pos)
        start_button.draw(screen)
        sound_button.draw(screen)

        font_title = pygame.font.Font(None, 80)
        title = font_title.render("Ball Eat Game", True, (200, 200, 100))
        title_rect = title.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2 - 120))
        screen.blit(title, title_rect)

    elif game_state == "playing" and not game_over:
        keys = pygame.key.get_pressed()

        if player1_alive:
            dx1, dy1 = 0, 0
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                dx1 = -1
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                dx1 = 1
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                dy1 = -1
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                dy1 = 1
            player1.update(dx1, dy1)

        if player2_alive:
            dx2, dy2 = 0, 0
            if keys[pygame.K_KP1]:
                dx2 = -1
            if keys[pygame.K_KP3]:
                dx2 = 1
            if keys[pygame.K_KP2]:
                dy2 = 1
            if keys[pygame.K_KP5]:
                dy2 = -1
            player2.update(dx2, dy2)

        if player1_alive and check_player_eat_food(player1):
            player1_alive = False
        if player2_alive and check_player_eat_food(player2):
            player2_alive = False

        check_players_collision()

        if not player1_alive and not player2_alive:
            game_over = True

        if len(food_balls) < config.FOOD_MIN_COUNT:
            for _ in range(10):
                food_balls.append(food_ball.FoodBall([(player1.x, player1.y), (player2.x, player2.y)]))

        ui.draw_background(screen)

        for ball in food_balls:
            ball.update()
            ball.draw(screen)

        if player1_alive:
            player1.draw(screen)
        else:
            pygame.draw.circle(screen, (80, 80, 80), (int(player1.x), int(player1.y)), player1.radius)
            pygame.draw.circle(screen, (50, 50, 50), (int(player1.x), int(player1.y)), player1.radius, 3)
            for i in range(8):
                angle = math.pi * 1.5 + i * (math.pi / 4)
                inner_r = player1.radius + 5
                outer_r = player1.radius + 12
                x1 = player1.x + math.cos(angle) * inner_r
                y1 = player1.y + math.sin(angle) * inner_r
                x2 = player1.x + math.cos(angle) * outer_r
                y2 = player1.y + math.sin(angle) * outer_r
                pygame.draw.line(screen, (50, 50, 50), (x1, y1), (x2, y2), 3)

        if player2_alive:
            player2.draw(screen)
        else:
            pygame.draw.circle(screen, (80, 80, 80), (int(player2.x), int(player2.y)), player2.radius)
            pygame.draw.circle(screen, (50, 50, 50), (int(player2.x), int(player2.y)), player2.radius, 3)
            for i in range(8):
                angle = math.pi * 1.5 + i * (math.pi / 4)
                inner_r = player2.radius + 5
                outer_r = player2.radius + 12
                x1 = player2.x + math.cos(angle) * inner_r
                y1 = player2.y + math.sin(angle) * inner_r
                x2 = player2.x + math.cos(angle) * outer_r
                y2 = player2.y + math.sin(angle) * outer_r
                pygame.draw.line(screen, (50, 50, 50), (x1, y1), (x2, y2), 3)

        font_small = pygame.font.Font(None, 28)
        status_y = 10
        if not player1_alive:
            text1 = font_small.render("Player 1 Failed", True, (150, 150, 150))
            screen.blit(text1, (10, status_y))
            status_y += 25
        if not player2_alive:
            text2 = font_small.render("Player 2 Failed", True, (150, 150, 150))
            screen.blit(text2, (10, status_y))

    elif game_over:
        ui.draw_background(screen)

        for ball in food_balls:
            ball.update()
            ball.draw(screen)

        if player1_alive:
            player1.draw(screen)
        else:
            pygame.draw.circle(screen, (80, 80, 80), (int(player1.x), int(player1.y)), player1.radius)
            pygame.draw.circle(screen, (50, 50, 50), (int(player1.x), int(player1.y)), player1.radius, 3)
            for i in range(8):
                angle = math.pi * 1.5 + i * (math.pi / 4)
                inner_r = player1.radius + 5
                outer_r = player1.radius + 12
                x1 = player1.x + math.cos(angle) * inner_r
                y1 = player1.y + math.sin(angle) * inner_r
                x2 = player1.x + math.cos(angle) * outer_r
                y2 = player1.y + math.sin(angle) * outer_r
                pygame.draw.line(screen, (50, 50, 50), (x1, y1), (x2, y2), 3)

        if player2_alive:
            player2.draw(screen)
        else:
            pygame.draw.circle(screen, (80, 80, 80), (int(player2.x), int(player2.y)), player2.radius)
            pygame.draw.circle(screen, (50, 50, 50), (int(player2.x), int(player2.y)), player2.radius, 3)
            for i in range(8):
                angle = math.pi * 1.5 + i * (math.pi / 4)
                inner_r = player2.radius + 5
                outer_r = player2.radius + 12
                x1 = player2.x + math.cos(angle) * inner_r
                y1 = player2.y + math.sin(angle) * inner_r
                x2 = player2.x + math.cos(angle) * outer_r
                y2 = player2.y + math.sin(angle) * outer_r
                pygame.draw.line(screen, (50, 50, 50), (x1, y1), (x2, y2), 3)

        font_small = pygame.font.Font(None, 28)
        status_y = 10
        if not player1_alive:
            text1 = font_small.render("Player 1 Failed", True, (150, 150, 150))
            screen.blit(text1, (10, status_y))
            status_y += 25
        if not player2_alive:
            text2 = font_small.render("Player 2 Failed", True, (150, 150, 150))
            screen.blit(text2, (10, status_y))
            status_y += 25

        ui.draw_game_over(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
