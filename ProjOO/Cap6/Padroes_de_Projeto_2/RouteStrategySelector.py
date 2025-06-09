from Transport import *
from Weather import *
from RouteStrategies import *

class RouteStrategySelector:
  def chooseStrategy(self, weather: Weather, transport: TransportMode) -> RouteStrategy:
    if transport == Bike():
      return EcoFriendlyRouteStrategy()
    elif transport == Bus():
      return CheapestRouteStrategy()
    elif transport == Car() and weather == Sunny():
      return FastestRouteStrategy()
    else:
      return ShortestRouteStrategy()