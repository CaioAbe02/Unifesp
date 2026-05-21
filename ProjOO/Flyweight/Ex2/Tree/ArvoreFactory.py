from Arvore import Arvore

class ArvoreFactory:
  def __init__(self):
    self.arvores_pool = []

  def getArvore(self, especie: str):
    arvore = next((arvore for arvore in self.algoritmos_pool if arvore.especie == especie), None)

    if arvore is None:
      arvore = Arvore(especie)
      self.arvores_pool.append(arvore)

    return arvore