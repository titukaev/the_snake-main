from random import choice, randint

import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 10

CENTRAL_POSITION = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject:
    """Родительский класс для игровых объектов."""

    def __init__(
            self,
            body_color=None,
            position=CENTRAL_POSITION
    ):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод для отрисовки объектов в дочерних классах."""
        raise NotImplementedError(
            'Определите draw в %s.' % (self.__class__.__name__))

    @staticmethod
    def draw_grid(
        surface,
        coordinates,
        color,
        size=GRID_SIZE,
        border_color=BORDER_COLOR,
        line_width=1
    ):
        """Метод для отрисовки квадратов."""
        rect = pygame.Rect(
            coordinates,
            (size, size)
        )
        pygame.draw.rect(
            surface,
            color,
            rect
        )
        pygame.draw.rect(
            surface,
            border_color,
            rect,
            line_width
        )


class Apple(GameObject):
    """Класс, который создает игровой объект - яблоко
    и задает его позицию на игровом поле.
    """

    def randomize_position(
            self,
            forbidden_position=()
    ):
        """Задает позицию яблока на игровом поле."""
        self.position = (randint(0, GRID_WIDTH - GRID_SIZE) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - GRID_SIZE) * GRID_SIZE)
        while self.position in forbidden_position:
            self.position = self.randomize_position()
        if len(forbidden_position) == GRID_WIDTH * GRID_HEIGHT:
            self.snake = Snake()
            self.snake.reset()

    def __init__(
            self,
            body_color=APPLE_COLOR
    ):
        self.body_color = body_color
        self.randomize_position()

    def draw(
            self,
            surface
    ):
        """Отрисовывает яблоко на игровой поверхности."""
        self.draw_grid(
            surface,
            self.position,
            self.body_color
        )


class Snake(GameObject):
    """Класс, который отвечает за создание игрового объекта - змейки
    и ее движение по игровому полю.
    """

    def __init__(
            self,
            body_color=SNAKE_COLOR,
            position=CENTRAL_POSITION
    ):
        super().__init__(body_color, position)
        self.reset()
        self.direction = RIGHT

    def update_direction(self):
        """Обновляет движение змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
            self.last = None

    def reset(self):
        """Метод возвращает змейку в начальное состояниие"""
        self.length = 1
        self.positions = [CENTRAL_POSITION]
        self.direction = choice([LEFT, RIGHT, UP, DOWN])
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Метод возвращает текущее положение головы змейки."""
        return self.positions[0]

    def move(self):
        """Метод отвечает за движение змейки."""
        head_position = self.get_head_position()
        new_head_position = [head_position[0] + self.direction[0] * GRID_SIZE,
                             head_position[1] + self.direction[1] * GRID_SIZE]
        if new_head_position[0] < 0:
            new_head_position[0] = 620
        elif new_head_position[0] > 620:
            new_head_position[0] = 0
        elif new_head_position[1] < 0:
            new_head_position[1] = 460
        elif new_head_position[1] > 460:
            new_head_position[1] = 0
        new_head_position = tuple(new_head_position)
        if new_head_position in self.positions[2:]:
            self.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        else:
            self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self,
             surface
             ):
        """Метод отвечает за отрисовку змейки и отрисовку движения."""
        self.draw_grid(
            surface,
            self.positions[0],
            self.body_color
        )
        if self.last:
            self.draw_grid(
                surface,
                self.last,
                color=BOARD_BACKGROUND_COLOR,
                border_color=BOARD_BACKGROUND_COLOR
            )


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif (event.key == pygame.K_DOWN
                    and game_object.direction != UP):
                game_object.next_direction = DOWN
            elif (event.key == pygame.K_LEFT
                    and game_object.direction != RIGHT):
                game_object.next_direction = LEFT
            elif (event.key == pygame.K_RIGHT
                    and game_object.direction != LEFT):
                game_object.next_direction = RIGHT


def main():
    """Создание игровых объектов и основной цикл игры."""
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
