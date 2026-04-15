from dataclasses import dataclass

@dataclass
class Route:
  origin: str
  destinantion: str
  time: float
  distance: float
  price: float
  co2_emission: float
