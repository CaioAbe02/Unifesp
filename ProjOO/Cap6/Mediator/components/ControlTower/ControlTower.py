from ControlTowerMediator import ControlTowerMediator
from ..Aircraft import Aircraft
from ...enums.notifications import Notification

class ControlTower(ControlTowerMediator):
  def __init__(self):
    self.aircrafts = []

  def addAircraft(self, aircraft: Aircraft):
    self.aircrafts.append(aircraft)

  def notify(self, sender: Aircraft, event: Notification):
    if event == Notification.REQUEST_LANDING:
      print(f"[Torre de Controle]: {sender.name} solicita permissão para pousar")