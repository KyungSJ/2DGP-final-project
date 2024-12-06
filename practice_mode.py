from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_f

import game_framework
from pico2d import load_image, delay, clear_canvas, update_canvas, get_events, get_time, load_font

import game_world
import play_mode
import title_mode
from Stage0 import Stage0
from skul import Skul
from stage1_tile_1 import Stage1_Tile1
from stage1_tile_2 import Stage1_Tile2


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_f:
                game_framework.change_mode(play_mode)
        else:
            skul.handle_event(event)

def init():
    global skul
    global whiteimage
    global font

    font = load_font('NotoSans-Medium.ttf', 40)

    stage0 = Stage0()
    game_world.add_object(stage0, 0)

    stage1_tile1 = [Stage1_Tile1(x * 64, 64) for x in range(0, 29)]
    for tile in stage1_tile1:
        game_world.add_object(tile, 1)
        game_world.add_collision_pair('skul:stage1_tile', None, tile)

    stage1_tile2 = [Stage1_Tile2(x * 64, 0) for x in range(0, 29)]
    for tile in stage1_tile2:
        game_world.add_object(tile, 1)

    skul = Skul(False)
    game_world.add_object(skul, 2)
    game_world.add_collision_pair('skul:stage1_tile', skul, None)
    whiteimage = load_image('하얀 바탕.png')

    pass


def finish():
    game_world.clear()
    pass

def update():
    game_world.update()
    game_world.handle_collisions()



def draw():
    clear_canvas()
    whiteimage.draw(900, 400)
    game_world.render()
    font.draw(780, 750, 'esc: go pre-mode', (0, 0, 0))
    font.draw(780, 700, 'z: dash', (0, 0, 0))
    font.draw(780, 650, 'x: attack', (0, 0, 0))
    font.draw(780, 600, 'c: jump', (0, 0, 0))
    font.draw(780, 550, 'right: move right', (0, 0, 0))
    font.draw(780, 500, 'left: move left', (0, 0, 0))
    font.draw(780, 450, 'F: game start', (0, 0, 0))
    update_canvas()

