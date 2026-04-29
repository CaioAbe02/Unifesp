# Factory, Singleton, Proxy

from abc import ABC

class Smartphone(ABC):
  pass

class SamsungSmartphone(Smartphone):
  def getBrand(self) -> str:
     return "samsung"

class AppleSmartphone(Smartphone):
  def getBrand(self) -> str:
     return "apple"

class Inventory(object):
  __instance = None
  __stock = {}

  def __new__(cls):
    if cls.__instance is None:
      cls.__instance = object.__new__(cls)
      cls.__stock = {"samsung": 10}
    return cls.__instance

  def printStock(self):
     print(f"Inventário {hex(id(self))}: ")

class SmartphoneFactory:
  @staticmethod
  def create() -> Smartphone:
    print("Utiizando os smartphones da Samsung")
    return SamsungSmartphone()

class Main:

    def f(self) -> None:
        inventory: Inventory = Inventory()
        print(f"Inventario {inventory}")
        c: Smartphone = SmartphoneFactory.create()

    def g(self) -> None:
        inventory: Inventory = Inventory()
        c: Smartphone = SmartphoneFactory.create()

    def h(self) -> None:
        inventory: Inventory = Inventory()
        c: Smartphone = SmartphoneFactory.create()

    @staticmethod
    def main() -> None:
        m = Main()
        m.f()
        m.g()
        m.h()

if __name__ == "__main__":
    Main.main()
