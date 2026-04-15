from .CharCounter import CharCounter
from ..CharCounterHandler import CharCounterHandler

class DotCounter(CharCounter):
  def __init__(self, handler: CharCounterHandler):
    self.next: CharCounter = None
    self.counter = 0
    self.handler = handler

  def setNext(self, next: CharCounter):
    self.next = next

  def countChar(self, text: str) -> str:
    for char in text:
      if char == ".":
        self.counter += 1
    self.handler.setDotQty(self.counter)
    return self.handleNext(text)