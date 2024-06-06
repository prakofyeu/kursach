from kivy.uix.widget import Widget





class Obstacle(Widget):
    def __init__(self, pos = None, object_id = 1, texture_path = 'fish.png', **kwargs):
        super().__init__(**kwargs)
        if pos == None:
            pos = 0,0
        self.id = object_id
        self.pos = pos
        self.size = 30, 30
        self.source = texture_path
    def obstacle_collision(self, ball):
        if self.collide_widget(ball):
            # print(f"collision with {self.id}")
            return True