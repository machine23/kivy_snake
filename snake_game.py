from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse
from kivy import properties as props

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

    def update(self, dt):
        snake_pos = [sum(x) for x in zip(self.snake.body[0].pos, self.movs[self.direction])]
        self.snake.move_to(snake_pos)


class SnakeApp(App):
    def build(self):
        game = SnakeGame()
        Clock.schedule_interval(game.update, SPEED)
        return game


if __name__ == "__main__":
    SnakeApp().run()
