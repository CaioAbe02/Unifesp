from Route import TouristInfoDecorator
from RoutePlanner import RoutePlanner
from RouteStrategySelector import RouteStrategySelector
from Transport import TransportMode, TransportFactory
from Weather import Weather, WeatherFactory
from Settings import SettingsManager
from MapService import ExternalMapAdapter, LegacyMapProvider
from RouteProxy import RouteService, BaseRouteService, CachedRouteProxy

class AppFacade():
  def __init__(self,
              planner: RoutePlanner,
              route_service: RouteService,
              config: SettingsManager,
              transport_factory: TransportFactory,
              weather_factory: WeatherFactory,
              strategy_selector: RouteStrategySelector):
    self.planner = planner
    self.route_service = route_service
    self.config = config
    self.transport_factory = transport_factory
    self.weather_factory = weather_factory
    self.strategy_selector = strategy_selector

  def showRouteWithEnhancements(self, origin, destination, transport_mode, current_weather):
    print(f"-== {origin} -> {destination} ==-")
    transport: TransportMode = self.transport_factory.create(transport_mode)
    weather: Weather = self.weather_factory.create(current_weather)

    strategy = self.strategy_selector.chooseStrategy(weather, transport)
    self.planner.setStrategy(strategy)
    self.planner.planRoute(origin, destination)
    route = self.planner.getRoute()

    map_data = self.route_service.get_route(origin, destination)
    print(map_data)

    print(f"{transport.__class__.__name__} | {weather.__class__.__name__} -> {strategy.__class__.__name__}")
    print(TouristInfoDecorator(route).display())

def main():
  config: SettingsManager = SettingsManager()

  map_service = ExternalMapAdapter(LegacyMapProvider())
  route_service = CachedRouteProxy(BaseRouteService(map_service))

  planner: RoutePlanner = RoutePlanner()
  strategy_selector: RouteStrategySelector = RouteStrategySelector()

  transport_factory: TransportFactory = TransportFactory()
  weather_factory: WeatherFactory = WeatherFactory()

  facade = AppFacade(planner, route_service, config, transport_factory, weather_factory, strategy_selector)
  facade.showRouteWithEnhancements("Av. Paulista", "USP", "bike", "sunny")

  facade.showRouteWithEnhancements("Av. Paulista", "USP", "bike", "sunny")

if __name__ == "__main__":
  main()
