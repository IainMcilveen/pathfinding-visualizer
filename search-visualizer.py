#import pygame and it's constants
import pygame
import sys
from pygame.locals import *

import time

#program constants
win_width = 1280
win_height = 720
gridScale = 40

#initialize pygame window
def initializeWin():
    #initialize pygame
    pygame.init()

    #create a window
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
    mouse["xPos"] = mousePos[0]
    mouse["yPos"] = mousePos[1]

    #get all keyboard inputs
    keyInputs = pygame.key.get_pressed()

    #storing needed keys into a dictionary
    keys = {}
    keys["esc"] = keyInputs[27]
    keys["s"] = keyInputs[115]
    keys["e"] = keyInputs[101]
    
    return mouse, keys

#draw the grid to the screen
def draw(grid,win):
    for row in grid:
        for sqr in row:
            #draw square with a lightly larger one for a black border
            pygame.draw.rect(win,Color(0,0,0),(sqr[1][0],sqr[1][1],gridScale,gridScale))
            pygame.draw.rect(win,Color(255,255,255),(sqr[1][0]+1,sqr[1][1]+1,gridScale-2,gridScale-2))

#update the grid with user input
def updateGrid(grid,mouse,keys):
    print(grid)



def main():
    
    #initialize window
    win = initializeWin()
    grid = initializeGrid()

    #main loop
    while True:
        
        #check to see if program should quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #get mouse and relevent key inputs        
        mouse, keys = inputs()

        #draw a white screen
        win.fill(Color(255, 255, 255))

        #draw the grid
        draw(grid,win)

        #update the screen
        pygame.display.update()
        time.sleep(0.1)


if __name__ == "__main__":
    main()