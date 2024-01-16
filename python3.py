import textbox
import pygame
import subprocess
import threading
import window

class Python3(window.Window):
    def __init__(self,file,directory,screen) -> None:
        super().__init__(100, 100, 360, 240, screen, "Python3")

        self.scrollOffset=0

        self.stdout=pygame.Rect(self.x+10,self.y+20,self.w-20,80)
        self.stdin=pygame.Rect(self.x+10,self.y+130,self.w-20,80)



        self.textInput=textbox.textInput(self.stdin.x,self.stdin.y,self.stdin.w,self.stdin.h,self.type)

        self.file=file
        self.directory=directory

        self.process = subprocess.Popen(["python3", self.file], cwd=self.directory,stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        self.stdout_list = [b""]
        self.stdin_list = []

        threading.Thread(target=self.stdout_thread).start()

    def stdout_thread(self):
        while c := self.process.stdout.read(1):
            self.stdout_list[-1] += c

    def draw(self,screen):
        super().draw(screen)
        pygame.draw.rect(screen,(155,155,155),self.stdout)
        pygame.draw.rect(screen,(155,155,155),self.stdin)

        c=0
        for text in self.textInput.texts:
            screen.blit(text,(self.stdin.x,self.stdin.y+10+c))
            c+=25

        c=0
        try:
            for text in self.stdout_list:
                for section in text.decode().split("\n"):
                    screen.subsurface((self.stdout.x,self.stdout.y,self.stdout.w,self.stdout.h)).blit(self.textInput.font.render(section.replace("\r",""), True, (255, 255, 255)),(0,10+self.scrollOffset+c))
                    c+=25
        except AttributeError as e: 
            self.mbHeld()
    def mbHeld(self,mousePos):
        super().mbHeld(mousePos)

        self.stdout=pygame.Rect(self.x+10,self.y+20,self.w-20,80)
        self.stdin=pygame.Rect(self.x+10,self.y+130,self.w-20,80)

        self.textInput.textbox=pygame.Rect((self.stdin.x,self.stdin.y,self.stdin.w,self.stdin.h))

    def keyPressed(self,event):
        if event.key != pygame.K_BACKSPACE:
            self.stdin_list += event.unicode
            #self.process.stdin.write(event.unicode.encode())

        else:
            self.stdin_list=self.stdin_list[:-1]
        
    def returnPressed(self):
        self.textInput.value=""
        self.textInput.values=[""]
        self.textInput.text = self.textInput.font.render(self.textInput.value, True, (255, 255, 255))
        self.textInput.texts=[self.textInput.text]
        for i in self.stdin_list:
            self.process.stdin.write(i.encode())
        self.process.stdin.write(b'\n')
        self.stdin_list = []
        try:
            self.process.stdin.flush()
        except BrokenPipeError as e:
            pass