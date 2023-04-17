from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFloatingActionButtonSpeedDial

class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        return (
            MDScreen (
                MDFloatingActionButtonSpeedDial (
                    data = {
                        'Python': 'language-python',
                        'PHP': 'language-php',
                        'C': 'language-c'
                    },
                    root_button_anim = True
                )
            )
        )

MyApp().run()