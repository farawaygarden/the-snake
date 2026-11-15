from random import randint

import pygame

# Константы для размеров поля и сетки.
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения.
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный.
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки.
BORDER_COLOR = (93, 216, 228)

# Цвет яблока.
APPLE_COLOR = (255, 0, 0)

# Цвет змейки.
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки.
SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()


class GameObject:
    """Описание основных классов игры"""

    # Инициализация параметров и атрибутов родительского класса.
    def __init__(self, surface=None, color=None):
        self.surface = surface
        self.color = color
        self.position = None
        self.body_color = self.color

    def draw(self):
        """Создали пустой метод отрисовки объектов класса"""
        pass


class Apple(GameObject):
    """Класс "яблоко".
    Задается генерация случайной позиции, отрисовка объекта
    """

    def __init__(self, surface=None, x=0, y=0):
        """Импортированы из родительского класса
        и заданы параметры и атрибуты яблока
        """
        super().__init__(surface, APPLE_COLOR)
        self.x = x
        self.y = y
        self.position = (x, y)
        self.body_color = APPLE_COLOR

    def randomize_position(self, snake_positions):
        """Генерация яблока в случайном положении.
        Проверка того, чтобы яблоко не появлялось внутри змейки
        """
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            position = (x, y)
            if position not in snake_positions:
                self.x, self.y = position
                self.position = position
                return

    def draw(self):
        """Отрисовывание яблока"""
        rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(self.surface, self.color, rect)
        pygame.draw.rect(self.surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс Snake
    Фиксируется позиция головы змейки, заданы движения, 'поглощение' яблока
    """

    def __init__(self, surface=None, start_x=0, start_y=0):
        """Инициализация параметров и атрибутов дочернего класса:
        импорт из родительского класса, определение собственных
        """
        super().__init__(surface, SNAKE_COLOR)
        self.length = 1
        self.positions = [(start_x, start_y)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.last = None

        self.position = (start_x, start_y)

        self.body_color = SNAKE_COLOR

    def get_head_position(self):
        """Позиция головы змейки"""
        return self.positions[0]

    def move(self):
        """Метод фиксирует координаты движения змейки
        с учетом ее способности уходить за стенки и
        появляться с другой стороны,
        добавляет 'поглощенное' яблоко
        """
        self.update_direction()
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        self.last = self.positions[-1]
        self.positions.insert(0, new_head)
        self.position = new_head

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывание змейки по каждому блоку"""
        for position in self.positions:
            rect = pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(self.surface, self.color, rect)
            pygame.draw.rect(self.surface, BORDER_COLOR, rect, 1)

    def update_direction(self):
        """Обновление позиции змейки во время движения"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Сброс змейки в начальное состояние"""
    start_x = (GRID_WIDTH // 2) * GRID_SIZE
    start_y = (GRID_HEIGHT // 2) * GRID_SIZE


def handle_keys(game_object):
    """Глобальная функция связывает действия игрока
    с реакциями игры
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
    return True


def main():
    """Сборка игры.
    Параметры игровой области, название, центральная стартовая позиция змейки,
    инициализация задействованных классов,
    описание механики движения по нажатию клавиши
    """
    pygame.init()

    start_x = (GRID_WIDTH // 2) * GRID_SIZE
    start_y = (GRID_HEIGHT // 2) * GRID_SIZE

    snake = Snake(screen, start_x, start_y)
    apple = Apple(
        screen, randint(0, GRID_WIDTH - 1) * GRID_SIZE,
        randint(0, GRID_HEIGHT - 1) * GRID_SIZE
    )

    running = True
    while running:
        # Передаем snake в функцию
        if not handle_keys(snake):
            running = False

        snake.move()

        if snake.get_head_position() == (apple.x, apple.y):
            snake.length += 1
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.flip()
        clock.tick(SPEED)

    pygame.quit()


if __name__ == '__main__':
    main()
