
# 10000 2->31
# 5005->5016->5026->5037->5047

# 10001 2->20
# 5006->5017->5027

# 10002 27->2
# 5039->5028->5018->5007->5001

# 10003 1->28
# 5000-5001-5002-5008-5019-5029-5040

# 10004


class Car:
    def __init__(self, id, origin, destination, speed, time, garage, p, WaitorStop):
        self.carId = id
        self.carOriginal = origin
        self.carDestination = destination
        self.carSpeed = speed
        self.carStartTime = time
        self.isInGarage = garage
        self.path = p
        self.waitOrStop = WaitorStop

