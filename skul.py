# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, load_font, \
    draw_rectangle, clamp, load_wav

import game_world
import game_framework
from skulAttack import skulAttack
from state_machine import start_event, right_down, left_up, left_down, right_up, space_down, StateMachine, time_out, \
    c_down, x_down, z_down, jump_out, hp_out

# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Idle:
    @staticmethod
    def enter(skul, e):
        if start_event(e):
            skul.face_dir = 1
        skul.frame = 0
        skul.wait_time = get_time()

    @staticmethod
    def exit(skul, e):
        pass

    @staticmethod
    def do(skul):
        if skul.hp <= 0:
            skul.state_machine.add_event(('HP_OUT', 0))

        skul.frame = (skul.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4



    @staticmethod
    def draw(skul):
        # Idle 애니메이션의 각 프레임 좌표와 크기
        idle_frames = [
            (5, 1251, 40, 36),  # 첫 번째 프레임 (x, y, w, h)
            (50, 1250, 42, 37),  # 두 번째 프레임
            (97, 1251, 44, 36),  # 세 번째 프레임
            (146, 1253, 42, 34)  # 네 번째 프레임
        ]

        # 현재 프레임 정보 가져오기
        frame_index = int(skul.frame) % len(idle_frames)
        x, y, w, h = idle_frames[frame_index]

        # 프레임을 그리기
        if skul.face_dir == 1:
            skul.image.clip_draw(x, y, w, h, skul.x, skul.y, w * 2, h * 2)
        else:
            skul.image.clip_composite_draw(x, y, w, h, 0, 'h', skul.x, skul.y, w * 2, h * 2)


class Run:
    @staticmethod
    def enter(skul, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            skul.dir, skul.face_dir = 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            skul.dir, skul.face_dir = -1, -1

    @staticmethod
    def exit(skul, e):
        pass
    @staticmethod
    def do(skul):
        if skul.hp <= 0:
            skul.state_machine.add_event(('HP_OUT', 0))
        skul.frame = (skul.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        skul.x += skul.face_dir * RUN_SPEED_PPS * game_framework.frame_time
        pass
    @staticmethod
    def draw(skul):
        run_frames = [
            (5, 1206, 42, 31),
            (52, 1204, 44, 33),
            (101, 1203, 42, 34),
            (148, 1203, 37, 34),
            (190, 1204, 37, 33),
            (232, 1201, 43, 36),
            (280, 1203, 42, 34),
            (327, 1203, 42, 34)
        ]

        frame_index = int(skul.frame) % len(run_frames)
        x, y, w, h = run_frames[frame_index]

        if skul.face_dir == 1:
            skul.image.clip_draw(x, y, w, h, skul.x, skul.y , w * 2, h * 2)
        else:
            skul.image.clip_composite_draw(x, y, w, h, 0, 'h', skul.x, skul.y, w * 2, h * 2)

class Jump:
    @staticmethod
    def enter(skul, e):
        if not skul.do_jump:
            skul.jump_sound = load_wav("./audio_clip/" + 'Default_Jump.wav')
            skul.jump_sound.set_volume(20)
            skul.jump_sound.play()
            skul.do_jump = True
        pass

    @staticmethod
    def exit(skul, e):
        pass

    @staticmethod
    def do(skul):
        if skul.hp <= 0:
            skul.state_machine.add_event(('HP_OUT', 0))
        # 속도 계산 및 위치 변경
        skul.jump_velocity += skul.gravity * game_framework.frame_time * 50  # 프레임 시간 기반 속도 변화
        skul.y += skul.jump_velocity * game_framework.frame_time * 50  # 프레임 시간 기반 위치 변화
        # 지면 충돌 처리

        if skul.y < 122:
            skul.y = 122
            skul.jump_velocity = 10  # 초기 점프 속도
            skul.jump_frame = 0
            skul.state_machine.add_event(('JUMP_OUT', 0))
            skul.do_jump = False

        # 애니메이션 프레임 처리
        skul.jump_frame = (skul.jump_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
    @staticmethod
    def draw(skul):
        if skul.jump_velocity > 0:
            jump_frames = [
                (5, 1111, 21, 36),
                (31, 1111, 22, 36)
            ]

            frame_index = int(skul.jump_frame)
            x, y, w, h = jump_frames[frame_index]

            if skul.face_dir == 1:
                skul.image.clip_draw(x, y, w, h, skul.x, skul.y, w * 2, h * 2)
            else:
                skul.image.clip_composite_draw(x, y, w, h, 0, 'h', skul.x, skul.y, w * 2, h * 2)
        else:
            jump_frames = [
                (5, 1062, 34, 36),
                (44, 1063, 34, 35)
            ]

            frame_index = int(skul.jump_frame)
            x, y, w, h = jump_frames[frame_index]

            if skul.face_dir == 1:
                skul.image.clip_draw(x, y, w, h, skul.x, skul.y, w * 2, h * 2)
            else:
                skul.image.clip_composite_draw(x, y, w, h, 0, 'h', skul.x, skul.y, w * 2, h * 2)

class Attack:
    @staticmethod
    def enter(skul, e):
        skul.attack_animation_set = 0 if skul.attack_animation_set == 1 else 1  # 첫 번째와 두 번째 애니메이션 전환
        if skul.attack_animation_set == 1:
            skul.Attack_sound1 = load_wav("./audio_clip/" + 'Skul_Atk 1.wav')
            skul.Attack_sound1.set_volume(20)
            skul.Attack_sound1.play()
        else:
            skul.Attack_sound2 = load_wav("./audio_clip/" + 'Skul_Atk 2.wav')
            skul.Attack_sound2.set_volume(20)
            skul.Attack_sound2.play()
        skul.attack_frame = 0  # 공격 애니메이션 프레임 초기화
        skul.skulattack = skulAttack(skul.x, skul.y, skul.face_dir)
        game_world.add_object(skul.skulattack, 2)
        game_world.add_collision_pair('skulAttack:adventurer', skul.skulattack, None)
        game_world.add_collision_pair('skulAttack:Energyball', skul.skulattack, None)

    @staticmethod
    def exit(skul, e):
        if skul.skulattack.alive:
            game_world.remove_object(skul.skulattack)
        pass

    @staticmethod
    def do(skul):
        if skul.hp <= 0:
            skul.state_machine.add_event(('HP_OUT', 0))
        # 공격 애니메이션 진행
        skul.attack_frame += FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time

        # 공격 애니메이션이 끝나면 Idle 상태로 전환
        if int(skul.attack_frame) >= 5:  # 5프레임 이후 상태 전환
            skul.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(skul):
        # 첫 번째 애니메이션 프레임
        attack1_frames = [
            (5, 950, 34, 46),
            (44, 951, 35, 45),
            (84, 939, 63, 57),
            (152, 956, 61, 40),
            (218, 961, 41, 35),
        ]
        # 두 번째 애니메이션 프레임
        attack2_frames = [
            (5, 893, 35, 33),
            (45, 867, 62, 59),
            (112, 874, 59, 52),
            (176, 882, 32, 44),
        ]

        # 현재 사용하는 프레임 세트 선택
        frames = attack1_frames if skul.attack_animation_set == 0 else attack2_frames
        frame_index = int(skul.attack_frame) % len(frames)

        x, y, w, h = frames[frame_index]

        if skul.face_dir == 1:
            skul.image.clip_draw(x, y, w, h, skul.x, skul.y, w * 2, h * 2)
        else:
            skul.image.clip_composite_draw(x, y, w, h, 0, 'h', skul.x, skul.y, w * 2, h * 2)


class Run_attack:
    @staticmethod
    def enter(skul, e):
        skul.attack_animation_set = 0 if skul.attack_animation_set == 1 else 1  # 첫 번째와 두 번째 애니메이션 전환
        if skul.attack_animation_set == 1:
            skul.Attack_sound1 = load_wav("./audio_clip/" + 'Skul_Atk 1.wav')
            skul.Attack_sound1.set_volume(20)
            skul.Attack_sound1.play()
        else:
            skul.Attack_sound2 = load_wav("./audio_clip/" + 'Skul_Atk 2.wav')
            skul.Attack_sound2.set_volume(20)
            skul.Attack_sound2.play()
        skul.attack_frame = 0  # 공격 애니메이션 프레임 초기화
        skul.skulattack = skulAttack(skul.x, skul.y, skul.face_dir)
        game_world.add_object(skul.skulattack, 2)
        game_world.add_collision_pair('skulAttack:adventurer', skul.skulattack, None)
        game_world.add_collision_pair('skulAttack:Energyball', skul.skulattack, None)

    @staticmethod
    def exit(skul, e):
        if skul.skulattack.alive:
            game_world.remove_object(skul.skulattack)
        pass

    @staticmethod
    def do(skul):
        if skul.hp <= 0:
            skul.state_machine.add_event(('HP_OUT', 0))
        # 공격 애니메이션 진행
        skul.attack_frame += FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time

        # 공격 애니메이션이 끝나면 Idle 상태로 전환
        if int(skul.attack_frame) >= 5:  # 5프레임 이후 상태 전환
            skul.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(skul):
        # 첫 번째 애니메이션 프레임
        attack1_frames = [
            (5, 950, 34, 46),
            (44, 951, 35, 45),
            (84, 939, 63, 57),
            (152, 956, 61, 40),
            (218, 961, 41, 35),
        ]
        # 두 번째 애니메이션 프레임
        attack2_frames = [
            (5, 893, 35, 33),
            (45, 867, 62, 59),
            (112, 874, 59, 52),
            (176, 882, 32, 44),
        ]

        # 현재 사용하는 프레임 세트 선택
        frames = attack1_frames if skul.attack_animation_set == 0 else attack2_frames
        frame_index = int(skul.attack_frame) % len(frames)

        x, y, w, h = frames[frame_index]

        if skul.face_dir == 1:
            skul.image.clip_draw(x, y, w, h, skul.x, skul.y, w * 2, h * 2)
        else:
            skul.image.clip_composite_draw(x, y, w, h, 0, 'h', skul.x, skul.y, w * 2, h * 2)


class Jump_attack:
    @staticmethod
    def enter(skul, e):
        skul.jump_Atk_sound = load_wav("./audio_clip/" + 'Skul_Jump_Atk.wav')
        skul.jump_Atk_sound.set_volume(20)
        skul.jump_Atk_sound.play()
        skul.jump_attack_frame = 0  # 애니메이션 프레임 초기화
        skul.skulattack = skulAttack(skul.x, skul.y, skul.face_dir)
        game_world.add_object(skul.skulattack, 2)
        game_world.add_collision_pair('skulAttack:adventurer', skul.skulattack, None)
        game_world.add_collision_pair('skulAttack:Energyball', skul.skulattack, None)


    @staticmethod
    def exit(skul, e):
        if skul.skulattack.alive:
            game_world.remove_object(skul.skulattack)
        pass

    @staticmethod
    def do(skul):
        if skul.hp <= 0:
            skul.state_machine.add_event(('HP_OUT', 0))
        # 애니메이션 프레임 진행
        skul.jump_attack_frame += FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time

        # 애니메이션이 끝나면 Idle 상태로 전환
        if int(skul.jump_attack_frame) >= 4:  # 4프레임 이후 상태 전환
            if skul.jump_velocity > 0:
                skul.jump_velocity = skul.jump_velocity * -1
            skul.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(skul):
        # 점프 공격 애니메이션 프레임
        jump_attack_frames = [
            (5, 812, 33, 42),
            (43, 797, 61, 57),
            (109, 810, 57, 44),
            (171, 817, 33, 37),
        ]

        frame_index = int(skul.jump_attack_frame) % len(jump_attack_frames)
        x, y, w, h = jump_attack_frames[frame_index]

        if skul.face_dir == 1:
            skul.image.clip_draw(x, y, w, h, skul.x, skul.y, w * 2, h * 2)
        else:
            skul.image.clip_composite_draw(x, y, w, h, 0, 'h', skul.x, skul.y, w * 2, h * 2)


class Jump_move_attack:
    @staticmethod
    def enter(skul, e):
        skul.jump_Atk_sound = load_wav("./audio_clip/" + 'Skul_Jump_Atk.wav')
        skul.jump_Atk_sound.set_volume(20)
        skul.jump_Atk_sound.play()
        skul.jump_attack_frame = 0  # 애니메이션 프레임 초기화
        skul.skulattack = skulAttack(skul.x, skul.y, skul.face_dir)
        game_world.add_object(skul.skulattack, 2)
        game_world.add_collision_pair('skulAttack:adventurer', skul.skulattack, None)
        game_world.add_collision_pair('skulAttack:Energyball', skul.skulattack, None)

    @staticmethod
    def exit(skul, e):
        if skul.skulattack.alive:
            game_world.remove_object(skul.skulattack)
        pass

    @staticmethod
    def do(skul):
        if skul.hp <= 0:
            skul.state_machine.add_event(('HP_OUT', 0))
        # 애니메이션 프레임 진행
        skul.jump_attack_frame += FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time

        # 애니메이션이 끝나면 Idle 상태로 전환
        if int(skul.jump_attack_frame) >= 4:  # 4프레임 이후 상태 전환
            if skul.jump_velocity > 0:
                skul.jump_velocity = skul.jump_velocity * -1
            skul.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(skul):
        # 점프 공격 애니메이션 프레임
        jump_attack_frames = [
            (5, 812, 33, 42),
            (43, 797, 61, 57),
            (109, 810, 57, 44),
            (171, 817, 33, 37),
        ]

        frame_index = int(skul.jump_attack_frame) % len(jump_attack_frames)
        x, y, w, h = jump_attack_frames[frame_index]

        if skul.face_dir == 1:
            skul.image.clip_draw(x, y, w, h, skul.x, skul.y, w * 2, h * 2)
        else:
            skul.image.clip_composite_draw(x, y, w, h, 0, 'h', skul.x, skul.y, w * 2, h * 2)


class Dash:
    @staticmethod
    def enter(skul, e):
        skul.dash_sound = load_wav("./audio_clip/" + 'Default_Dash.wav')
        skul.dash_sound.set_volume(20)
        skul.dash_sound.play()
        skul.init_x = skul.x
        pass
    @staticmethod
    def exit(skul, e):
        pass
    @staticmethod
    def do(skul):
        if skul.hp <= 0:
            skul.state_machine.add_event(('HP_OUT', 0))
        skul.x += skul.face_dir * 2
        if (skul.x - skul.init_x) * skul.face_dir >= 180:
            skul.state_machine.add_event(('TIME_OUT', 0))
        pass
    @staticmethod
    def draw(skul):
        if skul.face_dir == 1:
            skul.image.clip_draw(5, 1160, 42, 28, skul.x, skul.y, 42 * 2, 28 * 2)
        else:
            skul.image.clip_composite_draw(5, 1160, 42, 28, 0, 'h', skul.x, skul.y, 42 * 2, 28 * 2)
        pass

class Run_dash:
    @staticmethod
    def enter(skul, e):
        skul.dash_sound = load_wav("./audio_clip/" + 'Default_Dash.wav')
        skul.dash_sound.set_volume(20)
        skul.dash_sound.play()
        skul.init_x = skul.x
        pass
    @staticmethod
    def exit(skul, e):
        pass
    @staticmethod
    def do(skul):
        if skul.hp <= 0:
            skul.state_machine.add_event(('HP_OUT', 0))
        skul.x += skul.face_dir * 2
        if (skul.x - skul.init_x) * skul.face_dir >= 180:
            skul.state_machine.add_event(('TIME_OUT', 0))
        pass
    @staticmethod
    def draw(skul):
        if skul.face_dir == 1:
            skul.image.clip_draw(5, 1160, 42, 28, skul.x, skul.y, 42 * 2, 28 * 2)
        else:
            skul.image.clip_composite_draw(5, 1160, 42, 28, 0, 'h', skul.x, skul.y, 42 * 2, 28 * 2)
        pass

class Jump_Dash:
    @staticmethod
    def enter(skul, e):
        skul.dash_sound = load_wav("./audio_clip/" + 'Default_Dash.wav')
        skul.dash_sound.set_volume(20)
        skul.dash_sound.play()
        skul.init_x = skul.x
        if skul.jump_velocity > 0:
            skul.jump_velocity = skul.jump_velocity * -1
        pass

    @staticmethod
    def exit(skul, e):
        pass

    @staticmethod
    def do(skul):
        if skul.hp <= 0:
            skul.state_machine.add_event(('HP_OUT', 0))
        skul.x += skul.face_dir * 2
        if (skul.x - skul.init_x) * skul.face_dir >= 180:
            skul.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(skul):
        if skul.face_dir == 1:
            skul.image.clip_draw(5, 1160, 42, 28, skul.x, skul.y, 42 * 2, 28 * 2)
        else:
            skul.image.clip_composite_draw(5, 1160, 42, 28, 0, 'h', skul.x, skul.y, 42 * 2, 28 * 2)
        pass
class Jump_move_dash:
    @staticmethod
    def enter(skul, e):
        skul.dash_sound = load_wav("./audio_clip/" + 'Default_Dash.wav')
        skul.dash_sound.set_volume(20)
        skul.dash_sound.play()
        skul.init_x = skul.x
        if skul.jump_velocity > 0:
            skul.jump_velocity = skul.jump_velocity * -1
        pass

    @staticmethod
    def exit(skul, e):
        pass

    @staticmethod
    def do(skul):
        if skul.hp <= 0:
            skul.state_machine.add_event(('HP_OUT', 0))
        skul.x += skul.face_dir * 2
        if (skul.x - skul.init_x) * skul.face_dir >= 180:
            skul.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(skul):
        if skul.face_dir == 1:
            skul.image.clip_draw(5, 1160, 42, 28, skul.x, skul.y, 42 * 2, 28 * 2)
        else:
            skul.image.clip_composite_draw(5, 1160, 42, 28, 0, 'h', skul.x, skul.y, 42 * 2, 28 * 2)
        pass

class Air_move:
    @staticmethod
    def enter(skul, e):
        if not skul.do_jump:
            skul.jump_sound = load_wav("./audio_clip/" + 'Default_Jump.wav')
            skul.jump_sound.set_volume(20)
            skul.jump_sound.play()
            skul.do_jump = True
        if right_down(e) or left_up(e): # 오른쪽으로 MOVE
            skul.face_dir = 1
        elif left_down(e) or right_up(e): # 왼쪽으로 MOVE
            skul.face_dir = -1
        pass
    @staticmethod
    def exit(skul, e):
        pass
    @staticmethod
    def do(skul):
        if skul.hp <= 0:
            skul.state_machine.add_event(('HP_OUT', 0))
        # 속도 계산 및 위치 변경
        skul.jump_velocity += skul.gravity * game_framework.frame_time * 50  # 프레임 시간 기반 속도 변화
        skul.y += skul.jump_velocity * game_framework.frame_time * 50  # 프레임 시간 기반 위치 변화
        # 지면 충돌 처리

        if skul.y < 122:
            skul.y = 122
            skul.jump_velocity = 10  # 초기 점프 속도
            skul.jump_frame = 0
            skul.state_machine.add_event(('JUMP_OUT', 0))
            skul.do_jump = False

        # 애니메이션 프레임 처리
        skul.jump_frame = (skul.jump_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2

        skul.x += skul.face_dir * RUN_SPEED_PPS * game_framework.frame_time
        pass
    @staticmethod
    def draw(skul):
        if skul.jump_velocity > 0:
            jump_frames = [
                (5, 1111, 21, 36),
                (31, 1111, 22, 36)
            ]

            frame_index = int(skul.jump_frame)
            x, y, w, h = jump_frames[frame_index]

            if skul.face_dir == 1:
                skul.image.clip_draw(x, y, w, h, skul.x, skul.y, w * 2, h * 2)
            else:
                skul.image.clip_composite_draw(x, y, w, h, 0, 'h', skul.x, skul.y, w * 2, h * 2)
        else:
            jump_frames = [
                (5, 1062, 34, 36),
                (44, 1063, 34, 35)
            ]

            frame_index = int(skul.jump_frame)
            x, y, w, h = jump_frames[frame_index]

            if skul.face_dir == 1:
                skul.image.clip_draw(x, y, w, h, skul.x, skul.y, w * 2, h * 2)
            else:
                skul.image.clip_composite_draw(x, y, w, h, 0, 'h', skul.x, skul.y, w * 2, h * 2)

class Dead:
    @staticmethod
    def enter(skul, e):
        skul.frame = 0
        if skul.y > 120:
            skul.y = 120
        pass
    @staticmethod
    def exit(skul, e):
        pass
    @staticmethod
    def do(skul):
        if skul.hp <= 0:
            skul.state_machine.add_event(('HP_OUT', 0))
        if skul.frame < 2:
            skul.frame = (skul.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        pass
    @staticmethod
    def draw(skul):
        # Idle 애니메이션의 각 프레임 좌표와 크기
        dead_frames = [
            (5, 703, 41, 28),  # 첫 번째 프레임 (x, y, w, h)
            (51, 707, 41, 24),  # 두 번째 프레임
            (97, 710, 41, 21),  # 세 번째 프레임
        ]

        # 현재 프레임 정보 가져오기
        frame_index = int(skul.frame) % len(dead_frames)
        x, y, w, h = dead_frames[frame_index]

        # 프레임을 그리기
        if skul.face_dir == 1:
            skul.image.clip_draw(x, y, w, h, skul.x, skul.y - 20, w * 2, h * 2)
            skul.font.draw(830, 700, 'You lose', (0, 0, 0))
            skul.font.draw(700, 650, 'go practice mode: esc', (0, 0, 0))
        else:
            skul.image.clip_composite_draw(x, y, w, h, 0, 'h', skul.x, skul.y - 20, w * 2, h * 2)
            skul.font.draw(830, 700, 'You lose', (0, 0, 0))
            skul.font.draw(700, 650, 'go practice mode: esc', (0, 0, 0))
        pass







class Skul:
    def __init__(self, bar=None):
        self.jump_velocity = 10  # 초기 점프 속도
        self.gravity = -0.4  # 중력 가속도
        self.jump_frame = 0  # 점프 애니메이션 초기화
        self.ball = None
        self.do_jump = False
        self.x, self.y = 100, 120
        self.face_dir = 1
        self.hp = 150
        self.bar = bar
        self.font = load_font('NotoSans-Medium.ttf', 40)
        self.attack_animation_set = 1  # 공격 애니메이션 세트 (0 또는 1)
        self.image = load_image('기본 해골 스프라이트.png')
        self.healthimage = load_image('Player_HealthBar.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, c_down: Jump, x_down: Attack, z_down: Dash, hp_out: Dead},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, c_down: Air_move, x_down: Run_attack, z_down: Run_dash, hp_out: Dead},
                Jump: {right_down: Air_move, left_down: Air_move, right_up: Air_move, left_up: Air_move, jump_out: Idle, x_down: Jump_attack, z_down: Jump_Dash, hp_out: Dead},
                Air_move: {right_down: Jump, left_down: Jump, right_up: Jump, left_up: Jump, jump_out: Run, z_down: Jump_move_dash, x_down: Jump_move_attack, hp_out: Dead},
                Attack: {time_out: Idle, left_down: Run, right_down: Run, hp_out: Dead},
                Run_attack: {time_out: Run, left_up: Idle, right_up: Idle, hp_out: Dead},
                Jump_attack: {time_out: Jump, left_down: Air_move, right_down: Air_move, hp_out: Dead},
                Jump_move_attack: {time_out: Air_move, left_up: Jump, right_up: Jump, hp_out: Dead},
                Dash: {time_out: Idle, left_down: Run, right_down: Run, hp_out: Dead},
                Run_dash: {time_out: Run, left_up: Idle, right_up: Idle, hp_out: Dead},
                Jump_Dash: {time_out: Jump, left_down: Air_move, right_down: Air_move, hp_out: Dead},
                Jump_move_dash: {time_out: Air_move, left_up: Jump, right_up: Jump, hp_out: Dead},
                Dead: {}
            }
        )

    def update(self):
        self.state_machine.update()
        self.x = clamp(0, self.x, 1800)

    def handle_event(self, event):
        # 여기서 받을 수 있는 것만 걸러야 함. right left  등등..
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        if self.bar:
            self.healthimage.draw(608 + (516 / 150 * (150 - self.hp)) / 2, 776, 516 / 150 * self.hp, 44)
        # 충돌 영역 그리기
       #draw_rectangle(*self.get_bb())

    def get_bb(self):
        # 네개의 값을 리턴하는데, 사실 한개의 튜플
        if self.face_dir == 1:
            return  self.x-40, self.y-36, self.x+24, self.y+36
        else:
            return  self.x-24, self.y-36, self.x+40, self.y+36

    def get_attack_bb(self):
        if self.face_dir == 1:
            return self.x-40, self.y-55, self.x+58, self.y+55
        else:
            return self.x-58, self.y-55, self.x+40, self.y+55

    def handle_collision(self, group, other):
        # fill here
        if group == 'skul:stage1_tile':
            self.y = 122
            self.state_machine.add_event(('JUMP_OUT', 0))
        elif group == 'adventurerAttack:skul':
            self.hp -= 10
        elif group == 'Energyball:skul':
            self.EB_sound = load_wav("./audio_clip/" + 'AdventurerHero_EnergyBall.wav')
            self.EB_sound.set_volume(30)
            self.EB_sound.play()
            self.hp -= 5
        elif group == 'Energyblast:skul':
            self.hp -= 20
        pass