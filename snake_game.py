import random

from kivy import properties as props
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.label import Label
from kivy.uix.widget import Widget

SPEED = 0.1
SIZE = 30

LEFT = "left"
UP = "up"
RIGHT = "right"
DOWN = "down"


class Snake(Widget):
    body = props.ListProperty()
    size = props.ListProperty([SIZE, SIZE])

    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        for _ in range(4):
            self._grow([300, 300])

    @property
    def head_position(self):
        return self.body[0].pos

    def _grow(self, pos):
        with self.canvas:
            Color(0, 0, 1)
            head = Ellipse(pos=pos, size=self.size)
            self.body.append(head)

    def check_self_collision(self, next_head_pos):
        """ Проверка на столкновение головы змеи с телом """
        for body_segment in self.body[1:]:
            if list(body_segment.pos) == next_head_pos:
                return True
        return False

    def move_to(self, next_pos, grow=False):
        for i, segment in enumerate(self.body):
            self.body[i].pos, next_pos = next_pos, segment.pos
        if grow:
            self._grow(next_pos)


class Apple(Widget):
    coord = props.ListProperty([250, 300])
    body = props.ObjectProperty(None)

    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        with self.canvas:
            Color(1, 0, 0)
            self.body = Ellipse(pos=self.coord, size=(SIZE, SIZE))

    def check_collision(self, coord):
        print(self.coord, coord)
        if coord[0] <= self.coord[0] + SIZE/2 <= coord[0] + SIZE \
            and coord[1] <= self.coord[1] + SIZE/2 <= coord[1] + SIZE:
            print("check_collision")
            return True
        return False

    def new_position(self, snake):
        print("new_position")
        while True:
            apple_x = random.randint(SIZE, Window.size[0] - SIZE)
            apple_y = random.randint(SIZE, Window.size[1] - SIZE)

            apple_x -= apple_x % SIZE
            apple_y -= apple_y % SIZE

            for segment in snake.body:
                if [apple_x, apple_y] == segment.pos:
                    continue

            self.coord = [apple_x, apple_y]
            self.body.pos = [apple_x, apple_y]
            return


class SnakeGame(Widget):
    movs = {
        RIGHT: [SIZE, 0],
        LEFT: [-SIZE, 0],
        UP: [0, SIZE],
        DOWN: [0, -SIZE],
    }
    direction = props.StringProperty(RIGHT)

    def __init__(self):
        super().__init__()
        self.canvas.clear()
        self.snake = Snake(self.canvas)
        self.apple = Apple(self.canvas)

    def on_touch_down(self, touch):
        head_x = self.snake.head_position[0]
        head_y = self.snake.head_position[1]

        if self.direction in [UP, DOWN]:
            if touch.pos[0] > head_x:
                self.direction = RIGHT
            else:
                self.direction = LEFT
        else:
            if touch.pos[1] < head_y:
                self.direction = DOWN
            else:
                self.direction = UP

        return super(SnakeGame, self).on_touch_down(touch)

    @staticmethod
    def check_edges(position):
        window_size = Window.size
        if position[0] < 0:
            position[0] = window_size[0]
        elif position[0] + SIZE > window_size[0]:
            position[0] = 0

        if position[1] < 0:
            position[1] = window_size[1]
        elif position[1] + SIZE > window_size[1]:
            position[1] = 0

    def final_screen(self):
        Clock.unschedule(self.update)
        self.canvas.clear()
        l = Label(font_size=20, pos=(300, 300), text="Game Over!")

        self.add_widget(l)

    def update(self, dt):
        snake_pos = [
            sum(x) for x in zip(self.snake.head_position, self.movs[self.direction])
        ]
        self.check_edges(snake_pos)
        stop_game = self.snake.check_self_collision(snake_pos)
        if stop_game:
            self.final_screen()
            return

        get_apple = self.apple.check_collision(self.snake.head_position)

        if get_apple:
            self.apple.new_position(self.snake)

        self.snake.move_to(snake_pos, get_apple)


class SnakeApp(App):
    def build(self):
        game = SnakeGame()
        Clock.schedule_interval(game.update, SPEED)
        return game


if __name__ == "__main__":
    SnakeApp().run()
