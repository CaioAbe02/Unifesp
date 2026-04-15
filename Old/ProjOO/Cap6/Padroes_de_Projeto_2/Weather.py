from abc import ABC

class Weather(ABC):
  pass

class Sunny(Weather):
  pass

class Rainy(Weather):
  pass


class WeatherFactory:
  @staticmethod
  def create(transport: str) -> Weather:
    match transport:
      case "sunny":
        return Sunny()
      case "rainy":
        return Rainy()