class TV:
  def turnOn(self):
    print("TV was turned on")

  def turnOff(self):
    print("TV was turned off")

class MidiaPlayer:
  def turnOn(self):
    print("Midia player was turned on")

  def turnOff(self):
    print("Midia player was turned off")

  def playPlaylist(self, playlist_name):
    print(f"Midia player is playing: {playlist_name}")


class SoundSystem:
  def turnOn(self):
    print("Sound system was turned on")

  def turnOff(self):
    print("Sound system was turned off")

  def setVolume(self, volume):
    print(f"Sound volume was set to {volume}")

class AmbientLight:
  def turnOn(self):
    print("Ambient light was turned on")

  def turnOff(self):
    print("Ambient light was turned off")

  def setWarmLightTemperature(self):
    print("Ambient light temperature was set to: Warm")

  def setColdLightTemperature(self):
    print("Ambient light temperature was set to: Cold")

class HomeTheater:
  def __init__(self):
    self.tv = TV()
    self.midia_player = MidiaPlayer()
    self.sound_system = SoundSystem()
    self.ambient_light = AmbientLight()

  def watchMovie(self):
    print("Preparing to watch a movie...")
    self.midia_player.turnOff()
    self.tv.turnOn()
    self.sound_system.turnOn()
    self.sound_system.setVolume(50)
    self.ambient_light.turnOn()
    self.ambient_light.setWarmLightTemperature()
