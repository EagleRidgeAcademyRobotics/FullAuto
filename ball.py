#ball class this runs all logic on the balls

class Ball:

    lifetime = 10

    posX = 0
    posY = 0

    def __init__(self, x, y):
        self.posX = x
        self.posY = y


    def getRenderDims(self, ppm):
        return [round(self.posX * ppm), round(self.posY * ppm)]

    def periodic(self, deltaTime):
        self.lifetime -= deltaTime
