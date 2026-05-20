from abc import ABC, abstractmethod
import random

class Algoritmo(ABC):
  def __init__(self, id: int):
    self.id = id

class AlgoritmoConcreto(Algoritmo):
  def __init__(self, id: int):
    super().__init__(id)

class AlgoritmosFacotory:
  def __init__(self):
    self.algoritmos_pool = []
    self.num_instancias = 0
    self.instancias = []

  def getAlgoritmo(self, algoritmo: int):
    alg = next((alg for alg in self.algoritmos_pool if alg.id == algoritmo), None)

    if alg is None:
      alg = AlgoritmoConcreto(algoritmo)
      self.algoritmos_pool.append(alg)
      self.num_instancias += 1
      self.instancias.append(alg.id)

    return alg

def main():
  factory = AlgoritmosFacotory()

  for _ in range(10):
    for _ in range(10):
      random_algoritmo = random.randint(0, 9)
      algoritmo = factory.getAlgoritmo(random_algoritmo)
      print(algoritmo.id, end="")
    print()

  print(f"Instâncias diferentes: {factory.num_instancias} | {factory.instancias}")

if __name__ == "__main__":
  main()