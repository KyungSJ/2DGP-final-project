from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE

import game_framework
from pico2d import load_image, delay, clear_canvas, update_canvas, get_events, get_time

def handle_events():
    events = get_events()

def init():
    global image
    global running
    global logo_start_time
    global whiteimage

    image = load_image('tuk_credit.png')
    whiteimage = load_image('하얀 바탕.png')
    running = True
    logo_start_time = get_time()

def finish():
    global image
    global whiteimage
    del image
    del whiteimage

def update():
    global logo_start_time
    if get_time() - logo_start_time >= 2.0:
        logo_start_time = get_time()
        game_framework.change_mode(title_mode)

def draw():
    clear_canvas()
    whiteimage.draw(900, 400)
    image.draw(900, 400)
    update_canvas()

