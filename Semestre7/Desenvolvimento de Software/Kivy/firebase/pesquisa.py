from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
import requests
import json


class Pesquisa(MDScreen):
    pass

class MyApp(MDApp):
    dict_dados = {}
    def build(self):
        return Builder.load_file("pesquisa.kv")

    def pesquisar(self, cpf):
        if not self.validar_cpf(cpf):
            return False
        return True

    def validar_cpf(self, cpf):
        cpf = cpf.replace(".", "").replace("-", "")
        if len(cpf) == 0:
            self.root.ids.aviso.text = "CPF não pode estar vazio"
            return False
        elif not cpf.isdigit():
            self.root.ids.aviso.text = "CPF possui caractéres inválidos"
            return False
        elif not len(cpf) == 11:
            self.root.ids.aviso.text = "CPF não possui 11 dígitos"
            return False
        elif self.cpf_is_uniq(cpf):
            self.root.ids.aviso.text = "CPF não encontrado"
            return False
        return True

    def cpf_is_uniq(self, new_cpf):
        dados = requests.get("https://desenvolvimento-de-softw-5bbfe-default-rtdb.firebaseio.com/.json")
        self.dict_dados = dados.json()
        for cadastro in self.dict_dados.values():
            cpf = cadastro.get('CPF').replace(".", "").replace("-", "")
            if new_cpf == cpf:
                self.aparecer_textfields(cadastro)
                self.desabilitar_cpf()
                self.posicionar_botoes()
                return False
        return True

    def aparecer_textfields(self, cadastro):
        self.root.ids.endereco.pos_hint = {'center_x': .5}
        self.root.ids.endereco.text = cadastro['endereco']
        self.root.ids.idade.pos_hint = {'center_x': .5}
        self.root.ids.idade.text = str(cadastro['idade'])
        self.root.ids.nascimento.pos_hint = {'center_x': .5}
        self.root.ids.nascimento.text = cadastro['nascimento']
        self.root.ids.nome.pos_hint = {'center_x': .5}
        self.root.ids.nome.text = cadastro['nome']
        self.root.ids.salario.pos_hint = {'center_x': .5}
        self.root.ids.salario.text = str(cadastro['salario'])
        self.root.ids.aviso.text = "CPF encontrado!"

    def desabilitar_cpf(self):
        self.root.ids.cpf.disabled = True

    def posicionar_botoes(self):
        self.root.ids.pesquisar.pos_hint = {'center_x': 2}
        self.root.ids.modificar.pos_hint = {'center_x': .5}

    def modificar(self, cpf, endereco, idade, nascimento, nome, salario):
        cpf = cpf.replace(".", "").replace("-", "")
        print(cpf)
        for cadastro in self.dict_dados.values():
            dados_cpf = cadastro.get('CPF').replace(".", "").replace("-", "")
            print(dados_cpf)
            if dados_cpf == cpf:
                cadastro['endereco'] = endereco
                cadastro['idade'] = idade
                cadastro['nascimento'] = nascimento
                cadastro['nome'] = nome
                cadastro['salario'] = salario
                requests.patch("https://desenvolvimento-de-softw-5bbfe-default-rtdb.firebaseio.com/.json", data=json.dumps(self.dict_dados))
                self.root.ids.aviso.text = "Dados modificados com sucesso"

MyApp().run()