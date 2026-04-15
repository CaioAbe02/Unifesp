from RouteStartegies import *
from RoutePlanner import RoutePlanner
from Enums import *
from RouteStrategySelector import RouteStrategySelector

def printResult(planner: RoutePlanner, strategy_selector: RouteStrategySelector, transport: Transport, weather: Weather):
    strategy = strategy_selector.chooseStrategy(weather, transport)
    planner.setStrategy(strategy)
    planner.planRoute("Av. Paulista", "USP")
    print(f"{transport.name} | {weather.name} -> {strategy.__class__.__name__}")
    planner.printRoute()

def main():
  planner: RoutePlanner = RoutePlanner()
  strategy_selector: RouteStrategySelector = RouteStrategySelector()

  transport = Transport.BIKE
  weather = Weather.SUNNY
  printResult(planner, strategy_selector, transport=transport, weather=weather)

  transport = Transport.CAR
  weather = Weather.SUNNY
  printResult(planner, strategy_selector, transport=transport, weather=weather)

  transport = Transport.CAR
  weather = Weather.RAINY
  printResult(planner, strategy_selector, transport=transport, weather=weather)

  transport = Transport.BUS
  weather = Weather.RAINY
  printResult(planner, strategy_selector, transport=transport, weather=weather)

if __name__ == "__main__":
   main()
