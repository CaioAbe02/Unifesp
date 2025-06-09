from abc import ABC, abstractmethod

class ControlTowerMediator(ABC):
  @abstractmethod
  def notify(self):
    pass