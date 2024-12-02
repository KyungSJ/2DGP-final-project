from pico2d import *

import game_framework
import game_world
import play_mode

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
Energyball_SPEED_KMPH = 10.0  # Km / Hour
Energyball_SPEED_MPM = (Energyball_SPEED_KMPH * 1000.0 / 60.0)
Energyball_SPEED_MPS = (Energyball_SPEED_MPM / 60.0)
Energyball_SPEED_PPS = (Energyball_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
Energyball_FRAME_PER_ACTION = 3.0

class EnergyBall:
    def __init__(self, x=None, y=None):
        self.images = [load_image("./adventurer_hero/" + 'Hero_EnergyBall_Projectile' + "_%d" % i + ".png") for i in range(0, 48)]
        self.frame = 0
        self.dir = 0
        self.x = x
        self.y = y

    def update(self):
        self.dir = math.atan2(play_mode.skul.y - self.y, play_mode.skul.x - self.x)
        distance = Energyball_SPEED_PPS * game_framework.frame_time
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)
        self.frame += Energyball_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
        if int(self.frame) >= 48:
            game_world.remove_object(self)

        pass

    def draw(self):
        self.images[int(self.frame)].draw(self.x, self.y, 61, 61)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 17, self.y - 17, self.x + 17, self.y + 17

    def handle_collision(self, group, other):
        # fill here

        pass