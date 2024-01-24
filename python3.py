import textbox
import pygame
import subprocess
import threading
import window
import assets
import functions

class Python3(window.Window):
    def __init__(self,file,directory,screen) -> None:
        super().__init__(100, 100, 360, 240, screen, "Python3")

        self.scrollOffset=0

        self.stdout=pygame.Rect(self.x+10,self.y+20,self.w-20,80)
        self.stdin=pygame.Rect(self.x+10,self.y+130,self.w-20,80)



        self.textInput=textbox.textInput(self.stdin.x,self.stdin.y,self.stdin.w,self.stdin.h)

        self.file=file
        self.directory=directory

        self.process = subprocess.Popen(["python3", self.file], cwd=self.directory,stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        self.stdout_list = [b""]
        self.textInput.values = []

        threading.Thread(target=self.stdout_thread).start()

    def stdout_thread(self):
        while c := self.process.stdout.read(1):
            self.stdout_list[-1] += c

    def draw(self,screen):
        super().draw(screen)
        
        pygame.draw.rect(screen,(155,155,155),self.stdout)
        pygame.draw.rect(screen,(155,155,155),self.stdin)

        c=0
        try:
            for text in self.stdout_list:
                for section in text.decode().split("\n"):
                    screen.subsurface((self.stdout.x,self.stdout.y,self.stdout.w,self.stdout.h)).blit(self.textInput.font.render(section.replace("\r",""), True, (255, 255, 255)),(0,10+self.scrollOffset+c))
                    c+=25
        except AttributeError as e: 
            self.mbHeld()
        self.textInput.draw(self.x+10,self.y+130,self.w-20,80,screen)
    def onMouseMotion(self, event, mousePos) -> None:
        if self.textInput.focused:
            self.textInput.onMouseEvents(event, mousePos)
    def onMouseButtonUp(self, event, mousePos) -> None:
        self.textInput.onMouseEvents(event, mousePos)
    def mbHeld(self,mousePos):
        super().mbHeld(mousePos)
        print(self.textInput.startpoint,self.textInput.endpoint)
        self.stdout=pygame.Rect(self.x+10,self.y+20,self.w-20,80)
        self.stdin=pygame.Rect(self.x+10,self.y+130,self.w-20,80)

        self.textInput.textbox=pygame.Rect((self.stdin.x,self.stdin.y,self.stdin.w,self.stdin.h))


        
    def onReturnPressed(self):
        if self.textInput.focused:
            self.process.stdin.write(self.textInput.values[0].encode())
            self.process.stdin.write(b'\n')
            self.textInput.clearText()
            try:
                self.process.stdin.flush()
            except BrokenPipeError as e:
                pass

    def onKeyDown(self, event) -> bool:
        if self.textInput.focused:
            if event.key == pygame.K_RETURN:
                self.onReturnPressed()
            self.keyPressed(event)
            self.textInput.onKeyDown(event)
            return 1
        return 0
    def onMouseButtonDown(self, event, mousePos) -> None:
        self.textInput.onMouseEvents(event, mousePos)
    def onScrollWheel(self, event, mousePos) -> bool:
        if functions.collidePygameRect(self.rect, assets.mousePos):
            scroll_amount = event.y * 10  # Keep the original sign

            # Calculate the maximum scroll offset based on content height and window height
            max_scroll_offset = max(0, sum(text.decode().count("\n")+1 for text in self.stdout_list) * 25 - self.stdout.h)

            # Update the scroll offset within bounds
            self.scrollOffset += scroll_amount
            self.scrollOffset = min(0, max(self.scrollOffset, -max_scroll_offset))
            return 1
        return 0