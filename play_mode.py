import random

from pico2d import *
import game_framework

import game_world
from Healthbar import Healthbar
from adventurer_hero import Adventurer_hero
from stage1 import Stage1
from skul import Skul
from stage1_tile_1 import Stage1_Tile1
from stage1_tile_2 import Stage1_Tile2


# boy = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            skul.handle_event(event)

def init():
    global skul, adventurer_hero

    stage1 = Stage1()
    game_world.add_object(stage1, 0)
    
    healthbar = Healthbar(900, 799)
    game_world.add_object(healthbar, 1)

    stage1_tile1 = [Stage1_Tile1(x * 64, 64) for x in range(0, 29)]
    for tile in stage1_tile1:
        game_world.add_object(tile, 1)
        game_world.add_collision_pair('skul:stage1_tile', None, tile)

    stage1_tile2 = [Stage1_Tile2(x * 64, 0) for x in range(0, 29)]
    for tile in stage1_tile2:
        game_world.add_object(tile, 1)

    skul = Skul()
    game_world.add_object(skul, 2)
    game_world.add_collision_pair('skul:stage1_tile', skul, None)

    adventurer_hero = Adventurer_hero(800, 148)
    game_world.add_object(adventurer_hero, 2)
    game_world.add_collision_pair('skulAttack:adventurer', None, adventurer_hero)

def finish():
    game_world.clear()
    pass


def update():
    game_world.update() # 소년과 볼 위치가 다 업데이트 완료
    game_world.handle_collisions()

    # fill here
    # for ball in balls.copy():
    #     if game_world.collide(boy, ball):
    #         print('boy:ball COLLIDE') # 충돌 확인
    #         # 소년 볼 증가
    #         boy.ball_count += 1
    #        game_world.remove_object(ball)
    #         balls.remove(ball)



def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass


