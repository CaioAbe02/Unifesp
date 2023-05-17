from kivymd.app import MDApp
from kivy.lang import Builder

class MyApp(MDApp):
    def build(self):
        return Builder.load_file("DragBehavior+Image.kv")

MyApp().run()