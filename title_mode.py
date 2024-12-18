from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE

import game_framework
from pico2d import load_image, delay, clear_canvas, update_canvas, get_events, get_time, load_font, load_music, load_wav

import game_world
import play_mode
import practice_mode
from title_audio import title_audio


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            game_framework.change_mode(practice_mode)
        else:
            pass

def init():
    global image
    global running
    global image2
    global font


    image = load_image('Title_Art.png')
    image2 = load_image('Title_Logo.png')
    running = True
    font = load_font('NotoSans-Medium.ttf', 40)
    bgm = title_audio()
    game_world.add_object(bgm, 0)

def finish():
    global image
    global image2
    del image
    del image2
    game_world.clear()

def update():
    game_world.update()
    game_world.handle_collisions()
    pass

def draw():
    clear_canvas()
    image.draw(900, 400, 1800, 800)
    image2.draw(900, 400, 1800, 800)
    font.draw(780, 80, 'any key press', (255, 255, 255))
    game_world.render()
    update_canvas()

