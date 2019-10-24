class Area(object):
    """Include 2 points and angle"""

    def __init__(self, pointOne, pointTwo, angle):
        self.points = [pointOne, pointTwo]
        self.angle = angle