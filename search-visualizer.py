#import pygame and it's constants
import pygame
import sys
from pygame.locals import *

import time

#program constants
win_width = 640
win_height = 480

#initialize pygame window
def initialize():
    #initialize pygame
    pygame.init()

    #create a window
    window = pygame.display.set_mode((win_width,win_height))
    pygame.display.set_caption("Search Visualizer")

    return window

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

def main():
    
    win = initialize()

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

        #update the screen
        pygame.display.update()
        time.sleep(0.1)


if __name__ == "__main__":
    main()