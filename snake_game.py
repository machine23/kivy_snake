from kivy import properties as props
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse
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
        self._grow([300, 300])

    @property
    def pos(self):
        return self.body[0].pos

    def _grow(self, pos):
        with self.canvas:
            Color(0, 0, 1)
            head = Ellipse(pos=pos, size=self.size)
            self.body.append(head)

    def move_to(self, next_pos, grow=False):
        for i, segment in enumerate(self.body):
            self.body[i].pos, next_pos = next_pos, segment.pos
        if grow:
            self._grow(next_pos)


class SnakeGame(Widget):
    opposite_dirs = {
        RIGHT: LEFT,
        LEFT: RIGHT,
        UP: DOWN,
        DOWN: UP,
    }
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

    def on_touch_down(self, touch):
        window_size = Window.size
        direction = self.direction
        if window_size[0] - touch.pos[0] < window_size[0] / 4:
            direction = "right"
        elif touch.pos[0] < (window_size[0] / 4):
            direction = "left"
        elif window_size[1] - touch.pos[1] < window_size[1] / 4:
            direction = "up"
        elif touch.pos[1] < (window_size[1] / 4):
            direction = "down"

        if self.opposite_dirs[direction] != self.direction:
            self.direction = direction

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
        

    def update(self, dt):
        snake_pos = [
            sum(x) for x in zip(self.snake.pos, self.movs[self.direction])
        ]
        self.check_edges(snake_pos)
        self.snake.move_to(snake_pos)


class SnakeApp(App):
    def build(self):
        game = SnakeGame()
        Clock.schedule_interval(game.update, SPEED)
        return game


if __name__ == "__main__":
    SnakeApp().run()
