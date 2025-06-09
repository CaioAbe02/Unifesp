from .CharCounter import CharCounter

class SpaceCounter(CharCounter):
  def __init__(self):
    self.next: CharCounter = None
    self.counter = 0

  def setNext(self, next: CharCounter):
    self.next = next

  def countChar(self, text: str) -> str:
    for char in text:
      if char == " ":
        self.counter += 1
    print(f"Space: {self.counter}")
    return self.next.countChar(text)