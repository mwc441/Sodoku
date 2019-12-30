from pygame import *
from tkinter import *
import random


class GameBoard():
    screen_width=450
    screen_height=450
    boxheight = 50 # Size of individual sodoku boxes
    boxwidth = 50
     

    """
    Initializes the board using the given 2D Board Array, and the class variables listed above
    """
    def __init__(self, board):
        init()
        self.newboard = [] # Array to place in coordinates of previous valid moves
        self.x = 0 # X Coordinate of previous click
        self.y = 0 # Y Coordinate of previous click
        self.count = 0 # Dummy count variable
        self.screen=display.set_mode([self.screen_width, self.screen_height])
        self.board = board
        self.font = font.SysFont("arial", 30)

        ##############   INITIALIZING BOARD   ##################
        bg = Rect(0,0, self.screen_width, self.screen_height)
        draw.rect(self.screen,Color(255,255,255), bg)
        display.set_caption("Sudoku")
        boxarray = [[0]*9 for i in range(9)]
        for i in range(9):
            for j in range(9):
                newrect = Rect(j*self.boxwidth, i*self.boxheight, self.boxwidth, self.boxheight)
                draw.rect(self.screen, Color(220,220,220), newrect, 3)
                boxarray[i][j] = newrect
        draw.line(self.screen, Color(0,0,0), (147,0), (147,450), 6)
        draw.line(self.screen, Color(0,0,0), (297,0), (297,450), 6)  
        draw.line(self.screen, Color(0,0,0), (0,147), (450,147), 6)
        draw.line(self.screen, Color(0,0,0), (0,297), (450,297), 6)
        for i in range(9):
            for j in range(9):
                if(self.board[i][j] != 0):
                    txt = self.font.render(str(self.board[i][j]), 1, Color(0,0,0))
                    self.screen.blit(txt, (j*self.boxheight + 17, i*self.boxwidth+8))
        ###############   INITIALIZING BOARD   #################
        
        


    """
    Runs the game and allows users to interact with the pre-initialized board, if this isn't run, then users
    will not be able to interact with the board!
    """
    def runGame(self):
        run = True
        while run:
            total = 0
            time.delay(100)
            for i in range(9):
                for j in range(9):
                    if(self.board[i][j] != 0):
                        total = total + 1
            if (total == 81):
                run = False
                quit()
                mainmenu = StartupMenu()
                return mainmenu
                        
                
            for events in event.get():
                if events.type == QUIT:
                    run = False
                    quit()
                    mainmenu = StartupMenu()
                    return mainmenu
                if events.type == MOUSEBUTTONDOWN:
                    self.x,self.y = mouse.get_pos()
                    i = self.x//self.boxheight
                    j = self.y//self.boxwidth
                    if(self.board[j][i] == 0 or self.newboard.count([j,i]) > 0):
                        if self.count > 0:
                            draw.rect(self.screen, Color(255,255,255), newbox, 3)
                        selectorbox = Rect(0,0,self.boxheight-12, self.boxwidth-12)
                        newbox = selectorbox.move(i*self.boxwidth +6,j*self.boxheight+6)
                        draw.line(self.screen, Color(0,0,0), (147,0), (147,450), 6)
                        draw.line(self.screen, Color(0,0,0), (297,0), (297,450), 6)  
                        draw.line(self.screen, Color(0,0,0), (0,147), (450,147), 6)
                        draw.line(self.screen, Color(0,0,0), (0,297), (450,297), 6)
                        draw.rect(self.screen, Color(255,0,0), newbox, 2)
                        self.count = self.count + 1
                if events.type == KEYDOWN:
                    key = -1
                    if events.key == K_1:
                        key = 1
                    if events.key == K_2:
                        key = 2
                    if events.key == K_3:
                        key = 3
                    if events.key == K_4:
                        key = 4
                    if events.key == K_5:
                        key = 5
                    if events.key == K_6:
                        key = 6
                    if events.key == K_7:
                        key = 7
                    if events.key == K_8:
                        key = 8
                    if events.key == K_9:
                        key = 9
                    if events.key == K_DELETE:
                        key = 0
                    i = self.x //self.boxheight
                    j = self.y//self.boxheight
                    if(validmove([i,j], key, self.board) or key == 0):
                        if(key == 0 and self.newboard.count([j,i]) > 0 ):
                            selectorbox = selectorbox.move(i*self.boxwidth + 6, j*self.boxheight +6)
                            newbox = draw.rect(self.screen, Color(255,255,255), selectorbox)
                            newbox = draw.rect(self.screen,Color(255,0,0), newbox, 2)
                            self.board[j][i] = 0
                            self.newboard.remove([j,i])
                        elif(key > 0):
                            self.board[j][i] = key
                            self.newboard.append([j,i])
                            txt = self.font.render(str(key), 1, Color(255,0,0))
                            self.screen.blit(txt, (i*self.boxheight + 17, j*self.boxwidth+8))
            if run:
                display.update()


class StartupMenu():
    
    def runStartupMenu(self):
        self.frame = Tk()
        self.introLabel = Label(self.frame, text="Welcome to Sodoku")
        self.introLabel.pack()
        self.setupButtons()
        self.frame.title("Sodoku")
        self.frame.geometry("250x100")
        self.frame.resizable(False, False)
        self.frame.mainloop()

    def setupButtons(self):
        StartDefault = Button(self.frame, text="Start with Random grid", command=self.setupRandomGame)
        StartOwn = Button(self.frame, text="Start with Custom grid", command=self.setupCustomGame)
        Quit = Button(self.frame, text="Quit", command=self.quitmenu)
        StartDefault.pack()
        StartOwn.pack()
        Quit.pack()

    def quitmenu(self):
        self.frame.destroy()

    def setupRandomGame(self):
        self.frame.destroy()
        newgame = GameBoard(randomBoard())
        menu = newgame.runGame()
        menu.runStartupMenu()

    """
    Creates a blank board (setupBoard) which allows users to enter their own numbers into the board
    (valid numbers only)
    """
    def setupCustomGame(self):
        self.frame.destroy()
        newgame = setupBoard()
        board = newgame.runGame()
        if board != 0:
            ownGame = GameBoard(board)
            menu = ownGame.runGame()
            menu.runStartupMenu()
            
        else:
            newmenu = StartupMenu()
            newmenu.runStartupMenu()
            
        
"""
A setupBoard is a blank board with the functionality of a regular GameBoard
It checks for valid moves and allows users to create their own custom board
It has one extra functionality, pressing the enter key exits the board and returns
an array for their custom board!
"""
class setupBoard():
    screen_width=450
    screen_height=450
    boxheight = 50 # Size of individual sodoku boxes
    boxwidth = 50
    
    
    """
    Initializes the board using the given 2D Board Array, and the class variables listed above
    """
    def __init__(self):
        init()
        self.board = [[0]*9 for i in range(9)] # Empty 9x9 Board to let players place their own numbers
        self.newboard = [] # Array to place in coordinates of previous valid moves
        self.x = 0 # X Coordinate of previous click
        self.y = 0 # Y Coordinate of previous click
        self.count = 0 # Dummy count variable
        self.screen=display.set_mode([self.screen_width, self.screen_height])
        self.font = font.SysFont("arial", 30)

        ##############   INITIALIZING BOARD   ##################
        bg = Rect(0,0, self.screen_width, self.screen_height)
        draw.rect(self.screen,Color(255,255,255), bg)
        display.set_caption("Sudoku")
        boxarray = [[0]*9 for i in range(9)]
        for i in range(9):
            for j in range(9):
                newrect = Rect(j*self.boxwidth, i*self.boxheight, self.boxwidth, self.boxheight)
                draw.rect(self.screen, Color(220,220,220), newrect, 3)
                boxarray[i][j] = newrect
        draw.line(self.screen, Color(0,0,0), (147,0), (147,450), 6)
        draw.line(self.screen, Color(0,0,0), (297,0), (297,450), 6)  
        draw.line(self.screen, Color(0,0,0), (0,147), (450,147), 6)
        draw.line(self.screen, Color(0,0,0), (0,297), (450,297), 6)
        for i in range(9):
            for j in range(9):
                if(self.board[i][j] != 0):
                    txt = self.font.render(str(self.board[i][j]), 1, Color(0,0,0))
                    self.screen.blit(txt, (j*self.boxheight + 17, i*self.boxwidth+8))
        ###############   INITIALIZING BOARD   #################

    """
    This function returns an array of the users custom board
    If they click the quit/X exit button, it returns 0
    """
    def runGame(self):
        run = True
        while run:
            time.delay(100)
            
            for events in event.get():
                if events.type == QUIT:
                    run = False
                    quit()
                    return 0
                if events.type == MOUSEBUTTONDOWN:
                    self.x,self.y = mouse.get_pos()
                    i = self.x//self.boxheight
                    j = self.y//self.boxwidth
                    if(self.board[j][i] == 0 or self.newboard.count([j,i]) > 0):
                        if self.count > 0:
                            draw.rect(self.screen,Color(255,255,255), newbox, 3)
                        selectorbox = Rect(0,0,self.boxheight-12, self.boxwidth-12)
                        newbox = selectorbox.move(i*self.boxwidth +6,j*self.boxheight+6)
                        draw.line(self.screen, Color(0,0,0), (147,0), (147,450), 6)
                        draw.line(self.screen, Color(0,0,0), (297,0), (297,450), 6)  
                        draw.line(self.screen, Color(0,0,0), (0,147), (450,147), 6)
                        draw.line(self.screen, Color(0,0,0), (0,297), (450,297), 6)
                        draw.rect(self.screen, Color(255,0,0), newbox, 2)
                        self.count = self.count + 1
                if events.type == KEYDOWN:
                    if events.key == K_1:
                        key = 1
                    if events.key == K_2:
                        key = 2
                    if events.key == K_3:
                        key = 3
                    if events.key == K_4:
                        key = 4
                    if events.key == K_5:
                        key = 5
                    if events.key == K_6:
                        key = 6
                    if events.key == K_7:
                        key = 7
                    if events.key == K_8:
                        key = 8
                    if events.key == K_9:
                        key = 9
                    if events.key == K_DELETE:
                        key = 0
                    if events.key == K_KP_ENTER or events.key == K_RETURN:
                        key = -1
                    i = self.x //self.boxheight
                    j = self.y//self.boxheight
                    if(validmove([i,j], key, self.board) or key == 0):
                        if(key == 0 and self.newboard.count([j,i]) > 0 ):
                            selectorbox = selectorbox.move(i*self.boxwidth + 6, j*self.boxheight +6)
                            newbox = draw.rect(self.screen, Color(255,255,255), selectorbox)
                            newbox = draw.rect(self.screen, Color(255,0,0), newbox, 2)
                            self.board[j][i] = 0
                            self.newboard.remove([j,i])
                        elif(key > 0):
                            self.board[j][i] = key
                            self.newboard.append([j,i])
                            txt = self.font.render(str(key), 1, Color(255,0,0))
                            self.screen.blit(txt, (i*self.boxheight + 17, j*self.boxwidth+8))
                    if(key == -1):
                        run = False
            if run:
                display.update()
        return self.board

"""
Returns a random board filled in with between 30-40 numbers in random locations,
all valid!
"""
def randomBoard():
    num = random.randint(30,40)
    total = 0
    board = [[0]*9 for i in range(9)]
    while total != num:
        val = random.randint(1,9)
        i = random.randint(0,8)
        j = random.randint(0,8)
        if(validmove([i,j], val, board)):
            board[j][i] = val
            total = total + 1
    return board
 
"""
This checks if a move is valid, given the number "num", the location on the board,
and the board, and returns True if the move is valid
"""
def validmove(location, num, board):
    if board[location[1]][location[0]] != 0:
        return False
    for j in range(9):
        if board[j][location[0]] == num:
            return False
    for j in range(9):
        if board[location[1]][j] == num:
            return False
    for i in range(3):
        for j in range(3):
            if board[((location[1]//3)*3)+j][((location[0]//3)*3)+i] == num:
                return False
    return True

### MAIN, WHERE THE CODE STARTS!!!!!!!! ###
game = StartupMenu()
game.runStartupMenu()
