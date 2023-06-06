from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.app import MDApp
from kivy.app import App
from kivy.lang import Builder
import requests
import json

URL = "https://desenvolvimento-de-softw-5bbfe-default-rtdb.firebaseio.com/.json"
DICT_DADOS = requests.get(URL).json()

class Tabs(MDBoxLayout, MDTabsBase):
    pass

class MainScreen(MDScreen):
    pass

class Cadastro(MDScreen):
    def validar_dados(self, cpf, endereco, idade, nascimento, nome, salario):
        if not self.validar_cpf(cpf):
            return False
        elif not self.validar_endereco(endereco):
            return False
        elif not self.validar_idade(idade):
            return False
        elif not self.validar_nascimento(nascimento):
            return False
        elif not self.validar_nome(nome):
            return False
        elif not self.validar_salario(salario):
            return False
        return True

    def validar_cpf(self, cpf):
        cpf = cpf.replace(".", "").replace("-", "")
        if len(cpf) == 0:
            self.ids.aviso.text = "CPF não pode estar vazio"
            return False
        elif not cpf.isdigit():
            self.ids.aviso.text = "CPF possui caractéres inválidos"
            return False
        elif not len(cpf) == 11:
            self.ids.aviso.text = "CPF não possui 11 dígitos"
            return False
        elif not self.cpf_is_uniq(cpf):
            self.ids.aviso.text = "CPF já cadastrado"
            return False
        return True

    def cpf_is_uniq(self, new_cpf):
        for cadastro in DICT_DADOS.values():
            cpf = cadastro.get('CPF').replace(".", "").replace("-", "")
            if new_cpf == cpf:
                return False
        return True

    def formatar_cpf(self, cpf):
        cpf = cpf.replace(".", "").replace("-", "")
        cpf_formatado = cpf_formatado = "{}.{}.{}-{}".format(cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])
        return cpf_formatado

    def validar_endereco(self, validar_endereco):
        if len(validar_endereco) == 0:
            self.ids.aviso.text = "Endereço não pode estar vazio"
            return False
        return True

    def validar_idade(self, idade):
        if len(idade) == 0:
            self.ids.aviso.text = "Idade não pode estar vazio"
            return False
        elif not idade.isdigit():
            self.ids.aviso.text = "Idade não é um número"
            return False
        return True

    def validar_nascimento(self, nascimento):
        if len(nascimento) == 0:
            self.ids.aviso.text = "Data de nascimento não pode estar vazio"
            return False
        return True

    def validar_nome(self, nome):
        if len(nome) == 0:
            self.ids.aviso.text = "Nome não pode estar vazio"
            return False
        return True

    def validar_salario(self, salario):
        if len(salario) == 0:
            self.ids.aviso.text = "Salário não pode estar vazio"
            return False
        elif not salario.isdigit():
            self.ids.aviso.text = "Salário não é um número"
            return False
        return True

    def resetar(self):
        self.ids.cpf.text = ""
        self.ids.endereco.text = ""
        self.ids.idade.text = ""
        self.ids.nascimento.text = ""
        self.ids.nome.text = ""
        self.ids.salario.text = ""
        self.ids.aviso.text = ""

class Pesquisa(MDScreen):
    def validar_cpf(self, cpf):
        cpf = cpf.replace(".", "").replace("-", "")
        if len(cpf) == 0:
            self.ids.aviso.text = "CPF não pode estar vazio"
            return False
        elif not cpf.isdigit():
            self.ids.aviso.text = "CPF possui caractéres inválidos"
            return False
        elif not len(cpf) == 11:
            self.ids.aviso.text = "CPF não possui 11 dígitos"
            return False
        elif self.cpf_is_uniq(cpf):
            self.ids.aviso.text = "CPF não encontrado"
            return False
        return True

    def cpf_is_uniq(self, new_cpf):
        for cadastro in DICT_DADOS.values():
            cpf = cadastro.get('CPF').replace(".", "").replace("-", "")
            if new_cpf == cpf:
                self.aparecer_textfields(cadastro)
                self.desabilitar_cpf()
                self.posicionar_botoes()
                return False
        return True

    def aparecer_textfields(self, cadastro):
        self.ids.endereco.pos_hint = {'center_x': .5}
        self.ids.endereco.text = cadastro['endereco']
        self.ids.idade.pos_hint = {'center_x': .5}
        self.ids.idade.text = str(cadastro['idade'])
        self.ids.nascimento.pos_hint = {'center_x': .5}
        self.ids.nascimento.text = cadastro['nascimento']
        self.ids.nome.pos_hint = {'center_x': .5}
        self.ids.nome.text = cadastro['nome']
        self.ids.salario.pos_hint = {'center_x': .5}
        self.ids.salario.text = str(cadastro['salario'])
        self.ids.aviso.text = "CPF encontrado!"

    def desabilitar_cpf(self):
        self.ids.cpf.disabled = True

    def posicionar_botoes(self):
        self.ids.pesquisar.pos_hint = {'center_x': 2}
        self.ids.modificar.pos_hint = {'center_x': .5}

    def resetar(self):
        self.ids.cpf.disabled = False
        self.ids.cpf.text = ""
        self.ids.endereco.text = ""
        self.ids.endereco.pos_hint = {'center_x': 2}
        self.ids.idade.text = ""
        self.ids.idade.pos_hint = {'center_x': 2}
        self.ids.nascimento.text = ""
        self.ids.nascimento.pos_hint = {'center_x': 2}
        self.ids.nome.text = ""
        self.ids.nome.pos_hint = {'center_x': 2}
        self.ids.salario.text = ""
        self.ids.salario.pos_hint = {'center_x': 2}

        self.ids.aviso.text = ""

        self.ids.pesquisar.pos_hint = {'center_x': .5}
        self.ids.modificar.pos_hint = {'center_x': 2}

class MyApp(MDApp):
    def build(self):
        Builder.load_file('cadastro.kv')
        Builder.load_file('pesquisa.kv')
        Builder.load_file('main_screen.kv')
        return MainScreen()

    def register(self, cpf, endereco, idade, nascimento, nome, salario):
        cadastro = self.root.ids.cadastro

        if not cadastro.validar_dados(cpf, endereco, idade, nascimento, nome, salario):
            return False

        dados_novos = {
            'CPF': cadastro.formatar_cpf(cpf),
            'endereco': endereco,
            'idade': int(idade),
            'nascimento': nascimento,
            'nome': nome,
            'salario': int(salario)
        }
        global DICT_DADOS
        if DICT_DADOS == {}:
            DICT_DADOS = {'cadastro1' : dados_novos}
        else:
            novo_cadastro = f"cadastro{len(DICT_DADOS)+1}"
            DICT_DADOS.update({novo_cadastro: dados_novos})

        print("DICT_DADOS atualizado:", DICT_DADOS, "\n")
        requests.patch(URL, data=json.dumps(DICT_DADOS))

        return True

    def pesquisar(self, cpf):
        pesquisa = self.root.ids.pesquisa
        if not pesquisa.validar_cpf(cpf):
            return False
        return True

    def modificar(self, cpf, endereco, idade, nascimento, nome, salario):
        cpf = cpf.replace(".", "").replace("-", "")
        print(cpf)
        for cadastro in DICT_DADOS.values():
            dados_cpf = cadastro.get('CPF').replace(".", "").replace("-", "")
            print(dados_cpf)
            if dados_cpf == cpf:
                cadastro['endereco'] = endereco
                cadastro['idade'] = idade
                cadastro['nascimento'] = nascimento
                cadastro['nome'] = nome
                cadastro['salario'] = salario
                requests.patch(URL, data=json.dumps(DICT_DADOS))
                self.root.ids.pesquisa.ids.aviso.text = "Dados modificados com sucesso"

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        pesquisa = self.root.ids.pesquisa
        cadastro = self.root.ids.cadastro
        pesquisa.resetar()
        cadastro.resetar()
MyApp().run()
