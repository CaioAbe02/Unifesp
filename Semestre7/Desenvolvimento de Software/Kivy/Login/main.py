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

    def cadastro(self, usuario, senha):
        erro = self.verificar_cadastro(usuario, senha)

        if erro != "":
            return erro

        banco_dados = open("usuarios.txt", "a")
        banco_dados.write("\n")
        banco_dados.write(usuario+","+senha)
        banco_dados.close()
        return "Cadastro realizado com sucesso!"

    def verificar_cadastro(self, usuario, senha):
        banco_dados = open("usuarios.txt", "r")
        erro = ""

        for line in banco_dados:
            params = line.split(",")
            if params[0] == usuario:
                erro = "Usuário já cadastrado"

        if len(usuario) > 10:
            erro = "Usuário não pode ter mais de 10 caracteres"
        elif len(senha) > 10:
            erro = "Senha não pode ter mais de 10 caracteres"
        elif len(usuario) == 0:
            erro = "Usuário não pode estar vazio"
        elif len(senha) == 0:
            erro = "Senha não pode estar vazio"

        banco_dados.close()
        return erro

    def login(self, usuario, senha):
        erro = self.verificar_login(usuario, senha)

        if erro != "":
            return erro

        return "Login realizado com sucesso!"

    def verificar_login(self, usuario, senha):
        banco_dados = open("usuarios.txt", "r")
        erro = ""
        achou_usuario = False

        for line in banco_dados:
            params = line.split(",")
            if params[0] == usuario:
                achou_usuario = True
                if params[1] != senha:
                    erro = "Senha incorreta!"

        if achou_usuario == False:
            erro = "Usuário não encontrado!"
        elif len(usuario) > 10:
            erro = "Usuário não pode ter mais de 10 caracteres"
        elif len(senha) > 10:
            erro = "Senha não pode ter mais de 10 caracteres"
        elif len(usuario) == 0:
            erro = "Usuário não pode estar vazio"
        elif len(senha) == 0:
            erro = "Senha não pode estar vazio"

        banco_dados.close()
        return erro

MyApp().run()