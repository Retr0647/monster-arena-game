from settings import *
import sys
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from random import choice
from ui import *
from support import audio_importer, folder_importer, tile_importer
from timer import Timer


class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,
                                                        WINDOW_HEIGHT))
        pygame.display.set_caption('Monster Arena')
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_won = False

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # timers
        self.welcome_timer = Timer(5000, autostart=True)
        self.shoot_timer = Timer(PLAYER_DATA['Shooting speed'])
        self.enemy_event = pygame.event.custom_type()
        self.round_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 500)
        pygame.time.set_timer(self.round_event, 1000)
        self.spawn_positions = []
        self.hit_timer = Timer(500)
        self.current_round = list(ROUND_DATA.keys())
        self.round_duration = ROUND_DATA[self.current_round[0]]['duration']
        self.round_timer = Timer(self.round_duration * 1000)
        self.display_timer = TimerDisplay(self.current_round[0])

        # assets setup
        self.load_assets()
        self.setup()
        self.enemy_counter = 1
        self.score = 0
        self.max_enemies = ROUND_DATA[self.current_round[0]]['enemies']
        self.enemy = None
        self.immortality = True
        self.skills = PLAYER_SKILLS.keys()

        # music
        self.audio['music'].play(-1).set_volume(0.6)

        # ui
        self.health_bar = HealthBar(self.player)
        self.welcome_screen = WelcomeScreen()
        self.coin_counter = CoinCounter(self.player, self.coins)
        self.ui = UI(self.player, self.skills, self.skill_icons,
                     self.key_icons, self.ui_input)

    def load_assets(self):
        self.audio = audio_importer('audio')

        self.coins = tile_importer(5, 'images', 'coins')

        self.key_icons = folder_importer('images', 'keys', 'keyboard')

        self.skill_icons = folder_importer('images', 'skills')

        self.bullet_surf = pygame.image.load(join('images', 'gun', 'bullet.png'
                                                  )).convert_alpha()

        self.enemy_frames = {'bat': [], 'blob': [], 'skeleton': []}

        for enemy in self.enemy_frames.keys():
            for folder_path, sub_folders, file_names in (
                    walk(join('images', 'enemies', enemy))):
                if file_names:
                    for file_name in sorted(file_names, key=lambda name:
                                            int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.enemy_frames[enemy].append(surf)

    def ui_input(self, state, data=None):
        if state == 'Upgrade':
            self.apply_upgrade(data)
        elif state == 'Exit':
            sys.exit()

    def apply_upgrade(self, skill):
        if skill == 'Damage' and self.player.balance >= 500:
            self.player.balance -= 500
            self.player.damage += PLAYER_SKILLS['damage upgrade']
        elif skill == 'Health' and self.player.balance >= 750:
            self.player.balance -= 750
            self.player.max_health += PLAYER_SKILLS['health upgrade']
            self.player.health = self.player.max_health
        elif skill == 'Running speed' and self.player.balance >= 250:
            self.player.balance -= 250
            self.player.speed += PLAYER_SKILLS['speed upgrade']
        elif skill == 'Shooting speed' and self.player.balance >= 500:
            self.player.balance -= 500
            self.shoot_timer.duration -= PLAYER_SKILLS['shot speed upgrade']
            self.player.shot_speed -= PLAYER_SKILLS['shot speed upgrade']

    def input(self):
        keys = pygame.key.get_just_pressed()
        if pygame.mouse.get_pressed()[0] and self.shoot_timer.active is False:
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf, pos, self.gun.player_direction,
                   (self.all_sprites, self.bullet_sprites))
            self.audio['shoot'].play()
            self.shoot_timer.activate()
        if (keys[pygame.K_SPACE] and self.round_timer.active is False
                and self.ui.visible is False):
            self.round_timer.activate()
            self.audio['music'].stop()
            self.audio['music2'].play(-1).set_volume(0.6)
        if keys[pygame.K_e] and self.round_timer.active is False:
            self.welcome_timer.deactivate()
            self.ui.visible = True if self.ui.visible is False else False

    def bullet_collision(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collided_sprites = pygame.sprite.spritecollide(
                    bullet, self.enemy_sprites, False,
                    pygame.sprite.collide_mask)
                if collided_sprites:
                    self.audio['impact'].play()
                    for sprite in collided_sprites:
                        if sprite.name == 'skeleton':
                            sprite.health -= self.player.damage
                        if sprite.name == 'bat':
                            sprite.health -= self.player.damage
                        if sprite.name == 'blob':
                            sprite.health -= self.player.damage
                        if sprite.health <= 0:
                            self.audio['coin'].play()
                            self.score += (
                                SCORE_DATA)[self.current_round[0]]['kill']
                            self.player.balance += (
                                KILL_REWARD)[self.current_round[0]]
                            sprite.destroy()
                            self.enemy_counter -= 1
                    bullet.kill()

    def player_collision(self):
        if (pygame.sprite.spritecollide(self.player, self.enemy_sprites,
                                        False, pygame.sprite.collide_mask)
                and self.hit_timer.active is False):
            self.hit_timer.activate()
            for enemy in (
                    pygame.sprite.spritecollide(
                        self.player,
                        self.enemy_sprites, False,
                        pygame.sprite.collide_mask)):
                if enemy.name == 'skeleton':
                    self.player.health -= (
                     MONSTER_DATA)['skeleton'][self.current_round[0]]['damage']
                if enemy.name == 'bat':
                    self.player.health -= (
                     MONSTER_DATA)['bat'][self.current_round[0]]['damage']
                if enemy.name == 'blob':
                    self.player.health -= (
                     MONSTER_DATA)['blob'][self.current_round[0]]['damage']
            self.audio['hurt'].play()
            if self.player.health <= 0:
                self.running = False

    def round_end(self):
        if self.current_round[0] == 'Round 5':
            self.running = False
            self.game_won = True
            self.over()
        else:
            self.current_round = (
                    self.current_round[1:] + self.current_round[:1])
            self.round_timer.deactivate()
            self.score += SCORE_DATA[self.current_round[0]]['round']
            self.round_duration = ROUND_DATA[self.current_round[0]]['duration']
            self.max_enemies = ROUND_DATA[self.current_round[0]]['enemies']
            self.display_timer.current_time = self.round_duration
            self.round_timer = Timer(self.round_duration * 1000)
            self.audio['music2'].stop()
            self.audio['win'].play()
            self.audio['music'].play(-1).set_volume(0.4)

        for self.enemy in self.enemy_sprites:
            self.enemy.kill()
            self.enemy_counter = 0

    def over(self):
        if self.game_won:
            self.audio['music2'].stop()
            self.audio['win'].play()
            self.win_screen = WinScreen(self.score)
            self.win_screen.draw()
        else:
            self.audio['music2'].stop()
            self.audio['loose'].play()
            self.death_screen = DeathScreen()
            self.death_screen.draw()

        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True
                        sys.exit()

    def setup(self):
        # import graphic
        map = load_pygame(join('data', 'maps', 'world.tmx'))

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y),
                            pygame.Surface((obj.width, obj.height)),
                            (self.collision_sprites))

        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image,
                            (self.all_sprites, self.collision_sprites))

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y),
                                     self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)
            else:
                self.spawn_positions.append((obj.x, obj.y))

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if (event.type == self.enemy_event and
                        self.enemy_counter <= self.max_enemies and
                        self.round_timer.active):
                    self.enemy = Enemy(choice(self.spawn_positions),
                                       self.enemy_frames, (self.all_sprites,
                                       self.enemy_sprites),
                                       self.player,
                                       self.collision_sprites,
                                       choice(list(MONSTER_DATA.keys())),
                                       self.current_round[0])
                    self.enemy_counter += 1
                if event.type == self.round_event and self.round_timer.active:
                    self.display_timer.current_time -= 1
                    if self.display_timer.current_time <= 0:
                        self.round_end()

            # update
            self.input()
            self.hit_timer.update()
            self.shoot_timer.update()
            self.all_sprites.update(dt)
            self.bullet_collision()
            self.player_collision()
            self.ui.update()

            # draw
            self.display_surface.fill(COLORS['black'])
            self.all_sprites.draw(self.player.rect.center)
            if self.round_timer.active:
                self.display_timer.draw()
            self.health_bar.draw()
            self.ui.draw()
            self.coin_counter.draw()
            if self.welcome_timer.active:
                self.welcome_screen.draw()

            pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
    if not game.running:
        game.over()
