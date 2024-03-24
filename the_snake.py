from random import randint, choice

import pygame

# Инициализация PyGame:
pygame.init()

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
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:

    def __init__(self, body_color=(255, 255, 255)):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color
        self.last = None


    def draw(self):
        pass


class Apple(GameObject):
    
    def __init__(self, body_color=(255, 0, 0)):
        super().__init__(body_color)
        self.position = self.randomize_position()

        
    def randomize_position(self):
        position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
      
        print(position)
        return position
    
    """Прорисовка яблока""" 
    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


class Snake(GameObject):
    
    def __init__(self, body_color=(0, 255, 0)):
        super().__init__(body_color)
        self.positions = [(self.position)]
        self.length = len(self.positions)
        self.direction = RIGHT
        self.next_direction = None
        
    """Метод обновления направления после нажатия на кнопку"""
    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        head = self.get_head_position()
        if self.direction == RIGHT:
            new_head = (head[0] + GRID_SIZE, head[-1])
            self.last = self.positions.pop(-1)
            if new_head[0] > 620:
                new_head = (0, head[-1])
            
        elif self.direction == LEFT:
            new_head = (head[0] - GRID_SIZE, head[-1])
            self.last = self.positions.pop(-1)
            if new_head[0] < 0:
                new_head = (620, head[-1])
            
        elif self.direction == UP:
            new_head = (head[0], head[-1] - GRID_SIZE)
            self.last = self.positions.pop(-1)
            if new_head[-1] < 0:
                new_head = (head[0], 460)
            
        elif self.direction == DOWN:
            new_head = (head[0], head[-1] + GRID_SIZE)
            self.last = self.positions.pop(-1)
            if new_head[-1] > 460:
                new_head = (head[0], 0)

        self.positions.insert(0, new_head)
        head = new_head

    """прорисовка змейки"""
    def draw(self):
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        self.positions = [(self.position)]
        self.length = len(self.positions)
        self.direction = RIGHT
        self.next_direction = None
        screen.fill(BOARD_BACKGROUND_COLOR)

        
def main():
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        def handle_keys(game_object):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and game_object.direction != DOWN:
                        game_object.next_direction = UP
                    elif event.key == pygame.K_DOWN and game_object.direction != UP:
                        game_object.next_direction = DOWN
                    elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                        game_object.next_direction = LEFT
                    elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                        game_object.next_direction = RIGHT

        if snake.positions[0] == apple.position:
            apple.last == apple.position
            apple.position = apple.randomize_position()
            snake.positions.append(snake.positions[-1])
    
        for snake_part in snake.positions:
            if apple.position == snake_part:
                apple.randomize_position()
       
        for snake_part in snake.positions[2:]:
            if snake.positions[0] == snake_part:
                snake.reset()

        pygame.display.update()
        handle_keys(snake)
        snake.update_direction()
        apple.draw()
        snake.move()
        snake.draw()


if __name__ == '__main__':
    main()
