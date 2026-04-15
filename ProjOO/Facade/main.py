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
    print("Ready to watch a movie!")

  def listenToCalmPlaylist(self):
    print("Preparing to listen to the calm playlist songs...")
    self.tv.turnOff()
    self.sound_system.turnOn()
    self.sound_system.setVolume(60)
    self.ambient_light.turnOn()
    self.ambient_light.setWarmLightTemperature()
    self.midia_player.playPlaylist("Calm")
    print("Ready to listen to the calm playlist songs!")

  def turnEverythingOff(self):
    print("Preparing to turn everything off...")
    self.tv.turnOff()
    self.midia_player.turnOff()
    self.sound_system.turnOff()
    self.ambient_light.turnOff()
    print("Everything was turned off!")

def main():
  home_theater = HomeTheater()

  home_theater.watchMovie()
  print("\n---\n")
  home_theater.listenToCalmPlaylist()
  print("\n---\n")
  home_theater.turnEverythingOff()

if __name__ == "__main__":
  main()
