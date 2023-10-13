import textbox
import pygame
import assets
class TextEditor:
    def __init__(self,file,screen) -> None:
        self.screen=screen
        self.x=100
        self.y=100
        self.w=300
        self.h=200
        self.file=file
        self.rect=pygame.Rect(self.x,self.y,self.w,self.h)
        self.bar=pygame.Rect(self.x,self.y,self.w,10)
        self.exitRect=pygame.Rect(self.x+self.w-8,self.y+3,5,5)
        self.resizeRect=pygame.Rect(self.x+self.w-10,self.y+self.h-10,5,5)
        self.textInput=textbox.textInputNotepad(self.x,self.y,self.w,self.h,self.file)
        self.type="TextEditor"
        self.font = assets.Defaultfont
        
    def draw(self,screen):
        pygame.draw.rect(screen,(255,255,255),self.rect)

        if self.textInput.startpoint[1]>self.textInput.endpoint[1] or (self.textInput.startpoint[1]==self.textInput.endpoint[1] and self.textInput.startpoint[0]>self.textInput.endpoint[0]):
            startPos = self.textInput.endpoint
            endPos = self.textInput.startpoint
        else:
            startPos = self.textInput.startpoint
            endPos = self.textInput.endpoint
        
        if startPos[1]==endPos[1]:
            selectPos = self.font.render(self.textInput.values[startPos[1]][startPos[0]:endPos[0]],True,(255,255,255)).get_rect()

            acquireX = self.font.render(self.textInput.values[startPos[1]][:startPos[0]],True,(255,255,255)).get_rect()

            pygame.draw.rect(screen.subsurface((self.x,self.y,self.w,self.h)),(200,200,255),pygame.Rect(acquireX.w,25*startPos[1]+10+self.textInput.scrollOffset,selectPos.w,25))
            
        else:
            selectPos = self.font.render(self.textInput.values[startPos[1]][startPos[0]:],True,(255,255,255)).get_rect()

            acquireX = self.font.render(self.textInput.values[startPos[1]][:startPos[0]],True,(255,255,255)).get_rect()

            pygame.draw.rect(screen.subsurface((self.x,self.y,self.w,self.h)),(200,200,255),pygame.Rect(acquireX.w,25*startPos[1]+10+self.textInput.scrollOffset,selectPos.w,25))
            for i in range(startPos[1]+1,endPos[1]):
                selectPos = self.textInput.texts[i].get_rect()
                pygame.draw.rect(screen.subsurface((self.x,self.y,self.w,self.h)),(200,200,255),pygame.Rect(0,25*i+10+self.textInput.scrollOffset,selectPos.w,25))
            
            selectPos = self.font.render(self.textInput.values[endPos[1]][:endPos[0]],True,(255,255,255)).get_rect()
            pygame.draw.rect(screen.subsurface((self.x,self.y,self.w,self.h)),(200,200,255),pygame.Rect(0,25*endPos[1]+10+self.textInput.scrollOffset,selectPos.w,25))
        
        pygame.draw.rect(screen,(0,0,0),self.bar)
        pygame.draw.rect(screen,(255,0,0),self.exitRect)
        
        try:
            c=0
            for text in self.textInput.texts:

                screen.subsurface((self.x,self.y+10,self.w,self.h-10)).blit(text,(0,c+self.textInput.scrollOffset))
                #screen.blit(text,(self.x,self.y+10+c))
                c+=25

            pygame.draw.rect(screen.subsurface(self.rect),(0,0,0),pygame.Rect(self.textInput.textbeforecursor.get_rect().w,self.textInput.scrollOffset+10+25*(self.textInput.cursorpos[1]),2,self.textInput.textbeforecursor.get_rect().h))
        except:
            self.screen=screen
            self.mbHeld((100,100))

        if not self.textInput.saved:
            pygame.draw.circle(screen,(255,255,255),(self.x+4,self.y+4),3)
        pygame.draw.rect(screen,(0,255,0),self.resizeRect)
    def mbHeld(self,mousePos):
        self.x=mousePos[0]
        self.y=mousePos[1]

        
        if (self.x+self.w)>=self.screen.get_rect().w:
            self.x=self.screen.get_rect().w-self.w
        elif self.x<=0:
            self.x=0
        if (self.y+self.h)>=self.screen.get_rect().h:
            self.y=self.screen.get_rect().h-self.h
        elif self.y<=0:
            self.y=0
        
        self.rect=pygame.Rect(self.x,self.y,self.w,self.h)
        self.bar=pygame.Rect(self.x,self.y,self.w,10)
        self.textInput.textbox=pygame.Rect(self.x,self.y,self.w,self.h)
        self.exitRect=pygame.Rect(self.x+self.w-8,self.y+3,5,5)
        self.resizeRect=pygame.Rect(self.x+self.w-10,self.y+self.h-10,5,5)
        self.textInput.x = mousePos[0]
        self.textInput.y = mousePos[1]
    
    def resizeHeld(self,mousePos):
        self.w = mousePos[0]-self.x+7
        self.h = mousePos[1]-self.y+7

        while (self.x+self.w)>=self.screen.get_rect().w:
            self.w-=1

        while (self.y+self.h)>=self.screen.get_rect().h:
            self.h-=1

        while self.w<300:
            self.w+=1
        
        while self.h<200:
            self.h+=1

        self.rect=pygame.Rect(self.x,self.y,self.w,self.h)
        self.bar=pygame.Rect(self.x,self.y,self.w,10)
        self.textInput.textbox=pygame.Rect(self.x,self.y,self.w,self.h)
        self.exitRect=pygame.Rect(self.x+self.w-8,self.y+3,5,5)
        self.resizeRect=pygame.Rect(self.x+self.w-10,self.y+self.h-10,5,5)

        self.textInput.w = mousePos[0]-self.x+7
        self.textInput.h = mousePos[1]-self.y+7