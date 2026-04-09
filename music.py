# -*- coding: utf-8 -*-
import pygame
import os

class MusicPlayer:
    def __init__(self):
        self.enabled = False
        self.current_music = None
        self.music_file = "background_music.mp3"

    def toggle(self):
        if not pygame.mixer.get_init():
            return

        self.enabled = not self.enabled
        if self.enabled:
            if os.path.exists(self.music_file):
                pygame.mixer.music.load(self.music_file)
                pygame.mixer.music.play(-1)
                print("[Music] Playing")
            else:
                print("[Music] File not found")
                self.enabled = False
        else:
            pygame.mixer.music.stop()
            print("[Music] Stopped")

    def stop(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
