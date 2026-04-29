from Route import Route
from RouteStrategies import *

class RoutePlanner:
  def __init__(self):
    self._strategy: RouteStrategy = None
    self._route: Route = None

  def setStrategy(self, strategy: RouteStrategy):
    self._strategy = strategy

  def planRoute(self, origin: str, destination: str) -> Route:
    self._route = self._strategy.calculateRoute(origin, destination)

  def getRoute(self):
    return self._route
