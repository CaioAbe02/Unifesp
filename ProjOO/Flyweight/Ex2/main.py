import random
import sys
from Arvores.Arvore import EspecieArvore, Arvore
from Arvores.ArvoreFactory import ArvoreFactory

def tamanho_real(obj, visitados=None):
  if visitados is None:
    visitados = set()

  obj_id = id(obj)
  if obj_id in visitados:
    return 0

  visitados.add(obj_id)
  tamanho = sys.getsizeof(obj)

  if hasattr(obj, '__dict__'):
    for v in obj.__dict__.values():
      tamanho += tamanho_real(v, visitados)

  return tamanho

def main():
  factory = ArvoreFactory()

  araucaria = factory.getArvore("Araucaria", altura_min=20, altura_max=50, diametro_tronco_min=90, diametro_tronco_max=180, comprimento_folha_min=3, comprimento_folha_max=6)
  mandiocao = factory.getArvore("Mandiocão", altura_min=20, altura_max=30, diametro_tronco_min=60, diametro_tronco_max=90, comprimento_folha_min=20, comprimento_folha_max=40)
  guapuruvu = factory.getArvore("Guapuruvu", altura_min=20, altura_max=30, diametro_tronco_min=60, diametro_tronco_max=80, comprimento_folha_min=80, comprimento_folha_max=100)
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

  especies = [araucaria, mandiocao, guapuruvu, cedro, inga, araticum, barbatimao, embiricu, guatambu, uvaia, capitao, espeteiro, abrico_de_macaco]

  arvores_no_flyweight = []
  arvores_flyweight = []

  for especie in especies:
    for _ in range(10):
      altura = random.randint(especie.altura_min, especie.altura_max)
      diametro_tronco = random.randint(especie.diametro_tronco_min, especie.diametro_tronco_max)
      comprimento_folha = random.randint(especie.comprimento_folha_min, especie.comprimento_folha_max)

      arvore_no_fw = Arvore(
        especie=EspecieArvore(
          especie.especie,
          especie.altura_min,
          especie.altura_max,
          especie.diametro_tronco_min,
          especie.diametro_tronco_max,
          especie.comprimento_folha_min,
          especie.comprimento_folha_max
        ),
        altura=altura,
        diametro_tronco=diametro_tronco,
        comprimento_folha=comprimento_folha
      )
      arvores_no_flyweight.append(arvore_no_fw)

      arvore_fw = Arvore(
        especie=especie,
        altura=altura,
        diametro_tronco=diametro_tronco,
        comprimento_folha=comprimento_folha
      )
      arvores_flyweight.append(arvore_fw)
      arvore_fw.printArvore()

  visitados = set()
  tamanho_no_flyweight = sum(tamanho_real(arv, visitados) for arv in arvores_no_flyweight)

  visitados = set()
  tamanho_flyweight = sum(tamanho_real(arv, visitados) for arv in arvores_flyweight)

  print(f"Com flyweight: {tamanho_flyweight:,} bytes")
  print(f"Sem flyweight: {tamanho_no_flyweight:,} bytes")


if __name__ == "__main__":
  main()
