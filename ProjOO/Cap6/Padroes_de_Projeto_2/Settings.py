class SettingsManager(object):
  __instance = None

  def __new__(cls):
    if cls.__instance is None:
      cls.__instance = object.__new__(cls)
    return cls.__instance