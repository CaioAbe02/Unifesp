from components.Aircraft import Aircraft
from components.ControlTower import ControlTower

torre:ControlTower = ControlTower()

boeing747: Aircraft = Aircraft("Boeing-747")
boeing747.setControlTower(torre)

torre.addAircraft(boeing747)

boeing747.requestLanding()