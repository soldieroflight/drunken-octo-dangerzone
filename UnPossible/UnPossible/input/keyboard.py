import pygame
from .keymappings import *

KEY_MAP = {}

def initialize():
    global KEY_IDS, KEY_MAP
    for keyId in KEY_IDS:
        KEY_MAP[pygame.key.name(keyId)] = keyId

class Keyboard(object):
    def __init__(self):
        pass

    def get_key_pressed(self, key):
        global KEY_MAP
        pressed = False
        keyStates = pygame.key.get_pressed()
        if (keyStates[KEY_MAP[key]]):
            pressed = True
        return pressed
           