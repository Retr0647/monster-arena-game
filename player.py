import pygame.key

from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.state, self.frame_index = 'down', 0
        self.animation_speed = 5

        # setup
        self.image = pygame.image.load(join('images', 'player', 'down',
                                            '0.png')).convert_alpha()
        self.still_image = self.image.copy()
        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(-60, -90)

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = PLAYER_DATA['Running speed']
        self.collision_sprites = collision_sprites

        # stats
        self.name = 'Player'
        self.balance = PLAYER_BALANCE
        self._health = self.max_health = PLAYER_DATA['Health']
        self.damage = PLAYER_DATA['Damage']
        self.shot_speed = PLAYER_DATA['Shooting speed']
        self.stats = {'Damage': self.damage, 'Health': self.health,
                      'Running speed': self.speed,
                      'Shooting speed': self.shot_speed}

    def stats_update(self):
        self.stats = {'Damage': self.damage, 'Health': self.health,
                      'Running speed': self.speed,
                      'Shooting speed': self.shot_speed}

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = min(self.max_health, max(0, value))

    def load_images(self):
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}

        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(
                    join('images', 'player', state)):
                if file_names:
                    for file_name in sorted(file_names, key=lambda
                                            name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if (
            self.direction) else self.direction

    def move(self, delta):
        self.hitbox_rect.x += self.direction.x * self.speed * delta
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * delta
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top

    def animate(self, delta):
        # get state
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        # animate
        self.frame_index = (self.frame_index + self.animation_speed *
                            delta) if self.direction else 0
        self.image = self.frames[self.state][int(self.frame_index) %
                                             len(self.frames[self.state])]

    def update(self, delta):
        self.input()
        self.move(delta)
        self.animate(delta)
        self.stats_update()
