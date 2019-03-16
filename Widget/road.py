
class Road:
    def __init__(self, id, length, speed, channel, origin, destination, isDuplex):
        self.roadId = id
        self.roadLength = length
        self.roadSpeed = speed
        self.roadChannel = channel
        self.roadOrigin = origin
        self.roadDestination = destination
        self.roadisDuplex = isDuplex
        self.laneMatrixPositive = None
        self.laneMatrixNegative = None
