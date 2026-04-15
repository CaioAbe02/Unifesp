from abc import ABC

class RouteService(ABC):
  def get_route(self, origin, destination):
    pass

class BaseRouteService(RouteService):
  def __init__(self, map_service):
    self.map_service = map_service

  def get_route(self, origin, destination):
    print("[Base Route] Using base route service")
    print(f"[Base Route] Route found: {origin} -> {destination}\n")
    return self.map_service.get_route(origin, destination)

class CachedRouteProxy(RouteService):
  def __init__(self, base_service):
    self.base_service = base_service
    self.cache = {}

  def get_route(self, origin, destination):
    print("[Cache Route] Using route service proxy")
    key = (origin, destination)
    if key not in self.cache:
      print("[Cache Route] Route not found\n")
      self.cache[key] = self.base_service.get_route(origin, destination)
    else:
      print(f"[Cache Route] Route found: {origin} -> {destination}\n")
    return self.cache[key]