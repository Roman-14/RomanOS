import pygame
import functions
import math
import random
import pyperclip
import assets
pygame.init()

class textInput:
    def __init__(self,x,y,w,h,type,history=[]):
        self.x=x
        self.y=y
        self.w=w
        self.h=h

        self.type = type
        self.history=history
        self.historypos=0

        self.value=""
        self.values=[self.value]
        self.textbox=pygame.Rect(self.x,self.y,self.w,self.h)
        self.font = assets.Defaultfont
        self.text = self.font.render(self.value, True, (255, 255, 255))
        self.texts=[self.text]
        self.focused=False
    def update(self,event=pygame.event,mouse=pygame.mouse):
        if event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                if functions.collidePygameRect(self.textbox,mouse):
                    self.focused=True

                else:
                    self.focused=False
        if self.focused:
            if event.type == pygame.KEYDOWN:
                if sum([text.get_rect().h for text in self.texts])+20>self.textbox.h and event.key!=pygame.K_BACKSPACE and event.key!=pygame.K_RETURN:
                    return
                if event.key==pygame.K_UP and self.type=="terminal" and len(self.history)>abs(self.historypos):
                    self.historypos-=1
                    self.values=self.history[self.historypos]
                    self.value=self.values[-1]
                    self.text=self.font.render(self.value, True, (255, 255, 255))
                    temptexts=[]
                    for value in self.values:
                        temptexts.append(self.font.render(value, True, (255, 255, 255)))
                    self.texts=temptexts
                elif event.key==pygame.K_DOWN and self.type=="terminal" and self.historypos!=-1:
                    self.historypos+=1
                    self.values=self.history[self.historypos]
                    self.value=self.values[-1]
                    self.text=self.font.render(self.value, True, (255, 255, 255))
                    temptexts=[]
                    for value in self.values:
                        temptexts.append(self.font.render(value, True, (255, 255, 255)))
                    self.texts=temptexts
                elif event.key==pygame.K_RETURN and self.type=="terminal":
                    self.historypos=0
                elif event.key==pygame.K_BACKSPACE:
                    
                    if len(self.value)==0 and len(self.values) > 1:
                        self.values.pop()
                        self.texts.pop()
                        self.value = self.values[-1]
                        self.text = self.texts[-1]
                        

                        temptexts=[]
                        for value in self.values:
                            temptexts.append(self.font.render(value, True, (255, 255, 255)))
                        self.texts=temptexts
                    self.value=self.value[:-1]

                elif event.key!=pygame.K_RETURN:
                    self.value+=event.unicode

            self.text=self.font.render(self.value, True, (255, 255, 255))
            self.values[-1]=self.value
            self.texts[-1]=self.text
            
            if self.text.get_rect().w+15>self.textbox.w:
                self.texts.append(self.text)
                self.values.append(self.value)
                self.value=""
                self.text=self.font.render(self.value, True, (255, 255, 255))
                self.values[-1]=self.value
                self.texts[-1]=self.text
            
class textInputNotepad:
    def __init__(self,x,y,w,h,file):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.scrollOffset=0
        self.cursorpos=[0,0]
        
        self.values=[""]
        self.textbox=pygame.Rect(self.x,self.y,self.w,self.h)
        self.font = assets.Defaultfont
        self.text = self.font.render(self.values[self.cursorpos[1]], True, (0, 0, 0))
        self.texts=[self.text]
        self.focused=False

        

        self.valuebeforecursor=""
        self.textbeforecursor=self.font.render(self.valuebeforecursor,True,(255,255,255))
        self.saved=True
        self.file=file


        self.open_file = open(file,"r")
        self.values=[]
        self.texts=[]
        for i in self.open_file:
            self.values.append(i.replace("\n",""))
            self.texts.append(self.font.render(i.replace("\n",""), True, (0, 0, 0)))
        
        self.open_file.close()

        if self.values==[]:
            self.values=[""]
            self.text = self.font.render(self.values[self.cursorpos[1]], True, (0, 0, 0))
            self.texts=[self.text]

        self.selecting = False
        self.startpoint= [0,0]
        self.endpoint= [0,0]

    def getTextPosFromCoord(self, x : int, y: int) -> list[int, int]:
        cursorX = cursorY = 0

        line_index = round((y - self.y - self.scrollOffset-10)/25)
        cursorY = min(len(self.values) - 1, max(0, line_index))
        if self.cursorpos[1]<0:
            cursorY = 0

        prev_dist = 1000000

        for index in range(len(self.values[cursorY]) + 1):
            text_rect = self.font.render(self.values[cursorY][:index], True, (255, 255, 255)).get_rect()

            dist = self.x + text_rect.w - x
            if dist > 0:
                if abs(prev_dist) < abs(dist):
                    cursorX = index - 1
                else:
                    cursorX = index
                
                break

            prev_dist = dist

        else:
            cursorX = len(self.values[cursorY])

        return [cursorX, cursorY]

    def getSelection(self):
        if self.startpoint[1]>self.endpoint[1] or (self.startpoint[1]==self.endpoint[1] and self.startpoint[0]>self.endpoint[0]):
            startPos = self.endpoint
            endPos = self.startpoint
        else:
            startPos = self.startpoint
            endPos = self.endpoint
        
        if startPos[1]==endPos[1]:
            return self.values[startPos[1]][startPos[0]:endPos[0]]
        else:
            body=self.values[startPos[1]][startPos[0]:]+"\n"
            for i in range(startPos[1]+1,endPos[1]):
                body+=self.values[i]+"\n"
            body+=self.values[endPos[1]][:endPos[0]]
            return body
        
    def pasteText(self, value):
        if self.selecting:
            self.removeSelection()

        beforeCursor = self.values[self.cursorpos[1]][:self.cursorpos[0]]
        afterCursor = self.values[self.cursorpos[1]][self.cursorpos[0]:]

        # Insert the pasted text at the cursor position
        self.values[self.cursorpos[1]] = beforeCursor + value + afterCursor
        self.texts[self.cursorpos[1]] = self.font.render(self.values[self.cursorpos[1]], True, (0, 0, 0))
        self.text = self.font.render(self.values[self.cursorpos[1]], True, (0, 0, 0))

        # Update cursor position and selection
        self.cursorpos[0] += len(value)
        self.endpoint = self.cursorpos
        self.selecting = False

        # Merge lines that may have been split
        temp_values = []
        temp_texts = []
        for value in self.values:
            temp_values.extend(value.split("\n"))
        self.values = temp_values

        for i in range(len(self.values)):
            temp_texts.append(self.font.render(self.values[i], True, (0, 0, 0)))
        self.texts = temp_texts

    def removeSelection(self):
        if self.startpoint[1]>self.endpoint[1] or (self.startpoint[1]==self.endpoint[1] and self.startpoint[0]>self.endpoint[0]):
            startPos = self.endpoint
            endPos = self.startpoint
        else:
            startPos = self.startpoint
            endPos = self.endpoint
        

        if endPos[1]!=startPos[1]:
            end = self.values[endPos[1]][endPos[0]:]
            beg = self.values[startPos[1]][:startPos[0]]
            self.values = self.values[:startPos[1]]+[beg+end]+self.values[endPos[1]+1:]
        else:
            self.values[endPos[1]]=self.values[endPos[1]][:startPos[0]]+self.values[endPos[1]][endPos[0]:]
        
        self.endpoint = self.startpoint = self.cursorpos = startPos
        self.texts = self.texts[:startPos[1]] + [self.font.render(self.values[startPos[1]], True, (0, 0, 0))] + self.texts[endPos[1]+1:]
    def update(self,event=pygame.event,mouse=pygame.mouse) -> None:
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if event.button==1:
                        if functions.collidePygameRect(self.textbox,mouse):
                            self.focused=True

                        else:
                            self.focused=False
                if self.focused:
                    if event.type == pygame.KEYDOWN:
                        redraw = False
                        if event.key == pygame.K_s and event.mod & pygame.KMOD_CTRL:
                            id=random.randint(1000,10000)
                            newfile=open(self.file,"w")
                            for value in self.values:
                                newfile.write(value+"\n")
                            newfile.close()
                            self.saved=True
                        elif event.key == pygame.K_c and event.mod & pygame.KMOD_CTRL:
                            pyperclip.copy(self.getSelection())
                        elif event.key == pygame.K_v and event.mod & pygame.KMOD_CTRL:
                            clipboard_content = pyperclip.paste()
                            self.pasteText(clipboard_content)

                        elif event.key == pygame.K_DOWN:
                            if self.cursorpos[1] < len(self.values) - 1:
                                self.cursorpos[1] += 1
                                redraw = True
                        elif event.key == pygame.K_UP:
                            if self.cursorpos[1] > 0:
                                self.cursorpos[1] -= 1
                                redraw = True
                        elif event.key == pygame.K_RIGHT:
                            if self.cursorpos[0] < len(self.values[self.cursorpos[1]]):
                                self.cursorpos[0] += 1
                                redraw = True
                        elif event.key == pygame.K_LEFT:
                            if self.cursorpos[0] > 0:
                                self.cursorpos[0] -= 1
                                redraw = True
                        elif event.key == pygame.K_RETURN:
                            beforeCursor = self.values[self.cursorpos[1]][:self.cursorpos[0]]
                            afterCursor = self.values[self.cursorpos[1]][self.cursorpos[0]:]
                            self.values[self.cursorpos[1]]=beforeCursor
                            self.texts[self.cursorpos[1]]=self.font.render(beforeCursor, True, (0, 0, 0))
                            self.cursorpos[1]+=1
                            self.values.insert(self.cursorpos[1],afterCursor)
                            self.texts.insert(self.cursorpos[1], self.font.render(afterCursor, True, (0, 0, 0)))
                            redraw = True
                            self.cursorpos[0]=0
                            self.saved = False
                        elif event.key == pygame.K_BACKSPACE:
                            beforeCursor = self.values[self.cursorpos[1]][:self.cursorpos[0]]
                            afterCursor = self.values[self.cursorpos[1]][self.cursorpos[0]:]
                            self.saved=False
                            if self.cursorpos[0]!=0:
                                self.values[self.cursorpos[1]]=beforeCursor[:-1]+afterCursor
                                self.texts[self.cursorpos[1]]=self.font.render(beforeCursor[:-1]+afterCursor, True, (0, 0, 0))
                                self.cursorpos[0]-=1
                            else:
                                if self.cursorpos!=[0,0]:
                                    self.valuebeforecursor=self.values[self.cursorpos[1]-1]
                                    self.values.pop(self.cursorpos[1])
                                    self.texts.pop(self.cursorpos[1])
                                    
                                    self.values[self.cursorpos[1]-1]+=afterCursor
                                    self.texts[self.cursorpos[1]-1]=self.font.render(self.values[self.cursorpos[1]-1], True, (0, 0, 0))
                                    self.cursorpos[0]=len(self.values[self.cursorpos[1]-1])-len(afterCursor)
                                    self.cursorpos[1]-=1
                                    
                            self.removeSelection()

                                   

                            redraw = True

                        elif event.key!=pygame.K_LCTRL:
                            self.saved=False
                            self.removeSelection()
                            beforeCursor = self.values[self.cursorpos[1]][:self.cursorpos[0]]
                            afterCursor = self.values[self.cursorpos[1]][self.cursorpos[0]:]
                            self.cursorpos[0]+= len(event.unicode)
                            self.values[self.cursorpos[1]] = beforeCursor + event.unicode + afterCursor
                            self.texts[self.cursorpos[1]] = self.font.render(self.values[self.cursorpos[1]], True, (0, 0, 0))
                            self.text=self.font.render(self.values[self.cursorpos[1]], True, (0, 0, 0))
                            
                            
                            
                            redraw = True

                        if redraw:
                            self.valuebeforecursor = self.values[self.cursorpos[1]][:self.cursorpos[0]]
                            self.textbeforecursor = self.font.render(
                                self.valuebeforecursor, True, (255, 255, 255))
                    if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                        self.cursorpos = self.getTextPosFromCoord(mouse[0],mouse[1])
                        self.valuebeforecursor = self.values[self.cursorpos[1]][:self.cursorpos[0]]
                        self.textbeforecursor = self.font.render(self.valuebeforecursor, True, (255, 255, 255))
                        self.startpoint = self.cursorpos
                        self.selecting = True
                        self.endpoint = self.startpoint
                    elif self.selecting and event.type == pygame.MOUSEMOTION:
                        
                        self.endpoint=self.getTextPosFromCoord(mouse[0],mouse[1])
                    elif pygame.MOUSEBUTTONUP:
                        self.selecting = False
                      