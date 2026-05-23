from abc import ABC, abstractmethod

class IArvore(ABC):
  @abstractmethod
  def printArvore():
    pass

class EspecieArvore(IArvore):
  def __init__(
    self,
    especie: str,
    altura_min: int,
    altura_max: int,
    diametro_tronco_min: int,
    diametro_tronco_max: int,
    comprimento_folha_min: int,
    comprimento_folha_max: int
  ):
    self.especie = especie
    self.altura_min = altura_min
    self.altura_max = altura_max
    self.diametro_tronco_min = diametro_tronco_min
    self.diametro_tronco_max = diametro_tronco_max
    self.comprimento_folha_min = comprimento_folha_min
    self.comprimento_folha_max = comprimento_folha_max

  def printArvore(self):
    print(f"-= {self.especie} =-")
    print(f"Altura: {self.altura_min} a {self.altura_max} m")
    print(f"Diâmetro do tronco: {self.diametro_tronco_min} a {self.diametro_tronco_max} cm")
    print(f"Comprimento da folha: {self.comprimento_folha_min} a {self.comprimento_folha_max} cm")
    print()

class Arvore(IArvore):
  def __init__(self, especie: EspecieArvore, altura: int, diametro_tronco: int, comprimento_folha: int):
    self.especie = especie
    self.altura = altura
    self.diametro_tronco = diametro_tronco
    self.comprimento_folha = comprimento_folha

  def printArvore(self):
    print(f"-= {self.especie.especie} =-")
    print(f"Altura: {self.altura} m ({self.especie.altura_min} a {self.especie.altura_max} m)")
    print(f"Diâmetro do tronco: {self.diametro_tronco} cm ({self.especie.diametro_tronco_min} a {self.especie.diametro_tronco_max} cm)")
    print(f"Comprimento da folha: {self.comprimento_folha} cm ({self.especie.comprimento_folha_min} a {self.especie.comprimento_folha_max} cm)")
    print()