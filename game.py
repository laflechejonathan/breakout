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

    if pygame.key.get_pressed()[pygame.K_q] != 0:
        sys.exit()

def wait_for_key(key):
    while pygame.key.get_pressed()[key] != 0:
        quit_check()
    while pygame.key.get_pressed()[key] == 0:
        quit_check()
    while pygame.key.get_pressed()[key] != 0:
        quit_check()


def show_text(text, bg, fg):
    screen.fill(bg)
    game_over_text = font.render(text, 1, fg)
    text_position = ((const.SCREEN_WIDTH - game_over_text.get_width()) / 2, const.SCREEN_HEIGHT / 2)
    screen.blit(game_over_text, text_position)
    pygame.display.flip()
    wait_for_key(pygame.K_RETURN)


def show_game_over():
    show_text("Game Over! Press [Enter] to try again.", const.BLACK, const.RED)


def show_victory():
    show_text("Victory is yours! Press [Enter] to play again.", const.BLUE, const.BLACK)


def play_single_game():
    paddle = breakout.Paddle()
    ball = breakout.Ball()
    brick_grid = breakout.BrickGrid()

    while True:
        quit_check()

        # space bar pauses the game
        if pygame.key.get_pressed()[pygame.K_SPACE] != 0:
            wait_for_key(pygame.K_SPACE)

        if not all([
            paddle.interact(),
            ball.interact(),
            brick_grid.interact(),
            breakout.collision_check(ball, paddle, brick_grid),
        ]):
            # game over
            return False

        if not brick_grid.brick_set:
            return True

        screen.fill(const.BLACK)
        paddle.render(screen)
        ball.render(screen)
        brick_grid.render(screen)
        pygame.display.flip()


def main_loop():
    while True:
        if play_single_game():
            show_victory()
        else:
            show_game_over()


if __name__ == '__main__':
    main_loop()
