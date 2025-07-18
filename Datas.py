import pygame 
from Entity import * 

# Info about this page:
# It will be used as a global area for each py file to take and use for their functions such as changing screens, getting functions, and etc. 

# Initialising Pygame 
pygame.init()

#set framerate of the game
clock = pygame.time.Clock()
FPS = 60 

# Change for each update made for clear indication 
UPDATE_LOG = ' 0.0.4'

OB_EVENTS = "SCR_MENU" # An variable holding the game current events

# Screen dimensions (Can be adjustable for future changes)
WIDTH, HEIGHT = 1200, 600 
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#region All Colours 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)  # Color for running
ORANGE = (255, 151, 23)
#endregion

#region UI Functions
def draw_text(text, x, y, size, color, FONT=None):
    font = pygame.font.Font(FONT, size)  # Load the font with the specified size
    text_surface = font.render(text, True, color)  # Render the text surface with the specified color
    text_rect = text_surface.get_rect(center=(x, y))  # Position the text at the given (x, y) coordinates
    screen.blit(text_surface, text_rect)  # Draw the text on the screen

def drawing_healthbar(amount, x, y, colour):
    ratio = amount / 500
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34)) # bars arund the health
    pygame.draw.rect(screen, BLACK, (x, y, 400, 30)) # doesnt change 
    pygame.draw.rect(screen, colour, (x, y, 400 * ratio, 30)) # does change 
#endregion 

#region Button Class 
main_font = pygame.font.SysFont("cambria", 50) # defining the font the button will use

class ButtonFunction():
    def __init__(self, image, x_pos, y_pos, text_input, img2):
        self.image = image
        self.originalimage = image 
        self.imgae2 = img2
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = main_font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

        # Ensure the image has an alpha channel (transparency)
        if self.image.get_alpha() is None:
            self.image = self.image.convert_alpha()  # Convert to support transparency

        self.mask = pygame.mask.from_surface(self.image)  # Create a pixel mask

    def update(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        # Convert screen coordinates to local button coordinates
        local_x = position[0] - self.rect.left
        local_y = position[1] - self.rect.top
        
        # Check if the position is within the image mask (non-transparent pixel)
        if 0 <= local_x < self.rect.width and 0 <= local_y < self.rect.height:
            if self.mask.get_at((local_x, local_y)):  # If pixel is not transparent
                #print("Button pressed!")
                return True  # Click is valid

        return False  # Click is outside the button shape

    def changeColor(self, position):
        if self.rect.collidepoint(position):
            self.text = main_font.render(self.text_input, True, "orange")
            if self.image != self.imgae2:
                self.image = self.imgae2
                self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
                self.mask = pygame.mask.from_surface(self.image)
        else:
            self.text = main_font.render(self.text_input, True, "white")
            if self.image != self.originalimage:
                self.image = self.originalimage
                self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
                self.mask = pygame.mask.from_surface(self.image)

#endregion 

#region All Buttons 

# making a resuable variable that will determine length/width + look of the buttons
MENU_BTN_surface = pygame.image.load("Images/UI/Buttons/button2.png") # assinging avatar to button
MENU_BTN_surface = pygame.transform.scale(MENU_BTN_surface, (250, 75)) # determining the button size and height 

# doing the same but for another vairable with a different sprite
MENU_BTN_lit_button = pygame.image.load("Images/UI/Buttons/button1.png")
MENU_BTN_lit_button = pygame.transform.scale(MENU_BTN_lit_button, (250, 65))

# Buttons for the Main Menu 
START_BTN_MENU = ButtonFunction(MENU_BTN_surface, 600, 270, "START", MENU_BTN_lit_button) 
QUIT_BTN_MENU = ButtonFunction(MENU_BTN_surface, 600, 390, "QUIT", MENU_BTN_lit_button)

# Buttons for the Fights 
BACK_BTN_FIGHT = ButtonFunction(MENU_BTN_surface, 600, 270, "BACK", MENU_BTN_lit_button) 

#endregion

#region All Characters 

# defining player variables + player 
player_SIZE = 63 #127 # Pixels 
player_SCALE = 3
player_OFFSET = [47, 35]
player_DATA = [player_SIZE, player_SCALE, player_OFFSET]

PLAYER = Playable(200, 370, False, "PLAYER", player_DATA)

ENEMY = Playable(700, 370, True, "ENEMY_1", player_DATA) 
#endregion 