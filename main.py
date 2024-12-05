from pico2d import open_canvas, delay, close_canvas
import game_framework

import play_mode as play_mode

open_canvas(1800, 800)
game_framework.run(play_mode)
close_canvas()

