import pygame
import random
from random import randint
import numpy
import server
import client
import threading
from sys import exit
from itertools import product
import socket
import sys
import time
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
STATUS = ''
MY_NAME = "enter your name"
OPPONENT_NAME = ''
PLAYER_CLASS = "Dagger"
#constants
SCREEN_SIZE = (800,500)
DEEP_RED = (66, 15, 15)
BLACK = (0,0,0)
DARK_GRAY = (50,50,50)
RED = (255,0,0)
DARK_YELLOW = (130, 108, 0)
LIGHT_YELLOW = (227, 197, 0)
GRAY_YELLOW = (69,69,60)
DARK_BLUE = (15, 95, 117)
LIGHT_BLUE = (50, 143, 168)
BUTTON_1 = (100,300,200,120)
BUTTON_2 = (475,300,200,120)
BUTTON_3 = (20,370,200,120)
BACK_BUTTON = (310,370,150,80)
TEXT_ENTRY_BOX = (275, 170, 250, 40)
NAME_DISPLAY = (500,450,250,40)
OPPONENT_NAME_DISPLAY = (500,145,250,40)

class Button:
    def __init__(self, color=(0,0,0), rect=(0,0,0,0), text="", text_color=BLACK,text_font=''):
        self.color = color
        self.rect = rect
        self.text = text
        self.text_color = text_color
        self.text_font = text_font
        

    def draw(self, screen):
        pygame.draw.rect(screen, self.color,self.rect)
        if self.text != '':
            if self.text_font == '':
                font = pygame.font.SysFont('unispacebold', 40)
            else:
                font = pygame.font.SysFont(self.text_font[0],self.text_font[1])

            text = font.render(self.text, True, self.text_color)
            button_width_slicer = slice(2,3)
            button_width_tuple = self.rect[button_width_slicer]
            button_width = int(''.join(map(str,button_width_tuple)))
            button_height_slicer = slice(3,4)
            button_height_tuple = self.rect[button_height_slicer]
            button_height = int(''.join(map(str,button_height_tuple)))
           # print(button_width)
            button_center_x = (button_width//2)
            button_center_y = (button_height//2)
            button_pos_x = self.rect[0]
            button_pos_y_tuple = self.rect[1:2]
            button_pos_y = int(''.join(map(str,button_pos_y_tuple)))
            button_center = ((button_center_x+button_pos_x),+(button_center_y+button_pos_y))
            text_rect_center = (((text.get_width())//2,(text.get_height()//2)))
            


            text_rect = text.get_rect() # get text rect
            text_rect.center = button_center # center text on button
            screen.blit(text,tuple(numpy.subtract(button_center, text_rect_center)))

    def isOver(self, pos):
        button_pos_x = self.rect[0]
        button_pos_y_tuple = self.rect[1:2]
        button_pos_y = int(''.join(map(str,button_pos_y_tuple)))
        button_width_slicer = slice(2,3)
        button_width_tuple = self.rect[button_width_slicer]
        button_width = int(''.join(map(str,button_width_tuple)))
        button_height_slicer = slice(3,4)
        button_height_tuple = self.rect[button_height_slicer]
        button_height = int(''.join(map(str,button_height_tuple)))
        #Pos is the mouse position or a tuple of (x,y) coordinates+self.rect[rect_size_slice]
        if pos[0] > self.rect[0] and pos[0] < (button_pos_x+button_width):
            if pos[1] > self.rect[1] and pos[1] < (button_pos_y+button_height):
                return True
            
        return False

    def animate(self,size,start_stop):
        if start_stop == "start":
            if size == self.rect:
                #convert button location and size tuple into a string of floats to
                #change size on a percentage base
                a=list(self.rect)
                a=[float(i) for i in a]
                #shrinks all floats in string
                a= [i*.96 for i in a]
                #converts back to int and slices out the width and height
                a=[int(i) for i in a]
                b=a[2:]
                #same process as above; we need to figure out how much the button
                #shrinks by(roughly) so we can offset the position of the box so it appears
                #to shrink off of its center, instead of top left corner.
                c=list(self.rect)
                c=[float(i) for i in c]
                c= [i*.02 for i in c]
                c=[int(i) for i in c]
                #d=button width shrink amount, e=button height shrink amount
                d=c[2:3]
                e=c[3:]
                #similar process again, this time to modify the postion of our button
                f=list(self.rect)
                #g= button pos x
                g= f[:1]
                #h= button pos y
                h= f[1:2]
                j = (g[0]+d[0])
                k = (e[0]+h[0])
                #adding all adjusted elements back into a tuple
                l = (j,k,b[0],b[1])
                self.rect = l
            else:
                return
        elif start_stop == "stop":
            self.rect = size
 
#init pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Cloak and Dagger')
used_die_shader = pygame.Surface((130,130))  # the size of your rect
used_die_shader.set_alpha(120)                # alpha level
used_die_shader.fill((0,0,0))           # this fills the entire surface
#image loading
dice_image_a1 = pygame.image.load('Dice_images.py\dice_1.png')
dice_image_a2 = pygame.image.load('Dice_images.py\dice_2.png')
dice_image_a3 = pygame.image.load('Dice_images.py\dice_3.png')
dice_image_a4 = pygame.image.load('Dice_images.py\dice_4.png')
dice_image_a5 = pygame.image.load('Dice_images.py\dice_5.png')
dice_image_a6 = pygame.image.load('Dice_images.py\dice_6.png')
dice_image_shroud = pygame.image.load('Dice_images.py\dice_shroud.png').convert_alpha()
#self explanatory. it is used for alpha values for a fade in effect only.
def dbl_self(num_self):
    num_self == num_self
    return num_self
#button opacity handling, since I wrote my own buttons. Inside of pygame..ugh.
def fade_in_button(temp_button,opacity):
    surface = screen.convert_alpha()
    surface.fill([0,0,0,0])
    temp_button.draw(surface)
    surface.set_alpha(opacity)
    screen.blit(surface, (0,0))
#rough way of fading an objects opacity
def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)        
    target.blit(temp, location)
    return 0
#text entry for players name. maybe for i.p. look up in the future
def text():
    name_entry = Button("white",(TEXT_ENTRY_BOX),"enter your name","black",("unispacebold",20))
    user_text = ''
    running = True
    shade_fill = pygame.Surface((800,500), pygame.SRCALPHA)   # per-pixel alpha
    shade_fill.fill((0,0,0,1))
    fade_in = 20
    while running:
        clock.tick(30)
        dbl_self(fade_in)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not name_entry.isOver(pos):
                    user_text = "enter your name"
                    return user_text

            if event.type == pygame.KEYDOWN:
                    # Check for backspace
                if event.key == pygame.K_BACKSPACE:
        
                        # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
        
                    # Unicode standard is used for string
                    # formation
                elif event.key == pygame.K_RETURN:
                    if user_text == '':
                        user_text = "enter your name"
                    shade_fill.fill((66,15,15,28))
                    play_button = Button(DARK_YELLOW,BUTTON_1, "Play")
                    engage_button = Button(DARK_YELLOW,BUTTON_2, "Engage")
                    name_entry = Button("white",(TEXT_ENTRY_BOX),user_text,"grey",("unispacebold",20))
                    start_time = time.time()
                    seconds = .25
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()

                        current_time = time.time()
                        elapsed_time = current_time - start_time
                        screen.blit(shade_fill,(0,0))
                        name_entry.draw(screen)

                        blit_alpha(shade_fill,dice_image_a1,(10,25),fade_in)
                        blit_alpha(shade_fill,dice_image_a2,(140,25),fade_in)
                        blit_alpha(shade_fill,dice_image_a3,(270,25),fade_in)
                        blit_alpha(shade_fill,dice_image_a4,(400,25),fade_in)
                        blit_alpha(shade_fill,dice_image_a5,(530,25),fade_in)
                        blit_alpha(shade_fill,dice_image_a6,(660,25),fade_in)
                        fade_in_button(engage_button,fade_in)
                        fade_in_button(play_button,fade_in)
                        pygame.display.flip()
                    

                        if elapsed_time > seconds:
                            return user_text
    
                else:
                    if event.unicode.isalpha():
                        user_text += event.unicode


        name_entry.text = user_text
        screen.blit(shade_fill,(0,0))
        name_entry.draw(screen)
        pygame.display.flip()

      
    # set width of textfield so that text cannot get
    # outside of user's text input
   # input_rect.w = max(100, text_surface.get_width()+10)
#this handles the local player scoring only
def evaluate(d1,d2):
    global MY_NAME,OPPONENT_NAME,PLAYER_CLASS
    if PLAYER_CLASS == "Dagger":
        if d1 == 1:
            print("as dagger d1=1 no score")
            return 0
        elif d1 == 6:
            if d2 == 1:
                print("as dagger d1=6,d2=1 no score")
                return 0
                
            elif d2 == 6:
                print("as dagger d2=6 no score")
                return 0
            else:
                print("as dagger d1=6, d2!=1 or 6 score")
                return 1
        else:
            if d1>=d2:
                if d2 != 1:
                    print("as dagger d1>d2, score")
                    return 1
                else:
                    print("as dagger d1>d2,d1=1 no score")
                    return 0
            else:
                print("as dagger d1<d2, no score")
                return 0
        
    elif PLAYER_CLASS == "Cloak":
        if d1 == 1:
            if d2 == 6:
                print("as cloak d1=1,d2=6 score")
                return 1
            else:
                print("as cloak d1=1,no score")
                return 0
        elif d1 == 6:
            if d2 == 6:
                print("as cloak d1=6,d2=6 no score")
                return 0
            else:
                print("as cloak d1=6,d2!=6 score")
                return 1
        else:
            if d1<=d2:
                print("as cloak d1<=d2,no score")
                return 0
            else:
                print("as cloak d1>d2, score")
                return 1
#only used in solo play after practice() is called  
def computer_scoring(d1,d2):
    global MY_NAME,OPPONENT_NAME,PLAYER_CLASS
    if PLAYER_CLASS == "Cloak":
        if d2== 1:
            return 0
        elif d1 == 1:
            return 0
        elif d1 == 6:
            if d2 == 1:
                return 0
            elif d2 == 6:
                return 0
            else:
                return 1
        else:
            if d1>=d2:
                return 1
            else:
                return 0
        
    elif PLAYER_CLASS == "Dagger":
        if d1 == 1:
            if d2 == 6:
                return 1
            else:
                return 0
        elif d1 == 6:
            if d2 == 6:
                return 0
            else:
                return 1
        else:
            if d1<=d2:
                return 0
            else:
                return 1
#mostly rewritten as evaluate and coumputer_scoring, left it in for debugging
def die_reader(selected_die,opponents_selected_die):
    #  die_cup = [dice_image_a1, dice_image_a2,dice_image_a3,dice_image_a4, dice_image_a5,dice_image_a6]
    #  for names in die_cup:
    #      if names == selected_die:
    print (f"{selected_die}")
    print (f"{opponents_selected_die}")
#this initiates the opponents name as "Computer", and inits the game for solo play
def practice():
    global OPPONENT_NAME
    OPPONENT_NAME = "Computer" 
    play()
#rolls the computers dice upon being called from practice()
def opponent_dice_roll():
    die_cup = [dice_image_a1, dice_image_a2,dice_image_a3,dice_image_a4, dice_image_a5,dice_image_a6]
    d1 = random.randint(1,6) 
    rolled_die1 = die_cup[d1-1]
    d2 = random.randint(1,6)
    rolled_die2 = die_cup[d2-1]
    d3 = random.randint(1,6)
    rolled_die3 = die_cup[d3-1]
    d4 = random.randint(1,6)
    rolled_die4 = die_cup[d4-1]
    d5 = random.randint(1,6)
    rolled_die5 = die_cup[d5-1]
    d6 = random.randint(1,6)
    rolled_die6 = die_cup[d6-1]
    return (d1,d2,d3,d4,d5,d6,rolled_die1,rolled_die2,rolled_die3,rolled_die4,rolled_die5,rolled_die6)
#game loop
def play():
    global PLAYER_CLASS
    if PLAYER_CLASS == "Cloak":
        PLAYER_CLASS = "Dagger"
    elif PLAYER_CLASS == "Dagger":
        PLAYER_CLASS = "Cloak"
    score = 0
    opponent_score = 0
    menu_button = Button(DARK_YELLOW,BUTTON_3, "Menu")
    player_name = Button(BLACK,NAME_DISPLAY,MY_NAME,DARK_YELLOW,("unispacebold",20))
    player_score_display = Button(BLACK,(240,450,250,40),('Score:'+str(score)),DARK_YELLOW,("unispacebold",20))
    player_Class_display = Button(BLACK,(240,360,510,80),("You are the "+PLAYER_CLASS),DARK_YELLOW,("unispacebold",40))
    player_2_score_display = Button(BLACK,(240,145,250,40),('Score:'+str(opponent_score)),DARK_YELLOW,("unispacebold",20))
    player_2 = Button(BLACK,OPPONENT_NAME_DISPLAY,OPPONENT_NAME,DARK_YELLOW,("unispacebold",20))
    die1_blit_coordinates = (10,220)
    die2_blit_coordinates = (140, 220)
    die3_blit_coordinates = (270,220)
    die4_blit_coordinates = (400,220)
    die5_blit_coordinates = (530,220)
    die6_blit_coordinates = (660,220)

 #opponents dice handling
    player_2_die1 = dice_image_shroud
    player_2_die2 = dice_image_shroud
    player_2_die3 = dice_image_shroud
    player_2_die4 = dice_image_shroud
    player_2_die5 = dice_image_shroud
    player_2_die6 = dice_image_shroud
    player_2_die_coordinates = ((10,10),(140,10),(270,10),(400,10),(530,10),(660,10))
    player_2_die_locations = random.sample(player_2_die_coordinates,6)
    player_2_die1_placement = player_2_die_locations[0]
    player_2_die2_placement = player_2_die_locations[1]
    player_2_die3_placement = player_2_die_locations[2]
    player_2_die4_placement = player_2_die_locations[3]
    player_2_die5_placement = player_2_die_locations[4]
    player_2_die6_placement = player_2_die_locations[5]  
    opponents_dice_and_images_roll = opponent_dice_roll()
    opponents_dice = opponents_dice_and_images_roll[:6]
    opponents_dice_images = opponents_dice_and_images_roll[6:12]

 #players dice handling
    die1_used = False
    die2_used = False
    die3_used = False
    die4_used = False
    die5_used = False
    die6_used = False
    die_cup = [dice_image_a1, dice_image_a2,dice_image_a3,dice_image_a4, dice_image_a5,dice_image_a6]
    d1 = random.randint(1,6) 
    rolled_die1 = die_cup[d1-1]
    adjusted_rolled_die1 = rolled_die1
    d2 = random.randint(1,6)
    rolled_die2 = die_cup[d2-1]
    adjusted_rolled_die2 = rolled_die2
    d3 = random.randint(1,6)
    rolled_die3 = die_cup[d3-1]
    adjusted_rolled_die3 = rolled_die3
    d4 = random.randint(1,6)
    rolled_die4 = die_cup[d4-1]
    adjusted_rolled_die4 = rolled_die4
    d5 = random.randint(1,6)
    rolled_die5 = die_cup[d5-1]
    adjusted_rolled_die5 = rolled_die5
    d6 = random.randint(1,6)
    rolled_die6 = die_cup[d6-1]
    adjusted_rolled_die6 = rolled_die6

    die1_x = range(10,140)
    die2_x = range(141, 270)
    die3_x = range(271, 400)
    die4_x = range(401,530)
    die5_x = range(531,660)
    die6_x = range(661,790)
    die_y = range(220,350)
    die1_location = list(product(die1_x, die_y))
    die2_location = list(product(die2_x, die_y))
    die3_location = list(product(die3_x, die_y))
    die4_location = list(product(die4_x, die_y))
    die5_location = list(product(die5_x, die_y))
    die6_location = list(product(die6_x, die_y))
    running = True
    while running:
        clock.tick(60)
 #input
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEMOTION:
                if menu_button.isOver(pos):
                    menu_button.color = LIGHT_YELLOW
                    menu_button.animate(BUTTON_3,"start")
                else:
                    menu_button.color = DARK_YELLOW
                    menu_button.animate(BUTTON_3,"stop")
 
            #dice animations
            if event.type == pygame.MOUSEMOTION:
                if player_name.isOver(pos):
                    player_name.text_color = LIGHT_YELLOW
                else:
                    player_name.text_color = DARK_YELLOW

                if player_2.isOver(pos):
                    player_2.text_color = LIGHT_YELLOW
                else:
                    player_2.text_color = DARK_YELLOW

                if pos in die1_location:
                    if die1_used ==False:
                        adjusted_rolled_die1 = pygame.transform.scale(rolled_die1, (125, 125))
                else:
                    adjusted_rolled_die1 = rolled_die1

                if pos in die2_location:
                    if die2_used ==False:
                        adjusted_rolled_die2 = pygame.transform.scale(rolled_die2, (125, 125))
                else:
                    adjusted_rolled_die2 = rolled_die2
  
                if pos in die3_location:
                    if die3_used ==False:
                        adjusted_rolled_die3 = pygame.transform.scale(rolled_die3, (125, 125))
                else:
                    adjusted_rolled_die3 = rolled_die3            
 
                if pos in die4_location:
                    if die4_used ==False:
                        adjusted_rolled_die4 = pygame.transform.scale(rolled_die4, (125, 125))
                else:
                    adjusted_rolled_die4 = rolled_die4

                if pos in die5_location:
                    if die5_used ==False:
                        adjusted_rolled_die5 = pygame.transform.scale(rolled_die5, (125, 125))
                else:
                    adjusted_rolled_die5 = rolled_die5

                if pos in die6_location:
                    if die6_used ==False:
                        adjusted_rolled_die6 = pygame.transform.scale(rolled_die6, (125, 125))
                else:
                    adjusted_rolled_die6 = rolled_die6

            #die selection
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pos in die1_location:
                    if die1_used == False:
                        if OPPONENT_NAME != '':
                           # die_reader(d1,opponents_dice[0])
                            player_2_die1 = opponents_dice_images[0]
                            player_2_die1_placement = player_2_die_locations[0]
                            score +=(evaluate(d1,opponents_dice[0]))
                            if OPPONENT_NAME == "Computer":
                                opponent_score += computer_scoring(opponents_dice[0],d1)
                        if OPPONENT_NAME != '':
                            die1_used = True
                if pos in die2_location:
                    if die2_used == False:
                        if OPPONENT_NAME != '':
                           # die_reader(d2,opponents_dice[1])
                            player_2_die2 = opponents_dice_images[1]
                            player_2_die2_placement = player_2_die_locations[1]
                            score +=(evaluate(d2,opponents_dice[1]))
                            if OPPONENT_NAME == "Computer":
                                opponent_score += computer_scoring(opponents_dice[1],d2)

                        if OPPONENT_NAME != '':
                            die2_used = True
                if pos in die3_location:
                    if die3_used == False:
                        if OPPONENT_NAME != '':
                           # die_reader(d3,opponents_dice[2])
                            player_2_die3 = opponents_dice_images[2]
                            player_2_die3_placement = player_2_die_locations[2]
                            score +=(evaluate(d3,opponents_dice[2]))
                            if OPPONENT_NAME == "Computer":
                                opponent_score += computer_scoring(opponents_dice[2],d3)

                        if OPPONENT_NAME != '':
                            die3_used = True
                if pos in die4_location:
                    if die4_used == False:
                        if OPPONENT_NAME != '':
                            #die_reader(d4,opponents_dice[3])
                            player_2_die4 = opponents_dice_images[3]
                            player_2_die4_placement = player_2_die_locations[3]
                            score +=(evaluate(d4,opponents_dice[3]))
                            if OPPONENT_NAME == "Computer":
                                opponent_score += computer_scoring(opponents_dice[3],d4)

                        if OPPONENT_NAME != '':
                            die4_used = True
                if pos in die5_location:
                    if die5_used == False:
                        if OPPONENT_NAME != '':
                           # die_reader(d5,opponents_dice[4])
                            player_2_die5 = opponents_dice_images[4]
                            player_2_die5_placement = player_2_die_locations[4]
                            score +=(evaluate(d5,opponents_dice[4]))
                            if OPPONENT_NAME == "Computer":
                                opponent_score += computer_scoring(opponents_dice[4],d5)

                        if OPPONENT_NAME != '':
                            die5_used = True
                if pos in die6_location: 
                    if die6_used == False:
                        if OPPONENT_NAME != '':
                           # die_reader(d6,opponents_dice[5])
                            player_2_die6 = opponents_dice_images[5]
                            player_2_die6_placement = player_2_die_locations[5]
                            score +=(evaluate(d6,opponents_dice[5]))
                            if OPPONENT_NAME == "Computer":
                                opponent_score += computer_scoring(opponents_dice[5],d6)

                        if OPPONENT_NAME != '':
                            die6_used = True
                if menu_button.isOver(pos):
                    player_menu()

        player_score_display.text = ('Score:'+str(score))
        player_2_score_display.text = ('Score:'+str(opponent_score))
 #screen draw
        screen.fill(DEEP_RED)
        menu_button.draw(screen)
        if MY_NAME != "enter your name":
            player_name.draw(screen)
        if OPPONENT_NAME != '':
            player_2.text = OPPONENT_NAME
            player_2.draw(screen)
            player_score_display.draw(screen)
            player_2_score_display.draw(screen)
            player_Class_display.draw(screen)
        if False not in {die1_used,die2_used,die3_used,die4_used,die5_used,die6_used}:
            player_Class_display.text_color = RED
            if score>opponent_score:
                player_Class_display.text = "YOU WIN!"
            elif opponent_score>score:
                player_Class_display.text = "YOU LOSE!"
            else:
                player_Class_display.text = "DRAAAAAAAAAAAW!"
            player_Class_display.draw(screen)

    #players dice
        screen.blit(adjusted_rolled_die1, (die1_blit_coordinates))
        screen.blit(adjusted_rolled_die2, (die2_blit_coordinates))
        screen.blit(adjusted_rolled_die3, (die3_blit_coordinates))
        screen.blit(adjusted_rolled_die4, (die4_blit_coordinates))
        screen.blit(adjusted_rolled_die5, (die5_blit_coordinates))
        screen.blit(adjusted_rolled_die6, (die6_blit_coordinates))
    #shading on used dice

        if die1_used == True:
            screen.blit(used_die_shader,die1_blit_coordinates)          
        if die2_used == True:
            screen.blit(used_die_shader,die2_blit_coordinates)
        if die3_used == True:
            screen.blit(used_die_shader,die3_blit_coordinates)
        if die4_used == True:
            screen.blit(used_die_shader,die4_blit_coordinates)
        if die5_used == True:
            screen.blit(used_die_shader,die5_blit_coordinates)
        if die6_used == True:
            screen.blit(used_die_shader,die6_blit_coordinates)
    #opponents dice
        screen.blit(player_2_die1,player_2_die1_placement)
        screen.blit(player_2_die2,player_2_die2_placement)
        screen.blit(player_2_die3,player_2_die3_placement)
        screen.blit(player_2_die4,player_2_die4_placement)
        screen.blit(player_2_die5,player_2_die5_placement)
        screen.blit(player_2_die6,player_2_die6_placement)
        pygame.display.flip()
#the menu avaiable to players in a game       
def player_menu():
    global OPPONENT_NAME
 #setting up buttons
    TLB = (15,10,250,150)
    TMB =(275,10,250,150)
    TRB = (535,10,250,150)
    BLB = (15,180,250,150)
    BMB = (275,180,250,150)
    BRB = (535,180,250,150)
    RRB = (15,340,770,120)
    top_left_button = Button(DEEP_RED,(TLB),"Resume",LIGHT_YELLOW)
    top_midd_button = Button(DEEP_RED,(TMB),"Options", LIGHT_YELLOW)
    top_right_button = Button(DEEP_RED,(TRB), "Quit",LIGHT_YELLOW)
    bottom_left_button = Button(DEEP_RED,(BLB),"Rules",LIGHT_YELLOW)
    bottom_midd_button = Button(DEEP_RED,(BMB),"Credits",LIGHT_YELLOW)
    bottom_right_button = Button(DEEP_RED,(BRB),"Engage",LIGHT_YELLOW)
    reroll_button = Button(DARK_BLUE,(RRB), "Reroll Your Dice",LIGHT_YELLOW)


    running = True
    while running:
        clock.tick(60)
        if MY_NAME == "enter your name":
            bottom_right_button.color = GRAY_YELLOW
            bottom_right_button.text_color = DARK_GRAY
        else:
            if bottom_right_button. color != RED:
                bottom_right_button.color = DEEP_RED
                bottom_right_button.text_color = LIGHT_YELLOW

 #input
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
 #button animations
            if event.type == pygame.MOUSEMOTION:
                if top_left_button.isOver(pos):
                    top_left_button.color = RED
                    top_left_button.animate(TLB,"start")
                else:
                    top_left_button.color = DEEP_RED
                    top_left_button.animate(TLB,"stop")

            if event.type == pygame.MOUSEMOTION:
                if top_midd_button.isOver(pos):
                    top_midd_button.color = RED
                    top_midd_button.animate(TMB,"start")
                else:
                    top_midd_button.color = DEEP_RED
                    top_midd_button.animate(TMB,"stop")

            if event.type == pygame.MOUSEMOTION:
                if top_right_button.isOver(pos):
                    top_right_button.color = RED
                    top_right_button.animate(TRB,"start")
                else:
                    top_right_button.color = DEEP_RED
                    top_right_button.animate(TRB,"stop")

            if event.type == pygame.MOUSEMOTION:
                if bottom_left_button.isOver(pos):
                    bottom_left_button.color = RED
                    bottom_left_button.animate(BLB,"start")
                else:
                    bottom_left_button.color = DEEP_RED
                    bottom_left_button.animate(BLB,"stop")

            if event.type == pygame.MOUSEMOTION:
                if bottom_midd_button.isOver(pos):
                    bottom_midd_button.color = RED
                    bottom_midd_button.animate(BMB,"start")
                else:
                    bottom_midd_button.color = DEEP_RED
                    bottom_midd_button.animate(BMB,"stop")

            if event.type == pygame.MOUSEMOTION:
                if MY_NAME != "enter your name":
                    if bottom_right_button.isOver(pos):
                        bottom_right_button.color = RED
                        bottom_right_button.animate(BRB,"start")
                    else:
                        bottom_right_button.color = DEEP_RED
                        bottom_right_button.animate(BRB,"stop")

            if event.type == pygame.MOUSEMOTION:
                if reroll_button.isOver(pos):
                    reroll_button.color = LIGHT_BLUE
                    reroll_button.animate(RRB,"start")                    
                else:
                    reroll_button.color = DARK_BLUE
                    reroll_button.animate(RRB,"stop")

 #button functionality
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if top_left_button.isOver(pos):
                    return

                if top_midd_button.isOver(pos):
                    options()

                if top_right_button.isOver(pos):
                    if OPPONENT_NAME == "Computer":
                        OPPONENT_NAME = ''
                    main_menu()

                if bottom_left_button.isOver(pos):
                    rules()

                if bottom_midd_button.isOver(pos):
                    credits()

                if MY_NAME != "enter your name":
                    if bottom_right_button.isOver(pos):
                        engage_menu()

                if reroll_button.isOver(pos):
                    play()



 #screen draw
        screen.fill(DARK_YELLOW)
        top_left_button.draw(screen)
        top_midd_button.draw(screen)
        top_right_button.draw(screen)
        bottom_left_button.draw(screen)
        bottom_midd_button.draw(screen)
        bottom_right_button.draw(screen)
        reroll_button.draw(screen)
        pygame.display.flip()
#main menu / start screen
def main_menu():
    global MY_NAME
    running = True
    #main menu buttons
    play_button = Button(DARK_YELLOW,BUTTON_1, "Play")
    engage_button = Button(DARK_YELLOW,BUTTON_2, "Engage")
    player_name = Button(BLACK,NAME_DISPLAY,MY_NAME,DARK_YELLOW,("unispacebold",20))
    name_entry = Button("white",(TEXT_ENTRY_BOX),"enter your name","grey",("unispacebold",20))

    while running:
        clock.tick(60)
        if MY_NAME == "enter your name":
            engage_button.color = GRAY_YELLOW
            engage_button.text_color = DARK_GRAY
        elif engage_button.color != LIGHT_YELLOW:
            engage_button.color = DARK_YELLOW
            engage_button.text_color = "black"

    #input
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEMOTION:
                if player_name.isOver(pos):
                    player_name.text_color = LIGHT_YELLOW
                # player_name.animate(NAME_DISPLAY,"start")
                else:
                    player_name.text_color = DARK_YELLOW
                #  player_name.animate(NAME_DISPLAY,"stop")

                if play_button.isOver(pos):
                    play_button.color = LIGHT_YELLOW
                    play_button.animate(BUTTON_1,"start")
                else:
                    play_button.color = DARK_YELLOW
                    play_button.animate(BUTTON_1,"stop")
            
                if MY_NAME != "enter your name":
                    if engage_button.isOver(pos):
                        engage_button.color = LIGHT_YELLOW
                        engage_button.animate(BUTTON_2,"start")
                    else:
                        engage_button.color = DARK_YELLOW
                        engage_button.animate(BUTTON_2,"stop")

                if name_entry.isOver(pos):
                    name_entry.color = (230, 230, 230)
                    name_entry.text_font = ("unispacebold",19)
                else:
                    name_entry.color = "white"
                    name_entry.text_font = ("unispacebold",20)
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button.isOver(pos):
                    play()
                if MY_NAME != 'enter your name':
                    if engage_button.isOver(pos):
                        engage_menu()
                if name_entry.text == 'enter your name':
                    if name_entry.isOver(pos):
                        name_entry.text=text()
                        player_name.text = name_entry.text
                        MY_NAME = name_entry.text
                    


               
    #screen draw
        
        screen.fill(DEEP_RED)
        play_button.draw(screen)
        engage_button.draw(screen)

        #players name capture switch
        if MY_NAME == 'enter your name':
            name_entry.draw(screen)
        else:
            player_name.draw(screen)

        
        screen.blit(dice_image_a1, (10,25))
        screen.blit(dice_image_a2, (140,25))
        screen.blit(dice_image_a3, (270,25))
        screen.blit(dice_image_a4, (400,25))
        screen.blit(dice_image_a5, (530,25))
        screen.blit(dice_image_a6, (660,25))
        pygame.display.flip()
#engage menu, for connecting to another player online
def engage_menu():
    global STATUS
    start_client = threading.Thread(target= client.join_as_client, args=(ip_address,))
    start_server = threading.Thread(target= server.setup_server, args=(ip_address,))
    die_cup = [dice_image_a1, dice_image_a2,dice_image_a3,dice_image_a4, dice_image_a5,dice_image_a6]
    rolled_die1 = random.choice(die_cup)
    rolled_die2 = random.choice(die_cup)
    rolled_die3 = random.choice(die_cup)
    rolled_die4 = random.choice(die_cup)
    rolled_die5 = random.choice(die_cup)
    rolled_die6 = random.choice(die_cup)
    running = True
 #server/client menu buttons
    server_button = Button(DARK_YELLOW,BUTTON_1, "Server")
    client_button = Button(DARK_YELLOW,BUTTON_2, "Client")
    back_button = Button(DARK_BLUE,BACK_BUTTON,"Back")
    player_name = Button(BLACK,NAME_DISPLAY,MY_NAME,DARK_YELLOW,("unispacebold",20))

    while running:
        clock.tick(60)
        if STATUS == "server":
            server_button.color = RED
            server_button.text_color = LIGHT_YELLOW
            client_button.color = GRAY_YELLOW
            client_button.text_color = DARK_GRAY
        if STATUS == "client":
            client_button.color = RED
            client_button.text_color = LIGHT_YELLOW
            server_button.color = GRAY_YELLOW
            server_button.text_color = DARK_GRAY
    #input
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()    
            if event.type == pygame.MOUSEMOTION:
                if player_name.isOver(pos):
                    player_name.text_color = LIGHT_YELLOW
                else:
                    player_name.text_color = DARK_YELLOW
                if STATUS=='':
                    if server_button.isOver(pos):
                        server_button.color = LIGHT_YELLOW
                        server_button.animate(BUTTON_1,"start")
                    else:
                        server_button.color = DARK_YELLOW
                        server_button.animate(BUTTON_1,"stop")
                if STATUS =='':
                    if client_button.isOver(pos):
                        client_button.color = LIGHT_YELLOW
                        client_button.animate(BUTTON_2,"start")
                    else:
                        client_button.color = DARK_YELLOW
                        client_button.animate(BUTTON_2,"stop")
 #button functionality           
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if server_button.isOver(pos):
                    if STATUS!="client":
                        if STATUS !="server":
                            STATUS = "server"
                            start_server.start()#server start up
                if client_button.isOver(pos):
                    if STATUS!="server":
                        if STATUS!="client":
                            STATUS = "client"
                            start_client.start()#client calls server
                if back_button.isOver(pos):
                    return
            if event.type == pygame.MOUSEMOTION:
                if back_button.isOver(pos):
                    back_button.color = LIGHT_BLUE
                    back_button.animate(BACK_BUTTON,"start")
                else:
                    back_button.color = DARK_BLUE
                    back_button.animate(BACK_BUTTON,"stop")
            
        
        
    #screen draw
        screen.fill(DEEP_RED)
        if player_name.text != "enter your name":
            player_name.draw(screen)
        
        server_button.draw(screen)
        client_button.draw(screen)
        back_button.draw(screen)
        screen.blit(rolled_die1, (10,25))
        screen.blit(rolled_die2, (140,25))
        screen.blit(rolled_die3, (270,25))
        screen.blit(rolled_die4, (400,25))
        screen.blit(rolled_die5, (530,25))
        screen.blit(rolled_die6, (660,25))
        pygame.display.flip()
#rules and credits use the same format
def credits():
    back_button = Button(DARK_BLUE,BACK_BUTTON,"Back")
    title = pygame.font.SysFont('unispacebold', 60)
    title.set_underline(1)
    header = pygame.font.SysFont('unispacebold', 30)
    font = pygame.font.SysFont('unispacebold', 15)
    font_sig = pygame.font.SysFont('unispacebold', 25)
    font_sig.set_italic(1)
    font_sig.set_underline(1)

    #all text rendered into images
    credits_title = title.render("     Credits     ",1,BLACK)
    text1 = font.render("pygame 2.0.0 (SDL 2.0.12, python 3.9.2) : 2021",1,BLACK)
    text2 = font.render("Hello from the pygame community. https://www.pygame.org/contribute.html",1,BLACK)
    text3 = font.render("The dice images used were in the public domain, I can not find the original",1,BLACK)
    text4 = font.render("source however. Email me at calebstock91@gmail.com if you have the correct",1,BLACK)
    text5 = font.render("source and I will add full credit here. And ofcourse a special thanks to my",1,BLACK)
    text6 = font.render("wife for putting up with me and letting me play. THANK YOU,",1,BLACK) 
    text7 = font_sig.render("Caleb S.",1,BLACK) 
    #input (for the back button)
    running=True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.isOver(pos):
                        return
            if event.type == pygame.MOUSEMOTION:
                    if back_button.isOver(pos):
                        back_button.color = LIGHT_BLUE
                        back_button.animate(BACK_BUTTON,"start")
                    else:
                        back_button.color = DARK_BLUE
                        back_button.animate(BACK_BUTTON,"stop")
        #screen draw
        screen.fill(DARK_YELLOW)
        back_button.draw(screen)
        screen.blit(credits_title,(85,10))
        screen.blit(text1,(70,115))
        screen.blit(text2,(70,160))
        screen.blit(text3,(70,205))
        screen.blit(text4,(70,250))
        screen.blit(text5,(70,295))
        screen.blit(text6,(70,340))
        screen.blit(text7,(610,330))
        pygame.display.flip()
#pygame needs a better text entry mode.
def rules():
    back_button = Button(DARK_BLUE,BACK_BUTTON,"Back")
    title = pygame.font.SysFont('unispacebold', 60)
    title.set_underline(1)
    header = pygame.font.SysFont('unispacebold', 30)
    font = pygame.font.SysFont('unispacebold', 15)

    #all text rendered into images
    rules_title = title.render("     RULES     ",1,BLACK)
    one = header.render("1-",1,BLACK)
    text1 = font.render("Players take turns being Cloak and being Dagger.",1,BLACK)
    two = header.render("2-",1,BLACK)
    text2 = font.render("Both players roll 6 dice and keep them concealed from eachother.",1,BLACK)
    three = header.render("3-",1,BLACK)
    text3 = font.render("You each select one die at a time and reveal it, the higher die scores a point.",1,BLACK)
    four = header.render("4-",1,BLACK)
    text4 = font.render("Dagger wins if the dice are the same! (except on sixes).",1,BLACK)
    five = header.render("5-",1,BLACK)
    text5 = font.render("If Cloak reveals a one he doesn't allow Dagger to score,",1,BLACK)
    text6 = font.render("and if Dagger revealed a six against Cloaks one, then Cloak scores!",1,BLACK)   
    #input (for the back button)
    running=True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.isOver(pos):
                        return
            if event.type == pygame.MOUSEMOTION:
                    if back_button.isOver(pos):
                        back_button.color = LIGHT_BLUE
                        back_button.animate(BACK_BUTTON,"start")
                    else:
                        back_button.color = DARK_BLUE
                        back_button.animate(BACK_BUTTON,"stop")
        #screen draw
        screen.fill(DARK_YELLOW)
        back_button.draw(screen)
        screen.blit(rules_title,(122,10))
        screen.blit(one,(20,105))
        screen.blit(text1,(70,115))
        screen.blit(two,(20,150))
        screen.blit(text2,(70,160))
        screen.blit(three,(20,195))
        screen.blit(text3,(70,205))
        screen.blit(four,(20,240))
        screen.blit(text4,(70,250))
        screen.blit(five,(20,285))
        screen.blit(text5,(70,295))
        screen.blit(text6,(70,320))
        pygame.display.flip()
#this is one of those things that makes the game feel really good to me.slots left open for later ideas.
def options():
    back_button = Button(DARK_BLUE,BACK_BUTTON,"Back")
    global MY_NAME,OPPONENT_NAME,STATUS
    #setting up buttons
    TLB = (15,10,250,150)
    TMB =(275,10,250,150)
    TRB = (535,10,250,150)
    BLB = (15,180,250,150)
    BMB = (275,180,250,150)
    BRB = (535,180,250,150)
    top_left_button = Button(DEEP_RED,(TLB),"Practice",LIGHT_YELLOW)
    top_midd_button = Button(DEEP_RED,(TMB),"test", LIGHT_YELLOW)
    top_right_button = Button(DEEP_RED,(TRB), "Reset Name",LIGHT_YELLOW)
    bottom_left_button = Button(DEEP_RED,(BLB),"test",LIGHT_YELLOW)
    bottom_midd_button = Button(DEEP_RED,(BMB),"test",LIGHT_YELLOW)
    bottom_right_button = Button(DEEP_RED,BRB,"Disconnect",LIGHT_YELLOW)
    #input
    running=True
    while running:       
        clock.tick(60)
        if STATUS=='':
            bottom_right_button.color = GRAY_YELLOW
            bottom_right_button.text_color = DARK_GRAY
        elif bottom_right_button.color != RED:
            bottom_right_button.color = DEEP_RED
            bottom_right_button.text_color = LIGHT_YELLOW
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #button functionality
                if top_left_button.isOver(pos):
                    practice()
                if top_midd_button.isOver(pos):
                    pass
                if top_right_button.isOver(pos):
                    MY_NAME = "enter your name"
                    if OPPONENT_NAME == "Computer":
                        OPPONENT_NAME = ''
                    main_menu()
                if bottom_left_button.isOver(pos):
                    pass
                if bottom_midd_button.isOver(pos):
                    pass
                if bottom_right_button.isOver(pos):
                    if STATUS!='':
                        STATUS = ''
                        engage_menu()               
                if back_button.isOver(pos):
                    return

            if event.type == pygame.MOUSEMOTION:
                if back_button.isOver(pos):
                    back_button.color = LIGHT_BLUE
                    back_button.animate(BACK_BUTTON,"start")
                else:
                    back_button.color = DARK_BLUE
                    back_button.animate(BACK_BUTTON,"stop")
                    #button animations

                if top_left_button.isOver(pos):
                    top_left_button.color = RED
                    top_left_button.animate(TLB,"start")
                else:
                    top_left_button.color = DEEP_RED
                    top_left_button.animate(TLB,"stop")
                if top_midd_button.isOver(pos):
                    top_midd_button.color = RED
                    top_midd_button.animate(TMB,"start")
                else:
                    top_midd_button.color = DEEP_RED
                    top_midd_button.animate(TMB,"stop")
                if top_right_button.isOver(pos):
                    top_right_button.color = RED
                    top_right_button.animate(TRB,"start")
                else:
                    top_right_button.color = DEEP_RED
                    top_right_button.animate(TRB,"stop")
                if bottom_left_button.isOver(pos):
                    bottom_left_button.color = RED
                    bottom_left_button.animate(BLB,"start")
                else:
                    bottom_left_button.color = DEEP_RED
                    bottom_left_button.animate(BLB,"stop")
                if bottom_midd_button.isOver(pos):
                    bottom_midd_button.color = RED
                    bottom_midd_button.animate(BMB,"start")
                else:
                    bottom_midd_button.color = DEEP_RED
                    bottom_midd_button.animate(BMB,"stop")
                if STATUS !='':
                    if bottom_right_button.isOver(pos):
                        bottom_right_button.color = RED
                        bottom_right_button.animate(BRB,"start")
                    else:
                        bottom_right_button.color = DEEP_RED
                        bottom_right_button.animate(BRB,"stop")
        #screen draw
        screen.fill(DARK_YELLOW)
        top_left_button.draw(screen)
        top_midd_button.draw(screen)
        top_right_button.draw(screen)
        bottom_left_button.draw(screen)
        bottom_midd_button.draw(screen)
        bottom_right_button.draw(screen)
        back_button.draw(screen)
        pygame.display.flip()
#simply inits the game at the base menu. this specific line of code will only be ran once per session.
main_menu()