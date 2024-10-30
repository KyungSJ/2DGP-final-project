from pico2d import *

class Stage:
    def __init__(self):
        self.image = load_image('예비 스테이지.jpg')

    def update(self):
        pass

    def draw(self):
        self.image.draw(512, 208, 1024, 576)

    def get_bb(self):
        # fill here
        pass

