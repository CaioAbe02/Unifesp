from abc import ABC, abstractmethod
import random
from Route import Route

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
    time = random.randint(20, 30)
    distance = round(time * 0.15, 2)
    price = round(time * distance * 0.1, 2)
    co2_emission = round(0 * distance, 2)
    return Route(time=time, distance=distance, price=price, co2_emission=co2_emission, origin=origin, destinantion=destination)
