import pygame
from os.path import join
from os import walk

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TILE_SIZE = 64

PLAYER_BALANCE = 100

SCORE_DATA = {
    'Round 1': {'round': 1000, 'kill': 50},
    'Round 2': {'round': 2000, 'kill': 100},
    'Round 3': {'round': 3000, 'kill': 150},
    'Round 4': {'round': 5000, 'kill': 200},
    'Round 5': {'round': 8000, 'kill': 250}
}

KILL_REWARD = {
    'Round 1': 10,
    'Round 2': 20,
    'Round 3': 30,
    'Round 4': 40,
    'Round 5': 50
}

ROUND_DATA = {
    'Round 1': {'duration': 30, 'enemies': 10},
    'Round 2': {'duration': 45, 'enemies': 20},
    'Round 3': {'duration': 60, 'enemies': 30},
    'Round 4': {'duration': 75, 'enemies': 40},
    'Round 5': {'duration': 90, 'enemies': 50}
}

COLORS = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'gray': 'gray',
    'darkred': '#b22222',
    'red': (255, 0, 0),
    'green': (0, 255, 0)
}

PLAYER_DATA = {
    'Damage': 50,
    'Health': 200,
    'Running speed': 500,
    'Shooting speed': 200
}

PLAYER_SKILLS = {
    'speed upgrade': 100,
    'damage upgrade': 50,
    'shot speed upgrade': 50,
    'health upgrade': 100
}

MONSTER_DATA = {
    'skeleton': {
        'Round 1': {'health': 150, 'damage': 50},
        'Round 2': {'health': 200, 'damage': 75},
        'Round 3': {'health': 250, 'damage': 100},
        'Round 4': {'health': 300, 'damage': 125},
        'Round 5': {'health': 350, 'damage': 150}
    },
    'blob': {
        'Round 1': {'health': 50, 'damage': 25},
        'Round 2': {'health': 100, 'damage': 40},
        'Round 3': {'health': 150, 'damage': 55},
        'Round 4': {'health': 200, 'damage': 70},
        'Round 5': {'health': 250, 'damage': 75}
    },
    'bat': {
        'Round 1': {'health': 100, 'damage': 40},
        'Round 2': {'health': 150, 'damage': 60},
        'Round 3': {'health': 200, 'damage': 80},
        'Round 4': {'health': 250, 'damage': 100},
        'Round 5': {'health': 300, 'damage': 120}
    }
}

KEYS_DATA = {
    'W': 'Move player up',
    'A': 'Move player left',
    'S': 'Move player down',
    'D': 'Move player right',
    'E': 'Open menu',
    'MOUSEBUTTONLEFT': 'Shooting',
    'MOUSEMOVE': 'Move gun around',
    'ARROWUP': 'Menu index up',
    'ARROWLEFT': 'Menu index left',
    'ARROWDOWN': 'Menu index down',
    'ARROWRIGHT': 'Menu index right',
    'ENTER': 'Menu access',
    'ESC': 'Exit game or menu',
    'SPACE': 'Start round',
}
