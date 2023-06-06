from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
import requests
import json

DICT_DADOS = {}

class Registrar(MDScreen):
    pass

class Cadastro(MDApp):
    def build(self):
        return Builder.load_file("main.kv")

    def register(self, cpf, endereco, idade, nascimento, nome, salario):
        dados = requests.get("https://desenvolvimento-de-softw-5bbfe-default-rtdb.firebaseio.com/.json")
        DICT_DADOS = dados.json()

        if not self.validar_dados(cpf, endereco, idade, nascimento, nome, salario):
            return False

        dados_novos = {
            'CPF': self.formatar_cpf(cpf),
            'endereco': endereco,
            'idade': int(idade),
            'nascimento': nascimento,
            'nome': nome,
            'salario': int(salario)
        }

        if not DICT_DADOS:
            DICT_DADOS = {'cadastro1' : dados_novos}
        else:
            novo_cadastro = f"cadastro{len(DICT_DADOS)+1}"
            DICT_DADOS.update({novo_cadastro: dados_novos})

        print("DICT_DADOS atualizado:", DICT_DADOS, "\n")
        requests.patch("https://desenvolvimento-de-softw-5bbfe-default-rtdb.firebaseio.com/.json", data=json.dumps(DICT_DADOS))

        return True

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
            self.root.ids.aviso.text = "CPF não pode estar vazio"
            return False
        elif not cpf.isdigit():
            self.root.ids.aviso.text = "CPF possui caractéres inválidos"
            return False
        elif not len(cpf) == 11:
            self.root.ids.aviso.text = "CPF não possui 11 dígitos"
            return False
        elif not self.cpf_is_uniq(cpf):
            self.root.ids.aviso.text = "CPF já cadastrado"
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
            self.root.ids.aviso.text = "Endereço não pode estar vazio"
            return False
        return True

    def validar_idade(self, idade):
        if len(idade) == 0:
            self.root.ids.aviso.text = "Idade não pode estar vazio"
            return False
        elif not idade.isdigit():
            self.root.ids.aviso.text = "Idade não é um número"
            return False
        return True

    def validar_nascimento(self, nascimento):
        if len(nascimento) == 0:
            self.root.ids.aviso.text = "Data de nascimento não pode estar vazio"
            return False
        return True

    def validar_nome(self, nome):
        if len(nome) == 0:
            self.root.ids.aviso.text = "Nome não pode estar vazio"
            return False
        return True

    def validar_salario(self, salario):
        if len(salario) == 0:
            self.root.ids.aviso.text = "Salário não pode estar vazio"
            return False
        elif not salario.isdigit():
            self.root.ids.aviso.text = "Salário não é um número"
            return False
        return True



Cadastro().run()