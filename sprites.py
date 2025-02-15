from settings import *
from math import atan2, degrees
from timer import Timer


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.ground = True


class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)


class Gun(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        # player connection
        self.player = player
        self.distance = 100
        self.player_direction = pygame.math.Vector2(0, 1)

        # sprite setup
        super().__init__(groups)
        self.gun_surface = pygame.image.load(
            join('images', 'gun', 'gun.png')).convert_alpha()
        self.image = self.gun_surface
        self.rect = self.image.get_frect(
            center=self.player.rect.center +
            self.player_direction * self.distance)

    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.player_direction = (mouse_pos - player_pos).normalize() if (
            self.player_direction) else self.player_direction

    def rotate_gun(self):
        angle = degrees(atan2(self.player_direction.x,
                              self.player_direction.y)) - 90
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.gun_surface, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(
                self.gun_surface, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, False, True)

    def update(self, _):
        self.get_direction()
        self.rotate_gun()
        self.rect.center = (self.player.rect.center +
                            self.player_direction * self.distance)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 1000

        self.direction = direction
        self.speed = 1200

    def update(self, delta):
        self.rect.center += self.direction * self.speed * delta
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups):
        super().__init__(groups)
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center=pos)
        self.animation_speed = 5

    def animate(self, delta):
        self.frame_index += self.animation_speed * delta
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def update(self, delta):
        self.animate(delta)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player,
                 collision_sprites, name, round):
        super().__init__(groups)
        self.player = player
        self.health = self.max_health = MONSTER_DATA[name][round]['health']

        # image
        self.name, self.frames, self.frame_index = name, frames, 0
        self.image = pygame.image.load(join('images', 'enemies', self.name,
                                            '0.png')).convert_alpha()
        self.animation_speed = 6

        # rect
        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(-20, -40)
        self.collision_sprites = collision_sprites
        self.direction = pygame.math.Vector2()
        self.speed = 350

        # timer
        self.death_timer = Timer(100, func=self.kill)

    def move(self, delta):
        # get direction
        player_pos = pygame.math.Vector2(self.player.rect.center)
        enemy_pos = pygame.math.Vector2(self.rect.center)
        self.direction = (player_pos - enemy_pos).normalize()
        if self.direction == 0:
            self.direction = (player_pos - enemy_pos)

        # update the rect position
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
        self.frame_index += self.animation_speed * delta
        self.image = self.frames[self.name][int(self.frame_index) %
                                            len(self.frames[self.name])]

    def destroy(self):
        self.death_timer.activate()
        self.animation_speed = 0
        self.image = pygame.mask.from_surface(self.image).to_surface()
        self.image.set_colorkey('black')

    def update(self, delta):
        self.death_timer.update()
        if not self.death_timer:
            self.move(delta)
            self.animate(delta)
