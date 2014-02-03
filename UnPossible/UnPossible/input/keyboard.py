import pygame
from .keymappings import *

KEY_MAP = {}
keyboard = None

def initialize():
    global KEY_IDS, KEY_MAP, keyboard
    for keyId in KEY_IDS:
        KEY_MAP[pygame.key.name(keyId)] = keyId
    keyboard = Keyboard()

class Keyboard(object):
    def __init__(self):
        self.keyStates = pygame.key.get_pressed()
        self.previousStates = pygame.key.get_pressed()

    def get_key_pressed(self, key):
        global KEY_MAP
        return self.keyStates[KEY_MAP[key]]

    def get_key_just_pressed(self, key):
        global KEY_MAP
        return self.keyStates[KEY_MAP[key]] and not self.previousStates[KEY_MAP[key]]

    def get_key_released(self, key):
        global KEY_MAP
        return not self.keyStates[KEY_MAP[key]] and self.previousStates[KEY_MAP[key]]

    def update(self):
        self.previousStates = [x for x in self.keyStates]
        self.keyStates = pygame.key.get_pressed()

