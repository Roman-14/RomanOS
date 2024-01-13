import pygame
import assets
import math
import textbox

import pygame

class Icons:
    def __init__(self,screen) -> None:
        self.type="Icons"
        self.chosenIcon = "terminal"
        self.screen = screen
        self.x=100
        self.y=100
        self.w=360
        self.h=240
        self.scrollOffset=0
        self.rect=pygame.Rect((self.x,self.y,self.w,self.h))
        self.bar=pygame.Rect(self.x,self.y,self.w,10)
        self.exitRect=pygame.Rect(self.x+self.w-8,self.y+3,5,5)
        self.iconLocs = {}
    def draw(self,screen):
        pygame.draw.rect(screen,(70,70,70),self.rect)
        pygame.draw.rect(screen,(0,0,0),self.bar)
        pygame.draw.rect(screen,(255,0,0),self.exitRect)
        column = 0
        row = 0
        self.iconLocs = {}
        for icon in assets.icons:
            if row*75 > self.w:
                column+=1
                row=0
            screen.subsurface((self.x,self.y,self.w,self.h)).blit(assets.icons[icon],(row*75,column*60+10))
            self.iconLocs[icon] = [self.x+row*75,self.y+column*60+10,assets.width/assets.iconX,assets.height/assets.iconY]
            row += 1
            
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
        self.exitRect=pygame.Rect(self.x+self.w-8,self.y+3,5,5)

        self.stdout=pygame.Rect(self.x+10,self.y+20,self.w-20,80)
        self.stdin=pygame.Rect(self.x+10,self.y+130,self.w-20,80)
        
class Shortcut:
    def __init__(self,x,y,screen) -> None:
        self.type="Shortcut"
        self.screen = screen
        self.x = x
        self.y = y

        self.locX, self.locY = (math.floor(self.x/assets.width*assets.iconX), math.floor(self.y/assets.height*assets.iconY))
        
        self.x=100
        self.y=100
        self.w=360
        self.h=360

        self.rect=pygame.Rect((self.x,self.y,self.w,self.h))
        self.bar=pygame.Rect(self.x,self.y,self.w,10)
        self.exitRect=pygame.Rect(self.x+self.w-8,self.y+3,5,5)

        self.iconMenu = None
        self.chosenIcon = "terminal"

        self.addRect = pygame.Rect(self.x+30,self.y+155,35,35)
        self.addText = pygame.font.Font(None, 60).render("+", True, (0, 0, 0))

        self.text1 = assets.Defaultfont.render("Name of shortcut:", True, (0, 0, 0))
        self.text2 = assets.Defaultfont.render("Select shortcut icon:", True, (0, 0, 0))
        self.text3 = assets.Defaultfont.render("Enter command it should run:", True, (0, 0, 0))

        self.nameRect = pygame.Rect(self.x+30,self.y+80,300,50)
        self.commandRect = pygame.Rect(self.x+30,self.y+240,300,50)

        self.nameInput = textbox.textInput(self.nameRect.x,self.nameRect.y,self.nameRect.w,self.nameRect.h,self.type,fontsize=30)
        self.commandInput = textbox.textInput(self.commandRect.x,self.commandRect.y,self.commandRect.w,self.commandRect.h,self.type,fontsize=20)

        self.submit_text = assets.Defaultfont.render("Submit", True, (0, 0, 0))
        self.submit_rect = pygame.Rect(self.x+int(self.w/2)-50,self.y+self.h-50,100,25)

    def addRectClicked(self):
        self.iconMenu=Icons(self.screen)
        assets.windows = [self.iconMenu] + assets.windows

    def draw(self,screen):
        if self.iconMenu:
            self.chosenIcon = self.iconMenu.chosenIcon
        pygame.draw.rect(screen,"#FFBE0B",self.rect)
        pygame.draw.rect(screen,(0,0,0),self.bar)
        pygame.draw.rect(screen,(255,0,0),self.exitRect)

        pygame.draw.rect(screen,(0,255,0),self.submit_rect)

        screen.blit(self.text1,(self.x+30, self.y+50))
        screen.blit(self.text2,(self.x+30, self.y+130))
        screen.blit(self.text3,(self.x+30, self.y+210))

        screen.blit(self.submit_text,(self.x+int(self.w/2)-40,self.y+self.h-50))
        
        pygame.draw.rect(screen,"#FB5607",self.nameRect)
        pygame.draw.rect(screen,"#FB5607",self.commandRect)
        pygame.draw.rect(screen,(0,255,0),self.addRect)

        screen.blit(self.addText,(self.x+35,self.y+150))

        c=0
        for text in self.nameInput.texts:
            screen.blit(text,(self.nameRect.x,self.nameRect.y+10+c))
            c+=25

        c=0
        for text in self.commandInput.texts:
            screen.blit(text,(self.commandRect.x,self.commandRect.y+10+c))
            c+=25
            
        #if self.iconMenu != None:
        #    self.iconMenu.draw(screen)
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
        self.exitRect=pygame.Rect(self.x+self.w-8,self.y+3,5,5)
        self.addRect = pygame.Rect(self.x+30,self.y+155,35,35)
        self.nameRect = pygame.Rect(self.x+30,self.y+80,300,50)
        self.commandRect = pygame.Rect(self.x+30,self.y+240,300,50)

        self.submit_rect = pygame.Rect(self.x+int(self.w/2)-50,self.y+self.h-50,100,25)

        self.nameInput.textbox=self.nameRect
        self.commandInput.textbox=self.commandRect
    def submitClicked(self):
        #check if name, icon and command is filled
        assets.tiles[(self.locX,self.locY)] = [self.nameInput.values[0],self.chosenIcon,"".join(self.commandInput.values)]
        assets.tilesOffset[(self.locX,self.locY)] = 0
        assets.windows.remove(self)
        del self