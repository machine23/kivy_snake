from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock

SPEED = 0.1

class SnakeGame(Widget):
    def update(self, dt):
        pass


class SnakeApp(App):
    def build(self):
        game = SnakeGame()
        Clock.schedule_interval(game.update, SPEED)
        return game


if __name__ == "__main__":
    SnakeApp().run()
