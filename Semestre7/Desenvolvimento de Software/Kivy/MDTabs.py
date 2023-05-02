from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu

Window.size = [300, 500]

class Tabs(MDBoxLayout, MDTabsBase):
    pass


class Test(MDApp):
    def build(self):
        titles = [
            "Romance",
            "Drama"
        ]
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{title}",
                "height": dp(56),
                "on_release": lambda x=f"{title}": self.menu_callback(x),
             } for title in titles
        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )
        return Builder.load_file("MDTabs.kv")

    def callback(self, button):
        self.menu.caller = button
        self.menu.open()

    def menu_callback(self, text_item):
        self.menu.dismiss()

Test().run()