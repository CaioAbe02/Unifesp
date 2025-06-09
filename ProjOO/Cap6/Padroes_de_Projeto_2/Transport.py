from abc import ABC

class TransportMode(ABC):
  pass

class Car(TransportMode):
  pass

class Bus(TransportMode):
  pass

class Bike(TransportMode):
  pass

class TransportFactory:
  @staticmethod
  def create(transport: str) -> TransportMode:
    match transport:
      case "car":
        return Car()
      case "bus":
        return Bus()
      case "bike":
        return Bike()