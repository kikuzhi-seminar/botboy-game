"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/
"""
 
import pygame
 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
Vzero=1
a=3
Time=0
JAMP=False
JHeight=0

class Player(pygame.sprite.Sprite):
    """ The class is the player-controlled sprite. """


    # -- Methods
    def __init__(self, x, y):
        """Constructor function"""
        # Call the parent's constructor
        super().__init__()
 
        # Set height, width
        self.image = pygame.Surface([15, 15])
        self.image.fill(BLACK)



        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
        # -- Attributes
        # Set speed vector
        self.change_x = 0
        self.change_y = 0
 
    def changespeed(self, x, y):
        """ Change the speed of the player"""
        self.change_x += x
        self.change_y += y
 
    def update(self):
        """ Find a new position for the player"""
        self.rect.x += self.change_x
        self.rect.y += self.change_y

    def jamp(self,Time):
        self.rect.y += 1 * Time - 3 * Time*Time




 
 
# Call this function so the Pygame library can initialize itself
pygame.init()
 
# Create an 800x600 sized screen
screen = pygame.display.set_mode([800, 600])

def draw_stick_figure(screen, x,y):
    # Head
    pygame.draw.ellipse(screen, BLACK, [1 + x, y, 10, 10], 0)

    # Legs
    pygame.draw.line(screen, BLACK, [5 + x, 17 + y], [10 + x, 27 + y], 2)
    pygame.draw.line(screen, BLACK, [5 + x, 17 + y], [x, 27 + y], 2)

    # Body
    pygame.draw.line(screen, RED, [5 + x, 17 + y], [5 + x, 7 + y], 2)

    # Arms
    pygame.draw.line(screen, RED, [5 + x, 7 + y], [9 + x, 17 + y], 2)
    pygame.draw.line(screen, RED, [5 + x, 7 + y], [1 + x, 17 + y], 2)
# Set the title of the window
pygame.display.set_caption('Test')
 
# Create the player object
player = Player(500, 500)
all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(player)
 
clock = pygame.time.Clock()
done = False
 
while not done:
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
        # Set the speed based on the key pressed
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(3, 0)
            elif event.key == pygame.K_UP:
                if JAMP==False:
                    JAMP=True



            print(JAMP)
            if JAMP==True:
                Time+=1
            player.jamp(Time)
            if Time>30:
                JAMP=False
 
        # Reset speed when key goes up
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(3, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-3, 0)
#            elif event.key == pygame.K_UP:
#                player.changespeed(0, 3)

 
    # This actually moves the player block based on the current speed
    player.update()

    # -- Draw everything
    # Clear screen
    screen.fill(WHITE)

    draw_stick_figure(screen, player.rect.x, player.rect.y)
 
    # Draw sprites
    #all_sprites_list.draw(screen)
 
    # Flip screen
    pygame.display.flip()
 
    # Pause
    clock.tick(60)
 
pygame.quit()