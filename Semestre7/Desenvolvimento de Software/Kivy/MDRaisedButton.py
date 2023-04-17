from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton

class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        return (
            MDScreen (
                MDRaisedButton (
                    text = "Primary light",
                    pos_hint = {"center_x": .5, "center_y": .7},
                    md_bg_color = self.theme_cls.primary_light
                ),
                MDRaisedButton (
                    text = "Primary color",
                    pos_hint = {"center_x": .5, "center_y": .5}
                ),
                MDRaisedButton (
                    text = "Primary dark",
                    pos_hint = {"center_x": .5, "center_y": .3},
                    md_bg_color = self.theme_cls.primary_dark
                )
            )
        )

MyApp().run()