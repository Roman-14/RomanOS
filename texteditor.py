import textbox
import pygame
import assets
import window
import functions
import random
class TextEditor(window.Window):
    def __init__(self,file,screen) -> None:
        super().__init__(100, 100, 300, 200, screen, "TextEditor", (255, 255, 255))
        with open(file, "r") as text_file:
            lines = [i for i in text_file]
        self.file=file
        self.resizeRect=pygame.Rect(self.x+self.w-10,self.y+self.h-10,5,5)
        self.textInput=textbox.textInput(self.x,self.y,self.w,self.h,lines=lines, textColour=(0, 0, 0))
        self.font = assets.Defaultfont
        self.saved = True

    def draw(self,screen):
        super().draw(screen)
        self.textInput.draw(self.x,self.y,self.w,self.h,screen)

        if not self.saved:
            pygame.draw.circle(screen,(255,255,255),(self.x+4,self.y+4),3)
        pygame.draw.rect(screen,(0,255,0),self.resizeRect)
        
    def mbHeld(self,mousePos):
        super().mbHeld(mousePos)
        self.textInput.textbox=pygame.Rect(self.x,self.y,self.w,self.h)
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
    
    def onKeyDown(self, event) -> bool:
        if self.textInput.focused:
            if self.textInput.onKeyDown(event):
                self.saved = False
            if event.key == pygame.K_s and event.mod & pygame.KMOD_CTRL:
                newfile=open(self.file,"w")
                for value in self.textInput.values:
                    newfile.write(value+"\n")
                newfile.close()
                self.saved=True
            return 1
        return 0
    def onMouseMotion(self, event, mousePos) -> None:
        if self.textInput.focused:
            self.textInput.onMouseEvents(event, mousePos)
    def onMouseButtonUp(self, event, mousePos) -> None:
        self.textInput.onMouseEvents(event, mousePos)
    def onMouseButtonDown(self, event, mousePos) -> bool:
        self.textInput.onMouseEvents(event, mousePos)
        return functions.collidePygameRect(self.rect, assets.mousePos)
    def onScrollWheel(self, event, mousePos) -> bool:
        if functions.collidePygameRect(self.rect, assets.mousePos):
            scroll_amount = event.y * 10  # Keep the original sign

            # Calculate the maximum scroll offset based on content height and window height
            max_scroll_offset = max(0, len(self.textInput.values) * 25 - self.h + 10)

            # Update the scroll offset within bounds
            self.textInput.scrollOffset += scroll_amount
            self.textInput.scrollOffset = min(0, max(self.textInput.scrollOffset, -max_scroll_offset))
            return 1
        return 0
    def onResizeRectHeld(self, mousePos) -> bool:
        if functions.collidePygameRect(self.resizeRect, mousePos):
            assets.clicked_window = self
            assets.heldresize = [True, self]
            return 1
        return 0