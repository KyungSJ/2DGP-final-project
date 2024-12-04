from pico2d import *

import play_mode
from game_world import remove_object


class skulAttack:
    def __init__(self, x=None, y=None, dir=None):
        self.x = x
        self.y = y
        self.alive = True
        self.face_dir = dir

    def update(self):
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        if self.face_dir == 1:
            return self.x - 40, self.y - 55, self.x + 58, self.y + 55
        else:
            return self.x - 58, self.y - 55, self.x + 40, self.y + 55

    def handle_collision(self, group, other):
        if group == 'skulAttack:adventurer':
            play_mode.adventurer_hero.hp -= 5
            self.alive = False
            remove_object(self)
        pass