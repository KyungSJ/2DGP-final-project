from pico2d import *

class Stage0:
    def __init__(self):
        self.image = load_image('스테이지0.png')
        self.bgm = load_wav("./audio_clip/" + 'Chapter1.wav')
        self.bgm.set_volume(20)
        self.bgm.repeat_play()

    def update(self):
        pass

    def draw(self):
        self.image.draw(960, 400, 960 * 2, 400 * 2)


    def get_bb(self):
        # fill here
        pass

