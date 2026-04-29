class Route:
  def __init__(self, origin: str, destination: str, time: float, distance: float, price: float, co2_emission: float):
    self.origin = origin
    self.destination = destination
    self.time = time
    self.distance = distance
    self.price = price
    self.co2_emission = co2_emission

  def display(self):
    return f"{self.origin} -> {self.destination}: {self.time} min | R${self.price} | {self.distance} KM | {self.co2_emission} g\n"

class RouteDecorator(Route):
  def __init__(self, route: Route):
    self._route = route

  def display(self):
    return self._route.display()

class TouristInfoDecorator(RouteDecorator):
  def __init__(self, route: Route):
    super().__init__(route)

  def display(self):
    return self._route.display() + "Tourist points: Park 1\n"