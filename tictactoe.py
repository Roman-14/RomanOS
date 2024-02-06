import pygame
import functions
import random
import assets
import window

class TicTacToeAI:
    def __init__(self):
        self.board = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]
        
    def is_winner(self, player):
        for row in self.board:
            if row[0] == row[1] == row[2] == player:
                return True
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] == player:
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            return True
        return False
    
    def is_board_full(self):
        for row in self.board:
            for cell in row:
                if cell == ' ':
                    return False
        return True
    
    def get_available_moves(self):
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    moves.append((i, j))
        return moves
    
    def minimax(self, depth, maximizing):
        if self.is_winner('O'):
            return 10 - depth
        if self.is_winner('X'):
            return depth - 10
        if self.is_board_full():
            return 0
        
        if maximizing:
            max_eval = float('-inf')
            for i, j in self.get_available_moves():
                self.board[i][j] = 'O'
                eval = self.minimax(depth + 1, False)
                self.board[i][j] = ' '  # Undo move
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for i, j in self.get_available_moves():
                self.board[i][j] = 'X'
                eval = self.minimax(depth + 1, True)
                self.board[i][j] = ' '  # Undo move
                min_eval = min(min_eval, eval)
            return min_eval
    
    def best_move(self):
        max_eval = float('-inf')
        move = None
        for i, j in self.get_available_moves():
            self.board[i][j] = 'O'
            eval = self.minimax(0, False)
            self.board[i][j] = ' '  # Undo move
            if eval > max_eval:
                max_eval = eval
                move = (i, j)
        return move


class TicTacToe(window.Window):
    def __init__(self,screen,x=100,y=100) -> None:
        super().__init__(x, y, 360, 240, screen, "TicTacToe", (20, 189, 172))

        self.font = assets.Defaultfont

        self.tictactoe = self.font.render("Tic Tac Toe", True, (0, 0, 0))
        self.easy = self.font.render("Easy", True, (0, 0, 0))
        self.medium = self.font.render("Medium", True, (0, 0, 0))
        self.hard = self.font.render("Hard", True, (0, 0, 0))

        self.easyrect = pygame.Rect(self.x+self.w*0.5-50,self.y+self.h*0.3-20,100,40)
        self.mediumrect = pygame.Rect(self.x+self.w*0.5-50,self.y+self.h*0.5-20,100,40)
        self.hardrect =  pygame.Rect(self.x+self.w*0.5-50,self.y+self.h*0.7-20,100,40)
        self.phase = 1


        self.a1=pygame.Rect((self.x+95,self.y+40,50,45))
        self.b1=pygame.Rect((self.x+95+50+10,self.y+40,55,45))
        self.c1=pygame.Rect((self.x+95+50+10+55+10,self.y+40,50,45))
        
        self.a2=pygame.Rect((self.x+95,self.y+40+10+45,50,55))
        self.b2=pygame.Rect((self.x+95+50+10,self.y+40+10+45,55,55))
        self.c2=pygame.Rect((self.x+95+50+10+55+10,self.y+40+10+45,50,55))

        self.a3=pygame.Rect((self.x+95,self.y+40+10+45+55+10,50,50))
        self.b3=pygame.Rect((self.x+95+50+10,self.y+40+10+45+55+10,55,50))
        self.c3=pygame.Rect((self.x+95+60+60+5,self.y+40+10+45+55+10,50,50))

        self.difficulty=None
    
        self.blityouwin=False
        self.blityoulose=False
        self.blitdraw=False

        self.youwin=self.font.render("You win!", True, (13, 161, 146))
        self.youlose=self.font.render("You lose...", True, (13, 161, 146))
        self.drawtext=self.font.render("Draw", True, (13, 161, 146))

        self.game = TicTacToeAI()   

    def drawStart(self,screen) -> None:
        pygame.draw.rect(screen,(13, 161, 146),self.easyrect)
        pygame.draw.rect(screen,(13, 161, 146),self.mediumrect)
        pygame.draw.rect(screen,(13, 161, 146),self.hardrect)
        screen.blit(self.tictactoe,(self.x+self.w*0.5-60,self.y+self.h*0.15-20,100,40))
        screen.blit(self.easy, (self.x+self.w*0.5-27,self.y+self.h*0.3-10))
        screen.blit(self.medium, (self.x+self.w*0.5-42,self.y+self.h*0.5-10))
        screen.blit(self.hard, (self.x+self.w*0.5-27,self.y+self.h*0.7-10))

    def drawX(self,screen,x,y) -> None:
        pygame.draw.line(screen, (13,161,146),(x-20,y-20),(x+20,y+20),5)
        pygame.draw.line(screen, (13,161,146),(x-20,y+20),(x+20,y-20),5)
    def drawO(self,screen,x,y) -> None:
        pygame.draw.circle(screen,(13,161,146),(x,y),20,5)

    def drawGrid(self,screen):
        pygame.draw.line(screen, (13,161,146),(self.x+150,self.y+40),(self.x+150,self.y+210),7)
        pygame.draw.line(screen, (13,161,146),(self.x+215,self.y+40),(self.x+215,self.y+210),7)

        pygame.draw.line(screen, (13,161,146),(self.x+95,self.y+90),(self.x+270,self.y+90),7)
        pygame.draw.line(screen, (13,161,146),(self.x+95,self.y+155),(self.x+270,self.y+155),7)



        if self.game.board[0][0]=="X":
            self.drawX(screen,self.x+120,self.y+65)
        if self.game.board[0][1]=="X":
            self.drawX(screen,self.x+180,self.y+65)
        if self.game.board[0][2]=="X":
            self.drawX(screen,self.x+240,self.y+65)
        if self.game.board[1][0]=="X":
            self.drawX(screen,self.x+120,self.y+125)
        if self.game.board[1][1]=="X":
            self.drawX(screen,self.x+180,self.y+125)
        if self.game.board[1][2]=="X":
            self.drawX(screen,self.x+240,self.y+125)
        if self.game.board[2][0]=="X":
            self.drawX(screen,self.x+120,self.y+185)
        if self.game.board[2][1]=="X":
            self.drawX(screen,self.x+180,self.y+185)
        if self.game.board[2][2]=="X":
            self.drawX(screen,self.x+240,self.y+185)

        if self.game.board[0][0]=="O":
            self.drawO(screen,self.x+120,self.y+65)
        if self.game.board[0][1]=="O":
            self.drawO(screen,self.x+180,self.y+65)
        if self.game.board[0][2]=="O":
            self.drawO(screen,self.x+240,self.y+65)
        if self.game.board[1][0]=="O":
            self.drawO(screen,self.x+120,self.y+125)
        if self.game.board[1][1]=="O":
            self.drawO(screen,self.x+180,self.y+125)
        if self.game.board[1][2]=="O":
            self.drawO(screen,self.x+240,self.y+125)
        if self.game.board[2][0]=="O":
            self.drawO(screen,self.x+120,self.y+185)
        if self.game.board[2][1]=="O":
            self.drawO(screen,self.x+180,self.y+185)
        if self.game.board[2][2]=="O":
            self.drawO(screen,self.x+240,self.y+185)
    def draw(self,screen) -> None:
        super().draw(screen)
        if self.phase==1:
            self.drawStart(screen)
        elif self.phase==2:
            self.drawGrid(screen)
            if self.game.is_winner("X"):
                self.blityouwin=True

            
            elif self.game.is_winner("O"):
                self.blityoulose=True
        
            elif self.game.is_board_full():
                self.blitdraw=True

            if self.blityouwin:
                screen.blit(self.youwin,(self.x+self.w/2-40,self.y+self.h-30))
            elif self.blityoulose:
                screen.blit(self.youlose,(self.x+self.w/2-45,self.y+self.h-30))
            elif self.blitdraw:
                screen.blit(self.drawtext,(self.x+self.w/2-20,self.y+self.h-30))
    def mbHeld(self,mousePos):
        super().mbHeld(mousePos)
        self.easyrect = pygame.Rect(self.x+self.w*0.5-50,self.y+self.h*0.3-20,100,40)
        self.mediumrect = pygame.Rect(self.x+self.w*0.5-50,self.y+self.h*0.5-20,100,40)
        self.hardrect =  pygame.Rect(self.x+self.w*0.5-50,self.y+self.h*0.7-20,100,40)

        self.a1=pygame.Rect((self.x+95,self.y+40,50,45))
        self.b1=pygame.Rect((self.x+95+50+10,self.y+40,55,45))
        self.c1=pygame.Rect((self.x+95+50+10+55+10,self.y+40,50,45))
        
        self.a2=pygame.Rect((self.x+95,self.y+40+10+45,50,55))
        self.b2=pygame.Rect((self.x+95+50+10,self.y+40+10+45,55,55))
        self.c2=pygame.Rect((self.x+95+50+10+55+10,self.y+40+10+45,50,55))

        self.a3=pygame.Rect((self.x+95,self.y+40+10+45+55+10,50,50))
        self.b3=pygame.Rect((self.x+95+50+10,self.y+40+10+45+55+10,55,50))
        self.c3=pygame.Rect((self.x+95+60+60+5,self.y+40+10+45+55+10,50,50))

    def doNextMove(self):
        if not (self.blitdraw or self.blityoulose or self.blityouwin):
            if self.difficulty=="hard":
                if random.randint(1,10)==7:
                    i,j=self.game.get_available_moves()[random.randint(0,len(self.game.get_available_moves())-1)]
                    self.game.board[i][j] = 'O'
                else:
                    i,j=self.game.best_move()
                    self.game.board[i][j] = 'O'
            elif self.difficulty=="medium":
                if random.randint(1,2)==1:
                    i,j=self.game.get_available_moves()[random.randint(0,len(self.game.get_available_moves())-1)]
                    self.game.board[i][j] = 'O'
                else:
                    i,j=self.game.best_move()
                    self.game.board[i][j] = 'O'
            elif self.difficulty=="easy":
                if random.randint(1,3)==1:
                    i,j=self.game.best_move()
                    self.game.board[i][j] = 'O'
                else:
                    i,j=self.game.get_available_moves()[random.randint(0,len(self.game.get_available_moves())-1)]
                    self.game.board[i][j] = "O"

    def update(self,mousePos):
          
        if self.phase == 2 and self.game.is_board_full()==False:
            
            try:
                if self.game.board[0][0] == " " and functions.collidePygameRect(self.a1,mousePos):
                    self.game.board[0][0]="X"
                    if not self.game.is_winner("X"):
                        self.doNextMove()
                elif self.game.board[0][1] == " " and functions.collidePygameRect(self.b1,mousePos):
                    self.game.board[0][1]="X"
                    if not self.game.is_winner("X"):
                        self.doNextMove()
                elif self.game.board[0][2] == " " and functions.collidePygameRect(self.c1,mousePos):
                    self.game.board[0][2]="X"
                    if not self.game.is_winner("X"):
                        self.doNextMove()
                elif self.game.board[1][0] == " " and functions.collidePygameRect(self.a2,mousePos):
                    self.game.board[1][0]="X"
                    if not self.game.is_winner("X"):
                        self.doNextMove()
                elif self.game.board[1][1] == " " and functions.collidePygameRect(self.b2,mousePos):
                    self.game.board[1][1]="X"
                    if not self.game.is_winner("X"):
                        self.doNextMove()
                elif self.game.board[1][2] == " " and functions.collidePygameRect(self.c2,mousePos):
                    self.game.board[1][2]="X"
                    if not self.game.is_winner("X"):
                        self.doNextMove()
                elif self.game.board[2][0] == " " and functions.collidePygameRect(self.a3,mousePos):
                    self.game.board[2][0]="X"
                    if not self.game.is_winner("X"):
                        self.doNextMove()
                elif self.game.board[2][1] == " " and functions.collidePygameRect(self.b3,mousePos):
                    self.game.board[2][1]="X"
                    if not self.game.is_winner("X"):
                        self.doNextMove()
                elif self.game.board[2][2] == " " and functions.collidePygameRect(self.c3,mousePos):
                    self.game.board[2][2]="X"
                    if not self.game.is_winner("X"):
                        self.doNextMove()
            except:
                print("Exception occured in tic tac toe")
                pass

        if self.phase == 1:
            if functions.collidePygameRect(self.easyrect,mousePos):
                self.phase=2
                self.difficulty = "easy"
            if functions.collidePygameRect(self.mediumrect,mousePos):
                self.phase=2
                self.difficulty = "medium"
            if functions.collidePygameRect(self.hardrect,mousePos):
                self.phase=2
                self.difficulty = "hard"
        
        if (self.blityouwin or self.blitdraw or self.blityoulose) and functions.collidePygameRect(self.rect, mousePos):
            self.__init__(self.screen, self.x, self.y)
    
    def onMouseButtonDown(self, event, mousePos) -> None:
        self.update(mousePos)
        return functions.collidePygameRect(self.rect, mousePos)