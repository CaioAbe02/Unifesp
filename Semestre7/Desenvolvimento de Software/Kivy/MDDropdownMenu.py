from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu

class Test(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file("MDRaisedButton.kv")
        itens_do_menu = [
            {
                "text": f"Item {i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"Item {i}": self.imprime(x),
            } for i in range(5)
        ]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.botao,
            items=itens_do_menu,
            width_mult=3,
            max_height = dp(400),
            border_margin = dp(100),
            ver_growth = "down",
            hor_growth = "left",
            background_color = self.theme_cls.primary_light,
            radius = [24, 0, 24, 0]
        )

    def imprime(self, text_item):
        print(text_item)

    def build(self):
        return self.screen


Test().run()