import random
import pygame
import math

import geometry
import constants as const


class BrickGrid:
    def __init__(self):
        empty_horizontal_space = const.SCREEN_WIDTH - (2 + const.NUM_COLUMNS) * const.BRICK_WIDTH
        brick_horizontal_space = empty_horizontal_space / const.NUM_COLUMNS

        empty_vertical_space = const.SCREEN_HEIGHT / 2 - const.NUM_ROWS * const.BRICK_WIDTH
        brick_vertical_space = empty_vertical_space / const.NUM_ROWS

        self.bullet_set = set()
        self.brick_set = set()

        for i in range(const.NUM_COLUMNS):
            for j in range(const.NUM_ROWS):
                brick_x = (i + 1) * (brick_horizontal_space + const.BRICK_WIDTH)
                brick_y = (j + 1) * (brick_vertical_space + const.BRICK_HEIGHT)
                rect = geometry.Rect(brick_x, brick_y, const.BRICK_WIDTH, const.BRICK_HEIGHT)
                self.brick_set.add(rect)

        self.original_brick_count = len(self.brick_set)

    def get_num_cleared(self):
        return self.original_brick_count - len(self.brick_set)

    def reset(self):
        self.bullet_set = set()

    def render(self, screen):
        for b in self.brick_set:
            pygame.draw.rect(screen, const.GREEN, [b.x, b.y, b.width, b.height])

        for b in self.bullet_set:
            pygame.draw.rect(screen, const.GREY, [b.x, b.y, b.width, b.height])

    def interact(self):
        if random.uniform(0.0, 1.0) < const.PERCENT_BULLET:
            candidates = [
                b for b in self.brick_set if
                not any([other.x == b.x and other.y > b.y for other in self.brick_set])
            ]
            fires_bullet = random.choice(candidates)
            bullet_x = fires_bullet.x + (b.width + const.BULLET_WIDTH) / 2
            bullet_y = fires_bullet.y + b.height
            self.bullet_set.add(geometry.Rect(bullet_x, bullet_y, const.BULLET_WIDTH, const.BULLET_HEIGHT))

        remove_set = set()
        for b in self.bullet_set:
            b.y += const.BULLET_SPEED
            if b.y >= const.SCREEN_HEIGHT:
                remove_set.add(b)

        self.bullet_set -= remove_set
        return True


class Paddle:
    def __init__(self):
        x = const.SCREEN_WIDTH / 2
        y = const.SCREEN_HEIGHT - const.PADDLE_HEIGHT - const.PADDLE_SPACING
        self.rect = geometry.Rect(x, y, const.PADDLE_WIDTH, const.PADDLE_HEIGHT)
        self.speed = const.PADDLE_SPEED

    def interact(self):
        if pygame.key.get_pressed()[pygame.K_LEFT] != 0:
            self.rect.x -= self.speed
        if pygame.key.get_pressed()[pygame.K_RIGHT] != 0:
            self.rect.x += self.speed
        return True

    def render(self, screen):
        pygame.draw.rect(screen, const.RED, [self.rect.x, self.rect.y, self.rect.width, self.rect.height])

    def get_angle_for_x(self, x):
        '''
            TODO - currently all collisions are 45 degrees which is a bit boring

            With this code, depending on point of contact, rotation angle will
            vary between min and max angle
        '''
        x = float(x)
        delta = x - self.rect.x
        percentage_of_paddle = delta / self.rect.width

        degree_range = const.PADDLE_MAX_ANGLE - const.PADDLE_MIN_ANGLE
        angle = degree_range * percentage_of_paddle + const.PADDLE_MIN_ANGLE

        print 'For x={} in range {}/{}, got angle={}'.format(x, self.rect.x, self.rect.max_x, angle)
        return angle


class Ball:
    def __init__(self):
        self.radius = const.BALL_RADIUS
        self.speed = const.BALL_SPEED
        self.x = random.randint(0, const.SCREEN_WIDTH)
        self.y = const.SCREEN_HEIGHT - const.PADDLE_HEIGHT - const.PADDLE_SPACING - 4 * const.BALL_RADIUS
        self.heading = (random.choice([-0.5, 0.5]), -0.5)
        self.min_x = 0 + const.BALL_RADIUS
        self.max_x = const.SCREEN_WIDTH - const.BALL_RADIUS
        self.min_y = 0 + const.BALL_RADIUS
        self.max_y = const.SCREEN_HEIGHT
        self.paddle_y = const.SCREEN_HEIGHT - const.PADDLE_HEIGHT - const.PADDLE_SPACING - const.BALL_RADIUS

    def line_of_movement(self):
        current = self.x, self.y
        prev = self.x - int(const.BALL_SPEED * self.heading[0]), self.y - int(const.BALL_SPEED * self.heading[1])
        return (prev, current)

    def interact(self):
        self.x += int(const.BALL_SPEED * self.heading[0])
        self.y += int(const.BALL_SPEED * self.heading[1])

        if self.y >= self.max_y:
            return False

        return True

    def rotate(self, angle):
        theta = float(angle) * math.pi / 180.0
        x, y = self.heading
        new_x = x * math.cos(theta) - y * math.sin(theta)
        new_y = x * math.sin(theta) + y * math.cos(theta)
        self.heading = (new_x, new_y)

    def render(self, screen):
        pygame.draw.circle(screen, const.BLUE, (self.x, self.y), self.radius)


def collision_check(ball, paddle, brick_grid):
    if ball.x <= ball.min_x or ball.x >= ball.max_x:
        ball.heading = (-ball.heading[0], ball.heading[1])
    if ball.y <= ball.min_y:
        ball.heading = (ball.heading[0], -ball.heading[1])
    if paddle.rect.intersect(ball.line_of_movement(), const.BALL_RADIUS) != geometry.Intersection.NONE:
        ball.heading = (ball.heading[0], -ball.heading[1])
        ball.interact()

    for brick in brick_grid.brick_set:
        intersection = brick.intersect(ball.line_of_movement(), const.BALL_RADIUS)
        if intersection == geometry.Intersection.HORIZONTAL:
            ball.heading = (ball.heading[0], -ball.heading[1])
        elif intersection == geometry.Intersection.VERTICAL:
            ball.heading = (-ball.heading[0], ball.heading[1])

        if intersection != geometry.Intersection.NONE:
            brick_grid.brick_set.remove(brick)
            break

    for bullet in brick_grid.bullet_set:
        if bullet.y >= paddle.rect.y and bullet.x >= paddle.rect.x and bullet.x <= paddle.rect.max_x:
            return False

    return True
