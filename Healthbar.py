from pico2d import *

class Healthbar:
    def __init__(self, x=None, y=None):
        self.image = load_image('체력바.png')
        self.x = x
        self.y = y

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, 306 * 4, 58 * 4)

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        pass