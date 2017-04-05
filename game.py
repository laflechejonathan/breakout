# -*- coding: utf-8 -*-

import sys
import pygame

import constants as const
import breakout

pygame.init()
screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
bigFont = pygame.font.SysFont('Helvetica', 20)
smallFont = pygame.font.SysFont('Helvetica', 15)


def quit_check():
    if any(e.type == pygame.QUIT for e in pygame.event.get()):
        sys.exit()

    if pygame.key.get_pressed()[pygame.K_q] != 0:
        sys.exit()


def wait_for_key(key):
    while pygame.key.get_pressed()[key] != 0:
        quit_check()
    while pygame.key.get_pressed()[key] == 0:
        quit_check()
    while pygame.key.get_pressed()[key] != 0:
        quit_check()


def show_text(text, fg):
    rendered_text = bigFont.render(text, 1, fg)
    text_position = ((const.SCREEN_WIDTH - rendered_text.get_width()) / 2, const.SCREEN_HEIGHT / 2)
    screen.blit(rendered_text, text_position)
    pygame.display.flip()


def show_game_over():
    screen.fill(const.BLACK)
    show_text("Game Over! Press [Enter] to try again.", const.RED)
    wait_for_key(pygame.K_RETURN)


def show_victory():
    screen.fill(const.BLUE)
    show_text("Victory is yours! Press [Enter] to play again.", const.BLACK)
    wait_for_key(pygame.K_RETURN)


class SingleGame():

    def __init__(self):
        self.paddle = breakout.Paddle()
        self.ball = breakout.Ball()
        self.brick_grid = breakout.BrickGrid()
        self.lives = const.LIVES
        self.level = 1
        self.base_score = 0

    def lose_life(self):
        self.lives -= 1
        show_text(u"(×_×) Careful... Press [Space] to keep going.", const.WHITE)
        wait_for_key(pygame.K_SPACE)
        self.paddle = breakout.Paddle()
        self.brick_grid.reset()
        self.ball = breakout.Ball()

    def clear_level(self):
        self.base_score += self.compute_score()
        self.level += 1
        show_text(u"Level Cleared! Press [Space] to continue.", const.WHITE)
        wait_for_key(pygame.K_SPACE)
        self.paddle = breakout.Paddle()
        self.brick_grid = breakout.BrickGrid()
        self.ball = breakout.Ball()

    def render_info(self):
        texts = [
            "Level: {}".format(self.level),
            "Lives: {}".format(self.lives),
            "Score:{}".format(self.compute_score()),
        ]
        for i, t in enumerate(texts):
            rendered = smallFont.render(t, 1, const.WHITE)
            text_position = (10, 10 + 20 * i)
            screen.blit(rendered, text_position)

    def compute_score(self):
        return self.base_score + self.level * self.brick_grid.get_num_cleared() * 10

    def play(self):
        while True:
            quit_check()

            # space bar pauses the game
            if pygame.key.get_pressed()[pygame.K_SPACE] != 0:
                wait_for_key(pygame.K_SPACE)

            if not all([
                self.paddle.interact(),
                self.ball.interact(),
                self.brick_grid.interact(),
                breakout.collision_check(self.ball, self.paddle, self.brick_grid),
            ]):
                if self.lives == 0:
                    # game over
                    return False
                else:
                    self.lose_life()


            screen.fill(const.BLACK)
            self.paddle.render(screen)
            self.brick_grid.render(screen)
            self.render_info()
            self.ball.render(screen)
            pygame.display.flip()

            if not self.brick_grid.brick_set:
                self.clear_level()


def main_loop():
    while True:
        if SingleGame().play():
            show_victory()
        else:
            show_game_over()


if __name__ == '__main__':
    main_loop()
