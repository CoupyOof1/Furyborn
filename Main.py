import pygame
import sys
import random
from Datas import * # Imports all the variables and functions in this file onto the current opened one
from Events import * # Imports all the variables and functions in this file onto the current opened one
from UI import * # Imports all the variables and functions in this file onto the current opened one

# Initialising Pygame 
pygame.init()
pygame.display.set_caption('FuryBorn DEMO ver:'+UPDATE_LOG) # Display Game Name on Window

def main_loop():
    while True: 
        clock.tick(FPS)
        handle_events()
        updating_screens()
        pygame.display.update()

# Runs the main loop function to continously run the game on a loop
if __name__ == "__main__":
    main_loop()