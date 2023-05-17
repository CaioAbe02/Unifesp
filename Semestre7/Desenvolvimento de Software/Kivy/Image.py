from kivymd.app import MDApp
from kivy.lang import Builder

kv = '''
MDGridLayout:
    cols: 3
    lins: 2
    padding: dp(10), dp(10)
    spacing: dp(4)

    Image:
        source: "imgs/flores1.jpg"
    #     pos_hint: {"center_x": .5, "center_y": .5}
    #     size_hint: .2, .3
    Image:
        source: "imgs/flores2.jpg"
        # allow_stretch: True
    Image:
        source: "imgs/flores3.jpg"
    Image:
        source: "imgs/flores4.jpg"
    Image:
        source: "imgs/flores5.jpg"
    Image:
        source: "imgs/flores6.jpg"
'''

class MyApp(MDApp):
    def build(self):
        root = Builder.load_string(kv)
        return root

MyApp().run()