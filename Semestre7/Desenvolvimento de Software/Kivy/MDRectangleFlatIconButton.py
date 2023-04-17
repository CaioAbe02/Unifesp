from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.button import MDFloatingActionButtonSpeedDial

class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return (
            MDRectangleFlatIconButton (
                text = 'Hello World',
                font_size = '18sp',
                icon = 'language-python',
                icon_size = '64sp',
                icon_color = 'green',
                line_color = 'red',
                text_color = 'white'
            )
        )

MyApp().run()