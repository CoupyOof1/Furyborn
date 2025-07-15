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

        # Player cool down 
        self.attack_type = 0
        self.cooldown_dash = 0
        self.stun_timer = 0
        self.timer_dash = 0
        self.last_e_press_time = 0
        self.double_tap_threshold = 250

    def drawing_healthbar(self, screen, amount, x, y, colour, pos_y, pos_x):
        ratio = amount / 500
        x_offset = x - pos_x # determines the position of the healthbar 
        pygame.draw.rect(screen, (255, 255, 255), (x_offset - 2, y - (pos_y + 2), 104, 21))  # border
        pygame.draw.rect(screen, (255, 0, 0), (x_offset, y - pos_y, 100, 17))            # background
        pygame.draw.rect(screen, colour, (x_offset, y - pos_y, 100 * ratio, 17))      # foreground

    def drawsprite(self, surface):
        pygame.draw.rect(surface, (255,0,0), self.rect)
        self.drawing_healthbar(surface, self.health, self.rect.x, self.rect.y, (0, 255, 0), 34, 25)  # Red bar

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

        #performing other actions when not attacking 
        if self.attacking == False and self.defending == False:
            #movements of fighter
            if key[pygame.K_a]: #moved left
                self.flip = True
                dx = -SPEED
                self.running = True
            if key[pygame.K_d]: #moved right
                self.flip = False
                dx = SPEED
                self.running = True
            #jumping of Fighter
            if key[pygame.K_w] and self.jump == False: #jumping up
                self.vel_y = -30
                self.jump = True
            #attacks of fighter
            if key[pygame.K_e]:
                if current_time - self.last_e_press_time <= self.double_tap_threshold:
                    #Detecting double tap E
                    self.attack_type = 2
                else:
                    self.attack_type = 1
                self.last_e_press_time = current_time
                self.attack(surface, target)
            if key[pygame.K_r]:
                #self.attack_type = 3
                self.attack(surface, target)
                #self.stabattack(surface, target) #
            if key[pygame.K_f] and self.stamina > 0:
                self.defending = True
                self.stamina = max(self.stamina - self.cost_stamina, 0)
                #print("is defending")
            else:
                self.stamina = min(self.stamina + self.recovery_stamina, self.max_stamina)

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
        self.rect.x += dx
        self.rect.y += dy
    #endregion

    #region Attack Function 
    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                #print("Hit")

                if target.invincible:
                    return

                if target.defending == False:
                    target.health -= 20
                    target.hit = True
                    target.stun_timer = pygame.time.get_ticks() + 500
                else:
                    target.health -= 2
                    target.stamina -= 34

                    # Apply Knockback
                    KNOCKBACK_FORCE = 5  # Adjust strength of knockback
                    if self.flip:  
                        target.knockback = -KNOCKBACK_FORCE  # Knockback left
                    else:
                        target.knockback = KNOCKBACK_FORCE   # Knockback right

                # Check for simultaneous hit
                if target.attacking:
                    KNOCKBACK_FORCE = 40
                    self.hit = True
                    if target.flip:  
                        self.knockback = -KNOCKBACK_FORCE  # Knockback left
                        target.knockback = KNOCKBACK_FORCE  # Knockback right
                    else:
                        self.knockback = KNOCKBACK_FORCE   # Knockback right
                        target.knockback = -KNOCKBACK_FORCE  # Knockback left
                
            pygame.draw.rect(surface, (0, 255, 0), attacking_rect)
    #endregion 
