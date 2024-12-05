from pico2d import *

import game_world
import play_mode
from game_world import remove_object


class Energy_blast_attack_range:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
        self.alive = True

    def update(self):
        pass

    def draw(self):
        #draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        return self.x - 140, self.y - 100, self.x + 140, self.y + 60

    def handle_collision(self, group, other):
        if group == 'Energyblast:skul':
            game_world.remove_object(self)
            self.alive = False
            pass
        pass