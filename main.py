import math
from math import sin, cos, atan, sqrt
from kivy.properties import StringProperty
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from Obstacle import Obstacle
from Bullet import Bullet
import cannon_constants as CONST
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

SCREEN_WIDTH: int = CONST.SCREEN_WIDTH
SCREEN_HEIGHT: int = CONST.SCREEN_HEIGHT
Initial_velocity = CONST.BULLET_MAX_VEL
Frame_rate = 20.0
score = 0

class FirstWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass

class AimWidget(Widget):
    def __init__(self, **kwargs):
        super(AimWidget, self).__init__(**kwargs)
        self.size = (CONST.SCREEN_WIDTH / 3, CONST.SCREEN_HEIGHT / 3)
        self.pos_hint = {'x': 0, 'y': 0}

    def on_touch_down(self, touch):
        print(f"Touch on aim_widget")
class SecondWindow(Screen):
    global score
    ball = ObjectProperty(None)
    ball_released = False
    start = False
    after = False
    obstacles_added = False
    obstacle = ObjectProperty(None)
    obstacles = ListProperty([])
    chosen_weapon = "bullet"
    score_label = Label(text = str(score))

    def __init__(self, **kwargs):
        super(SecondWindow, self).__init__(**kwargs)
    def change_weapon(self, weapon):
        self.chosen_weapon = weapon
        print(f"chosen weapon is {self.chosen_weapon}")

    def bullet_blast(self, target_block):
        pos = target_block.pos
        # print(len(self.obstacles))
        for obs in self.obstacles[:]:
            distance = sqrt((pos[0] - obs.pos[0])**2 + (pos[1] - obs.pos[1])**2)
            # print(obs.id)
            # print(distance)
            # print(CONST.BULLET_RADIUS)
            if distance <= CONST.BULLET_RADIUS:
                # print("deleted")
                self.remove_obstacle(obs)
            # print()
        # print(len(self.obstacles))
    def startGame(self):
        self.start = True

    def remove_obstacle(self, obstacle):
        global score
        self.remove_widget(obstacle)
        self.obstacles.remove(obstacle)
        score+=1
        print(score)

    def serve_ball(self, ang, coef):
        self.ball_released = True
        self.ball.pos = SCREEN_WIDTH / 3, SCREEN_HEIGHT / 3
        self.ball.velocity = (Initial_velocity * cos(ang) * coef, Initial_velocity * sin(ang) * coef)

    def spawn_ball(self):
        self.ball.pos = SCREEN_WIDTH / 3, SCREEN_HEIGHT / 3
        self.ball.velocity = (0, 0)
        self.ball_released = False

    def addObstacles(self, pos, object_id, n_of_obstacles_x, n_of_obstacles_y):
        print("obstacles added")
        for i in range(n_of_obstacles_x):
            for j in range(n_of_obstacles_y):
                obstacle = Obstacle(pos=(600 + 30 * i, 0 + 30 * j), object_id=int(f"{i}{j}"))
                self.add_widget(obstacle)
                self.obstacles.append(obstacle)
        self.obstacles_added = True

    def update(self, dt):
        for obstacle in self.obstacles:
            if obstacle.obstacle_collision(self.ball):
                self.bullet_blast(obstacle)
                self.spawn_ball()
                # self.remove_obstacle(obstacle)
        if self.ball_released:
            self.ball.move()
            if self.ball.pos[0] > CONST.SCREEN_WIDTH + 10:
                self.spawn_ball()

        if self.start:
            print("game started")
            but = self.ids["start_button"]
            self.remove_widget(but)
            self.start = False
            self.after = True

    # def on_touch_down(self, touch):
    #     if self.after:
    #         self.spawn_ball()
    #     else:
    #         Clock.schedule_once(lambda dt: self.on_touch_down(touch))
    #         return super(Game, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if (touch.x < self.width / 3) and (touch.y < self.height / 3):
            angle = atan((self.height / 3 - touch.y) / (self.width / 3 - touch.x))
            c = sqrt(((self.height / 3) - touch.y) ** 2 + (self.width / 3 - touch.x) ** 2) / sqrt(
                ((self.height / 3) ** 2 + (self.width / 3) ** 2))
            self.serve_ball(ang=angle, coef=c)


kv = Builder.load_file('main.kv')

class MyApp(App):
    def build(self):
        return kv
    
MyApp().run()