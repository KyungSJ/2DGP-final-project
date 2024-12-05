from pico2d import *

import play_mode
from game_world import remove_object


class adventurerAttack:
    def __init__(self, x=None, y=None, dir=None):
        self.x = x
        self.y = y
        self.alive = True
        self.dir = dir

    def update(self):
        pass

    def draw(self):
        #draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        if math.cos(self.dir) < 0:
            return self.x - 48 - 36 * 2, self.y - 31 * 2, self.x - 48 + 36 * 2, self.y + 31 * 2
        else:
            return self.x + 48 - 36 * 2, self.y - 31 * 2, self.x + 48 + 36 * 2, self.y + 31 * 2

    def handle_collision(self, group, other):
        if group == 'adventurerAttack:skul':
            self.alive = False
            remove_object(self)
        pass