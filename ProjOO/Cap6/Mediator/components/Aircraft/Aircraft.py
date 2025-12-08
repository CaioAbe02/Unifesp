from ..ControlTower.ControlTower import ControlTowerMediator
from ..enums.notifications import Notification

class Aircraft:
  def __init__(self, name: str):
    self._control_tower: ControlTowerMediator = None
    self.name = name

  def setControlTower(self, control_tower: ControlTowerMediator):
    self._control_tower = control_tower

  def getControlTower(self) -> ControlTowerMediator:
    return self._control_tower

  def requestLanding(self):
    print(f"[{self.name}]: Solicitando permissão para pouso.\n")
    self._control_tower.notify(self, Notification.REQUEST_LANDING)

  def land(self):
    print(f"[{self.name}]: Pouso comcluído.")
    self._control_tower.notify(Notification.LANDED)

  def waitLanding(self):
    print(f"[{self.name}]: Recebido.")