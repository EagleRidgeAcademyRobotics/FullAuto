import helpers
import math
import numpy as np
import ultrasonic

#config values
WIDTH = 32 * .0254 #M
HEIGHT = 28 * .0254 #M


#turret position from center of robot
TURRET_X = 0
TURRET_Y = 0


ultrasonics = [ultrasonic.Ultrasonic(0, 0, 0)]



#Instance values
class Robot:

    ppm = 0

    xPos = 12.4 #real world position in m , center of frame
    yPos = 5.7 #real worl position in m
    rotation = 180

    
    #These values are information for the AI to work on
    balls = 3
    game_time = 0


    #Command values, These are set by the program and are sent to the robot.
    #The top command is followed first, and some commands will run at the same time
    pathfind = None #[[0, 0],[1, 1]]
    intakeBallAt = None #[0, 0]
    shoot = False
    doEndGame = False    
    endGamePosition = 1

    def __init__ (self, ppm):
        self.ppm = ppm


    def move (self, speed):
        self.xPos += math.cos(np.deg2rad(self.rotation)) * speed
        self.yPos += math.sin(np.deg2rad(self.rotation)) * speed

    def setPos (self, x, y, rotation):
        self.xPos = x
        self.yPos = y
        self.rotation = rotation


    #Returns a render rect. this is centered on the robots position.
    def getRenderRect (self, ppm):
#        return [[round((self.xPos - (WIDTH / 2)) * ppm), round((self.yPos + (HEIGHT / 2)) * ppm)],
#                [round((self.xPos + (WIDTH / 2)) * ppm), round((self.yPos + (HEIGHT / 2)) * ppm)],
#                [round((self.xPos + (WIDTH / 2)) * ppm), round((self.yPos - (HEIGHT / 2)) * ppm)],
#                [round((self.xPos - (WIDTH / 2)) * ppm), round((self.yPos - (HEIGHT / 2)) * ppm)],
#                ]

        return [helpers.rotate_on_point_rounded((self.xPos - (WIDTH / 2)) * ppm, (self.yPos + (HEIGHT / 2)) * ppm, self.xPos * ppm, self.yPos * ppm, self.rotation),
                helpers.rotate_on_point_rounded((self.xPos + (WIDTH / 2)) * ppm, (self.yPos + (HEIGHT / 2)) * ppm, self.xPos * ppm, self.yPos * ppm, self.rotation),
                helpers.rotate_on_point_rounded((self.xPos + (WIDTH / 2)) * ppm, (self.yPos - (HEIGHT / 2)) * ppm, self.xPos * ppm, self.yPos * ppm, self.rotation),
                helpers.rotate_on_point_rounded((self.xPos - (WIDTH / 2)) * ppm, (self.yPos - (HEIGHT / 2)) * ppm, self.xPos * ppm, self.yPos * ppm, self.rotation),
                ]


    #This is run periodically for the robot. 
    def periodic (self, test, FRAME_TIME):
        if test:
            #We want to automatically execute commands.
            self.game_time += FRAME_TIME
            #We also want to execute the commands
            
            if self.pathfind != None:
                #We have a pathfinding command therefore we want to follow it.
                self.move(3 * FRAME_TIME)
                x = self.pathfind[0][1]
                y = self.pathfind[0][0]
                dx = x - self.xPos
                dy = y - self.yPos

                deg = (-np.rad2deg(math.atan2(dx, dy)) - 90) + 180
                self.rotation = deg

                #We have finished our pathfind if this is true
                if len(self.pathfind) == 0:
                    patfind = None
            
            
        else:
            #periodically run during normal operation
            self.rotation += 0
    

    #length is in pixels
    def getFacingLinePoints(self, ppm, length): 
        return [round(self.xPos * ppm),
                round(self.yPos * ppm),
                round(self.xPos * ppm + (math.cos(np.deg2rad(self.rotation)) * length)),
                round(self.yPos * ppm + (math.sin(np.deg2rad(self.rotation)) * length))]
    



