from abc import ABC, abstractmethod

class LegacyMapProvider:
    def get_path(self, start, end):
        return f"Map path from {start} to {end}"

class MapService(ABC):
    @abstractmethod
    def get_route(self, origin, destination):
        pass

class ExternalMapAdapter(MapService):
    def __init__(self, legacy_provider):
        self.legacy_provider = legacy_provider

    def get_route(self, origin, destination):
        return self.legacy_provider.get_path(origin, destination)