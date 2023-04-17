from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFloatingActionButtonSpeedDial

class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.primary_hue = "900"
        return (
            MDScreen (
                MDFloatingActionButtonSpeedDial (
                    id = 'speed_dial',
                    root_button_anim = True
                )
            )
        )
    def on_start(self):
        data = {
            "Python": 'language-python',
            "JS": [
                "language-javascript",
                "on_press", lambda x: print("pressed JS")
            ],
            "PHP": [
                "language-php",
                "on_press", lambda x: print("pressed PHP")
            ],
            "C++": [
                "language-cpp",
                "on_press", lambda x: print("pressed C++")
            ],
        }
        self.root.ids.speed_dial.data = data

MyApp().run()