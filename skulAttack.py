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
        #draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        if self.face_dir == 1:
            return self.x - 40, self.y - 55, self.x + 58, self.y + 55
        else:
            return self.x - 58, self.y - 55, self.x + 40, self.y + 55

    def handle_collision(self, group, other):
        if group == 'skulAttack:adventurer':
            self.hit_sound = load_wav("./audio_clip/" + 'Skul_Hit 3 (b copy) (Unused).wav')
            self.hit_sound.set_volume(30)
            self.hit_sound.play()
            self.alive = False
            remove_object(self)
        elif group == 'skulAttack:Energyball':
            self.hit_sound2 = load_wav("./audio_clip/" + 'Skul_Hit 1 (Unused).wav')
            self.hit_sound2.set_volume(30)
            self.hit_sound2.play()
            self.EB_sound3 = load_wav("./audio_clip/" + 'AdventurerHero_EnergyBall.wav')
            self.EB_sound3.set_volume(30)
            self.EB_sound3.play()
            pass
        pass