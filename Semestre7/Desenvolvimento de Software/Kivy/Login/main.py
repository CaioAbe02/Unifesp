from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

class TelaInicial(Screen):
    pass

class Padrao(Screen):
    pass

class Cadastro(Screen):
    pass

class Login(Screen):
    pass

class WindowManager(ScreenManager):
    pass


class MyApp(MDApp):
    def build(self):
        return Builder.load_file("main.kv")

    def close_app(self):
        MDApp.get_running_app().stop()
        Window.close()

MyApp().run()