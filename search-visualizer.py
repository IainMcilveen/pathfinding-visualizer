#import pygame and it's constants
import pygame
import sys
from pygame.locals import *

import time

#program constants
win_width = 640
win_height = 480

def main():
    #initialize pygame
    pygame.init()

    #create a window
    win = pygame.display.set_mode((win_width,win_height))
    pygame.display.set_caption("Search Visualizer")

    #main loop
    while True:
        
        #check to see if program should quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        
        #draw a white screen
        win.fill(Color(255, 255, 255))

        #update the screen
        pygame.display.update()
        time.sleep(0.1)

        #close_win = True

if __name__ == "__main__":
    main()