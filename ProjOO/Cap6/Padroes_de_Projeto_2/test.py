from abc import ABC, abstractmethod
from threading import Lock

# --- Strategy Pattern ---
class RouteStrategy(ABC):
    @abstractmethod
    def calculate_route(self, origin, destination):
        pass

class FastestRouteStrategy(RouteStrategy):
    def calculate_route(self, origin, destination):
        return f"Fastest route from {origin} to {destination}"

class EcoFriendlyRouteStrategy(RouteStrategy):
    def calculate_route(self, origin, destination):
        return f"Eco-friendly route from {origin} to {destination}"

# --- Factory Method ---
class TransportMode(ABC):
    @abstractmethod
    def __str__(self):
        pass

class Bike(TransportMode):
    def __str__(self):
        return "Bike"

class Car(TransportMode):
    def __str__(self):
        return "Car"

class Bus(TransportMode):
    def __str__(self):
        return "Bus"

class TransportFactory:
    def create(self, mode):
        modes = {"bike": Bike, "car": Car, "bus": Bus}
        if mode.lower() in modes:
            return modes[mode.lower()]()
        raise ValueError("Unknown transport mode")

# --- Singleton ---
class SettingsManager:
    _instance = None
    _lock = Lock()

    def __init__(self):
        if SettingsManager._instance is not None:
            raise Exception("Use getInstance() method")
        self.settings = {}

    @staticmethod
    def getInstance():
        if SettingsManager._instance is None:
            with SettingsManager._lock:
                if SettingsManager._instance is None:
                    SettingsManager._instance = SettingsManager()
        return SettingsManager._instance

# --- Adapter ---
class LegacyMapProvider:
    def get_path(self, start, end):
        return f"Legacy path from {start} to {end}"

class MapService(ABC):
    @abstractmethod
    def get_route(self, origin, destination):
        pass

class ExternalMapAdapter(MapService):
    def __init__(self, legacy_provider):
        self.legacy_provider = legacy_provider

    def get_route(self, origin, destination):
        return self.legacy_provider.get_path(origin, destination)

# --- Proxy ---
class BaseRouteService:
    def __init__(self, map_service):
        self.map_service = map_service

    def get_route(self, origin, destination):
        return self.map_service.get_route(origin, destination)

class CachedRouteProxy:
    def __init__(self, base_service):
        self.base_service = base_service
        self.cache = {}

    def get_route(self, origin, destination):
        key = (origin, destination)
        if key not in self.cache:
            self.cache[key] = self.base_service.get_route(origin, destination)
        return self.cache[key]

# --- Decorator ---
class Route:
    def __init__(self, description):
        self.description = description

    def get_description(self):
        return self.description

class RouteDecorator(Route):
    def __init__(self, route):
        self.route = route

    def get_description(self):
        return self.route.get_description()

class SafetyAlertDecorator(RouteDecorator):
    def get_description(self):
        return super().get_description() + " + Safety Alerts"

class TouristInfoDecorator(RouteDecorator):
    def get_description(self):
        return super().get_description() + " + Tourist Info"

# --- Observer ---
class RouteObserver(ABC):
    @abstractmethod
    def update(self, route):
        pass

class ConsoleObserver(RouteObserver):
    def update(self, route):
        print(f"[Observer] New route calculated: {route.get_description()}")

# --- Facade ---
class RoutePlanner:
    def __init__(self):
        self.strategy = None
        self.observers = []

    def set_strategy(self, strategy):
        self.strategy = strategy

    def attach(self, observer):
        self.observers.append(observer)

    def notify(self, route):
        for observer in self.observers:
            observer.update(route)

    def plan_route(self, origin, destination, transport):
        if not self.strategy:
            raise Exception("Route strategy not set")
        description = self.strategy.calculate_route(origin, destination) + f" using {transport}"
        route = Route(description)
        self.notify(route)
        return route

class AppFacade:
    def __init__(self, planner, route_service, config):
        self.planner = planner
        self.route_service = route_service
        self.config = config

    def show_route_with_enhancements(self, origin, destination, mode):
        transport = TransportFactory().create(mode)
        map_data = self.route_service.get_route(origin, destination)
        route = self.planner.plan_route(origin, destination, transport)
        decorated = TouristInfoDecorator(SafetyAlertDecorator(route))
        print(f"[Facade] Map: {map_data}\n[Facade] Route: {decorated.get_description()}")

# --- Example usage ---
if __name__ == "__main__":
    config = SettingsManager.getInstance()
    config.settings["language"] = "en"

    factory = TransportFactory()
    transport = factory.create("bike")

    map_service = ExternalMapAdapter(LegacyMapProvider())
    route_service = CachedRouteProxy(BaseRouteService(map_service))

    planner = RoutePlanner()
    planner.set_strategy(EcoFriendlyRouteStrategy())
    planner.attach(ConsoleObserver())

    facade = AppFacade(planner, route_service, config)
    facade.show_route_with_enhancements("Centro", "Parque Ibirapuera", "bike")
