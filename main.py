import pygame

import robot
import helpers
import ball
import robotpathfinding

#The fields dimensions in real life

FIELD_HEIGHT = 8.21 #m
FIELD_WIDTH = 15.98 #m

TEST_MODE = True
FPS_MAX = 10
FRAME_TIME = 1/FPS_MAX


#All field starting configuration balls are listed here
balls = [
    ball.Ball(9.6, 7.2), #trench balls
    ball.Ball(8.8, 7.2),
    ball.Ball(8.0, 7.2),
    ball.Ball(6.5, 7.0),
    ball.Ball(6.5, 7.4), #end of trench balls
    ball.Ball(9.85, 5.05), #shield generator
    ball.Ball(9.5, 5.2),
    ball.Ball(10.0, 4.5),
    ball.Ball(9.85, 4.15),
    ball.Ball(9.7, 3.8), #end of shield generator
    
    ball.Ball(9.5, 1.3), #opposing team trench
    ball.Ball(7.1, 1.1),
    ball.Ball(6.4, 1.1),
    ball.Ball(8.0, 1.1), #end of opposing trench
    ball.Ball(6.45, 3.05), #opposing generator
    ball.Ball(6.1, 3.2),
    ball.Ball(6.0, 3.7),
    ball.Ball(6.1, 4.0),
    ball.Ball(6.25, 4.35), #end of opposing generator
]


#Define colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
YELLOW = (255, 255, 0)

#Initialize pygame
pygame.init()


#Dimensions of the display window
HEIGHT = 500
WIDTH = round(HEIGHT * (FIELD_WIDTH/FIELD_HEIGHT))


#Load resources
fieldImage = pygame.image.load('fieldDrawing.png')
fieldImage = pygame.transform.scale(fieldImage, (WIDTH,HEIGHT))

font = pygame.font.SysFont("arial", 24)

#Calculate pixels per meter
ppm = HEIGHT / FIELD_HEIGHT



myRobot = robot.Robot(ppm)


# Open a new window
size = (WIDTH, HEIGHT + 100)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Field Display")



def renderRobot():
    robotRect = myRobot.getRenderRect(ppm)

    #print(robotRect)
    
    #pygame.draw.rect(screen, GREEN, robotRect,0)
    pygame.draw.polygon(screen, GREEN, robotRect)
    
    line = myRobot.getFacingLinePoints(ppm, 50)
    pygame.draw.line(screen, BLACK, (line[0], line[1]), (line[2], line[3]), 1)


def renderBalls():
    for b in balls:
        dims = b.getRenderDims(ppm)
        pygame.draw.circle(screen, YELLOW, dims, round(5 * 0.0254 * ppm), 0)


#render pathfinding array
def renderGrid():
    for x in robotpathfinding.pathfinding_grid:
        for e in x:
            c = RED
            if e.difficulty == 8:
                c = GREEN    
            if e.difficulty != 0:
                pygame.draw.circle(screen, c, (e.displayX, e.displayY), 1, 0)
            


def renderPath(path):
    
    render_path = []
    for e in path:
        render_path.append((round(e[1] * ppm), round(e[0] * ppm)))
        
    if len(render_path) > 1:
        pygame.draw.lines(screen, RED, False, render_path, 1)


def tickBalls():
    for ball in balls:
        ball.periodic(FRAME_TIME)
        if ball.lifetime <= 0:
            balls.remove(ball)


# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True
 
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

 
# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            carryOn = False # Flag that we are done so we exit this loop

     # --- Game logic should go here

     
    mouseX = round(pygame.mouse.get_pos(0)[0] / ppm, 1)
    mouseY = round(pygame.mouse.get_pos(0)[1] / ppm, 1)

    key=pygame.key.get_pressed()  #checking pressed keys
    if key[pygame.K_w]:myRobot.move(2 * FRAME_TIME)
    if key[pygame.K_a]:myRobot.rotation -= 180 * FRAME_TIME
    if key[pygame.K_s]:myRobot.move(-2 * FRAME_TIME)
    if key[pygame.K_d]:myRobot.rotation += 180 * FRAME_TIME
    if key[pygame.K_t]:myRobot.setPos(mouseX, mouseY, 180)
    if key[pygame.K_p]:
        path = robotpathfinding.getPath((myRobot.xPos, myRobot.yPos), (mouseX, mouseY))
        myRobot.pathfind = path
    if key[pygame.K_b]:balls.append(ball.Ball(mouseX, mouseY))
            


    
    #Do ai logic here
    
    
    
     
 
    # --- Drawing code should go here
    # First, clear the screen to white. 
    screen.fill(BLACK)
    screen.blit(fieldImage, (0, 0))
    #The you can draw different shapes and lines or add text to your background stage.
    
    #pygame.draw.line(screen, GREEN, [0, 0], [100, 100], 5)
    #pygame.draw.ellipse(screenrobot.render(screen)


    


    myRobot.periodic(TEST_MODE, FRAME_TIME)


    tickBalls()
    
    #calculate grid
    robotpathfinding.generateGrid(ppm, FIELD_WIDTH, FIELD_HEIGHT, robotpathfinding.zones)

    renderRobot()

    renderBalls()

    renderGrid()


    #
    #print(path)

    #for b in balls:
    #    path = robotpathfinding.getPath((myRobot.xPos, myRobot.yPos), (b.posX, b.posY))
    #    renderPath(path)
    
    if myRobot.pathfind != None:
        renderPath(myRobot.pathfind)

    #render overlays
    text = font.render("X:" + str(mouseX) + "m Y:" + str(mouseY) +"m" + "    GAME TIME: " + str(round(myRobot.game_time)), True, (255, 255, 255))
    screen.blit(text, (0, HEIGHT))

    info_text = font.render("T: Set pos | B: add ball | P: pathfind | S: Shoot | I: Intake | E: Endgame (1:Close,2:Mid,3:Far)", True, (255, 255, 255))
    screen.blit(info_text, (0, HEIGHT + 75))

    fps_text = font.render("FPS: " + str(round(clock.get_fps(), 1)), True, (255, 255, 255))
    screen.blit(fps_text, (WIDTH - 120, HEIGHT))

 
     # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
     # --- Limit to 10 frames per second
    clock.tick(FPS_MAX)
    

    
 
#Once we have exited the main program loop we can stop the game engine:
pygame.quit()
