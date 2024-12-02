from pico2d import *

class Stage1_Tile2:
    def __init__(self,x=None,y=None):
        self.image = load_image('스테이지1 타일2.png')
        self.x = x
        self.y = y

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, 32 * 2, 32 * 2)

    def get_bb(self):
        return self.x - 32, self.y - 32, self.x + 32, self.y + 28
        pass