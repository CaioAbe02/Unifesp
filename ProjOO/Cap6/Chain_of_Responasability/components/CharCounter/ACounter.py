from .CharCounter import CharCounter

class ACounter(CharCounter):
  def __init__(self):
    self.next: CharCounter = None
    self.counter = 0

  def setNext(self, next: CharCounter):
    self.next = next

  def countChar(self, text: str) -> str:
    for char in text:
      if char == "A" or char == "a":
        self.counter += 1
    print(f"A: {self.counter}")
    return ""