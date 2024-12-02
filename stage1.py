from pico2d import *

class Stage1:
    def __init__(self):
        self.image = load_image('스테이지1.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(900, 400, 1800, 800)

    def get_bb(self):
        # fill here
        pass

