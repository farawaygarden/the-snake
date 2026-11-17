from random import randint

import pygame as pg

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

DIRECTIONS = {
    (UP, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_LEFT): LEFT,
    (DOWN, pg.K_RIGHT): RIGHT,
    (LEFT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_UP): UP,
    (RIGHT, pg.K_DOWN): DOWN
}

# Константы для цвета.
# Цвет фона - черный.
BOARD_BACKGROUND_COLOR = (0, 0, 0)
# Цвет границы ячейки.
BORDER_COLOR = (93, 216, 228)
# Цвет яблока.
APPLE_COLOR = (255, 0, 0)
# Цвет змейки.
SNAKE_COLOR = (0, 255, 0)
# Ошибка
ERROR_COLOR = (255, 0, 255)

# Скорость движения змейки.
SPEED = 10

# Центр игрового поля.
CENTER = ((GRID_WIDTH // 2) * GRID_SIZE, (GRID_HEIGHT // 2) * GRID_SIZE)

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pg.time.Clock()


class GameObject:
    """Содержание родительского класса для игры.

    Атрибуты:
    position (tuple): координаты.
    color (tuple): цвет объекта.
    body_color (tuple): цвет тела объекта.

    Методы:
    draw_rect(position, color=None): рисует один закрашенный
    квадрат по координатам
    draw(): напоминание о необходимости реализовать
    метод draw в дочерних классах.
    """

    def __init__(self, color=ERROR_COLOR):
        self.position = CENTER
        self.body_color = color

    def draw_rect(self, position, color=None):
        """Отрисовка одного блока игрового объекта.

        Args:
        position (tuple): координаты.
        color (tuple): цвет заливки. Если не указан, используется body_color.

        Эффект:
        Рисует прямоугольник на глобальном экране screen.
        """
        color = color or self.body_color
        rect = pg.Rect(*position, GRID_SIZE, GRID_SIZE)
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Функция выводит сообщение об ошибке,
        если фунция draw пропущена в дочерних классах.
        """
        raise NotImplementedError(
            'Метод draw не реализован в классе Apple или Snake'
        )


class Apple(GameObject):
    """Определение дочернего класса Apple.

    Отвечает за генерацию случайной позиции яблока в игре,
    проверяет, что позиция не совпадает с телом змейки,
    закрашивает яблоко.

    Аргументы:
    forbidden_positions (list): список координат,
    где яблоко не может появиться.

    Методы:
    randomize_position(): подбирает случайные координаты для яблока
    с учетом ограничений.
    draw(): отрисовывает яблоко.
    """

    def __init__(self, forbidden_positions=None):
        super().__init__(APPLE_COLOR)
        self.randomize_position(forbidden_positions or [])

    def randomize_position(self, forbidden_positions):
        """Генерация случайной позиции для яблока.

        Метод подбирает случайные координаты с учетом ограничений,
        указанных в self.forbidden_positions.
        """
        while self.position in forbidden_positions:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            pass

    def draw(self):
        """Отрисовывание яблока."""
        self.draw_rect(self.position, APPLE_COLOR)


class Snake(GameObject):
    """Определение дочернего класса Snake

    Отвечает за появление объекта змейка, ее движение в различных направлениях,
    поглощение яблока с увеличением тела,
    выделение элемента, позволяющего избавиться от эффекта шлейфа.

    Аргументы:
    length (int): длина (число сегментов).
    positions (list): список кортежей с координатами объекта.
    direction (tuple): текущее направление движения.
    next_direction (tuple): следующее направление движения.
    last (tuple | None): координаты последнего удаленного сегмента.

    Методы:
    get_head_position(): декоратор, возвращает координаты головы змейки.
    update_direction(): функция задает новое направление движения змейки.
    move(): обновляет позицию змейки, добавляет голову, удаляет шлейф.
    eat(): обновляет длину змейки при поедании яблока.
    draw(): отрисовывание текущей позиции головы змейки.
    update_direction(): применяет новое направление движения змейки.
    check_self_collision(): проверяет движение змейки на столкновение с собой.
    reset(): сбрасывает змейку до начального состояния.
    """

    def __init__(self):
        super().__init__(SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.last = None

    @property
    def get_head_position(self):
        """Функция возвращает координаты головы змейки"""
        return self.positions[0]

    def update_direction(self):
        """Функция применяет новое направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction

    def move(self):
        """Метод обновляет позицию змейки в заданном направлении.

        Добавляет голову при поглощении яблока и удаляет хвост
        (если яблока не было).

        Эффекты:
        Обновляет self.positions,
        Обновляет self.last.
        """
        head_x, head_y = self.get_head_position
        step_x, step_y = self.direction

        new_x = (head_x + step_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + step_y * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def eat(self):
        """Метод реализует функцию поедания: увеличивает тело змейки"""
        self.length += 1

    def check_self_collision(self):
        """Метод проверяет змейку на столкновение со своим телом"""
        head = self.get_head_position
        return head in self.positions[1:]

    def draw(self):
        """Метод отрисовывает голову змейки."""
        if self.last is not None:
            rect = pg.Rect(self.last[0], self.last[1], GRID_SIZE, GRID_SIZE)
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)

        self.draw_rect(self.get_head_position, SNAKE_COLOR)

    def reset(self):
        """Сброс змейки в начальное состояние:
        положение в центре поля, длина 1 сегмент.
        """
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.last = None


def handle_keys(game_object):
    """Функция обрабатывает нажатия клавиш для изменения движения змейки."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            screen.fill(BOARD_BACKGROUND_COLOR)
            return False
        if event.type == pg.KEYDOWN:
            key = event.key
            current_direction = game_object.direction
            game_object.next_direction = DIRECTIONS.get(
                (current_direction, key),
                current_direction
            )
    return True


def main():
    """Основная функция игры.

    Отвечает за сборку и выполнение компонентов.
    Запускает игровой цикл с объектами: обрабатывает действия пользователя,
    обновляет состояние игры, проверяет условия завершения.
    """
    pg.init()

    snake = Snake()
    apple = Apple(snake.positions)

    running = True
    while running:
        if not handle_keys(snake):
            running = False
            break

        snake.update_direction()
        snake.move()

        if snake.check_self_collision():
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(snake.positions)
        elif snake.get_head_position == apple.position:
            snake.eat()
            apple.randomize_position(snake.positions)

        apple.draw()
        snake.draw()
        pg.display.flip()
        clock.tick(SPEED)

    pg.quit()


if __name__ == '__main__':
    main()
