import math
import random

from pico2d import load_image, draw_rectangle

import game_framework
import play_mode
from behavior_tree import BehaviorTree, Condition, Sequence, Action, Selector

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 50.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
IDLE_FRAMES_PER_ACTION = 6.0
WALK_FRAMES_PER_ACTION = 5.0
ATTACK_FRAMES_PER_ACTION = 10.0
INTRO_FRAMES_PER_ACTION = 10.0
ENERGYBALL_FRAMES_PER_ACTION = 15.0

animation_names = ['Idle', 'Intro', 'Walk', 'Attack', 'EnergyBall']

class Adventurer_hero:
    images = None

    def load_images(self):
        if Adventurer_hero.images == None:
            Adventurer_hero.images = {}
            for name in animation_names:
                if name == 'Idle':
                    Adventurer_hero.images[name] = [load_image("./adventurer_hero/" + name + "_%d" % i + ".png") for i in range(0, 6)]
                elif name == 'Intro':
                    Adventurer_hero.images[name] = [load_image("./adventurer_hero/" + name + "_%d" % i + ".png") for i in range(0, 43)]
                elif name == 'Walk':
                    Adventurer_hero.images[name] = [load_image("./adventurer_hero/" + name + "_%d" % i + ".png") for i in range(0, 5)]
                elif name == 'Attack':
                    Adventurer_hero.images[name] = [load_image("./adventurer_hero/" + name + "_%d" % i + ".png") for i in range(0, 35)]
                elif name == 'EnergyBall':
                    Adventurer_hero.images[name] = [load_image("./adventurer_hero/" + name + "_%d" % i + ".png") for i in range(0, 15)]




    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
        self.load_images()
        self.dir = 180.0
        self.speed = 0.0
        self.frame = 0
        self.state = "Idle"
        self.intro = False
        self.random = 1

        self.build_behavior_tree()


    def get_bb(self):
        return self.x - 36 * 2, self.y - 31 * 2, self.x + 36 * 2, self.y + 31 * 2

    def get_Attack_bb(self):
        if math.cos(self.dir) < 0:
            return self.x - 36 * 2, self.y - 31 * 2, self.x + 36 * 2, self.y + 31 * 2
        else:
            return self.x - 36 * 2, self.y - 31 * 2, self.x + 36 * 2, self.y + 31 * 2


    def update(self):
        if self.state == 'Idle':
            self.frame = (self.frame + IDLE_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % IDLE_FRAMES_PER_ACTION
        elif self.state == 'Intro':
            self.frame += INTRO_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
            if int(self.frame) >= 43:
                self.state = 'Idle'
                self.frame = 0
                self.intro = True
                print('Intro 끝')
        elif self.state == 'Walk':
            self.frame = (self.frame + WALK_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % WALK_FRAMES_PER_ACTION
        elif self.state == 'Attack':
            self.frame += ATTACK_FRAMES_PER_ACTION * (ACTION_PER_TIME / 2.0) * game_framework.frame_time
            if int(self.frame) >= 35:
                self.state = 'Idle'
                self.frame = 0
                self.random = random.randint(1, 3)
        elif self.state == 'EnergyBall':
            self.frame += ENERGYBALL_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
            if int(self.frame) >= 15:
                self.state = 'Idle'
                self.frame = 0
                self.random = random.randint(1, 3)
        self.bt.run()


    def draw(self):
        if math.cos(self.dir) < 0:
            Adventurer_hero.images[self.state][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 72 * 2, 62 * 2)
        else:
            Adventurer_hero.images[self.state][int(self.frame)].draw(self.x, self.y, 72 * 2, 62 * 2)
        #draw_rectangle(*self.get_bb())
        pass

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        pass

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1-x2)**2 +(y1-y2)**2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty-self.y, tx-self.x)
        distance = RUN_SPEED_PPS * game_framework.frame_time
        self.x += distance * math.cos(self.dir)

    def is_Intro_do(self):
        if self.intro:
            return BehaviorTree.FAIL
        else:
            return BehaviorTree.SUCCESS

    def is_skul_nearby(self, r):
        if self.distance_less_than(play_mode.skul.x, play_mode.skul.y, self.x, self.y, r):
            return BehaviorTree.FAIL
        else:
            return BehaviorTree.SUCCESS

    def move_to_skul(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(play_mode.skul.x, play_mode.skul.y)
        if self.distance_less_than(play_mode.skul.x, play_mode.skul.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def do_Intro(self):
        self.state = 'Intro'
        return BehaviorTree.SUCCESS

    def is_random1(self):
        if self.random == 1:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def Attack(self):
        self.state = 'Attack'
        return BehaviorTree.SUCCESS

    def is_random2(self):
        if self.random == 2:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def Energy_ball(self):
        if self.state != 'EnergyBall':  # 중복 실행 방지
            self.state = 'EnergyBall'
            self.frame = 0  # 애니메이션 초기화
        return BehaviorTree.SUCCESS
        #energyball = EnergyBall(self.x, self.y, self.dir*10)
        pass

    def build_behavior_tree(self):
        c1 = Condition('Intro를 안했는가?', self.is_Intro_do)
        a1 = Action('Intro 하기', self.do_Intro)

        root = is_do_intro = Sequence('Intro 하기', c1, a1)

        c2 = Condition('스컬이 근처에 없는가?', self.is_skul_nearby, 4)
        a2 = Action('스컬 한테 가기', self.move_to_skul)

        root = chase_skul = Sequence('스컬 한테 가기', c2, a2)

        c3 = Condition('랜덤값이 1 인가?', self.is_random1)
        a3 = Action('3단 검법 휘두르기', self.Attack)

        root = attack_skul = Sequence('스컬 3단 검법으로 공격하기', c3, a3)

        c4 = Condition('랜덤값이 2 인가?', self.is_random2)
        a4 = Action('에니지 볼', self.Energy_ball)

        root = EnergyBall_to_skul = Sequence('에너지볼 스컬한테 발사', c4, a4)

        root = intro_and_chase = Selector('인트로하고 추적', is_do_intro, chase_skul, attack_skul, EnergyBall_to_skul)

        self.bt = BehaviorTree(root)
        pass

