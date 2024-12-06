from pico2d import *

class Stage1:
    def __init__(self):
        self.image = load_image('스테이지1.png')
        self.bgm = load_wav("./audio_clip/" + 'Adventurer.wav')
        self.bgm.set_volume(20)
        self.bgm.repeat_play()

    def update(self):
        pass

    def draw(self):
        self.image.draw(900, 400, 1800, 800)

    def get_bb(self):
        # fill here
        pass

