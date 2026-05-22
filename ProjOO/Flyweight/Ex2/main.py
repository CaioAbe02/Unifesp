from Arvores.Arvore import EspecieArvore, Arvore
from Arvores.ArvoreFactory import ArvoreFactory

def main():
  factory = ArvoreFactory()

  araucaria = factory.getArvore("Araucaria", altura_min=20, altura_max=50, diametro_tronco_min=90, diametro_tronco_max=180, comprimento_folha_min=3, comprimento_folha_max=6)
  mandiocao = factory.getArvore("Mandiocão", altura_min=20, altura_max=30, diametro_tronco_min=60, diametro_tronco_max=90, comprimento_folha_min=20, comprimento_folha_max=40)
  guapuruvu = factory.getArvore("Araucaria", altura_min=20, altura_max=30, diametro_tronco_min=60, diametro_tronco_max=80, comprimento_folha_min=80, comprimento_folha_max=100)
  cedro = factory.getArvore("Cedro", altura_min=20, altura_max=35, diametro_tronco_min=60, diametro_tronco_max=90, comprimento_folha_min=60, comprimento_folha_max=100)
  inga = factory.getArvore("Ingá", altura_min=5, altura_max=10, diametro_tronco_min=20, diametro_tronco_max=30, comprimento_folha_min=4, comprimento_folha_max=14)
  araticum = factory.getArvore("Araticum", altura_min=3, altura_max=10, diametro_tronco_min=20, diametro_tronco_max=30, comprimento_folha_min=9, comprimento_folha_max=15)
  barbatimao = factory.getArvore("Barbatimão", altura_min=4, altura_max=5, diametro_tronco_min=20, diametro_tronco_max=30, comprimento_folha_min=3, comprimento_folha_max=5)
  embiricu = factory.getArvore("Embiriçu", altura_min=6, altura_max=10, diametro_tronco_min=30, diametro_tronco_max=40, comprimento_folha_min=7, comprimento_folha_max=13)
  guatambu = factory.getArvore("Guatambú", altura_min=15, altura_max=20, diametro_tronco_min=40, diametro_tronco_max=50, comprimento_folha_min=9, comprimento_folha_max=15)
  uvaia = factory.getArvore("Uvaia", altura_min=6, altura_max=13, diametro_tronco_min=30, diametro_tronco_max=50, comprimento_folha_min=4, comprimento_folha_max=7)
  capitao = factory.getArvore("Capitão", altura_min=8, altura_max=16, diametro_tronco_min=40, diametro_tronco_max=50, comprimento_folha_min=6, comprimento_folha_max=14)
  espeteiro = factory.getArvore("Espeteiro", altura_min=10, altura_max=40, diametro_tronco_min=50, diametro_tronco_max=90, comprimento_folha_min=4, comprimento_folha_max=8)
  abrico_de_macaco = factory.getArvore("Abricó-de-macaco", altura_min=8, altura_max=15, diametro_tronco_min=30, diametro_tronco_max=50, comprimento_folha_min=15, comprimento_folha_max=20)

  araucaria.printArvore()

if __name__ == "__main__":
  main()
