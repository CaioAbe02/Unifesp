from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.behaviors import DragBehavior
from kivy.lang import Builder

class DragLabel(DragBehavior, Label):
    pass


class MyApp(App):
    def build(self):
        return Builder.load_file("DragLabel.kv")

MyApp().run()