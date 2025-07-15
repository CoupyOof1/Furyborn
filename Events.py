import pygame 
import sys
from Datas import * # Imports all the variables and functions in this file onto the current opened one

# Initialize Pygame
pygame.init()

#region Updating Screens Functions 
def updating_screens():
    # this funcion will be used to constantly update and change the current screen to players 
    global OB_EVENTS # If Variables are constantly changing throughout the program we will also retrieve that new value 

    screen.fill((0, 0, 0))  # Clear screen
    if OB_EVENTS == "SCR_MENU": # if the variable is set to menu, draws the menu screen to players 
        drawing_menu()
    elif OB_EVENTS == "SCR_FIGHT":
        drawing_fight()
    elif OB_EVENTS == "SCR_QUIT":
        pygame.quit()
        sys.exit()
#endregion 

#region Drawing Menu
def drawing_menu():
    screen.fill((0, 0, 0))  # Clear screen

    # draws text on screen 
    draw_text("FuryBorn", 600, 105, 105, WHITE, "Fonts/JMH CTH ARCADE.ttf")

    # Make button visible 
    for button in [START_BTN_MENU, QUIT_BTN_MENU]:
        button.update(screen)
        button.changeColor(pygame.mouse.get_pos())
#endregion

#region Drawing Team Menu 
def drawing_fight():
    screen.fill((0, 0, 0))  # Clear screen

    global PLAYER 
    # draws text on screen 
    draw_text("sfhadfshadfh", 600, 105, 105, WHITE, "Fonts/JMH CTH ARCADE.ttf")

    # Makes Button visible 
    for button in [BACK_BTN_FIGHT]:
        button.update(screen)
        button.changeColor(pygame.mouse.get_pos())

    PLAYER.move(WIDTH, HEIGHT, 50, screen, ENEMY)
    for Entities in [PLAYER, ENEMY]:
        Entities.drawsprite(screen)
        Entities.updates()
#endregion 

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_events()
#endregion

#region mouse events
def handle_mouse_events():
    global OB_EVENTS

    pos = pygame.mouse.get_pos()
    if OB_EVENTS == "SCR_MENU":
        handle_menu_clicks(pos)
    elif OB_EVENTS == "SCR_FIGHT":
        handle_fight_clicks(pos)
    elif OB_EVENTS == "SCR_OVER":
        pass
        #handle_game_over_clicks(pos)
    elif OB_EVENTS == "SCR_VICTORY":
        pass
        #handle_door_opened_clicks(pos) 
    elif OB_EVENTS == "SCR_QUIT":
        pygame.quit()
        sys.exit()
#endregion 

#region handle menu clicks 
def handle_menu_clicks(pos):
    global OB_EVENTS
    
    # Telling what screen to switch when button pressed 
    if START_BTN_MENU.checkForInput(pos):
        OB_EVENTS = "SCR_FIGHT"
        print(OB_EVENTS)
    elif QUIT_BTN_MENU.checkForInput(pos):
        OB_EVENTS = "SCR_QUIT"
        print(OB_EVENTS)
#endregion 

#region handle fight clicks 
def handle_fight_clicks(pos):
    global OB_EVENTS 

    if BACK_BTN_FIGHT.checkForInput(pos):
        OB_EVENTS = "SCR_MENU"
#endregion 