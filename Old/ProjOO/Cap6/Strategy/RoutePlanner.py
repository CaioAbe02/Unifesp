from Route import Route
from RouteStartegies import *

class RoutePlanner:
  def __init__(self):
    self._strategy: RouteStrategy = None
    self._route: Route = None

  def setStrategy(self, strategy: RouteStrategy):
    self._strategy = strategy

  def planRoute(self, origin: str, destination: str) -> Route:
    self._route = self._strategy.calculateRoute(origin, destination)

  def printRoute(self):
     route = self._route
     print(f"{route.origin} -> {route.destinantion}: {route.time} min | R${route.price} | {route.distance} KM | {route.co2_emission} g\n")
