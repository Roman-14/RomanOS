import pygame

class ImageViewer:
    def __init__(self,image,screen) -> None:
        self.type="ImageViewer"
        self.screen=screen
        self.x=100
        self.y=100
        self.w=360
        self.h=240
        self.scrollOffset=0
        self.rect=pygame.Rect((self.x,self.y,self.w,self.h))
        self.bar=pygame.Rect(self.x,self.y,self.w,10)
        self.exitRect=pygame.Rect(self.x+self.w-8,self.y+3,5,5)
        self.image=image
        self.loadedImg = pygame.image.load(self.image)
        self.loadedImg = pygame.transform.scale(self.loadedImg, (self.w, self.h-10))
    def draw(self,screen):
        pygame.draw.rect(screen,(70,70,70),self.rect)
        pygame.draw.rect(screen,(0,0,0),self.bar)
        pygame.draw.rect(screen,(255,0,0),self.exitRect)
        screen.blit(self.loadedImg,(self.x,self.y+10))
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

        