from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.clock import Clock

class LogoScreen(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.switch_to_main_menu, 2)

    def switch_to_main_menu(self, dt):
        self.manager.transition = FadeTransition()
        self.manager.current = 'main_menu'

class MainMenu(Screen):
    pass

class AddProduct(Screen):
    pass

class ViewProduct(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class PrecoBom(MDApp):
    def build(self):
        main_kv = Builder.load_file("kv/main.kv")
        self.theme_cls.theme_style = "Dark"

        return main_kv

    def calculate_discount(self, original_price, new_price):
       return 100 - (original_price / new_price) * 100

    def new_price_text(self, new_price, discount):
        return f"R${new_price}     {self.get_number_sign(discount)}{abs(int(discount))}%"

    def get_number_sign(self, number):
        if number > 0:
            return "+"
        elif number < 0:
            return "-"
        else:
            return ""


PrecoBom().run()