#Defines an ultrasonic sensor on the robot.
class Ultrasonic:

    x = 0
    y = 0
    rot = 0

    measurement = 0

    def __init__ (self, x, y, rot):
        self.x = x
        self.y = y
        self.rot = rot


    def setDistance (self, distance):
        self.measurement = distance

