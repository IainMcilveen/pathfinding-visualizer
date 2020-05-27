import pygame, sys, time
from pygame.locals import *

#program constants
win_width = 1280
win_height = 720
gridScale = 40

#create a node class to act as each point in the grid for a*
class Node:
    def __init__(self,parent,x,y):
        self.parent = parent
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
    #allow for comparison between nodes
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
        

#initialize pygame and create a window
def initializeWin():
    pygame.init()
    window = pygame.display.set_mode((win_width,win_height))
    pygame.display.set_caption("Search Visualizer")

    return window

#initialize a grid to used
def initializeGrid():

    grid = []
    for y in range(int(win_width/gridScale)):
        grid.append([])
        for x in range(int(win_height/gridScale)):
            grid[y].append([" ",(y*gridScale,x*gridScale)])
    return grid

#get user inputs
def inputs():

    #get mouse inputs and position
    mousePressed = pygame.mouse.get_pressed()
    mousePos = pygame.mouse.get_pos()

    #add all of the mouse inputs into a dictionary
    mouse = {}
    mouse["lmb"] = mousePressed[0]
    mouse["rmb"] = mousePressed[2]
    mouse["posX"] = mousePos[0]
    mouse["posY"] = mousePos[1]

    #get all keyboard inputs
    keyInputs = pygame.key.get_pressed()

    #storing needed keys into a dictionary
    keys = {}
    keys["esc"] = keyInputs[27]
    keys["s"] = keyInputs[115]
    keys["e"] = keyInputs[101]
    keys["space"] = keyInputs[32]
    
    return mouse, keys

#draw the grid to the screen
def draw(grid,win):
    for row in grid:
        for sqr in row:
            #get the color of the square
            if(sqr[0] == " "):
                gridColor = Color(255,255,255)
            elif(sqr[0] == "W"):
                gridColor = Color(96,96,96)
            elif(sqr[0] == "S"):
                gridColor = Color(0,255,0)
            elif(sqr[0] == "E"):
                gridColor = Color(255,0,0)
            elif(sqr[0] == "P"):
                gridColor = Color(0,0,255)
            elif(sqr[0] == "B"):
                gridColor = Color(0,0,125)

            #draw square with a slightly larger one for a black border
            pygame.draw.rect(win,Color(0,0,0),(sqr[1][0],sqr[1][1],gridScale,gridScale))
            pygame.draw.rect(win,gridColor,(sqr[1][0]+1,sqr[1][1]+1,gridScale-2,gridScale-2))

#reset the grid to allow for multiple pathfinding runs on the same grid
def resetGrid(grid,sPos,ePos):
    for row in grid:
        for sqr in row:
            if(sqr[0] == "P" or sqr[0] == "B"):
                sqr[0] = " "
    grid[sPos[0]][sPos[1]][0] = "S"
    grid[ePos[0]][ePos[1]][0] = "E"
    return grid

#update the grid with user input
def updateGrid(grid,mouse,keys,start,end):
    #convert coordinates of mouse into grid coordinates
    (gridX,gridY) = int(mouse["posX"]/gridScale),int(mouse["posY"]/gridScale)
    
    #set the grid points based on mouse and key presses
    if(mouse["rmb"] == 1):
        grid[gridX][gridY][0] = " "
    elif(mouse["lmb"] == 1):
        grid[gridX][gridY][0] = "W"
    elif(keys["e"] == 1):
        grid[end[0][0]][end[0][1]][0] = " "
        grid[gridX][gridY][0] = "E"
        end = [(gridX,gridY),True]
    elif(keys["s"] == 1):
        grid[start[0][0]][start[0][1]][0] = " "
        grid[gridX][gridY][0] = "S"
        start = [(gridX,gridY),True]

    return start,end

def astar(win,grid,sCords,eCords):

    #initialize open and closed list, as well as list for storing the path
    openList = []
    closedList = []

    #create start and end nodes
    startNode = Node(None,sCords[0],sCords[1])
    startNode.g = startNode.f = startNode.h = 0
    endNode = Node(None,eCords[0],eCords[1])
    endNode.g = endNode.f = endNode.h = 0

    openList.append(startNode)

    while(len(openList) > 0):

        #get node in open list with smallest f value and make it the current node
        curNode = openList[0]
        for node in openList:
            if(node.f < curNode.f):
                curNode = node
        
        #remove current node from openList and put it in the closedList
        openList.remove(curNode)
        closedList.append(curNode)

        #if the current node is the end node, done
        if(curNode == endNode):
            path = []
            while curNode is not None:
                path.append((curNode.x,curNode.y))
                curNode = curNode.parent
            drawPath(win,grid,path[::-1])
            return

        #generate the child nodes
        childNodes = []
        for cord in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]:
            childX = curNode.x+cord[0]
            childY = curNode.y+cord[1]
            #check to make sure that the child node is not out of bounds
            if(childX < 0 or childX > (int(win_width/gridScale)-1) or childY < 0 or childY > (int(win_height/gridScale)-1)):
                continue
            #check to make sure that the child node is not a wall
            if(grid[childX][childY][0] == "W"):
                continue

            #create childNode and append it to the list
            chNode = Node(curNode,childX,childY)
            grid[childX][childY][0] = "B"
            childNodes.append(chNode)
            
        for child in childNodes:
            #check to make sure that child is not already in openList
            inOpenList = False
            for node in openList:
                if(node == child):
                    inOpenList = True
                    break
            if(inOpenList):
                continue

             #calculate the g,h,f values
            child.g = curNode.g + 1
            child.h = ((childX-eCords[0])**2 + (childY-eCords[1])**2)*0.5
            child.f = child.g + child.h

            #check to see if the node is in the closed list, if it is check the g score
            inClosedList = False
            for node in closedList:
                if(node == child and child.g > node.g):
                    inClosedList = True
                    break
            if(inClosedList):
                continue
        
            #add child to the open list
            openList.append(child)

def drawPath(win,grid,path):
    
    for coord in path:
        grid[coord[0]][coord[1]][0] = "P"
        draw(grid,win)
        pygame.display.update()
        time.sleep(0.005)

def main():
    
    #initialize window and grid
    win = initializeWin()
    grid = initializeGrid()

    #start and end points
    start = [(0,0),False]
    end = [(0,0),False]

    #flag to stop user from editing when pathfinding is happening
    editing = True 
    find = False

    while True:
        
        #check to see if program should quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #get mouse and relevent key inputs        
        mouse, keys = inputs()

        #if editing, update grid
        if editing:
            #update the grid
            start,end = updateGrid(grid,mouse,keys,start,end)
        else: #if not check to see if user wants to begin editing
            if(mouse["lmb"] == 1):
                grid = resetGrid(grid,start[0],end[0])
                editing = True
                time.sleep(0.1)

        #begin pathfinding if theres a start and end point
        if(keys["space"] == 1):
            if(start[1] == True and end[1] == True):
                find = True

        #begin a*
        if(start[1] == True and end[1] == True and find == True):
            astar(win,grid,start[0],end[0])
            editing = find = False
        
        #draw a white screen
        win.fill(Color(255, 255, 255))

        #draw the grid
        draw(grid,win)

        #update the screen
        pygame.display.update()
        time.sleep(0.01)


if __name__ == "__main__":
    main()
