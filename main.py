import pyglet
import pyglet.gl as gl

pyglet.options["debug_gl"] = False  # makes things slow, so disable it

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_draw(self):
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)
        self.clear()
    
class Game:
    def __init__(self):
        self.config = gl.Config(major_version=3)
        self.window = Window(width=800, height=600, config=self.config, caption="PygletMinecraft")

    def run(self):
        pyglet.app.run()

if __name__ == "__main__":
    game = Game()
    game.run()