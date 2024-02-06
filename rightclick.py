import pygame
import assets
import functions
import shortcut
import terminal
import math

invisterminal = terminal.Terminal(assets.screen)
rightClickBox = None

def onRightClick(event, mousePos, rightClickBox):
    for window in assets.windows:
        if functions.collidePygameRect(window.rect,mousePos):
            break
    else:
        if event.button == assets.rightClickCode:
            locX,locY = (math.floor(mousePos[0]/assets.width*assets.iconX),math.floor(mousePos[1]/assets.height*assets.iconY))
            if (locX,locY) not in assets.tiles:
                rightClickBox = RightClickBox(x=mousePos[0],y=mousePos[1],clicked="empty slot",screen=assets.screen)
            else:
                rightClickBox = RightClickBox(x=mousePos[0],y=mousePos[1],clicked="filled slot",screen=assets.screen)
        elif event.button == assets.leftClickCode:
            for tile in assets.tiles:
                if functions.collidePygameRect(pygame.Rect(tile[0]*assets.width/assets.iconX,tile[1]*assets.height/assets.iconY,assets.width/assets.iconX, assets.height/assets.iconY),mousePos):
                    invisterminal.command(values=[],autostart=assets.tiles[tile][2])
    if event.button == assets.leftClickCode:
        if rightClickBox != None:
            rightClickBox.update(mousePos)
        rightClickBox=None
    return rightClickBox
class RightClickBox:
    def __init__(self,x,y,clicked,screen) -> None:
        self.screen = screen
        self.x=x
        self.y=y

        self.minifont = pygame.font.Font(None, 25)
        self.options = {}
        if clicked=="empty slot":
            self.options["Create Shortcut"] = self.minifont.render("Create Shortcut", True, (0, 0, 0))
            self.options["Open Terminal"] = self.minifont.render("Open Terminal", True, (0, 0, 0))
        if clicked=="filled slot":
            self.options["Delete Shortcut"] = self.minifont.render("Delete Shortcut", True, (0, 0, 0))
            self.options["Open Terminal"] = self.minifont.render("Open Terminal", True, (0, 0, 0))
    def draw(self,screen):
        height_decrement = 0
        for i in self.options:
            pygame.draw.rect(screen, (240,240,240), pygame.Rect(self.x,self.y+height_decrement,150,25))
            screen.blit(self.options[i],(self.x,self.y+height_decrement+5))
            height_decrement+=25
    def update(self,mousePos):
        height_decrement = 0
        for i in self.options:
            if functions.collidePygameRect(pygame.Rect(self.x,self.y+height_decrement,150,25),mousePos):
                if i == "Create Shortcut":
                    assets.windows.append(shortcut.Shortcut(self.x,self.y,self.screen))
                elif i == "Open Terminal":
                    assets.windows.append(terminal.Terminal(self.screen))
                elif i == "Delete Shortcut":
                    locX, locY = (math.floor(self.x/assets.width*assets.iconX), math.floor(self.y/assets.height*assets.iconY))
                    del assets.tiles[(locX,locY)]
                break
            height_decrement+=25