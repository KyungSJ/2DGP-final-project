from pico2d import *

class title_audio:
    def __init__(self):
        self.bgm = load_wav("./audio_clip/" + 'MainTitle.wav')
        self.bgm.set_volume(20)
        self.bgm.repeat_play()

    def update(self):
        pass

    def draw(self):
        pass

    def get_bb(self):
        # fill here
        pass

