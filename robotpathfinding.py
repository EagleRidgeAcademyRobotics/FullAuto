import matplotlib.path as mpltPath
from matplotlib import path
import numpy

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder



#size = 0.25
size = .8

#nodes per meter conversion. This is how many nodes are in 1 meter.
npm = 1 / size

pathfinding_grid = []


class Zone:
    
    difficulty = 0
    polygon = []
    padding = 0
    
    def __init__ (self, difficulty, padding, polygon):
        self.difficulty = difficulty
        self.padding = padding
        self.polygon = polygon


zones = [
    Zone(8, 1.5, [[5.7,3.3],[9.0,2.0],[10.3,5.0],[6.8,6.2]]), #center thing
    Zone(0, 0.75, [[5.6, 0.0],[10.4, 0.0],[10.4, 1.6],[5.6, 1.6]]), #enemy trench
    Zone(0, -0.5, [[5.8, 3.3],[9.0, 2.1],[9.5, 3.4],[6.5, 4.8]]), #enemy climbing area
    Zone(0, 1.0, [[15.3, 2.8]]), #enemy ball intake

    #The little walls
    Zone(0, 0.5, [[5.8, 3.4]]),
    Zone(0, 0.6, [[6.9, 6.5]]),
    Zone(0, 0.6, [[9.0, 2.0]]),
    Zone(0, 0.6, [[10.3, 5.0]]),

    
    
]

class Gridnode:
    
    ex = 0
    ey = 0

    x = 0
    y = 0

    displayX = 0
    displayY = 0

    difficulty = 0

    def __init__(self, ex, ey, x, y, ppm):

        self.ex = ex
        self.ey = ey
        
        self.x = x
        self.x = y

        self.displayX = round(x * ppm)
        self.displayY = round(y * ppm)
        



def generateGrid (ppm, FIELD_WIDTH, FIELD_HEIGHT, zones):
    global pathfinding_grid

    w = round(FIELD_HEIGHT / size) + 1
    h = round(FIELD_WIDTH / size) + 1

    pathfinding_grid = [[0 for x in range(w)] for y in range(h)]
    
    for x in range(h):
        for y in range(w):

            element = Gridnode(x, y, (x * size), (y * size), ppm)
            element.difficulty = 1

            for zone in zones:
                #print("testing zone " + str(polygon))

                if len(zone.polygon) == 1:
                    #we want to define a circle instead of a polygon
                    if numpy.sqrt( numpy.square((x * size) - zone.polygon[0][0]) +  numpy.square((y * size) - zone.polygon[0][1]) )  <= zone.padding:
                        element.difficulty = zone.difficulty
                else:
                    if path.Path(zone.polygon).contains_point([(x * size), (y * size)], radius=zone.padding):#radius is the ~max dimenstion of the robot
                        #print(str(element.x) + " " + str(element.y) + " is bad")
                        #print("X")
                        element.difficulty = zone.difficulty

                pathfinding_grid[x][y] = element


#provided starting and stopping locations in meters, it will find a path given the current grid
def getPath (start, end):

    maze = [[0 for x in range(len(pathfinding_grid[0]))] for y in range(len(pathfinding_grid))]

    for x in pathfinding_grid:
        for e in x:
             maze[e.ex][e.ey] = e.difficulty
               


    if nodeFromCords(end[0]) > len(maze) - 1:
        print("target out of bounds")
        return []
    if nodeFromCords(end[1]) > len(maze[0]) - 1:
        print("out of bounds")
        return []
        
    #find the closest node to the real world cords.
    if pathfinding_grid[nodeFromCords(end[0])][nodeFromCords(end[1])].difficulty == 0:
        print("BAD TARGET POSITION")
        return []

    grid = Grid(matrix=maze)

    start_node = grid.node(nodeFromCords(start[1]), nodeFromCords(start[0]))
    end_node = grid.node(nodeFromCords(end[1]), nodeFromCords(end[0]))

    #This accepts weights. So 0 is wall, 1+ is increasingly harder to traverse.
    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path, runs = finder.find_path(start_node, end_node, grid)

    print('operations:', runs, 'path length:', len(path))
    #print(grid.grid_str(path=path, start=start, end=end))

    world_path = []

    if path != None:
        for e in path:
            world_path.append((e[0] / npm, e[1] / npm))
        #remove the first element in the list as that is the approx robot position.
        if len(world_path) > 1:
            world_path.pop(0)
            world_path[-1] = (end[1], end[0])

    return world_path


#returns closest node to the meter cords x
def nodeFromCords (x):
    return round(x * npm)


