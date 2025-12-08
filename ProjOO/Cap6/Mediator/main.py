from components.Aircraft.Aircraft import Aircraft
from components.ControlTower.ControlTower import ControlTower

torre: ControlTower = ControlTower()

boeing747: Aircraft = Aircraft("Boeing-747")
boeing737: Aircraft = Aircraft("Boeing-737")
embraer190e2: Aircraft = Aircraft("Embraer 190-E2")

boeing747.setControlTower(torre)
boeing737.setControlTower(torre)
embraer190e2.setControlTower(torre)

torre.addAircraft(boeing747)
torre.addAircraft(boeing737)
torre.addAircraft(embraer190e2)

boeing747.requestLanding()
boeing747.land()