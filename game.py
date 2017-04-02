import sys
import pygame

import constants as const
import breakout

pygame.init()
screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
font = pygame.font.Font(None, 30)


def quit_check():
    if any(e.type == pygame.QUIT for e in pygame.event.get()):
        sys.exit()


def wait_for_enter():
    while True:
        quit_check()
        if pygame.key.get_pressed()[pygame.K_RETURN] != 0:
            break


def show_game_over():
    screen.fill(const.BLACK)
    game_over_text = font.render("Game Over! Press [Enter] to try again.", 1, const.RED)
    text_position = ((const.SCREEN_WIDTH - game_over_text.get_width()) / 2, const.SCREEN_HEIGHT / 2)
    screen.blit(game_over_text, text_position)
    pygame.display.flip()
    wait_for_enter()


def play_single_game():
    paddle = breakout.Paddle()
    ball = breakout.Ball()
    brick_grid = breakout.BrickGrid()

    while True:
        quit_check()

        if not all([
            paddle.interact(),
            ball.interact(),
            brick_grid.interact(),
            breakout.collision_check(ball, paddle, brick_grid),
        ]):
            # game over
            return

        screen.fill(const.BLACK)
        paddle.render(screen)
        ball.render(screen)
        brick_grid.render(screen)
        pygame.display.flip()


def main_loop():
    while True:
        play_single_game()
        show_game_over()


if __name__ == '__main__':
    main_loop()
