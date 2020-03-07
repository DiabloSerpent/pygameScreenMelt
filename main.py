import pygame
import random

pygame.init()

SCREENSIZE = (800, 600)
SCREEN = pygame.display.set_mode(SCREENSIZE)
BACKGROUND_SCREEN = pygame.Surface(SCREENSIZE)
BACKGROUND_SCREEN.fill((0, 0, 0))
BOUNDS = pygame.Rect((0, 0), SCREENSIZE)
TIME = pygame.time.Clock()

YELLOW = pygame.Color("yellow")
RED = pygame.Color("red")
GRAY = pygame.Color("gray21")


# This was imported from the testPygame project
class Message:
    def __init__(self, msg, size=60):
        self.font = pygame.font.Font(None, size)
        self.msg = msg
        self.rect = pygame.Rect((0, 0), self.font.size(msg))
        self.image = pygame.Surface((0, 0))

    def create_image(self, text, background):
        self.image = self.font.render(self.msg, 0, text, background)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# Spice up the melt effect with some text
title = Message("DOOM", 150)
title.create_image(GRAY, RED)
title.rect.center = BOUNDS.center
title.rect.move_ip(0, -150)

old_screen = pygame.Surface(SCREENSIZE)
old_screen.fill(RED)
title.draw(old_screen)

new_screen = pygame.Surface(SCREENSIZE)
new_screen.fill(YELLOW)


class ScreenMelter(pygame.sprite.Sprite):
    INITIAL_DELAY = 4 * 60
    MAX_OFFSET = 130
    MELT_SPEED = 4
    MAX_TICKS = (SCREENSIZE[1] + MAX_OFFSET + INITIAL_DELAY) // MELT_SPEED

    def __init__(self, old_surf, new_surf):
        super().__init__()
        self.old = old_surf
        global BACKGROUND_SCREEN
        BACKGROUND_SCREEN = new_surf
        self.offsets = []
        self.columns = []
        cls = self.__class__
        temp_old_screen = old_surf.copy()
        column = pygame.Surface((1, SCREENSIZE[1]))
        for x in range(SCREENSIZE[0]):
            # Get a random offset for each column
            offset = -random.randint(0, cls.MAX_OFFSET) - cls.INITIAL_DELAY
            self.offsets.append(offset)
            # Get the column as a surface
            column.blit(temp_old_screen, (0, 0))
            temp_old_screen.scroll(-1, 0)
            self.columns.append(column.copy())

    def update(self):
        cls = self.__class__
        # Shift the columns downward
        for x in range(len(self.offsets)):
            self.offsets[x] += cls.MELT_SPEED

    def draw(self, screen):
        for x in range(SCREENSIZE[0]):
            if self.offsets[x] < 0:
                # Ignore offset if it is negative, this also creates
                # the delay effect.
                screen.blit(self.columns[x], (x, 0))
            else:
                screen.blit(self.columns[x], (x, self.offsets[x]))


melter = ScreenMelter(old_screen, new_screen)

stop = False

for _ in range(ScreenMelter.MAX_TICKS):
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            stop = True
    if stop:
        break
    # Reset screen
    SCREEN.blit(BACKGROUND_SCREEN, (0, 0))
    melter.update()
    melter.draw(SCREEN)
    pygame.display.flip()
    TIME.tick(60)
