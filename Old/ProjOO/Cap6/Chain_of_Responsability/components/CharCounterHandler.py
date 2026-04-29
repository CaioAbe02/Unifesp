class CharCounterHandler:
  def __init__(self):
    self.space_qty: int = 0
    self.a_qty: int = 0
    self.dot_qty: int = 0

  def setSpaceQty(self, quantity: int):
    self.space_qty = quantity

  def setAQty(self, quantity: int):
    self.a_qty = quantity

  def setDotQty(self, quantity: int):
    self.dot_qty = quantity

  def printResults(self):
    print("Space:", self.space_qty)
    print("A:", self.a_qty)
    print("Dot:", self.dot_qty)