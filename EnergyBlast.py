from pico2d import *

import game_framework
import game_world
import play_mode

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
EnergyBlast_SPEED_KMPH = 10.0  # Km / Hour
EnergyBlast_SPEED_MPM = (EnergyBlast_SPEED_KMPH * 1000.0 / 60.0)
EnergyBlast_SPEED_MPS = (EnergyBlast_SPEED_MPM / 60.0)
EnergyBlast_SPEED_PPS = (EnergyBlast_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
EnergyBlast_FRAME_PER_ACTION = 20.0

class EnergyBlast:
    def __init__(self, x=None, y=None):
        self.images = [load_image("./adventurer_hero/" + 'AdventurerHero_EnergyBlast' + "_%d" % i + ".png") for i in range(0, 18)]
        self.frame = 0
        self.dir = 0
        self.x = x
        self.y = y

    def update(self):
        self.frame += EnergyBlast_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
        if int(self.frame) >= 18:
            game_world.remove_object(self)

    def draw(self):
        self.images[int(self.frame)].draw(self.x, self.y, 200 * 2, 145 * 2)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 140, self.y - 100, self.x + 140, self.y + 60    

    def handle_collision(self, group, other):
        pass