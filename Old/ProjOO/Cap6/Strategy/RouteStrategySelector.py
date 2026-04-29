from Enums import *
from RouteStartegies import *

class RouteStrategySelector:
  def chooseStrategy(self, weather: Weather, transport: Transport) -> RouteStrategy:
    if transport == Transport.BIKE:
      return EcoFriendlyRouteStrategy()
    elif transport == Transport.BUS:
      return CheapestRouteStrategy()
    elif transport == Transport.CAR and weather == Weather.SUNNY:
      return FastestRouteStrategy()
    else:
      return ShortestRouteStrategy()