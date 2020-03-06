import matplotlib.path as mpltPath
from matplotlib import path

#size = 0.25
size = 1

#nodes per meter conversion. This is how many nodes are in 1 meter.
npm = 1 / size

pathfinding_grid = []

#in meters
nogo_zones = [
    [[0, 0],[16, 0],[16, .5],[0, .5]], #top zone
    [[5.6, 0.6],[10.4, 0.6],[10.4, 1.6],[5.6, 1.6]], #enemy trench
    [[5.5,3.1],[9.0,2.0],[10.5,5.0],[6.9,6.5]],
    #[[0, 0], [12, 0], [16, 8], [0, 8]]
    ]

class Gridnode:

    ex = 0
    ey = 0

    x = 0
    y = 0

    displayX = 0
    displayY = 0

    valid = True
    
    def __init__(self, ex, ey, x, y, ppm):

        self.ex = ex
        self.ey = ey
        
        self.x = x
        self.x = y

        self.displayX = round(x * ppm)
        self.displayY = round(y * ppm)
        



def generateGrid (ppm, FIELD_WIDTH, FIELD_HEIGHT):
    global pathfinding_grid

    w = round(FIELD_HEIGHT / size) - 1
    h = round(FIELD_WIDTH / size) - 1

    pathfinding_grid = [[0 for x in range(w)] for y in range(h)]
    
    for x in range(h):
        for y in range(w):

            element = Gridnode(x, y, (x * size) + size, (y * size) + size, ppm)
            element.valid = True

            #if element.x < 5:
            #    element.valid = False

            for polygon in nogo_zones:
                #print("testing zone " + str(polygon))
                if path.Path(polygon).contains_point([(x * size) + size, (y * size) + size], radius=.7):#radius is the ~max dimenstion of the robot
                    #print(str(element.x) + " " + str(element.y) + " is bad")
                    #print("X")

                    element.valid = False


            pathfinding_grid[x][y] = element

#provided starting and stopping locations in meters, it will find a path given the current grid
def getPath (start, end):

    maze = [[0 for x in range(len(pathfinding_grid[0]))] for y in range(len(pathfinding_grid))]

    for x in pathfinding_grid:
        for e in x:
            if e.valid == True:
                maze[e.ex][e.ey] = 0
            else:
                maze[e.ex][e.ey] = 1


    #find the closest node to the real world cords.
    if pathfinding_grid[nodeFromCords(end[0])][nodeFromCords(end[1])].valid == False:
        print("BAD TARGET POSITION")
        return []
          
    path = astar(maze, (nodeFromCords(start[0]), nodeFromCords(start[1])), (nodeFromCords(end[0]), nodeFromCords(end[1])))

    world_path = []

    if path != None:
        for e in path:
            world_path.append((e[0] / npm, e[1] / npm))

    return world_path


#returns closest node to the meter cords x
def nodeFromCords (x):
    return round(x * npm)

#Code for Astar stuff
class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)





