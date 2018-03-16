
import pygame
import random
 
# Global constants
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (245, 158, 44)
DARK_ORANGE = (189, 108, 2)
SEA_BLUE = (79, 194, 243)
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700



class Object(pygame.sprite.Sprite):

    def __init__(self, imported_image):

        pygame.sprite.Sprite.__init__(self)
        #unsure if this is the correct way to import image, might have to
        #import it here directly with quotes and all
        self.image = pygame.image.load(imported_image).convert()
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        #Define change_y here so we can mess with gravity in player class later
        self.change_y = 0

    def update(self):
        self.rect.x -= 5
        self.mask = pygame.mask.from_surface(self.image)
        #Get rid of object if it goes far off screen left
        if self.rect.x < -500:
                self.kill()

class Player(Object):
    def update(self):
        #add some gravity
        self.calc_grav()
        self.rect.y += self.change_y
        #set parameters for how player will react to keychanges (as seen
        #makes sure player doesn't sink off screen
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - self.rect.height
        if self.rect.y <= -20:
            self.rect.y = -20
        #Load images for animating swimming, take away comment hashtags to activate
        #self.swimming_fish = []
        #image = pygame.image.load("fish_swim_1.png").convert()
        #self.swimming_fish.append(image)
        #image = pygame.image.load("fish_swim_2.png").convert()
        #self.swimming_fish.append(image)
        #image = pygame.image.load("fish_swim_3.png").convert()
        #self.swimming_fish.append(image)
        #image = pygame.image.load("fish_swim_4.png").convert()
        #self.swimming_fish.append(image)
        #image = pygame.image.load("fish_swim_5.png").convert()
        #self.swimming_fish.append(image)

        #if self.change_y < 0:
            #frame = (self.rect.y // 30) % len(self.swimming_fish)
            #self.image = self.swimming_fish[frame]

        if self.change_y < 0:
            self.bubble_sound.play()
            

        self.mask = pygame.mask.from_surface(self.image)

        #add bubble pop sound
        self.bubble_sound = pygame.mixer.Sound("pop.ogg")


    def swim(self):
        self.change_y = -10

    def sink(self):
        self.change_y = 0
        
    def calc_grav(self):
        self.change_y += 0.5


class Game(object):

    def __init__(self):
        self.game_over = False

        #list of bad guys
        self.enemy_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        self.background_x = 0

        #Create 10 sharks in random locations on and beyond screen
        for i in range(10):
            shark = Object("pixilShark2.png")

            #set renadom location for sharks
            shark.rect.x = random.randrange(400, 5000)
            shark.rect.y = random.randrange(-200, 300)
            

            #add shark to list of objects
            self.enemy_list.add(shark)
            self.all_sprites_list.add(shark)

        #Create 12 sea mines
        for i in range(12):
            mine = Object("sea_mine.png")

            mine.rect.x = random.randrange(5000, 8000)
            mine.rect.y = random.randrange(300, 450)

            self.enemy_list.add(mine)
            self.all_sprites_list.add(mine)
                
      

        #Add player as an instance of Player class)
        self.player = Player("fish_swim_5.png")
        #set initial location of player
        self.player.rect.x = 150
        self.player.rect.y = 150
        self.all_sprites_list.add(self.player)

        #TRYING TO GET SHARKS TO SLOW DOWN WHEN BACKGROUND IMAGES PAUSES FOR
        #PLAYER ON BOTTOM OF SCREEN
        if self.player.rect.y >= (SCREEN_HEIGHT - self.player.rect.height):
            for self.shark in self.enemy_list:
                self.shark.rect.x -= 3
        

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    self.__init__()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.swim()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.player.sink()
                
        return False

    def run_logic(self):
        if not self.game_over:
            self.all_sprites_list.update()
            #check for collision, mask code found at this tutorial: https://www.youtube.com/watch?v=Dspz3kaTKUg&list=PLOxCywNiBgqp3G9qDJIQJkDFBtpI303fc&index=1&t=0s
            self.sprite_hit_list = pygame.sprite.spritecollide(self.player, self.enemy_list, False)                   
            if len(self.sprite_hit_list) >= 1:
                self.spritemask_hit_list = pygame.sprite.spritecollide(self.player,
                                                                   self.enemy_list, False,
                                                                   pygame.sprite.collide_mask)
                if len(self.spritemask_hit_list) >=1:
                    self.game_over = True
                    
                
            #If I want to add a scored item it would go here apparently

    def display_frame(self, screen):
        
        background_image = pygame.image.load("underwater_tileable.png").convert()
        #Scroll background image, code found at tutorial here: https://www.youtube.com/watch?v=US3HSusUBeI
        self.rel_x = self.background_x % background_image.get_rect().width
        
        self.background_x -= 3
        #Created the below variable so I could plug it in to pause background image
        #on game over screen or when fish is on bottom of screen instead of
        #having it reset to 0
        self.adjusted_background_coordinate = self.rel_x - background_image.get_rect().width
        
        screen.blit(background_image, [self.adjusted_background_coordinate, 0])
        if self.rel_x < SCREEN_WIDTH:
            screen.blit(background_image, [self.rel_x, 0])

        #This pauses background image where it is when player on floor of ocean
        if self.player.rect.y >= (SCREEN_HEIGHT - self.player.rect.height):
            self.background_x = self.rel_x - background_image.get_rect().width
        
            

        
        
       
        

        if self.game_over:
            # font = pygame.font.Font("Menlo", 25)
            font = pygame.font.SysFont("Menlo", 25)
            text = font.render("Game Over: Click screen to restart", True, BLACK)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])
            #stop background image if game is over 
            self.background_x = self.rel_x - background_image.get_rect().width
            

        if not self.game_over:
            self.all_sprites_list.draw(screen)
            
        
        pygame.display.flip()
        



def main():
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    #bring in global background x coordinate starting point of 0
    

   

    pygame.display.set_caption("Golden Fish")

    

    done = False
    clock = pygame.time.Clock()
    

    #create instance of Game class
    game = Game()

    while not done:

        #Process events (keystrokes, mouse clicks, etc.)
        done = game.process_events()

        #Update object positions, check for collisions
        game.run_logic()

        #Draw the current frame
        game.display_frame(screen)

        

        
                
        #Pause for the next frame
        clock.tick(60)
        
        
        

    pygame.quit()

if __name__ == "__main__":
    main()



