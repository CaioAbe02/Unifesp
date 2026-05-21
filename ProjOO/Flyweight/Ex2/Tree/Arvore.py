from abc import ABC, abstractmethod

class IArvore(ABC):
  pass

class EspecieArvore:
  def __init__(self, especie: str):
    self.especie = especie

class Arvore(IArvore):
  def __init__(self, especie: EspecieArvore):
    self.especie = especie