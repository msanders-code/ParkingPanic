
import pygame as pg  #imports the game engine 

width = 800  #width of game screen
height = 900  #height of game screen

FPS = 60  #max frame rate

class setUp:  #initial game set up class
    
    pg.init()  #initializes the pygame module
    
    #Sets the display icon to the game icon
    icon_image = pg.image.load(r"C:\Python\Game_Dev\ParkingPanic\RPG1\icon.png")
    icon = pg.transform.scale(icon_image, (20,20))
    icon_surface = pg.Surface((20,20))
    new_icon = icon_surface.blit(icon, (0,0))
    pg.display.set_icon(icon_surface)


    def __init__(self,width,height):  #holds all the initial set up parameters and loads all game images
        self.width = width
        self.height = height
        
        global  screen,clock,background,image_2,enemy_image,goal_image,font, enemy_image_2
        
        screen = pg.display.set_mode((self.width,self.height))  #sets the parameters to draw the game window
        clock = pg.time.Clock()  #time count for FPS
        pg.display.set_caption("Parking Panic!")  #adds a title to the game window
    
        image_1 = pg.image.load(r"C:\Python\Game_Dev\ParkingPanic\RPG1\background_2.jpg") #loading background image
        image_2 = pg.image.load(r"C:\Python\Game_Dev\ParkingPanic\RPG1\car_sprite.png") #loading player image
        image_3 = pg.image.load(r"C:\Python\Game_Dev\ParkingPanic\RPG1\enemy2.png") #loading the enemy image
        image_4 = pg.image.load(r"C:\Python\Game_Dev\ParkingPanic\RPG1\end_goal2.png") #loading the end goal image
        background = pg.transform.scale(image_1,(self.width,self.height)) #scaling the background image to the game window
        enemy_image = pg.transform.scale(image_3, (int(self.width*0.08),int(self.height*0.08))) #scaling the enemy image
        enemy_image_2 = pg.transform.scale(image_3, (int(self.width*0.06),int(self.height*0.06))) #scaling the enemy image
        goal_image = pg.transform.scale(image_4, (int(self.width*0.1),int(self.height*0.1))) #scaling the end goal image

class gameObject:  #generic game object characteristics

    def __init__(self,image,x_pos,y_pos,W,H):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.W = W
        self.H = H

    def draw(self,window):
        window.blit(self.image,(self.x_pos,self.y_pos))
 
class gamePlayer: #sets up the player's characteristics
        
    def __init__(self,x_pos,y_pos,W,H,speed,w_change = (width*0.0012),h_change = (height*0.0012)):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.W = W
        self.H = H
        self.speed = speed
        self.width_change = w_change
        self.height_change = h_change

    def movement(self,direction):

        speed = self.speed

        # movement and scaling for forced perspective of character
        if direction == 1:
            self.y_pos -= speed
            self.W -= self.width_change
            self.x_pos += (self.width_change/2)
            self.H -= self.height_change
        elif direction == -1:
            self.y_pos += speed
            self.W += self.width_change
            self.x_pos -= (self.width_change/2)
            self.H += self.height_change

        # Bounds checking to keep player on screen
        if self.y_pos > int(height - ((height*0.125)+((height*0.125)/4))):
            self.y_pos = int(height - ((height*0.125)+((height*0.125)/4)))
            self.x_pos = int((width/2)-((width*0.125)/2))
            self.W = int(width*0.125)
            self.H = int(height*0.125)
        elif self.y_pos <= 20:
            self.y_pos = int(height - ((height*0.125)+((height*0.125)/4)))
            self.x_pos = int((width/2)-((width*0.125)/2))
            self.W = int(width*0.125)
            self.H = int(height*0.125)
    
    def collision(self,other_object):
        #checking y position
        if self.y_pos > (other_object.y_pos + other_object.H):
            return False
        elif (self.y_pos + self.H) < other_object.y_pos:
            return False
        
        #checking x position
        if self.x_pos > (other_object.x_pos + other_object.W):
            return False
        elif (self.x_pos + self.W) < other_object.x_pos:
            return False

        return True

    def draw_char(self,window):
        player_image = pg.transform.scale(image_2,(int(self.W),int(self.H))) #scaling the player image
        gameObject(player_image,self.x_pos,self.y_pos,self.W,self.H).draw(window)

class enemyChar(gameObject):  #sets up enemy characteristics

    def __init__(self,x_pos,y_pos,W,H,speed,image):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.W = W
        self.H = H
        self.speed = speed
        self.image = image

    def movement(self):
        
        global width
        speed = self.speed
        
        if self.x_pos <= 20:
            self.speed = abs(self.speed)
        elif self.x_pos >= ((int(width*(1-0.08))) - 20):
            self.speed = -abs(self.speed)
        self.x_pos += speed

    def draw_char(self,window):
        super().draw(window)

class endGoal(gameObject):  #sets the end goal characteristics

    def __init__(self,image,W,H,x_pos,y_pos = int(height*0.135)):
        self.image = image
        self.H = H
        self.W = W
        self.x_pos = x_pos
        self.y_pos = y_pos

    def draw(self,window):
        super().draw(window)

class titleScreen:
    """
    Starts the game with a title screen to show controls.
    """

    def __init__(self, frame_rate, game_window):
        self.frame_rate = frame_rate
        self.game_window = game_window

    def loop(self):
        start_game = False
        global width, height

        while not start_game:

            for choice in pg.event.get():
                if choice.type == pg.QUIT:
                    start_game = True
                    return pg.quit()
                elif choice.type == pg.KEYDOWN:
                    if choice.key == pg.K_SPACE:
                        start_game = True
                        gameLoop(FPS, screen, 1, 6).loop()
                        return pg.quit()
                    elif choice.key == pg.K_ESCAPE:
                        start_game = True
                        return pg.quit()

            self.game_window.fill((97, 115, 249))
            font_1 = pg.font.SysFont("Arial", 100, True)
            font_2 = pg.font.SysFont("Arial", 50, True)
            line_1 = font_1.render("Welcome", True, (0, 0, 0))
            line_2 = font_1.render("to Parking Panic!", True, (0, 0, 0))
            line_3 = font_2.render("> W to go forward", True, (0, 0, 0))
            line_4 = font_2.render("> S to go backward", True, (0, 0, 0))
            line_5 = font_2.render("- hit SPACEBAR to continue -", True, (0, 0, 0))
            line_6 = font_2.render("- hit ESC to exit -", True, (0, 0, 0))
            self.game_window.blit(line_1, (width/2 - 180, height - 850))
            self.game_window.blit(line_2, (width - 730, height - 650))
            self.game_window.blit(line_3, (width - 730, height - 450))
            self.game_window.blit(line_4, (width - 730, height - 400))
            self.game_window.blit(line_5, (width - 680, height - 225))
            self.game_window.blit(line_6, (width - 555, height - 175))

            pg.display.update()
            clock.tick(self.frame_rate)

class gameLoop:  #game loop class 

    def __init__(self,frame_rate,game_window, level, enemy_speed):
        self.frame_rate = frame_rate
        self.game_window = game_window
        self.level = level  #Game level
        self.enemy_speed = enemy_speed  #speed of the enemy character(s)
        
    def loop(self):
        pg.init()

        game_over = False  #game state variable
        direction = 0  #variable to set character movement direction
        character_speed = 8  #speed of the player's character
        global width, height  #screen size variables

        #player initial set up in game loop
        character = gamePlayer(int((width/2)-((width*0.125)/2)),int(height - ((height*0.125)+((height*0.125)/4))),(width*0.125),(height*0.125),character_speed)
        enemy = enemyChar(20,(height/2),int(width*0.08),int(height*0.08),self.enemy_speed,enemy_image) #enemy initial set up in game loop
        enemy_2 = enemyChar(int(width*(1-0.08)) - 20,int(height*(1/3))-10,int(width*0.06),int(height*0.06),self.enemy_speed,enemy_image_2) #enemy initial set up in game loop
        goal = endGoal(goal_image,int(width*0.1),int(height*0.1),((width/2)-(int(width*0.1)/2))) #goal initial set up in game loop
        while not game_over:  #game loop
            
            for e in pg.event.get():  #recods actions in the game
                if e.type == pg.QUIT:
                    game_over = True
                    return pg.quit()
                elif e.type == pg.KEYDOWN:
                    if e.key == pg.K_w:
                        direction = 1
                    elif e.key == pg.K_s:
                        direction = -1
                elif e.type == pg.KEYUP:
                    if e.key == pg.K_w or e.key == pg.K_s:
                        direction = 0

            #adds a background image to the game window
            self.game_window.blit(background, (0,0))  
            
            #drawing the end goar on the screen
            goal.draw(self.game_window)
            
             #adding enemy character and enemy movement to screen
            if self.level == 1:
                enemy.movement()
                enemy.draw(self.game_window)
            elif self.level == 2:
                enemy.movement()
                enemy_2.movement()
                enemy.draw(self.game_window)
                enemy_2.draw(self.game_window)
            else:
                enemy.movement()
                enemy_2.movement()
                enemy.draw(self.game_window)
                enemy_2.draw(self.game_window)
            #adding character movement and drawing character on screen
            character.movement(direction)
            character.draw_char(self.game_window)

            #collision detection
            if character.collision(enemy) == True or character.collision(enemy_2) == True:
                
                while not game_over: 
                    decision_window = pg.Rect((width/2 - 250, height/2 - 150),(500, 300)) 
                    pg.draw.rect(self.game_window,(201, 158, 230), decision_window)
                    font_1 = pg.font.SysFont("Arial", 75, True)
                    font_2 = pg.font.SysFont("Arial", 25, True)
                    line_1 = font_1.render("You Lose!", True, (0, 0, 0))
                    line_2 = font_2.render("Quit?(ESCAPE) or Play again?(SPACEBAR)", True, (0, 0, 0))
                    self.game_window.blit(line_1, (width/2 - 150, height/2 - 100))
                    self.game_window.blit(line_2, (width/2 - 218, height/2 + 85))
                    for decision in pg.event.get():
                        if decision.type == pg.KEYDOWN:
                            if decision.key == pg.K_ESCAPE:
                                game_over = True
                                return pg.quit()
                            elif decision.key == pg.K_SPACE:
                                game_over = True
                                return gameLoop(FPS, screen, 1, 6).loop()
                        elif decision.type == pg.QUIT:
                            game_over = True
                            return pg.quit()
                    pg.display.update()
                    clock.tick(self.frame_rate)
            elif character.collision(goal) == True:
                
                while not game_over:
                    decision_window = pg.Rect((width/2 - 250, height/2 - 150),(500, 300)) 
                    pg.draw.rect(self.game_window,(201, 158, 230), decision_window)
                    font_1 = pg.font.SysFont("Arial", 75, True)
                    font_2 = pg.font.SysFont("Arial", 25, True)
                    line_1 = font_1.render("You Win!", True, (0, 0, 0))
                    line_2 = font_2.render("Quit?(ESCAPE) or Next Level?(SPACEBAR)", True, (0, 0, 0))
                    self.game_window.blit(line_1, (width/2 - 140, height/2 - 100))
                    self.game_window.blit(line_2, (width/2 - 218, height/2 + 85))
                    for decision in pg.event.get():
                        if decision.type == pg.KEYDOWN:
                            if decision.key == pg.K_ESCAPE:
                                game_over = True
                                return pg.quit()
                            elif decision.key == pg.K_SPACE:
                                game_over = True
                                return gameLoop(FPS, screen, self.level + 1, self.enemy_speed + 1).loop()
                        elif decision.type == pg.QUIT:
                            game_over = True
                            return pg.quit()
                    pg.display.update()
                    clock.tick(self.frame_rate)
            
            pg.display.update()  #Re-draws the display
            clock.tick(self.frame_rate)  #sets the max frame rate


if __name__ == "__main__":
    setUp(width,height)
    titleScreen(FPS, screen).loop()



