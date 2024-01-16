import pygame

class Window:
    
    def __init__(self, x, y, w, h, screen, type, colour = (70,70,70)) -> None:
        self.type = type
        self.screen = screen
        self.colour = colour
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect=pygame.Rect((self.x,self.y,self.w,self.h))
        self.bar=pygame.Rect(self.x,self.y,self.w,10)
        self.exitRect=pygame.Rect(self.x+self.w-8,self.y+3,5,5)
        
    def draw(self,screen) -> None:
        pygame.draw.rect(screen,self.colour,self.rect)
        pygame.draw.rect(screen,(0,0,0),self.bar)
        pygame.draw.rect(screen,(255,0,0),self.exitRect)
    
    def onMouseButtonDown(self) -> None:
        pass

    def onRightClickDown(self) -> None:
        pass

    def onLeftClickDown(self) -> None:
        pass

    def onScrollWheel(self) -> None:
        pass

    def onKeyDown(self) -> None:
        pass

    def mbHeld(self, mousePos) -> None:
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