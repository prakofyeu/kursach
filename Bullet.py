from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.properties import (
    NumericProperty, ReferenceListProperty
)
Frame_rate = 20.0
Free_fall_acceleration = 9.81


class Bullet(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.velocity = self.velocity_x, self.velocity_y - (Free_fall_acceleration / Frame_rate)
        self.pos = Vector(*self.velocity) + self.pos