from abc import ABC, abstractmethod
from dataclasses import dataclass
import random

@dataclass
class Route:
  origin: str
  destinantion: str
  time: float
  distance: float
  price: float
  co2_emission: float

class RouteStrategy(ABC):
  @classmethod
  @abstractmethod
  def calculateRoute(self, origin: str, destination: str) -> Route:
    pass

class FastestRouteStrategy(RouteStrategy):
  def calculateRoute(self, origin: str, destination: str) -> Route:
    time = random.randint(4, 7)
    distance = round(time * 0.5, 2)
    price = round(time * distance, 2)
    co2_emission = round(120 * distance, 2)
    return Route(time=time, distance=distance, price=price, co2_emission=co2_emission, origin=origin, destinantion=destination)

class ShortestRouteStrategy(RouteStrategy):
  def calculateRoute(self, origin: str, destination: str) -> Route:
    time = random.randint(8, 10)
    distance = round(time * 0.2, 2)
    price = round(time * distance, 2)
    co2_emission = round(120 * distance, 2)
    return Route(time=time, distance=distance, price=price, co2_emission=co2_emission, origin=origin, destinantion=destination)

class CheapestRouteStrategy(RouteStrategy):
  def calculateRoute(self, origin: str, destination: str) -> Route:
    time = random.randint(8, 10)
    distance = round(time * 0.35, 2)
    price = round(time * distance * 0.2, 2)
    co2_emission = round(120 * distance, 2)
    return Route(time=time, distance=distance, price=price, co2_emission=co2_emission, origin=origin, destinantion=destination)

class EcoFriendlyRouteStrategy(RouteStrategy):
  def calculateRoute(self, origin: str, destination: str) -> Route:
    time = random.randint(8, 10)
    distance = round(time * 0.35, 2)
    price = round(time * distance, 2)
    co2_emission = round(50 * distance, 2)
    return Route(time=time, distance=distance, price=price, co2_emission=co2_emission, origin=origin, destinantion=destination)

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
     print(f"{route.origin} -> {route.destinantion}: {route.time} min | R${route.price} | {route.distance} KM | {route.co2_emission} g")

def main():
  planner: RoutePlanner = RoutePlanner()

  print("Rota mais rápida")
  planner.setStrategy(FastestRouteStrategy())
  planner.planRoute("Av. Paulista", "USP")
  planner.printRoute()

  print("\nRota mais curta")
  planner.setStrategy(ShortestRouteStrategy())
  planner.planRoute("Av. Paulista", "USP")
  planner.printRoute()

  print("\nRota mais barata")
  planner.setStrategy(CheapestRouteStrategy())
  planner.planRoute("Av. Paulista", "USP")
  planner.printRoute()

  print("\nRota mais ecológica")
  planner.setStrategy(EcoFriendlyRouteStrategy())
  planner.planRoute("Av. Paulista", "USP")
  planner.printRoute()

if __name__ == "__main__":
   main()
