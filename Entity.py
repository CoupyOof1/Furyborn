import pygame 
import random 
from Datas import * 

class Playable():
    def __init__(self, x, y, flip, id, data):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        #self.animation_list = self.load_images(sprite_sheet, anim_steps)
        self.action = 0 # 0: idle 1: attack 2: run 3: jumping 4: getting hurt 5: death 6: attack2 7: attack 3 8 defending
        self.frame_index = 0
        #self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks() 
        self.rect = pygame.Rect((x, y, 40, 90)) # Actual box for the entity 
        self.vel_y = 0
        self.combo_window = 500
        self.knockback = 0  # Store knockback force

        # player states 
        self.alive = True
        self.invincible = False
        self.hit = False
        self.running = False
        self.jump = False
        self.attacking = False
        self.dashing = False
        self.defending = False

        # Player Attributes 
        self.health = 500
        self.stamina = 1000
        self.max_stamina = 1000
        self.cost_stamina = 8
        self.recovery_stamina = 4
        self.attack_cooldown = 0
        self.stamina_cooldown = 500

        # Player cool down 
        self.attack_type = 0
        self.cooldown_dash = 0
        self.stun_timer = 0
        self.timer_dash = 0
        self.last_e_press_time = 0
        self.double_tap_threshold = 250
        self.action_cooldown = 0        # A cooldown for whenether an entity/character is hit to add a delay in input 

        # Player Combo Cool Down 
        self.combo_count = 0
        self.combo_start_time = 0
        self.combo_max_hits = 3
        self.combo_timeout = 800         # Time allowed between presses (ms)
        self.combo_cooldown_time = 1500  # Long cooldown after full combo (ms)
        self.combo_blocked_until = 0     # Time when E can be used again

        # Player crouch state + variables 
        self.crouching = False                  # Making a state for animation to play
        self.original_height = self.rect.height # Storing the original value for the height 
        self.crouching_height = 45              # Adding new value to change the hitbox to half it height 

        # Player Blocking object 
        self.defending_rect = pygame.Rect(0, 0, 0, 0)   # Actual Object for the blocking mechanic 



    def drawing_healthbar(self, screen, amount, max_amount, x, y, colour, pos_y, pos_x):
        ratio = amount / max_amount
        x_offset = x - pos_x # determines the position of the healthbar 
        pygame.draw.rect(screen, (255, 255, 255), (x_offset - 2, y - (pos_y + 2), 104, 21))  # border
        pygame.draw.rect(screen, (255, 0, 0), (x_offset, y - pos_y, 100, 17))            # background
        pygame.draw.rect(screen, colour, (x_offset, y - pos_y, 100 * ratio, 17))      # foreground

    def drawsprite(self, surface):
        pygame.draw.rect(surface, (255,0,0), self.rect)
        self.drawing_healthbar(surface, self.health, 500, self.rect.x, self.rect.y, (0, 255, 0), 44, 25)  # Red bar
        self.drawing_healthbar(surface, self.stamina, self.max_stamina, self.rect.x, self.rect.y, (0, 0, 255), 28, 25)  # Blue bar

    #region AI TEST
    def AI_TEST(self, screen_width, screen_height, pixel_ground, surface, target):
        current_time = pygame.time.get_ticks()
        
        #speed of the player and entity
        SPEED = 10
        GRAVITY = 2
        DASH_SPEED = 25
        DASH_DURATION = 300
        DASH_COOLDOWN_TIME = 1000

        #coordinate variables determine position
        dx = 0 #left/right
        dy = 0 #up/down

        #performing other actions when not attacking/being hit/ or when action is not above 0 
        if self.attacking == False and self.hit == False and self.action_cooldown == 0:
            # Test: Defending 
            self.defend(surface, target)

        # Apply Knockback
        if self.knockback != 0:
            dx += self.knockback
            self.knockback *= 0.8  # Reduce knockback effect over time
            if abs(self.knockback) < 1:
                self.knockback = 0  # Stop knockback when it's too small

        # Apply gravity, but slow descent if attacking mid-air
        if self.attacking == True and self.jump == True:
            self.vel_y += GRAVITY * 0.06  # Reduce fall speed while attacking
            self.vel_y = max(self.vel_y, -5)  # Apply a small upward push to stall
        else:
            self.vel_y += GRAVITY  # Normal gravity when not attacking
        dy += self.vel_y

        # Ensuring fighters stay on screen
        if self.rect.left + dx < 0: #left border
            dx = -self.rect.left
        if self.rect.right + dx > screen_width: #right border
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - pixel_ground:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - pixel_ground - self.rect.bottom

        # Reducing the action points if it > 0 
        if self.action_cooldown != 0:
            self.action_cooldown -= 1
        else: 
            self.action_cooldown = 0 

        #update the fighter's position 
        self.rect.x += dx
        self.rect.y += dy
    #endregion 

    #region player controls 
    def move(self, screen_width, screen_height, pixel_ground, surface, target):
        current_time = pygame.time.get_ticks()
        
        #speed of the player and entity
        SPEED = 10
        GRAVITY = 2
        DASH_SPEED = 25
        DASH_DURATION = 300
        DASH_COOLDOWN_TIME = 1000

        #coordinate variables determine position
        dx = 0 #left/right
        dy = 0 #up/down
        self.running = False #reset the running state
        self.attack_type = 0

        current_time = pygame.time.get_ticks()

        #getting inputs of user
        key = pygame.key.get_pressed()

        if self.dashing:
            if current_time > self.timer_dash:
                self.dashing = False
                self.invincible = False
            else:
                dx = DASH_SPEED if not self.flip else -DASH_SPEED  # Ensure correct direction
                self.running = True
                self.defending = False  # Can't defend while dashing
                
                # APPLY THE MOVEMENT BEFORE EXITING
                self.rect.x += dx  
                
                #print(f"Dashing: dx={dx}, New Position={self.rect.x}")  # Debugging
                return  # Stop other movements while dashing

        if key[pygame.K_q] and not self.dashing and current_time > self.cooldown_dash:
            self.dashing = True
            self.invincible = True  # Become invincible while dashing
            self.timer_dash = current_time + DASH_DURATION  # Set dash end time
            self.cooldown_dash = current_time + DASH_COOLDOWN_TIME  # Set cooldown
            return  # Stop other movements while dashing starts

        # performing other actions when not attacking 
        if self.attacking == False and self.defending == False:
            # movements
            if key[pygame.K_a]: #moved left
                self.flip = True
                dx = -SPEED
                self.running = True
            elif key[pygame.K_d]: #moved right
                self.flip = False
                dx = SPEED
                self.running = True
            # jumping
            if key[pygame.K_w] and self.jump == False: #jumping up
                self.vel_y = -30
                self.jump = True
            # crouching 
            elif key[pygame.K_s] and not self.jump:
                if not self.crouching: 
                    self.rect.height = self.crouching_height
                    self.rect.y += self.original_height - self.crouching_height # Adjusting hitbox to go down 
                    self.crouching = True                                       # Turns the bool true for animation to play 
            else: 
                if self.crouching:
                    self.rect.y -= self.original_height - self.crouching_height # Moving the hitbox back up 
                    self.rect.height = self.original_height
                    self.crouching = False                                      # Turning the bool off to stop animation                     
            
            if pygame.mouse.get_pressed()[2]: 
                self.attack_heavy(surface, target)
            #attacks of fighter
            elif pygame.mouse.get_pressed()[0]:
                if current_time - self.last_e_press_time <= self.double_tap_threshold:
                    self.attack_type = 2
                else:
                    self.attack_type = 1
                self.last_e_press_time = current_time
                self.attack(surface, target)#'''
            elif key[pygame.K_f] and self.stamina > 0:
                self.defending = True
                self.stamina = max(self.stamina - self.cost_stamina, 0)
                #print("is defending")
            else:
                self.stamina = min(self.stamina + self.recovery_stamina, self.max_stamina)#'''

            if self.defending == True:
                self.defend(surface, target)

        #apply the gravity
        # Apply gravity, but slow descent if attacking mid-air
        if self.attacking == True and self.jump == True:
            self.vel_y += GRAVITY * 0.06  # Reduce fall speed while attacking
            self.vel_y = max(self.vel_y, -5)  # Apply a small upward push to stall
        else:
            self.vel_y += GRAVITY  # Normal gravity when not attacking
        dy += self.vel_y

        # Apply Knockback
        if self.knockback != 0:
            dx += self.knockback
            self.knockback *= 0.8  # Reduce knockback effect over time
            if abs(self.knockback) < 1:
                self.knockback = 0  # Stop knockback when it's too small

        #Ensuring fighters stay on screen
        if self.rect.left + dx < 0: #left border
            dx = -self.rect.left
        if self.rect.right + dx > screen_width: #right border
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - pixel_ground:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - pixel_ground - self.rect.bottom

        #apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        #update the fighter's position 
        if self.action_cooldown == 0:
            self.rect.x += dx
            self.rect.y += dy
    #endregion

    #region Animation Updates 
    #handle animation updates
    def updates(self):
        #chcking player action type
        if self.health <= 0:
            self.health = 0 
            self.alive = False
            self.update_action(5) # death 
        elif self.hit == True:
            self.update_action(4) # getting hit
        elif self.defending == True:
            self.update_action(8) #is defending 
        elif self.attacking == True:
            #self.update_action(6) # attacking #1 '''
            if self.attack_type == 1:
                self.update_action(1) # attacking #1
            elif self.attack_type == 2:
                self.update_action(6) # attacking #2
            elif self.attack_type == 3:
                self.update_action(7) # attacking #2
        elif self.jump == True:
            self.update_action(3) # jumping
        elif self.running == True:
            self.update_action(2) # running
        else:
            self.update_action(0) # idle

        animation_cooldown = 100 # miliseconds 
        #updating the entity image
        '''self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the ;ast update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #checking once the animation is finished
        if self.frame_index >= len(self.animation_list[self.action]):
            #check if the fighter is dead then end the animation 
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else: 
                self.frame_index = 0 # go back to the begining
            #if fighter is defending
            if self.action == 8: #or self.stamina == 0: 
                self.defending = False
            #if attack was made 
            if self.action == 1: #or self.action == 4 
                self.attacking = False
                self.attack_cooldown = 8 # prevent constant spam
            if self.action == 6: 
                self.attacking = False
                self.attack_cooldown = 8 # prevent constant spam
            if self.action == 7: 
                self.attacking = False
                self.attack_cooldown = 8 # prevent constant spam
            #checking if damage was recieved
            if self.action == 4:
                self.hit = False
                #if both fighters attack each other at the same time
                self.attacking = False
                self.attack_cooldown = 15#'''
        #check if the fighter is dead then end the animation 
        if self.alive == False:
            #self.frame_index = len(self.animation_list[self.action]) - 1
            pass 
        else: 
            self.frame_index = 0 # go back to the begining
        #if fighter is defending
        if self.action == 8: #or self.stamina == 0: 
            self.defending = False
        #if attack was made 
        if self.action == 1: #or self.action == 4 
            self.attacking = False
            self.attack_cooldown = 8 # prevent constant spam
        if self.action == 6: 
            self.attacking = False
            self.attack_cooldown = 8 # prevent constant spam
        if self.action == 7: 
            self.attacking = False
            self.attack_cooldown = 8 # prevent constant spam
        #checking if damage was recieved
        if self.action == 4:
            self.hit = False
            #if both fighters attack each other at the same time
            self.attacking = False
            self.attack_cooldown = 15
    #endregion 

    #region Knockback Function
    def knockback_function(self, force, target):
        # This function will serve as a recallable feature to knock player/entity away froma certain distance 
        
        # Applying Knockback
        KNOCKBACK_FORCE = force  # Adjust strength of knockback
        if self.flip:  
            target.knockback = -KNOCKBACK_FORCE  # Knockback left
        else:
            target.knockback = KNOCKBACK_FORCE   # Knockback right
    #endregion 

    #region Attack Function 
    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            attacking_rect = pygame.Rect(
                self.rect.centerx - (2 * self.rect.width * self.flip), 
                self.rect.y, 
                2 * self.rect.width, 
                self.rect.height
            )
            
            # Checks for the attack block is hitting the defence block zone 
            if attacking_rect.colliderect(target.defending_rect):
                print("Attack has been blocked")
                self.knockback_function(5, target)
                target.stamina -= 26
            
            # If not hotting the defence block but hitting the target
            elif attacking_rect.colliderect(target.rect):
                if target.invincible:
                    return

                # if target is not defending 
                if target.defending == False:
                    target.health -= 20                                 # Subtracts 20 health
                    target.hit = True                                   # turns on the state of being hit 
                    target.stun_timer = pygame.time.get_ticks() + 500   # adds value to stun 
                    target.action_cooldown = 45                         # adds value to action cooldown to prevent opponents from instant action 

                    # Apply Knockback
                    self.knockback_function(2, target)
                else:
                    target.health -= 2
                    target.stamina -= 34

                    # Apply Knockback
                    self.knockback_function(5, target)

                # Check for simultaneous hit
                if target.attacking:
                    self.hit = True
                    self.knockback_function(40, target)
                
            pygame.draw.rect(surface, (0, 255, 0), attacking_rect)
    #endregion 

    #region attack(kick) function
    def attack_heavy(self, surface, target):
        if self.attack_cooldown == 0:
            #self.attacking = True
            heavyact_rect = pygame.Rect(
                self.rect.centerx - (1.75 * self.rect.width * self.flip), 
                self.rect.y, 
                1.75 * self.rect.width, 
                self.rect.height
            )

            # Checks for the attack block is hitting the defence block zone 
            if heavyact_rect.colliderect(target.defending_rect):
                self.knockback_function(8, target)
                target.stamina -= 1000

             # If not hotting the defence block but hitting the target
            elif heavyact_rect.colliderect(target.rect):
                if target.invincible:
                    return

                # if target is not defending 
                if target.defending == False:
                    target.health -= 20                                 # Subtracts 20 health
                    target.hit = True                                   # turns on the state of being hit 
                    target.stun_timer = pygame.time.get_ticks() + 500   # adds value to stun 
                    target.action_cooldown = 45                         # adds value to action cooldown to prevent opponents from instant action 

                    # Apply Knockback
                    self.knockback_function(2, target)
                else:
                    target.health -= 2
                    target.stamina -= 110

                    # Apply Knockback
                    self.knockback_function(5, target)

            pygame.draw.rect(surface, (0, 255, 0), heavyact_rect)
    #endregion 

    #region Defending Function 
    def defend(self, surface, target):
        self.defending_rect = pygame.Rect(
            self.rect.centerx - (1.65 * self.rect.width * self.flip), # X-Position 
            self.rect.y,                                             # Y-Position 
            1.65 * self.rect.width,                                  # Width 
            self.rect.height                                         # Height 
            )
        
        pygame.draw.rect(surface, (0, 0, 255), self.defending_rect)
    #endregion 

    #region update actions 
    def update_action(self, new_action):
        #checking if the new action is different 
        if new_action != self.action:
            self.action = new_action
            #updating the animation settings
            self.frame_index = 0 
            self.update_time = pygame.time.get_ticks()
    #endregion


