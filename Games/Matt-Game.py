#!/usr/bin/python3
""" 
Reference: https://www.pygame.org/docs/
           https://realpython.com/pygame-a-primer/
"""
# Import the pygame library
import pygame 
# Import Randomization functions from random library
import random
# Import time for seeding rand
import time
# Import system library
from sys import exit
pygame.init() #init game library


# Global variable for controlling screen size 
ScreenSize = WIDTH , HEIGHT = 800, 800
# Global variable that sets a default screen color, this is a tuple and could be represented as (250, 250, 250) in place of this variable
BaseColor = 0, 0, 0 
# Global variable that is used to set the screen a specific color when the player dies
GameOverColor = 250, 0, 0

# A variable that controls the speed of the waves
WaveSpeed = 1250 # 1.25 seconds

# a custom event for adding a new enemy
NEWWAVE = pygame.USEREVENT + 1
pygame.time.set_timer(NEWWAVE, WaveSpeed)



# This is a class square that inherits from pygames Sprite class
class square(pygame.sprite.Sprite):
    # This defines how far the object will move at each key press
    move_speed = 10 
    # This defines the color of the square (player), it is a 3-tuple of RGB
    color = (250, 250, 250)

    # init function that takes a integer size to make a specifically sized square
    # this has a default value of 100
    def __init__(self, size:int = 100):
        #calls init method of parent class
        super(square,self).__init__() 
        self.surf = pygame.Surface((size, size)) # sets size of surface
        self.surf.fill(self.color) # sets color of the surface (In this case it is white)
        self.rect = self.surf.get_rect() # The rectangular coordinates of the surface are returned.        

    # This is a function that is called to update to position of the players square
    def update(self, keyInput):
        if keyInput[pygame.K_w] and ((self.rect.top - self.move_speed) >= 0):
            if not keyInput[pygame.K_d] and not keyInput[pygame.K_a]:
                self.rect.move_ip(0, -self.move_speed) # move up 10 pixels
            elif keyInput[pygame.K_d] and ((self.rect.right + self.move_speed) <= WIDTH):
                self.rect.move_ip(self.move_speed, -self.move_speed)
            elif keyInput[pygame.K_a] and ((self.rect.left - self.move_speed) >= 0):
                self.rect.move_ip(-self.move_speed, -self.move_speed)
        elif keyInput[pygame.K_s] and ((self.rect.bottom + self.move_speed) <= HEIGHT):
            if not keyInput[pygame.K_d] and not keyInput[pygame.K_a]:
                self.rect.move_ip(0, self.move_speed) # move up 10 pixels
            elif keyInput[pygame.K_d] and ((self.rect.right + self.move_speed) <= WIDTH):
                self.rect.move_ip(self.move_speed, self.move_speed)
            elif keyInput[pygame.K_a] and ((self.rect.left - self.move_speed) >= 0):
                self.rect.move_ip(-self.move_speed, self.move_speed)
        elif keyInput[pygame.K_a] and ((self.rect.left - self.move_speed) >= 0):
            self.rect.move_ip(-self.move_speed, 0) # move left 10 pixels
        elif keyInput[pygame.K_d] and ((self.rect.right + self.move_speed) <= WIDTH):
            self.rect.move_ip(self.move_speed, 0) # move right 10 pixels

# this class represents the enemy sprites 
class EnemySprite(pygame.sprite.Sprite):
    # This defines the color of the square (player), it is a 3-tuple of RGB
    color = (255, 0, 0)
    # This is used in the randomization of how 'fast' the blocks will approach by changing how far out they are 'spawned'
    distMul = 100
    base = 10

    def __init__(self, size:int = 50):
        #calls init method of parent class
        super(EnemySprite,self).__init__()
        # seed random number generator with the current time
        random.seed(time.time())
        # This defines how far the object will move at each tick, in this case they are random between 1 and 20 pixels a tick
        self.move_speed = random.randint(1 , 20) 
        self.surf = pygame.Surface((size, size)) # sets size of surface
        self.surf.fill(self.color) # sets color of the surface (In this case it is white)
        self.rect = self.surf.get_rect(
            # This randomizes the spawn point of the block, it will appear off screen and should move on screen, we vary the distance as they all move at the same speed 
            center = (
                random.randint((WIDTH + size), (WIDTH + (size  + (self.base * self.distMul)))),
                random.randint(0, HEIGHT)
            )

        ) # The rectangular coordinates of the surface are returned.   

    def update(self):
        self.rect.move_ip(-self.move_speed, 0)
        if self.rect.right < 0:
            self.kill()


# This is used to update the sprite groups
def createEnemySprites():
    # This value defines the number of enemies that will be 'spawned' each round.
    num_enemy = 10
    # This value defines the minimum size of the block (must be greater than 0)
    min_size = 10
    # This value defines the max size of the block
    max_size = 30
    # These are used for temporary storage of the sprites to be returned.
    TempSpriteGroup = []

    # Initialize the enemies
    for x in range(num_enemy):
        TempSpriteGroup.append(EnemySprite(int(random.randint(min_size, max_size))))
    # Return a 2-tuple to be unpacked and assigned to All Sprites and Enemy Sprite groups 
    return TempSpriteGroup

def main():
    # Setup the clock for a decent and constant framerate
    clock = pygame.time.Clock()
    # Set up the drawing window, this is determined by the 2-tuple of ScreenSize - (Height x Width) pixels
    screen = pygame.display.set_mode(ScreenSize)
    # This boolean value determines whether the game continues running or not 
    ContinueRunning = True
    # This variables controls the (loose) max number of sprites on the screen
    # as they are made in batches if the batch size is 10, and 49 sprites are created then the max is really 59
    # if the limit is set at 50.
    max_sprites = 100

    # player_sprite = square(), this is the player sprite
    player_sprite = square(int(30))
    # the to groups of sprites (objects) to display, one is used for displaying and the other collision detection
    # Generate both using the createEnemySprites function
    EnemyGroup = pygame.sprite.Group()
    AllGroup = pygame.sprite.Group()

    # add player to the group to draw
    AllGroup.add(player_sprite)

    # This is while loop, the comparison is added for clarity.
    # While the condition evaluates to true the body (indented aria below) is executed.
    while ContinueRunning == True: 
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == pygame.K_ESCAPE:
                    pygame.quit() #quit the game
                    exit() #imported from sys, since we are doing from sys import exit, we dont need sys.exit
            elif event.type == pygame.QUIT:
                pygame.quit() #quit the game
                exit() # exits current running process 

            elif event.type == NEWWAVE:
                # This adds the enemy sprite to each group, (to draw and enemy)
                # we check the number of objects in the EnemyGroup object and if
                # it is less than the max_sprites value a new wave will be spawned
                if len(EnemyGroup.sprites()) < max_sprites:
                    for e_sprite in createEnemySprites():
                        EnemyGroup.add(e_sprite)
                        AllGroup.add(e_sprite)
        # fills screen with the RGB color represented by the 3-tuple BaseColor
        screen.fill(BaseColor) 

        # update player position based on the keys pressed
        player_sprite.update(pygame.key.get_pressed())
        # updates each enemy sprite in the EnemyGroup object
        EnemyGroup.update()        

        # loop through all sprites in the group, place them on the screen 
        for sprite in AllGroup:
            screen.blit(sprite.surf, sprite.rect)
            
        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(player_sprite, EnemyGroup): 
            # remove the player from the screen 
            player_sprite.kill()
            # stop execution of the game loop
            ContinueRunning = False
            # set color of the screen to be red to signify the game is over
            screen.fill(GameOverColor)
        pygame.display.flip() #updates the displayed application
        clock.tick(30)
    #sleep for 5 seconds
    time.sleep(3)
    pygame.quit() #quit the game


# This allows us to make a 'main' function as if the __name__ is set to __main__ when it is executed as a well an executable and not 
# imported into another script, then it will execute the main function, otherwise nothing in this case will happen
if __name__ == "__main__": 
    main()
