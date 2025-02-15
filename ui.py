from settings import *
from sprites import Coin


class UI:
    def __init__(self, player, skills, skill_icon, key_icons, get_input):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 30)
        self.left = WINDOW_WIDTH / 2 - 100
        self.top = WINDOW_HEIGHT / 2 + 50
        self.player = player
        self.skill = skills
        self.skill_icon = skill_icon
        self.keys = list(KEYS_DATA.keys())
        self.descriptions = list(KEYS_DATA.values())
        self.key_icons = key_icons
        self.visible_keys = 8
        self.get_input = get_input
        self.visible = False

        # control
        self.general_options = ['Controls', 'Stats', 'Upgrade', 'Exit']
        self.general_skills = ['Damage', 'Health', 'Shooting speed',
                               'Running speed']
        self.general_index = {'column': 0, 'row': 0}
        self.skill_index = {'column': 0, 'row': 0}
        self.switch_index = 0
        self.state = 'general'
        self.rows, self.cols = 2, 2

    def input(self):
        keys = pygame.key.get_just_pressed()
        if self.state == 'general':
            self.general_index['row'] = ((self.general_index['row']
                                         + int(keys[pygame.K_DOWN])
                                         - int(keys[pygame.K_UP]))
                                         % self.rows)
            self.general_index['column'] = ((self.general_index['column'] +
                                            int(keys[pygame.K_RIGHT]) -
                                            int(keys[pygame.K_LEFT]))
                                            % self.cols)
            if keys[pygame.K_RETURN]:
                self.state = self.general_options[
                    self.general_index['column'] +
                    2 * self.general_index['row']]

        elif self.state == 'Upgrade':
            self.skill_index['row'] = (self.skill_index['row'] +
                                       int(keys[pygame.K_DOWN]) -
                                       int(keys[pygame.K_UP])) % self.rows
            self.skill_index['column'] = (self.skill_index['column'] +
                                          int(keys[pygame.K_RIGHT]) -
                                          int(keys[pygame.K_LEFT])) % self.cols
            if keys[pygame.K_RETURN]:
                skill = self.general_skills[self.skill_index['column']
                                            + 2 * self.skill_index['row']]
                self.get_input(self.state, skill)
                self.state = 'general'

        elif self.state == 'Controls':
            self.get_input('Controls')
            self.switch_index = (self.switch_index + int(keys[pygame.K_DOWN])
                                 - int(keys[pygame.K_UP])) % len(self.keys)

        elif self.state == 'Stats':
            self.get_input('Stats')

        elif self.state == 'Exit':
            self.get_input('Exit')
            self.state = 'general'

        if keys[pygame.K_ESCAPE]:
            self.state = 'general'
            self.general_index = {'column': 0, 'row': 0}
            self.skill_index = {'column': 0, 'row': 0}
            self.switch_index = 0

    def quad_select(self, index, options):
        # bg
        rect = pygame.FRect(self.left + 40, self.top + 60, 400, 200)
        pygame.draw.rect(self.display_surface, COLORS['white'],
                         rect, 0, 4)
        pygame.draw.rect(self.display_surface, COLORS['gray'],
                         rect, 4, 4)

        # menu
        for col in range(self.cols):
            for row in range(self.rows):
                x = (rect.left + rect.width / (self.cols * 2) +
                     (rect.width / self.cols) * col)
                y = (rect.top + rect.height / (self.rows * 2) +
                     (rect.height / self.rows) * row)
                i = col + 2 * row
                color = COLORS['gray'] if (col == index['column'] and row ==
                                           index['row']) else COLORS['black']

                text_surface = self.font.render(options[i], True, color)
                text_rect = text_surface.get_rect(center=(x, y))
                self.display_surface.blit(text_surface, text_rect)

    def name_box(self):
        # bg
        rect = pygame.FRect(self.left, self.top, 250, 80)
        pygame.draw.rect(self.display_surface, COLORS['white'],
                         rect, 0, 4)
        pygame.draw.rect(self.display_surface, COLORS['gray'],
                         rect, 4, 4)

        # data
        name_surf = self.font.render(self.player.name, True, COLORS['black'])
        name_rect = name_surf.get_frect(
            topleft=rect.topleft + pygame.math.Vector2(rect.width * 0.05, 12))
        self.display_surface.blit(name_surf, name_rect)

    def controls(self):
        # bg
        rect = pygame.FRect(WINDOW_WIDTH / 2 - 300, 50, 600, 600)
        pygame.draw.rect(self.display_surface, COLORS['white'],
                         rect, 0, 4)
        pygame.draw.rect(self.display_surface, COLORS['gray'],
                         rect, 4, 4)

        v_offset = 0 if self.switch_index < self.visible_keys \
            else (-(self.switch_index - self.visible_keys + 1) *
                  rect.height / self.visible_keys)
        for i in range(len(self.keys)):
            x = rect.centerx
            y = (rect.top + rect.height / (self.visible_keys * 2)
                 + rect.height / self.visible_keys * i + v_offset)
            color = COLORS['gray'] \
                if i == self.switch_index else COLORS['black']

            name = self.keys[i]
            description = self.descriptions[i]
            icon_surf = self.key_icons[name]
            icon_rect = icon_surf.get_rect(center=(x - 150, y))

            text_surface = self.font.render(description, True, color)
            text_rect = text_surface.get_rect(midleft=(x - 50, y))

            if rect.collidepoint(text_rect.center):
                self.display_surface.blit(text_surface, text_rect)
                self.display_surface.blit(icon_surf, icon_rect)

    def stats(self):
        # bg
        rect = pygame.FRect(WINDOW_WIDTH / 2 - 250, 150, 500, 400)
        pygame.draw.rect(self.display_surface, COLORS['white'],
                         rect, 0, 4)
        pygame.draw.rect(self.display_surface, COLORS['gray'],
                         rect, 4, 4)

        # left side
        left_side_surf = self.player.still_image
        left_side_rect = left_side_surf.get_rect(
            center=(rect.x + 80, rect.centery))
        self.display_surface.blit(left_side_surf, left_side_rect)

        for i in range(len(self.general_skills)):
            x = rect.centerx
            y = rect.top + rect.height / (
                        4 * 2) + rect.height / 4 * i
            color = COLORS['black']

            name = self.general_skills[i]
            icon_surf = self.skill_icon[name]
            icon_rect = icon_surf.get_rect(center=(x - 50, y))

            text_surface = self.font.render(
                name + ': ' + str(self.player.stats[name]), True, color)
            text_rect = text_surface.get_rect(midleft=(x, y))

            self.display_surface.blit(text_surface, text_rect)
            self.display_surface.blit(icon_surf, icon_rect)

    def draw(self):
        if self.visible:
            match self.state:
                case 'general': self.quad_select(
                    self.general_index, self.general_options)
                case 'Upgrade': self.quad_select(
                    self.skill_index, self.general_skills)
                case 'Controls': self.controls()
                case 'Stats': self.stats()

            if self.state != 'Controls' and self.state != 'Stats':
                self.name_box()

    def update(self):
        self.input()
        self.stats()


class CoinCounter:
    def __init__(self, player, coins):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.coin_image = coins
        self.font = pygame.font.Font(join('data', 'font',
                                          'PublicPixel.ttf'), 20)

    def draw(self):
        rect = pygame.FRect(WINDOW_WIDTH - 100, 0, 100, 80)

        self.coin_font = pygame.font.Font(join('data', 'font',
                                               'PublicPixel.ttf'), 30)
        text_surf = self.coin_font.render(
            str(self.player.balance), True, COLORS['white'])
        text_rect = text_surf.get_frect(
            topright=rect.topright + pygame.math.Vector2(-10, 12))

        coin_surf = self.coin_image['MonedaD'][0]
        coin_rect = coin_surf.get_rect(
            topright=rect.topright + pygame.math.Vector2(-130, 12))

        self.display_surface.blit(coin_surf, coin_rect)
        self.display_surface.blit(text_surf, text_rect)


class HealthBar:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player_name = 'Player'
        self.player = player
        self.font = pygame.font.Font(join('data', 'font',
                                          'PublicPixel.ttf'), 20)

    def stats(self):
        # bg
        rect = pygame.FRect(0, 0, 250, 80)

        # data
        name_surf = self.font.render(
            self.player_name, True, COLORS['white'])
        name_rect = name_surf.get_frect(
            topleft=rect.topleft + pygame.math.Vector2(rect.width * 0.05, 12))
        self.display_surface.blit(name_surf, name_rect)

        # health bar
        health_rect = pygame.FRect(
            name_rect.left, name_rect.bottom + 10, rect.width * 0.9, 20)
        progress_rect_border = health_rect.inflate(4, 6)
        pygame.draw.rect(self.display_surface, COLORS['gray'], health_rect)
        pygame.draw.rect(self.display_surface, COLORS['white'],
                         progress_rect_border, 3)
        self.draw_bar(health_rect, self.player.health, self.player.max_health)

    def draw_bar(self, rect, value, max_value):
        ratio = rect.width / max_value
        progress_rect = pygame.FRect(
            rect.topleft, (value * ratio, rect.height))
        pygame.draw.rect(self.display_surface, COLORS['red'], progress_rect)

    def draw(self):
        self.stats()


class DeathScreen:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.background = pygame.Surface(
            self.display_surface.get_size(), pygame.SRCALPHA)
        self.background.convert()
        self.background.fill((0, 0, 0, 128))
        self.font = pygame.font.Font(join('data', 'font',
                                          'PublicPixel.ttf'), 26)
        self.game_over_surf = self.font.render(
            'Game Over', True, COLORS['red'])
        self.game_over_rect = self.game_over_surf.get_frect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.play_again_surf = self.font.render(
            'Press ESC to quit', True, COLORS['red'])
        self.play_again_rect = self.play_again_surf.get_frect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50))

    def draw(self):
        self.display_surface.blit(self.background, (0, 0))
        self.display_surface.blit(self.game_over_surf, self.game_over_rect)
        self.display_surface.blit(self.play_again_surf, self.play_again_rect)

        pygame.display.update()


class WinScreen:
    def __init__(self, score):
        self.score = score
        self.display_surface = pygame.display.get_surface()
        self.background = pygame.Surface(
            self.display_surface.get_size(), pygame.SRCALPHA)
        self.background.convert()
        self.background.fill((0, 0, 0, 128))
        self.font = pygame.font.Font(join('data', 'font',
                                          'PublicPixel.ttf'), 26)
        self.game_over_surf = self.font.render(
            'You won!', True, COLORS['green'])
        self.game_over_rect = self.game_over_surf.get_frect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.score_surf = self.font.render(
            "Score: " + str(self.score), True, COLORS['green'])
        self.score_rect = self.score_surf.get_frect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50))
        self.play_again_surf = self.font.render(
            'Press ESC to quit', True, COLORS['green'])
        self.play_again_rect = self.play_again_surf.get_frect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 100))

    def draw(self):
        self.display_surface.blit(self.background, (0, 0))
        self.display_surface.blit(self.game_over_surf, self.game_over_rect)
        self.display_surface.blit(self.score_surf, self.score_rect)
        self.display_surface.blit(self.play_again_surf, self.play_again_rect)

        pygame.display.update()


class TimerDisplay:
    def __init__(self, round):
        self.current_time = ROUND_DATA[round]['duration']
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(join('data', 'font',
                                          'PublicPixel.ttf'), 26)

    def draw(self):
        if self.current_time >= 0:
            self.display_time = self.current_time % 60

        self.text_surf = self.font.render(
            str(self.current_time), True, COLORS['white'])
        self.text_rect = self.text_surf.get_frect(
            midbottom=(WINDOW_WIDTH / 2, 0 + 50))
        pygame.draw.rect(self.display_surface,
                         COLORS['white'],
                         self.text_rect.inflate(20, 20).move(0, 0), 5, 10)
        self.display_surface.blit(self.text_surf, self.text_rect)


class WelcomeScreen:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.background = pygame.Surface(
            self.display_surface.get_size(), pygame.SRCALPHA)
        self.background.convert()
        self.background.fill((0, 0, 0, 128))
        self.font = pygame.font.Font(join('data', 'font',
                                          'PublicPixel.ttf'), 26)

    def draw(self):
        self.welcome_surf = self.font.render(
            'Press "E" to open menu', True, COLORS['white'])
        self.welcome_rect = self.welcome_surf.get_frect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100))
        self.display_surface.blit(self.background, (0, 0))
        self.display_surface.blit(self.welcome_surf, self.welcome_rect)
