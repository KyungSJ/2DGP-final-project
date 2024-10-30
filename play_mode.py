import random

from pico2d import *
import game_framework

import game_world
from stage import Stage
from skul import Skul



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
    global skul

    stage = Stage()
    game_world.add_object(stage, 0)

    skul = Skul()
    game_world.add_object(skul, 1)

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

