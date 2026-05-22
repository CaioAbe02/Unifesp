from .Arvore import EspecieArvore

class ArvoreFactory:
  def __init__(self):
    self.arvores_pool = []

  def getArvore(
    self,
    especie: str,
    altura_min: int,
    altura_max: int,
    diametro_tronco_min: int,
    diametro_tronco_max: int,
    comprimento_folha_min: int,
    comprimento_folha_max: int
  ):
    arvore = next((arvore for arvore in self.arvores_pool if arvore.especie == especie), None)

    if arvore is None:
      arvore = EspecieArvore(especie, altura_min, altura_max, diametro_tronco_min, diametro_tronco_max, comprimento_folha_min, comprimento_folha_max)
      self.arvores_pool.append(arvore)

    return arvore