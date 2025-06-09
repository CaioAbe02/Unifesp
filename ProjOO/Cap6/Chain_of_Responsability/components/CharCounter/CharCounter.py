from abc import ABC, abstractmethod

class CharCounter(ABC):
  @abstractmethod
  def setNext(self):
    pass

  @abstractmethod
  def countChar(self):
    pass