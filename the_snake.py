import sys
from random import randint, choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Центр поля (для змейки)
MIDDLE = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2


class GameObject:
    """Базовый класс.

    хранит начальные метод move - метод прорисовки,
    данный метод используется в классах:
    Apple
    Snake
    """

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR, position=MIDDLE):
        self.position = position
        self.body_color = body_color

    def draw(self, position, new_color=None):
        """Отрисовка квадратика"""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        color = new_color if new_color else self.body_color

        pygame.draw.rect(screen, color, rect)
        if not new_color:
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки.

    Наследуется от GameObject.
    Наследует метод draw.

    Добавлены методы:
    update_direction(след. позиция)
    move(перемещение)
    get_head_position(получение головы)
    reset(сбросс)
    """

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.next_direction = None
        self.reset()

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод перемещения змейки."""
        head = self.get_head_position()
        x, y = self.direction
        new_head = (
            (head[0] + x * GRID_SIZE) % SCREEN_WIDTH,
            (head[-1] + y * GRID_SIZE) % SCREEN_HEIGHT)
        self.last = self.positions.pop(-1)
        self.positions.insert(0, new_head)

    def draw(self):
        """Отрисовка змейки"""
        super().draw(self.positions[0])

        if self.last:
            super().draw(self.last, BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Возвращает позицую головы змеи."""
        return self.positions[0]

    def reset(self):
        """Сбросс до начального состояния."""
        self.positions = [MIDDLE]
        self.direction = choice((RIGHT, LEFT, UP, DOWN))
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.last = None


class Apple(GameObject):
    """
    Класс предназначен для хранения параметров
    яблока и его логики.
    """

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)

    def randomize_position(self, snake_pos):
        """Метод случайного появления яблока."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in snake_pos:
                break

    def draw(self):
        """Вызов родительского метода
        для отрисовки яблока
        """
        super().draw(self.position)


def handle_keys(game_object):
    """Функция движения змейки."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit([0])
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция."""
    # Инициализация PyGame:
    pygame.init()

    # Инициализация классов
    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake.positions)
    while True:
        clock.tick(SPEED)
        if snake.get_head_position() == apple.position:
            apple.randomize_position(snake.positions)
            snake.positions.append(snake.positions[-1])

        for snake_part in snake.positions[2:]:
            if snake.positions[0] == snake_part:
                snake.reset()

        pygame.display.update()
        handle_keys(snake)
        snake.update_direction()
        snake.draw()
        apple.draw()
        snake.move()


if __name__ == '__main__':
    main()
