from abc import ABC, abstractmethod
from ..ControlTower import ControlTowerMediator
from ...enums.notifications import Notification

class Aircraft(ABC):
  def __init__(self, name: str):
    self._control_tower: ControlTowerMediator = None
    self.name = name

  def setControlTower(self, control_tower: ControlTowerMediator):
    self._control_tower = control_tower

  def getControlTower(self) -> ControlTowerMediator:
    return self._control_tower

  def requestLanding(self):
    print(f"[{self.name}]: Solicitando permissão para pouso.\n")
    self.getControlTower.notify(self, Notification.REQUEST_LANDING)

  @abstractmethod
  def land(self):
    pass

  @abstractmethod
  def waitLanding(self):
    pass