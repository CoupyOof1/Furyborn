import pygame 
import sys
from Datas import * # Imports all the variables and functions in this file onto the current opened one
'''
#region Handling Events Functions 
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

#'''