class Drink:
  def cost(self):
    pass

  def description(self):
    pass

class Espresso(Drink):
  def cost(self):
    return 5

  def description(self):
    return "Espresso"

class Cappuccino(Drink):
  def cost(self):
    return 7

  def description(self):
    return "Cappuccino"

class Tea(Drink):
  def cost(self):
    return 3.5

  def description(self):
    return "Tea"

class AddonDecorator(Drink):
  def __init__(self, drink):
    self.drink = drink

class Milk(AddonDecorator):
  def cost(self):
    return self.drink.cost() + 1

  def description(self):
    return self.drink.description() + ", Milk"

class Chantilly(AddonDecorator):
  def cost(self):
    return self.drink.cost() + 0.75

  def description(self):
    return self.drink.description() + ", Chantilly"

class Cinnamon(AddonDecorator):
  def cost(self):
    return self.drink.cost() + 0.5

  def description(self):
    return self.drink.description() + ", Cinnamon"

class Chocolate(AddonDecorator):
  def cost(self):
    return self.drink.cost() + 1.25

  def description(self):
    return self.drink.description() + ", Chocolate"

def main():
  drink = Chocolate(Milk(Espresso()))

  print(drink.description())
  print(drink.cost())

if __name__ == "__main__":
  main()
