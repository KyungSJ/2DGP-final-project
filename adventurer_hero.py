import math
import random

from pico2d import load_image, draw_rectangle

import adventurerAttack
import adventurer_hero
import game_framework
import game_world
import play_mode
from EnergyBall import EnergyBall
from EnergyBlast import EnergyBlast
from Energy_blast_attack_range import Energy_blast_attack_range
from adventurerAttack import adventurerAttack
from behavior_tree import BehaviorTree, Condition, Sequence, Action, Selector

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 300.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
IDLE_FRAMES_PER_ACTION = 6.0
WALK_FRAMES_PER_ACTION = 5.0
ATTACK_FRAMES_PER_ACTION = 10.0
INTRO_FRAMES_PER_ACTION = 8.0
ENERGYBALL_FRAMES_PER_ACTION = 15.0
EXPLOSION_LOOP_FRAMES_PER_ACTION = 1.0

animation_names = ['Idle', 'Intro', 'Walk', 'Attack', 'EnergyBall', 'Explosion_Loop', 'Dead']

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
                elif name == 'Explosion_Loop':
                    Adventurer_hero.images[name] = [load_image("./adventurer_hero/" + name + "_%d" % i + ".png") for i in range(0, 9)]
                elif name == 'Dead':
                    Adventurer_hero.images[name] = [load_image("./adventurer_hero/" + name + "_%d" % i + ".png") for i in range(0, 1)]

    def __init__(self, x=None, y=None):
        self.energy_blast_attack_range = None
        self.x = x
        self.y = y
        self.hp = 200
        self.load_images()
        self.dir = 180.0
        self.speed = 0.0
        self.frame = 0
        self.state = "Idle"
        self.intro = False
        self.explosion = True
        self.random = 3
        self.unbeatable = False
        self.healthimage = load_image('AdventurerHealthBar.png')
        self.recentframe = 0
        self.recentframe2 = 0

        self.build_behavior_tree()


    def get_bb(self):
        if not self.unbeatable:
            return self.x - 36 * 2, self.y - 31 * 2, self.x + 36 * 2, self.y + 31 * 2
        else:
            return self.x+20000, self.y+20000, self.x+20000, self.y+20000


    def get_Attack_bb(self):
        if math.cos(self.dir) < 0:
            return self.x - 36 * 2, self.y - 31 * 2, self.x + 36 * 2, self.y + 31 * 2
        else:
            return self.x - 36 * 2, self.y - 31 * 2, self.x + 36 * 2, self.y + 31 * 2


    def update(self):
        print(self.recentframe2)
        if self.state == 'Idle':
            self.frame = (self.frame + IDLE_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % IDLE_FRAMES_PER_ACTION
        elif self.state == 'Intro':
            self.frame += INTRO_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
            if int(self.frame) >= 43:
                self.state = 'Idle'
                self.frame = 0
                self.intro = True
                self.unbeatable = False
                print('Intro 끝')
        elif self.state == 'Walk':
            self.frame = (self.frame + WALK_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % WALK_FRAMES_PER_ACTION
        elif self.state == 'Attack':
            self.recentframe += 1
            if self.recentframe == 390 or self.recentframe == 602 or self.recentframe == 780:
                adventurer_hero.adventurerattack = adventurerAttack(self.x, self.y, self.dir)
                game_world.add_object(adventurer_hero.adventurerattack, 2)
                game_world.add_collision_pair('adventurerAttack:skul', adventurer_hero.adventurerattack, None)
            elif self.recentframe == 426 or self.recentframe == 638 or self.recentframe == 816:
                if adventurer_hero.adventurerattack.alive:
                    game_world.remove_object(adventurer_hero.adventurerattack)
            self.frame += ATTACK_FRAMES_PER_ACTION * (ACTION_PER_TIME / 2.0) * game_framework.frame_time
            if int(self.frame) == 11 or int(self.frame) == 17 or int(self.frame) == 22:
                self.dir = math.atan2(play_mode.skul.y - self.y, play_mode.skul.x - self.x)
                self.x += 3 * math.cos(self.dir)
            if int(self.frame) >= 35:
                self.state = 'Idle'
                self.recentframe = 0
                self.frame = 0
                self.random = random.randint(1, 4)
        elif self.state == 'EnergyBall':
            self.frame += ENERGYBALL_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
            if int(self.frame) >= 15:
                self.state = 'Idle'
                self.frame = 0
                self.random = random.randint(1, 4)
        elif self.state == 'Explosion_Loop':
            self.recentframe2 += 1
            self.frame += EXPLOSION_LOOP_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
            if int(self.frame) == 2:
                if self.explosion:
                    energyblast = EnergyBlast(self.x - 20, self.y + 30)
                    game_world.add_object(energyblast, 2)
                    self.energy_blast_attack_range = Energy_blast_attack_range(self.x - 20, self.y + 30)
                    game_world.add_object(self.energy_blast_attack_range, 2)
                    game_world.add_collision_pair('Energyblast:skul', self.energy_blast_attack_range, None)
                    self.explosion = False
            if self.recentframe2 == 342:
                if self.energy_blast_attack_range.alive:
                    game_world.remove_object(self.energy_blast_attack_range)
            if int(self.frame) >= 9:
                self.state = 'Idle'
                self.frame = 0
                self.explosion = True
                self.recentframe2 = 0
                self.random = random.randint(1, 4)
        self.bt.run()


    def draw(self):
        if math.cos(self.dir) < 0:
            if self.state == 'Explosion_Loop':
                Adventurer_hero.images[self.state][int(self.frame)].composite_draw(0, 'h', self.x, self.y + 54, 72 * 2, 116 * 2)
            elif self.state == 'Dead':
                Adventurer_hero.images[self.state][0].composite_draw(0, 'h', self.x, self.y - 50, 70 * 2, 23 * 2)
            else:
                Adventurer_hero.images[self.state][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 72 * 2, 62 * 2)
        else:
            if self.state == 'Explosion_Loop':
                Adventurer_hero.images[self.state][int(self.frame)].draw(self.x, self.y + 54, 72 * 2, 116 * 2)
            elif self.state == 'Dead':
                Adventurer_hero.images[self.state][0].draw(self.x, self.y - 50, 70 * 2, 23 * 2)
            else:
                Adventurer_hero.images[self.state][int(self.frame)].draw(self.x, self.y, 72 * 2, 62 * 2)
        self.healthimage.draw(1192 - (516 / 200 * (200 - self.hp)) / 2, 776, 516 / 200 * self.hp, 44)

        #draw_rectangle(*self.get_bb())
        pass

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'skulAttack:adventurer':
            self.hp -= 5
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

    def is_not_skul_nearby(self, r):
        if self.distance_less_than(play_mode.skul.x, play_mode.skul.y, self.x, self.y, r):
            return BehaviorTree.FAIL
        else:
            return BehaviorTree.SUCCESS

    def is_skul_nearby(self, r):
        if self.distance_less_than(play_mode.skul.x, play_mode.skul.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL


    def move_to_skul(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(play_mode.skul.x, play_mode.skul.y)
        if self.x - play_mode.skul.x < -100 or self.x - play_mode.skul.x > 100:
            return BehaviorTree.SUCCESS
        else:
            self.frame = 0
            self.random = random.randint(1, 4)
            return BehaviorTree.FAIL

    def do_Intro(self):
        self.state = 'Intro'
        self.unbeatable = True
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

    def is_random3(self):
        if self.random == 3:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def is_random4(self):
        if self.random == 4:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def is_died(self):
        if self.hp <= 0:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def Energy_ball(self):
        if self.state != 'EnergyBall':  # 중복 실행 방지
            energyball = EnergyBall(self.x + 10 * math.cos(self.dir), self.y)
            game_world.add_object(energyball, 2)
            game_world.add_collision_pair('Energyball:skul', energyball, None)
            game_world.add_collision_pair('skulAttack:Energyball', None, energyball)
            self.state = 'EnergyBall'
            self.frame = 0  # 애니메이션 초기화
        return BehaviorTree.SUCCESS
        pass

    def do_Energy_blast(self):
        if self.state != 'Explosion_Loop':
            self.state = 'Explosion_Loop'
            self.frame = 0
        pass

    def dead(self):
        if self.state != 'Dead':
            self.state = 'Dead'
            self.random = 0
        pass

    def build_behavior_tree(self):
        c1 = Condition('Intro를 안했는가?', self.is_Intro_do)
        a1 = Action('Intro 하기', self.do_Intro)

        root = is_do_intro = Sequence('Intro 하기', c1, a1)

        c2 = Condition('랜덤값이 4 인가?', self.is_random4)
        a2 = Action('스컬 한테 가기', self.move_to_skul)

        root = chase_skul = Sequence('스컬 한테 가기', c2, a2)

        c3 = Condition('랜덤값이 1 인가?', self.is_random1)
        a3 = Action('3단 검법 휘두르기', self.Attack)

        root = attack_skul = Sequence('스컬 3단 검법으로 공격하기', c3, a3)

        c4 = Condition('랜덤값이 2 인가?', self.is_random2)
        a4 = Action('에니지 볼', self.Energy_ball)

        root = EnergyBall_to_skul = Sequence('에너지볼 스컬한테 발사', c4, a4)

        c5 = Condition('랜덤값이 3 인가?', self.is_random3)
        a5 = Action('기폭발', self.do_Energy_blast)

        root = EnergyBlast_to_skul = Sequence('스컬에게 기폭발', c5, a5)

        c6 = Condition('모함가의 체력이 0이하인가?', self.is_died)
        a6 = Action('죽음', self.dead)

        root = Adventurer_dead = Sequence('모험가의 죽음', c6, a6)

        root = intro_and_chase = Selector('인트로하고 패턴', is_do_intro,Adventurer_dead, chase_skul, attack_skul, EnergyBall_to_skul, EnergyBlast_to_skul)

        self.bt = BehaviorTree(root)
        pass

