from abc import ABC, abstractmethod

class CharCounter(ABC):
  @abstractmethod
  def setNext(self):
    pass

  def handleNext(self, text: str):
    if not self.next:
      return text
    return self.next.countChar(text)

  @abstractmethod
  def countChar(self, text: str):
    pass
