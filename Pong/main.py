import random
import pygame
from pygame.locals import *
from config import Config

class Player:
    def __init__(self, config, type_):
        self.cfg = config
        self.type_ = type_
        self.width = 15
        self.height = 60
        self.reset()

    def reset(self):
        if self.type_ == 'LEFT':
            self.x = 0
            self.y = (self.cfg.SCREENSIZE[1] - self.height) // 2
        else:
            self.x = (self.cfg.SCREENSIZE[0] - self.width)
            self.y = (self.cfg.SCREENSIZE[1] - self.height) // 2

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # speed
        self.speed = 5

    def move(self, direction):
        if direction == 'UP':
            self.y = max(0, self.y - self.speed)
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        elif direction == 'DOWN':
            self.y = min(self.cfg.SCREENSIZE[1] - self.height, self.y + self.speed)
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        if self.type_ == 'LEFT':
            pygame.draw.rect(surface,self.cfg.BLUE, self.rect)
        else:
            pygame.draw.rect(surface, self.cfg.RED, self.rect)

class Ball:
    def __init__(self, config):
        self.cfg = config
        self.radius = 7
        self.reset()

    def reset(self):
        self.x = (self.cfg.SCREENSIZE[0]-self.radius)//2
        self.y = (self.cfg.SCREENSIZE[1]-self.radius)//2
        self.rect = pygame.Rect(self.x, self.y, 2*self.radius, 2*self.radius)

        self.direction_x = random.choice([1, -1])
        self.direction_y = random.choice([1, -1])

        self.speed = 3

    def move(self, player_left, player_right):
        self.x = self.x + self.speed * self.direction_x
        self.y = self.y - self.speed * self.direction_y

        self.rect = pygame.Rect(self.x, self.y, 2 * self.radius, 2 * self.radius)

        if self.rect.colliderect(player_left) or self.rect.colliderect(player_right):
            self.direction_x = -self.direction_x
            self.speed += 0.2

        elif self.y <= 0:
            self.direction_y = -self.direction_y

        elif self.y >= self.cfg.SCREENSIZE[1] - self.radius:
            self.direction_y = -self.direction_y

        elif self.x <=0:
            self.reset()
        elif self.x >=self.cfg.SCREENSIZE[0] - self.radius:
            self.reset()

    def draw(self, surface):
        pygame.draw.circle(surface, self.cfg.WHITE, (self.x, self.y), self.radius)


class App:
    def __init__(self, config):
        self._running = True
        self._display_surf = None
        self.cfg = config
        self.player_left = Player(self.cfg, 'LEFT')
        self.player_right = Player(self.cfg, 'RIGHT')
        self.ball = Ball(self.cfg)


    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.cfg.SCREENSIZE, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.mouse.set_visible(0)
        pygame.display.set_caption(self.cfg.TITLE)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False


    def on_loop(self):

        self.ball.move(self.player_left, self.player_right)
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_w]:
            self.player_left.move('UP')
        elif pressed_keys[pygame.K_s]:
            self.player_left.move('DOWN')

        if pressed_keys[pygame.K_UP]:
            self.player_right.move('UP')
        elif pressed_keys[pygame.K_DOWN]:
            self.player_right.move('DOWN')



    def on_render(self):
        clock = pygame.time.Clock()
        self._display_surf.fill(self.cfg.BLACK)
        self.player_left.draw(self._display_surf)
        self.player_right.draw(self._display_surf)
        self.ball.draw(self._display_surf)
        pygame.display.flip()
        clock.tick(60)

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App(Config)
    theApp.on_execute()