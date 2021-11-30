import pygame
import time
import random
from tkinter import *
import sqlite3
import os
import hashlib


#Initialising pygame
pygame.init()
win = pygame.display.set_mode((800,600))

#Setting the colours
blue = (0,150,255)
Bright_blue = (0,255,255)
black = (0,0,0)
Purple=(96,96,200)
red = (200,0,0)
bright_red =(255,0,0)
wall_colour_1 = (0,190,0)
wall_colour_2 = (200,80,0)
wall_colour_3 = (0,150,255)
wall_colour_4 = (100,0,0)
#Lists of sprites
Stand_1 = pygame.image.load("Hat_man1.png").convert_alpha()
walkRight_1 = [pygame.image.load("Hat_man1.png").convert_alpha(),pygame.image.load("Hat_man2.png").convert_alpha(),
               pygame.image.load("Hat_man3.png").convert_alpha(),pygame.image.load("Hat_man4.png").convert_alpha()]
walkLeft_1 = [pygame.image.load("Hat_man5.png").convert_alpha(),pygame.image.load("Hat_man6.png").convert_alpha(),
              pygame.image.load("Hat_man7.png").convert_alpha(),pygame.image.load("Hat_man8.png").convert_alpha()]

Stand_2 = pygame.image.load("Hat_man1-2.png").convert_alpha()
walkRight_2 = [pygame.image.load("Hat_man1-2.png").convert_alpha(),pygame.image.load("Hat_man2-2.png").convert_alpha(),
               pygame.image.load("Hat_man3-2.png").convert_alpha(),pygame.image.load("Hat_man4-2.png").convert_alpha()]
walkLeft_2 = [pygame.image.load("Hat_man5-2.png").convert_alpha(),pygame.image.load("Hat_man6-2.png").convert_alpha(),
              pygame.image.load("Hat_man7-2.png").convert_alpha(),pygame.image.load("Hat_man8-2.png").convert_alpha()]

#For backgorunds and windows that are not in the main menu

bg1 = pygame.image.load("high_mountain_nature_game_background_dribbble.png")
bg2 = pygame.image.load("Dessertland_background.jpg")
bg3 = pygame.image.load("Snow_background.png")
bg4 = pygame.image.load("Game over.jpg")
bg5 = pygame.image.load("volcano.jpg")

#Key pad images
Control_1 = pygame.image.load("Arrows - Controls.png")
Control_2 = pygame.image.load("WASD-Controls.png")
    
walls = []
platforms = []

#works as the games frame rate
clock = pygame.time.Clock()
#Database for users
Users = sqlite3.connect("Users.db")
U = Users.cursor()

#Creating class for login system using Tkinter
#Group A class
class Login_sys():
    def __init__(self):
        #Setting attributes that are required
        self.screen1 = None
        self.screen2 = None
        self.screen3 = None
        self.username = ""
        self.password = ""
        self.first_name = ""
        self.surname = ""
        self.username_entry = ""
        self.password_entry = ""
        self.first_entry = ""
        self.sur_entry = ""
        self.UserID = ""

    def Start_up(self):
        #Creates the initial Screen users see
        #Sets size and displays the text and buttons
        self.screen1 = Tk()
        self.screen1.geometry("400x300")
        self.screen1.title("Login or Register")
        Label(text = "Login or Register", bg = "grey", width = 400, height = 3, font = ("Calibiri",18)).pack()
        Label(text = "").pack()
        Button(text = "Login", height = "2", width = "30", command = self.Login).pack()
        Label(text = "").pack()
        Button(text = "Register",height = "2", width = "30", command = self.Registration).pack()


        self.screen1.mainloop()

    def Registration(self):
        #Shows the screen when registering
        self.screen2 = Toplevel(self.screen1)
        self.screen2.title("Register")
        self.screen2.geometry("400x300")
        #attributes for values the user enters
        self.first_name = StringVar()
        self.surname = StringVar()
        self.username = StringVar()
        self.password = StringVar()

        Label(self.screen2, text = "Enter Details Below").pack()
        Label(self.screen2, text = "").pack()
        Label(self.screen2, text = "First Name ").pack()
        #Displays what the user is typing onto the screen
        self.first_entry = Entry(self.screen2, textvariable = self.first_name)
        self.first_entry.pack()
        Label(self.screen2, text = "Surname ").pack()
        self.sur_entry = Entry(self.screen2, textvariable = self.surname)
        self.sur_entry.pack()
        Label(self.screen2, text = "Username ").pack()
        self.username_entry = Entry(self.screen2, textvariable = self.username)
        self.username_entry.pack()
        Label(self.screen2, text = "Password ").pack()
        #Displays what the user is typing as *
        self.password_entry =  Entry(self.screen2, textvariable = self.password, show = '*')
        self.password_entry.pack()
        Label(self.screen2, text = "").pack()
        #Checks Runs the checking method to see if user already exists.
        Button(self.screen2, text = "Register", width = 10, height = 1, command = self.Check_Reg).pack()
  
    def Check_Reg(self):
        #Checks if username exists
        #Group C skill
        for row in U.execute('SELECT Username FROM Users'):
            user = str(row).replace("'","").replace(",","").replace("(","").replace(")","")
            if user == self.username.get():
                print("Username is taken already")
                invalid = True
                break
            else:
                invalid = False
                pass

        if invalid:
            #Prevents user from being created if username is in use
            self.screen2.destroy()
            self.Registration()
        else:
            #Adds user to the database
            print("User Created")
            self.Register()

            

    def Register(self):
        #Group A skill
        #obtains a true radom salt then hashes the password
        salt = os.urandom(16)
        password = self.password.get()
        h_pass = hashlib.sha256(password.encode("utf-8")+salt).hexdigest()
        #Inserts the users details along with the salt and hashed password
        data = (self.username.get(), h_pass, self.first_name.get(), self.surname.get(), salt)

        U.execute('insert INTO Users(Username,Password,First_Name,Surname,Salt) VALUES(?,?,?,?,?)',
                   data)
        Users.commit()

        self.screen2.destroy()
        self.screen1.destroy()
        self.Start_up()

    def Login(self):
        #Displays login screen
        self.screen3 = Toplevel(self.screen1)
        self.screen3.title("Login")
        self.screen3.geometry("400x250")

        self.username = StringVar()
        self.password = StringVar()
        
        Label(self.screen3, text = "Enter Details Below").pack()
        Label(self.screen3, text = "").pack()
        Label(self.screen3, text = "Username ").pack()
        #Displays users text they entered
        self.username_entry = Entry(self.screen3, textvariable = self.username)
        self.username_entry.pack()
        Label(self.screen3, text = "Password ").pack()
        #Displays the password entered as * 
        self.password_entry =  Entry(self.screen3, textvariable = self.password, show = '*')
        self.password_entry.pack()
        Label(self.screen3, text = "").pack()
        #Checks if details match
        Button(self.screen3, text = "Login", width = 10, height = 1, command = self.Check_Log).pack()

    def Check_Log(self):
        #Group C
        #Checks if Username is in the database
        for row in U.execute('SELECT Username FROM Users'):
            user = str(row).replace("'","").replace(",","").replace("(","").replace(")","")

            if user == self.username.get():
                valid1 = True
                break
            else:
                valid1 = False
                pass

        if valid1:
            #If the username exists it obtains the salt assigned with that user
            U.execute('SELECT Salt FROM Users WHERE Username = ?',(self.username.get(),))
            #The salt is then used to hash the user entered password
            Salt = U.fetchone()[0]
            h_pass = hashlib.sha256(self.password.get().encode("utf-8")+Salt).hexdigest()

            U.execute('SELECT Password FROM Users WHERE Username = ?',(self.username.get(),))
            #Checks if passwords match
            if U.fetchone()[0] == h_pass:
                valid2 = True
                
            else:
                valid2 = False
                

        else:
            #If username does not match
            print("Username Does Not Exist")
            self.screen3.destroy()
            self.screen1.destroy()
            self.Start_up()

        
        if valid2:
            #If passwords match they are taken to the main menu
            print("Login Successful")
            U.execute('SELECT UserID FROM Users WHERE Username = ?',(self.username.get(),))
            self.UserID = U.fetchone()[0]
            self.screen3.destroy()
            self.screen1.destroy()
            Start.Game_menu()
            
            
        else:
            #User is returned to login menu
            print("Password Does Not Match")
            self.screen3.destroy()
            self.Login()


#Class for main menu
#Group A skill
class Main_menu():
    def __init__(self, display_width = 0, display_height = 0, gameDisplay = ""):
        self.display_width = display_width
        self.display_height = display_height
        self.gameDisplay = gameDisplay


    def get_display(self):
        #Setting the size of the window
        self.display_width = 800
        self.display_height = 600    
        #Dealing with game display
        self.gameDisplay = pygame.display.set_mode((self.display_width,self.display_height))
        pygame.display.set_caption('Mystery Adventure')


    #Creating buttons
    #(Text,text size,x co ordinate,y co ordinate,width,height,inactive colour,active colour,button command)
    def button(self,msg,s,x,y,w,h,ic,ac,Action=None):
        #Reads mouse position and mouse button presses
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        #Changes button colour when mouse hovers over it
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(self.gameDisplay, ac,(x,y,w,h))

            #Carrys out button action if clicked
            if click[0] == 1 and Action != None:
                Action()
        else:
            pygame.draw.rect(self.gameDisplay, ic,(x,y,w,h))

        #Displays text and draws buttons
        smallText = pygame.font.Font("freesansbold.ttf",s)
        textSurf, textRect = text_render(msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        self.gameDisplay.blit(textSurf, textRect)



    #Creating the menu
    def Game_menu(self):
        run = True
        
        self.get_display()

        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    return

            #Creates background and main text
            self.gameDisplay.blit(bg1,(0,0))
            largeText = pygame.font.Font("freesansbold.ttf",80)
            TextSurf, TextRect = text_render("Mystery Adventure", largeText)
            TextRect.center = ((self.display_width/2),(self.display_height/8))
            self.gameDisplay.blit(TextSurf, TextRect)

            #optains buttons for menu
            self.button("Tutorial",20,150,300,125,75,Bright_blue,Purple,tutorial)
            self.button("Single Player",18,350,300,125,75,Bright_blue,Purple,self.Single_menu)
            self.button("Multiplayer",20,550,300,125,75,Bright_blue,Purple,self.Multi_menu)
            self.button("Controls",20,150,425,100,50,blue,Bright_blue,self.Controls)
            self.button("Leaderboards",20,150,500,150,50,blue,Bright_blue,self.Leader)

            self.button("Exit",20,600,500,100,50,red,bright_red,quit)

            pygame.display.update()



    #single player menu
    def Single_menu(self):
        #Tells rest of the code to ignore the second player
        global multi
        multi = False

        run = True

        while run:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Game_menu()
                    return
                    
            #Title text
            self.gameDisplay.blit(bg1,(0,0))
            largeText = pygame.font.Font("freesansbold.ttf",80)
            TextSurf, TextRect = text_render("Single player", largeText)
            TextRect.center = ((self.display_width/2),(self.display_height/8))
            self.gameDisplay.blit(TextSurf, TextRect)

            #All the buttons currently leading to the tutorial untill stages are created
            self.button("1",20,150,150,75,75,Bright_blue,Purple,L1)
            self.button("2",20,250,150,75,75,Bright_blue,Purple,L2)
            self.button("3",20,350,150,75,75,Bright_blue,Purple,L3)
            self.button("4",20,450,150,75,75,Bright_blue,Purple,L4)
            self.button("5",20,550,150,75,75,Bright_blue,Purple,L5)

            self.button("6",20,150,250,75,75,Bright_blue,Purple,L6)
            self.button("7",20,250,250,75,75,Bright_blue,Purple,L7)
            self.button("8",20,350,250,75,75,Bright_blue,Purple,L8)
            self.button("9",20,450,250,75,75,Bright_blue,Purple,L9)
            self.button("10",20,550,250,75,75,Bright_blue,Purple,L10)

            self.button("11",20,150,350,75,75,Bright_blue,Purple,L11)
            self.button("12",20,250,350,75,75,Bright_blue,Purple,L12)
            self.button("13",20,350,350,75,75,Bright_blue,Purple,L13)
            self.button("14",20,450,350,75,75,Bright_blue,Purple,L14)
            self.button("15",20,550,350,75,75,Bright_blue,Purple,L15)

            self.button("Return",20,600,500,100,50,red,bright_red,self.Game_menu)

            pygame.display.update()


    #multiplayer menu
    def Multi_menu(self):
        #Global variable telling the rest of the code to recognise the second player
        global multi
        multi = True

        run = True

        while run:
            
            #Makes it the exit button in pygame returns to the stage select menu when in a stage
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Game_menu()
                    return
                    
            #Title text
            self.gameDisplay.blit(bg1,(0,0))
            largeText = pygame.font.Font("freesansbold.ttf",80)
            TextSurf, TextRect = text_render("Multiplayer", largeText)
            TextRect.center = ((self.display_width/2),(self.display_height/8))

            self.gameDisplay.blit(TextSurf, TextRect)            

            #All the buttons currently leading to the tutorial untill stages are created
            self.button("1",20,150,150,75,75,Bright_blue,Purple,L1)
            self.button("2",20,250,150,75,75,Bright_blue,Purple,L2)
            self.button("3",20,350,150,75,75,Bright_blue,Purple,L3)
            self.button("4",20,450,150,75,75,Bright_blue,Purple,L4)
            self.button("5",20,550,150,75,75,Bright_blue,Purple,L5)

            self.button("6",20,150,250,75,75,Bright_blue,Purple,L6)
            self.button("7",20,250,250,75,75,Bright_blue,Purple,L7)
            self.button("8",20,350,250,75,75,Bright_blue,Purple,L8)
            self.button("9",20,450,250,75,75,Bright_blue,Purple,L9)
            self.button("10",20,550,250,75,75,Bright_blue,Purple,L10)

            self.button("11",20,150,350,75,75,Bright_blue,Purple,L11)
            self.button("12",20,250,350,75,75,Bright_blue,Purple,L12)
            self.button("13",20,350,350,75,75,Bright_blue,Purple,L13)
            self.button("14",20,450,350,75,75,Bright_blue,Purple,L14)
            self.button("15",20,550,350,75,75,Bright_blue,Purple,L15)
            #Return to main menu button
            self.button("Return",20,600,500,100,50,red,bright_red,self.Game_menu)

            pygame.display.update()



    def Controls(self):
        
        run = True

        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Game_menu()
            #Displays images of the arrow keys and WASD
            self.gameDisplay.blit(bg1,(0,0))
            self.gameDisplay.blit(Control_1,((self.display_width//30),(self.display_height//4)))
            self.gameDisplay.blit(Control_2,((self.display_width*4//8),(self.display_height//4)))
            #Displays Controls text
            largeText = pygame.font.Font("freesansbold.ttf",80)
            TextSurf, TextRect = text_render("Controls", largeText)
            TextRect.center = ((self.display_width/2),(self.display_height/8))

            self.gameDisplay.blit(TextSurf, TextRect)
            #Displays player 1 text
            largeText = pygame.font.Font("freesansbold.ttf",30)
            TextSurf, TextRect = text_render("Player 1", largeText)
            TextRect.center = ((self.display_width//4),(self.display_height//4))
            self.gameDisplay.blit(TextSurf, TextRect)
            #Displays player 2 text
            largeText = pygame.font.Font("freesansbold.ttf",30)
            TextSurf, TextRect = text_render("Player 2", largeText)
            TextRect.center = ((self.display_width*3//4),(self.display_height//4))
            self.gameDisplay.blit(TextSurf, TextRect)
            #Creates a return buutton
            self.button("Return",20,600,500,100,50,red,bright_red,self.Game_menu)
            
            pygame.display.update()



    def Leader(self):

        run = True

        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Game_menu()                
                    return
            #Displays leaderboards text
            self.gameDisplay.blit(bg1,(0,0))
            largeText = pygame.font.Font("freesansbold.ttf",80)
            TextSurf, TextRect = text_render("Leaderboards", largeText)
            TextRect.center = ((self.display_width/2),(self.display_height/8))
            self.gameDisplay.blit(TextSurf, TextRect)
            
            #Creates buttons that display times for each level
            
            self.button("1",20,150,150,75,75,Bright_blue,Purple,C1)
            self.button("2",20,250,150,75,75,Bright_blue,Purple,C2)
            self.button("3",20,350,150,75,75,Bright_blue,Purple,C3)
            self.button("4",20,450,150,75,75,Bright_blue,Purple,C4)
            self.button("5",20,550,150,75,75,Bright_blue,Purple,C5)

            self.button("6",20,150,250,75,75,Bright_blue,Purple,C6)
            self.button("7",20,250,250,75,75,Bright_blue,Purple,C7)
            self.button("8",20,350,250,75,75,Bright_blue,Purple,C8)
            self.button("9",20,450,250,75,75,Bright_blue,Purple,C9)
            self.button("10",20,550,250,75,75,Bright_blue,Purple,C10)

            self.button("11",20,150,350,75,75,Bright_blue,Purple,C11)
            self.button("12",20,250,350,75,75,Bright_blue,Purple,C12)
            self.button("13",20,350,350,75,75,Bright_blue,Purple,C13)
            self.button("14",20,450,350,75,75,Bright_blue,Purple,C14)
            self.button("15",20,550,350,75,75,Bright_blue,Purple,C15)

            #Return to main menu button
            self.button("Return",20,600,500,100,50,red,bright_red,self.Game_menu)
                

            pygame.display.update()

    def Game_over(self):
        
        run = True
        
        while run:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Game_menu()
            #Shows game over screen
            self.gameDisplay.blit(bg4,(0,0))
            #creates return button
            self.button("Return",20,350,450,100,50,red,bright_red,self.Game_menu)
            pygame.display.update()
 







#Player class
class Player(object):
    #Sets all the initial values for the character *Will also use player number when creating multiplayer*
    def __init__(self,x,y,player_number):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 60
        self.player_number = player_number

    def get_attributes(self):
        #player speed
        self.vel = 7
        #checks if player is moving or jumping
        self.isJump = False
        self.left = False
        self.right = False
        self.ontop = False
        #checks how many steps character has moved
        self.walkCount = 0
        #Jump height
        self.jumpCount = 12
        self.hitbox = (self.x+12,self.y+12,60,90)
        self.sprite = pygame.Rect((self.x + 12, self.y + 12)+(60,90))

    def move(self):

        #Gets what keys have been pressed by user
        keys = pygame.key.get_pressed()

        gravity = True
        if self.player_number == 1:
            #All character movement and gives gravity to diffrent situations for player 1
            if keys[pygame.K_LEFT] and self.x > self.vel and pygame.Rect(self.hitbox).y <(600 - 60):
                self.x -= self.vel
                gravity = True
                if gravity == True:
                    self.y += 10
                self.left = True
                self.right = False
            elif keys[pygame.K_RIGHT] and self.x < 800 - self.width - self.vel and pygame.Rect(self.hitbox).y <(600 - 60):
                self.x += self.vel
                gravity = True
                if gravity == True:
                    self.y += 10
                self.right = True
                self.left = False

            elif pygame.Rect(self.hitbox).y < (600 - 60): 
                gravity = True
                if gravity == True:
                    self.y += 10



            else:
                self.right = False
                self.left = False
                self.walkCount = 0

            if not(self.isJump):
                if keys[pygame.K_UP]:
                    self.isJump = True
                    self.right = False
                    self.left = False
                    self.walkCount = 0

            else:    
                if self.jumpCount >= -12:
                    neg = 1
                    if self.jumpCount < 0:
                        neg = -1
                    self.y -= (self.jumpCount ** 2) * 0.5 * neg
                    self.jumpCount -= 1
                else:
                    self.isJump = False
                    self.jumpCount = 12

        if self.player_number == 2:
            #All character movement and gives gravity to diffrent situations for player 2
            if keys[pygame.K_a] and self.x > self.vel and pygame.Rect(self.hitbox).y <(600 - 60):
                self.x -= self.vel
                gravity = True
                if gravity == True:
                    self.y += 10
                self.left = True
                self.right = False
            elif keys[pygame.K_d] and self.x < 800 - self.width - self.vel and pygame.Rect(self.hitbox).y <(600 - 60):
                self.x += self.vel
                gravity = True
                if gravity == True:
                    self.y += 10
                self.right = True
                self.left = False

            elif pygame.Rect(self.hitbox).y < (600 - 60): 
                gravity = True
                if gravity == True:
                    self.y += 10



            else:
                self.right = False
                self.left = False
                self.walkCount = 0

            if not(self.isJump):
                if keys[pygame.K_w]:
                    self.isJump = True
                    self.right = False
                    self.left = False
                    self.walkCount = 0

            else:    
                if self.jumpCount >= -12:
                    neg = 1
                    if self.jumpCount < 0:
                        neg = -1
                    self.y -= (self.jumpCount ** 2) * 0.5 * neg
                    self.jumpCount -= 1
                else:
                    self.isJump = False
                    self.jumpCount = 12
            

        return gravity


    #Deals with character animations
    def draw(self, win, gravity):
        #Group A skill
        if self.player_number == 1:
        #Deals with movement and cycling through player animations
            if self.walkCount + 1 >= 40:
                self.walkCount = 0

            if self.left:
                win.blit(walkLeft_1[self.walkCount//10], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight_1[self.walkCount//10], (self.x,self.y))
                self.walkCount +=1
            else:
                win.blit(Stand_1, (self.x,self.y))
        if self.player_number == 2:
            #Deals with movement and cycling through player animations
            if self.walkCount + 1 >= 40:
                self.walkCount = 0

            if self.left:
                win.blit(walkLeft_2[self.walkCount//10], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight_2[self.walkCount//10], (self.x,self.y))
                self.walkCount +=1
            else:
                win.blit(Stand_2, (self.x,self.y))


        #Checks for collision detection
        self.x,self.y,self.sprite,self.hitbox,gravity,self.ontop=collision_detection(self.x,self.y,self.sprite,self.hitbox,gravity,self.ontop)



        
        return(win,gravity)


class Enemy(object):
    #Enemy Sprites
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'),
                 pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'),
                 pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'),
                pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'),
                pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
    
    def __init__(self, x, y, end):
        #Enemy attributes
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        #Enemy movement path
        self.path = [x, end]
        self.walkCount = 0
        self.vel = 3
        self.sprite = pygame.Rect((self.x , self.y )+(60,90))

    def draw(self, win):
        self.move()
        #Displays sprites based enemy movement
        if self.walkCount + 1 >= 33:
            self.walkCount = 0
        
        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1
            self.sprite = pygame.Rect((self.x + 15, self.y + 5 )+(45,90))
        else:
            win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1
            self.sprite = pygame.Rect((self.x + 50, self.y + 5 )+(45,90))

        

            
    def move(self):
        #Moves Enemy based on velocity and path
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0


#a new class for walls 
class Wall(object):
    def __init__(self, wx, wy):
        walls.append(self)
        self.rect = pygame.Rect(wx,wy,30,60)

#Class for platforms
class Platform(object):
    def __init__(self,px,py):
        platforms.append(self)
        self.rect = pygame.Rect(px,py,45,45)


def collision_detection(x,y,sprite,hitbox,gravity,ontop):

   
    sprite = pygame.Rect((x + 12, y + 14)+(60,90))
    #Makes sure character can walk on floor
    for wall in walls:
        if sprite.colliderect(wall.rect):
            if y + 90 > 0:
                gravity = False
                sprite.bottom = wall.rect.top
                y = sprite.bottom - 110
                ontop = False

    #Allows chracter to stand on platform and prevents them from jumping through them.

    for platform in platforms:
        #Prevents jumping through
        if y + 90 > platform.rect.top + 45:
            if sprite.colliderect(platform.rect):
                if ontop == True:
                    pass
                else:
                    gravity = True
                    sprite.bottom = wall.rect.top 
                    y = sprite.bottom - 110
                    ontop = False
        #Allows to stand
        if y - 90 < platform.rect.top - 45:
            if sprite.colliderect(platform.rect):
                gravity = False
                sprite.bottom = platform.rect.top
                y = platform.rect.top - 110
                ontop = True

         
    return x,y,sprite,hitbox,gravity,ontop



    


def Init_wall(LEVEL):
    #Group A skill
    #if enemies is in stage
    enemies = False
    #if teleporting is in the stage
    teleportation = False
    #prevents syntax error if none are present
    gob = False
    tel_rect_1 = False
    tel_rect_2 = False
    #Uses list to create a level design specified by the list
    x = y = 0
    for row in LEVEL:
        for col in row:
            if col == "W":
                #wall class
                Wall(x, y)
            if col == "E":
                #ending square
                end_rect = pygame.Rect(x,y,30,30)
            if col == "P":
                #platform class
                Platform(x,y)
            if col == "1":
                #drawing teleport square 1 and changing variable
                tel_rect_1 = pygame.Rect(x,y,30,30)
                teleportation = True
            if col == "2":
                #drawing teleport square 2 and changing variable
                tel_rect_2 = pygame.Rect(x,y,30,30)
                teleportation = True
            if col == "S":
                #Player 1
                char1 = Player(x, y, 1)
                char1.get_attributes()
                #Player 2
                char2 = Player(x, y, 2)
                char2.get_attributes()
            if col =="G":
                #Enemy class and changing variable
                gob = Enemy(x-37,y-37, x+30)
                enemies = True
                            
            x += 30
        y += 60
        x=0

    return end_rect,tel_rect_1,tel_rect_2,teleportation,enemies,char1,char2,gob

#Tutorial level list
#P = platforms
#W = Wall/floor
#E = Exit
#1 = Teleport point
#2 = Teleport end
#G = Goblin/Enemy

level_1 = [
        "                           ",
        "                           ",
        "                           ",
        "                           ",
        "                           ",
        "                           ",
        "                           ",
        "                           ",
        "S                        E ",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]

level_2 = [
        "                           ",
        "                           ",
        "                           ",
        "                           ",
        "                           ",
        "          E                ",
        "       PPPP                ",
        "                           ",
        "S                          ",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]


level_3 = [
        "                           ",
        "                           ",
        "                           ",
        "                           ",
        "                           ",
        "                     E     ",
        "       PPPP      PPPPP     ",
        "                           ",
        "S                          ",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]

level_4 = [
        "                           ",
        "                           ",
        "                           ",
        "                     E     ",
        "                   PPP     ",
        "            PPPP           ",
        "     PPP                   ",
        "                           ",
        "S                          ",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]

level_5 = [
        "                           ",
        "                           ",
        "                           ",
        "   E                       ",
        "   P                       ",
        "           PP              ",
        "                   PPP     ",
        "                           ",
        "                         S ",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]

level_6 = [
        "                           ",
        "              E            ",
        "             PPP           ",
        "                        2  ",
        "                     PPPP  ",
        "    1                      ",
        "  PPP                      ",
        "                           ",
        "S                          ",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]

level_7 = [
        "            E              ",
        "         PPPP              ",
        "                           ",
        "2                          ",
        "PPPP                       ",
        "                  1        ",
        "                PPP        ",
        "                           ",
        "S                          ",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]

level_8 = [
        "                           ",
        "                           ",
        "  E                        ",
        "                   2       ",
        "        PP       PPP       ",
        "                        1  ",
        "                           ",
        "                           ",
        "S                          ",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]

level_9 = [
        "                           ",
        "                           ",
        "                      E    ",
        "2                          ",
        "PP      P       PP         ",
        "                           ",
        "                           ",
        "                           ",
        "S                        1 ",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]

level_10 = [
        "                           ",
        "  E                        ",
        "         P                 ",
        "                 P         ",
        "                          2",
        "                         PP",
        "                           ",
        "                           ",
        "S                        1 ",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]

level_11 = [
        "                           ",
        "                           ",
        "                           ",
        "                           ",
        "                           ",
        "                           ",
        "                           ",
        "                           ",
        "S                  G     E ",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]

level_12 = [
        "                           ",
        "                           ",
        "                        E  ",
        "                  G        ",
        "                PPPPP      ",
        "                           ",
        "     PPPPP                 ",
        "                           ",
        "S                          ",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]

level_13 = [
        "                           ",
        "                           ",
        "                        E  ",
        "2                G         ",
        "P     P    P    PPPPP      ",
        "                           ",
        "                           ",
        "                           ",
        "S                       1  ",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]

level_14 = [
        "                           ",
        "        G   E              ",
        "      PPPPPPP              ",
        "2                          ",
        "PP                         ",
        "                         1 ",
        "                        PPP",
        "                           ",
        "S                          ",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]

level_15 = [
        "                           ",
        "E                          ",
        "       P      G            ",
        "             PPPPP         ",
        "                         2 ",
        "                         PP",
        "                           ",
        "                           ",
        "S                        1 ",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]


#Rendering the text that appears
def text_render(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


#Adds users time for a stage into the database
def insert_time(Time,Stage_num):
    data = (Time,Stage_num)
    U.execute('insert INTO Leaderboards(Time,Level) VALUES(?,?)',
                   data)

    U.execute('SELECT CompleteID FROM Leaderboards WHERE Time = ? AND Level = ?',
              data)

    data = (Main.UserID,U.fetchone()[0])


    U.execute('insert INTO Identification(UserID,CompleteID) VALUES(?,?)',
              data)

    Users.commit()




    
#Updates the screen for the tutorial
def redraw_tutorial(gravity,end_rect,char1,gob):
    win.blit(bg1, (0,0))

    #Updates screens
    largeText = pygame.font.Font("freesansbold.ttf",30)
    TextSurf, TextRect = text_render("Left and Right arrows to move", largeText)
    TextRect.center = ((800/2),(600/8))
    win.blit(TextSurf, TextRect)

    largeText = pygame.font.Font("freesansbold.ttf",30)
    TextSurf, TextRect = text_render("Up arrow to jump", largeText)
    TextRect.center = ((800/2),(600/6))
    win.blit(TextSurf, TextRect)
    #Updates chracter animation
    char1.draw(win,gravity)
    #Updates the walls and platforms
    #Group A skills
    for wall in walls:
        pygame.draw.rect(win,wall_colour_1,wall.rect)

    for platform in platforms:
        pygame.draw.rect(win,wall_colour_1,platform.rect)
    pygame.draw.rect(win,bright_red,end_rect)
 



    pygame.display.update()

#Redraws all levels
def redraw_level(enemies,teleportation,gravity,end_rect,tel_rect_1,tel_rect_2,stage_num,char1,char2,gob):
    #Displays correct background based on stage number
    if stage_num > 0 and stage_num < 6:
        win.blit(bg1, (0,0))
    if stage_num > 5 and stage_num < 11:
        win.blit(bg2, (0,0))
    if stage_num > 10 and stage_num < 15:
        win.blit(bg3, (0,0))
    if stage_num == 15:
        win.blit(bg5, (0,0))
    #Updates chracter animation
    char1.draw(win,gravity)
    if multi:
        char2.draw(win,gravity)

    if enemies:
        gob.draw(win)
    #Updates the walls and platforms depending on stage nummber
    #Each ste of stages will have diffrent platform/wall colours
    #Group A skill
    if stage_num > 0 and stage_num < 6:

        for wall in walls:
            pygame.draw.rect(win,wall_colour_1,wall.rect)

        for platform in platforms:
            pygame.draw.rect(win,wall_colour_1,platform.rect)

    if stage_num > 5 and stage_num < 11:

        for wall in walls:
            pygame.draw.rect(win,wall_colour_2,wall.rect)

        for platform in platforms:
            pygame.draw.rect(win,wall_colour_2,platform.rect)
            
    if stage_num > 10 and stage_num < 15:
        
        for wall in walls:
            pygame.draw.rect(win,wall_colour_3,wall.rect)

        for platform in platforms:
            pygame.draw.rect(win,wall_colour_3,platform.rect)

    if stage_num == 15:
        
        for wall in walls:
            pygame.draw.rect(win,wall_colour_4,wall.rect)

        for platform in platforms:
            pygame.draw.rect(win,wall_colour_4,platform.rect)

    #Draws Teleport and ending blocks
    if teleportation == True:
        pygame.draw.rect(win,Purple,tel_rect_1)
        pygame.draw.rect(win,Bright_blue,tel_rect_2)

    pygame.draw.rect(win,bright_red,end_rect)
    
    

    pygame.display.update()

    

#Main tutorial
def tutorial():
    #Tutorial loop

    
    end_rect,tel_rect_1,tel_rect_2,teleportation,enemies,char1,char2,gob = Init_wall(level_1)

    run = True
    while run:
        #Frame rate
        clock.tick(40)
        #Allows user to return to main menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                del walls [:]
                run = False

        gravity = char1.move()

        #Ends stages when player collides with end rectangle
        if char1.sprite.colliderect(end_rect):
            #Group A skill
            del walls [:]
            run = False

          
        #Calls for the screen to be updated
        redraw_tutorial(gravity,end_rect,char1,gob)

#Main stage function
def stage(level,stage_num):

    #Draws stage
    end_rect,tel_rect_1,tel_rect_2,teleportation,enemies,char1,char2,gob = Init_wall(level)
    #Starts timer
    start = time.time()
    
    run = True
    while run:
        #Frame rate
        clock.tick(40)
        #Allows user to return to main menu and resets values
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                del walls [:]
                del platforms [:]
                start = 0
                run = False

        #Calling player movement
        gravity = char1.move()
        if multi:
            gravity = char2.move()

        #Ends stages when players collides with end rectangle
        #Obtains time elapsed to insert into the database
        if char1.sprite.colliderect(end_rect):
            #Group A skill
            del walls [:]
            del platforms [:]
            end = time.time()
            elapsed = round((end-start),2)
            insert_time(elapsed,stage_num)
            run = False
        if multi:
            if char2.sprite.colliderect(end_rect):
                del walls [:]
                del platforms [:]
                end = time.time()
                elapsed = round((end-start),2)
                insert_time(elapsed,stage_num)
                run = False

        #Teleports player 1 from one rectangle to the other
        if teleportation == True:
            if char1.sprite.colliderect(tel_rect_1):
                teleport = True

            else:
                teleport = False

            if teleport:
                if not(char1.sprite.colliderect(tel_rect_2)):
                    char1.sprite.left = tel_rect_2.right
                    char1.sprite.bottom = tel_rect_2.top
                    char1.x = char1.sprite.left - 30
                    char1.y = char1.sprite.bottom - 110
                teleport = False
            else:
                pass

        #Teleports player 2 from one rectangle to the other
        if multi:
            if teleportation == True:
                if char2.sprite.colliderect(tel_rect_1):
                    teleport = True

                else:
                    teleport = False

                if teleport:
                    if not(char2.sprite.colliderect(tel_rect_2)):
                        char2.sprite.left = tel_rect_2.right
                        char2.sprite.bottom = tel_rect_2.top
                        char2.x = char2.sprite.left - 30
                        char2.y = char2.sprite.bottom - 110
                    teleport = False
                else:
                    pass

        #Game over screen is shown when the user collides with and enemy
        if enemies:
            if char1.sprite.colliderect(gob.sprite) or char2.sprite.colliderect(gob.sprite):
                del walls [:]
                del platforms [:]
                start = 0
                
                Start.Game_over()
            
        redraw_level(enemies,teleportation,gravity,end_rect,tel_rect_1,tel_rect_2,stage_num,char1,char2,gob)

#Displays data for the stage selected.
def display_data(stage_num):
    #Group A skill
    #Fetches the data searched
    U.execute('''SELECT Users.Username,Leaderboards.Time,Leaderboards.Level FROM Users,Leaderboards,Identification
    WHERE Users.UserID = Identification.UserID AND Leaderboards.Level = ? AND Identification.CompleteID = Leaderboards.CompleteID
    ORDER BY Leaderboards.Time ASC''',(stage_num,))
    data_list = U.fetchall()
    print("Username|Time(s)|Level")
    #Displays data
    for x in range (len(data_list)):
        data = str(data_list[x])
        print (data.replace("(","").replace(")","").replace("'",""))

    #Uses aggregate SQL function to display average time
    U.execute('''SELECT AVG(Time) FROM Leaderboards WHERE Leaderboards.Level = ?''',(stage_num,))
    data = round(U.fetchone()[0],2)

    print("\nAverage Time = ",data)






#Levels Calling the stage function with correct level and stage number
def L1():
    stage_num = 1
    stage(level_1,stage_num)

def L2():
    stage_num = 2
    stage(level_2,stage_num)
    
def L3():
    stage_num = 3
    stage(level_3,stage_num)
    
def L4():
    stage_num = 4
    stage(level_4,stage_num)
    
def L5():
    stage_num = 5
    stage(level_5,stage_num)

def L6():
    stage_num = 6
    stage(level_6,stage_num)

def L7():
    stage_num = 7
    stage(level_7,stage_num)

def L8():
    stage_num = 8
    stage(level_8,stage_num)

def L9():
    stage_num = 9
    stage(level_9,stage_num)

def L10():
    stage_num = 10
    stage(level_10,stage_num)

def L11():
    stage_num = 11
    stage(level_11,stage_num)

def L12():
    stage_num = 12
    stage(level_12,stage_num)

def L13():
    stage_num = 13
    stage(level_13,stage_num)

def L14():
    stage_num = 14
    stage(level_14,stage_num)

def L15():
    stage_num = 15
    stage(level_15,stage_num)

#Checking functions calling display data with correct stage number to check times
def C1():
    display_data(1)

def C2():
    display_data(2)

def C3():
    display_data(3)

def C4():
    display_data(4)

def C5():
    display_data(5)

def C6():
    display_data(6)
    
def C7():
    display_data(7)

def C8():
    display_data(8)

def C9():
    display_data(9)

def C10():
    display_data(10)

def C11():
    display_data(11)

def C12():
    display_data(12)

def C13():
    display_data(13)

def C14():
    display_data(14)

def C15():
    display_data(15)
    
#Calling the main menu and login system

Start = Main_menu()
Main = Login_sys()
Main.Start_up()
