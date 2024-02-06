import pygame
import functions
import math
import random
import pyperclip
import assets
import bisect

pygame.init()

class textInput:
    def __init__(self,x,y,w,h, lines = None, textColour = (255, 255, 255),fontsize = 32):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.rect = pygame.Rect(self.x,self.y,self.w,self.h)
        self.scrollOffset=0
        self.cursorpos=[0,0]
        
        self.values=[""]
        self.textbox=pygame.Rect(self.x,self.y,self.w,self.h)
        self.textColour = textColour
        self.font = pygame.font.Font(None, fontsize)
        self.text = self.font.render(self.values[self.cursorpos[1]], True, self.textColour)
        self.texts=[self.text]
        self.focused=False
        

        self.valuebeforecursor=""
        self.textbeforecursor=self.font.render(self.valuebeforecursor,True,self.textColour)
        self.saved=True

        self.values=[]
        self.texts=[]
        if lines != None:
            for i in lines:
                self.values.append(i.replace("\n",""))
                self.texts.append(self.font.render(i.replace("\n",""), True, self.textColour))

        if self.values==[]:
            self.values=[""]
            self.text = self.font.render(self.values[self.cursorpos[1]], True, self.textColour)
            self.texts=[self.text]

        self.selecting = False
        self.startpoint= [0,0]
        self.endpoint= [0,0]

    def splitCoordsToNormal(self, cursorX, cursorY):
        y = 0
        buildup = ""
        for i in range(cursorY):
            buildup += self.split_values[i]
            if len(buildup) >= len(self.values[y]):
                buildup = ""
                y += 1

        x = len(buildup) + cursorX
        return [x, y]
    
    def normalCoordsToSplit(self, normalX, normalY):
        y = 0
        splitY = 0
        splitX = 0
        buildup = ""
        for i, value in enumerate(self.split_values):
            buildup += value
            if y == normalY:
                if len(buildup) >= normalX:
                    splitX = + normalX - len(buildup) + len(value) 
                    splitY = i
                    break
        
            elif len(buildup) >= len(self.values[y]):
                buildup = ""
                y += 1

        return [splitX, splitY]
    
    def getTextPosFromCoord(self, x : int, y: int) -> list[int, int]:
        cursorX = cursorY = 0

        line_index = round((y - self.y - self.scrollOffset-10)/25)
        cursorY = min(len(self.split_values) - 1, max(0, line_index))
        if self.cursorpos[1]<0:
            cursorY = 0

        prev_dist = 1000000

        for index in range(len(self.split_values[cursorY]) + 1):
            text_rect = self.font.render(self.split_values[cursorY][:index], True, self.textColour).get_rect()

            dist = self.x + text_rect.w - x
            if dist > 0:
                if abs(prev_dist) < abs(dist):
                    cursorX = index - 1
                else:
                    cursorX = index
                
                break

            prev_dist = dist

        else:
            cursorX = len(self.split_values[cursorY])

        y = 0
        buildup = ""
        for i in range(cursorY):
            buildup += self.split_values[i]
            if len(buildup) >= len(self.values[y]):
                buildup = ""
                y += 1

        x = len(buildup) + cursorX
        return [x, y]
    
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
        self.texts[self.cursorpos[1]] = self.font.render(self.values[self.cursorpos[1]], True, self.textColour)
        self.text = self.font.render(self.values[self.cursorpos[1]], True, self.textColour)

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
            temp_texts.append(self.font.render(self.values[i], True, self.textColour))
        self.texts = temp_texts
    def clearText(self):
        self.startpoint=[0,0]
        self.endpoint=[0,0]
        self.values=[""]
        if self.cursorpos[1] > len(self.values) - 1:
            self.cursorpos[1] = len(self.values) - 1
        if self.cursorpos[0] > len(self.values[self.cursorpos[1]]):
            self.cursorpos[0] = len(self.values[self.cursorpos[1]])
        self.text = self.font.render(self.values[self.cursorpos[1]], True, self.textColour)
        self.texts=[self.text]
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
        self.texts = self.texts[:startPos[1]] + [self.font.render(self.values[startPos[1]], True, self.textColour)] + self.texts[endPos[1]+1:]

    def onMouseEvents(self,event,mousePos):
        if event.type==pygame.MOUSEBUTTONDOWN:
            if not functions.collidePygameRect(self.rect, mousePos):
                return
            if event.button==1:
                if functions.collidePygameRect(self.textbox,mousePos):
                    self.focused=True

                else:
                    self.focused=False
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            self.cursorpos = self.getTextPosFromCoord(mousePos[0],mousePos[1])
            self.valuebeforecursor = self.values[self.cursorpos[1]][:self.cursorpos[0]]
            self.textbeforecursor = self.font.render(self.valuebeforecursor, True, self.textColour)
            self.startpoint = self.cursorpos
            self.selecting = True
            self.endpoint = self.startpoint
        elif self.selecting and event.type == pygame.MOUSEMOTION:
            self.endpoint=self.getTextPosFromCoord(mousePos[0],mousePos[1])

        elif pygame.MOUSEBUTTONUP:
            self.selecting = False
    
    def draw(self, x, y, w, h, screen):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        self.split_values = []
        self.split_texts = []
        split_textbeforecursor = self.textbeforecursor
        split_cursorpos = self.cursorpos[:]
        split_startpos = self.startpoint[:]
        split_endpos = self.endpoint[:]
        for y, (line, text) in enumerate(zip(self.values, self.texts)):
            if text.get_rect().w > self.w:
                last_index = 0
                while last_index < len(line):
                    i = bisect.bisect(range(len(line)), self.w, lo=last_index, key=lambda i: self.font.size(line[last_index:i])[0])
                    self.split_values += [line[last_index:i]]
                    self.split_texts += [self.font.render(line[last_index:i],True,self.textColour)]

                    if self.cursorpos[1] == y and last_index <= self.cursorpos[0] <= i:
                        split_cursorpos = [self.cursorpos[0] - last_index, len(self.split_values)-1]
                        split_textbeforecursor = self.font.render(line[last_index:last_index + split_cursorpos[0]],True,self.textColour)
                    if self.startpoint[1] == y and last_index <= self.startpoint[0] < i:
                        split_startpos = [self.startpoint[0] - last_index, len(self.split_values)-1]
                    if self.endpoint[1] == y and last_index <= self.endpoint[0] < i:
                        split_endpos = [self.endpoint[0] - last_index, len(self.split_values)-1]

                    last_index = i

            else:
                self.split_values += [line]
                self.split_texts += [text]

                if self.cursorpos[1] == y:
                    split_cursorpos[1] = len(self.split_values)-1
                if self.startpoint[1] == y:
                    split_startpos[1] = len(self.split_values)-1
                if self.endpoint[1] == y:
                    split_endpos[1] = len(self.split_values)-1
        
        if split_startpos[1]>split_endpos[1] or (split_startpos[1]==split_endpos[1] and split_startpos[0]>split_endpos[0]):
            startPos = split_endpos
            endPos = split_startpos
        else:
            startPos = split_startpos
            endPos = split_endpos
        

        if startPos[1]==endPos[1]:
            selectPos = self.font.size(self.split_values[startPos[1]][startPos[0]:endPos[0]])
            acquireX = self.font.size(self.split_values[startPos[1]][:startPos[0]])

            pygame.draw.rect(screen.subsurface((self.x,self.y,self.w,self.h)),(200,200,255),pygame.Rect(acquireX[0],25*startPos[1]+10+self.scrollOffset,selectPos[0],25))
            
        else:
            selectPos = self.font.size(self.split_values[startPos[1]][startPos[0]:])
            acquireX = self.font.size(self.split_values[startPos[1]][:startPos[0]])

            pygame.draw.rect(screen.subsurface((self.x,self.y,self.w,self.h)),(200,200,255),pygame.Rect(acquireX[0],25*startPos[1]+10+self.scrollOffset,selectPos[0],25))
            for i in range(startPos[1]+1,endPos[1]):
                selectPos = self.split_texts[i].get_rect()
                pygame.draw.rect(screen.subsurface((self.x,self.y,self.w,self.h)),(200,200,255),pygame.Rect(0,25*i+10+self.scrollOffset,selectPos.w,25)) 
            selectPos = self.font.size(self.split_values[endPos[1]][:endPos[0]])
            pygame.draw.rect(screen.subsurface((self.x,self.y,self.w,self.h)),(200,200,255),pygame.Rect(0,25*endPos[1]+10+self.scrollOffset,selectPos[0],25))
        
        

        c=0
        for text in self.split_texts:

            screen.subsurface((self.x,self.y+10,self.w,self.h-10)).blit(text,(0,c+self.scrollOffset))
            #screen.blit(text,(self.x,self.y+10+c))
            c+=25

        pygame.draw.rect(screen.subsurface(self.rect),(0,0,0),pygame.Rect(split_textbeforecursor.get_rect().w,self.scrollOffset+10+25*(split_cursorpos[1]),2,split_textbeforecursor.get_rect().h))
    
    def onKeyDown(self, event) -> bool:
                hasChanged = False
                if self.focused:
                    if event.type == pygame.KEYDOWN:
                        redraw = False
                        if event.key == pygame.K_s and event.mod & pygame.KMOD_CTRL:
                            pass
                        elif event.key == pygame.K_CAPSLOCK:
                            pass
                        elif event.key == pygame.K_c and event.mod & pygame.KMOD_CTRL:
                            pyperclip.copy(self.getSelection())
                        elif event.key == pygame.K_v and event.mod & pygame.KMOD_CTRL:
                            clipboard_content = pyperclip.paste()
                            self.pasteText(clipboard_content)

                        elif event.key == pygame.K_DOWN:
                            if self.normalCoordsToSplit(self.cursorpos[0],self.cursorpos[1])[1] < len(self.values) - 1:
                                temp = self.normalCoordsToSplit(self.cursorpos[0],self.cursorpos[1])
                                temp[1]+=1
                                self.cursorpos=self.splitCoordsToNormal(temp[0],temp[1])
                                redraw = True
                        elif event.key == pygame.K_UP:
                            if self.normalCoordsToSplit(self.cursorpos[0],self.cursorpos[1])[1] > 0:
                                temp = self.normalCoordsToSplit(self.cursorpos[0],self.cursorpos[1])
                                temp[1]-=1
                                self.cursorpos=self.splitCoordsToNormal(temp[0],temp[1])
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
                            self.texts[self.cursorpos[1]]=self.font.render(beforeCursor, True, self.textColour)
                            self.cursorpos[1]+=1
                            self.values.insert(self.cursorpos[1],afterCursor)
                            self.texts.insert(self.cursorpos[1], self.font.render(afterCursor, True, self.textColour))
                            redraw = True
                            self.cursorpos[0]=0
                            hasChanged = True
                        elif event.key == pygame.K_BACKSPACE:
                            beforeCursor = self.values[self.cursorpos[1]][:self.cursorpos[0]]
                            afterCursor = self.values[self.cursorpos[1]][self.cursorpos[0]:]
                            hasChanged = True
                            if self.cursorpos[0]!=0:
                                self.values[self.cursorpos[1]]=beforeCursor[:-1]+afterCursor
                                self.texts[self.cursorpos[1]]=self.font.render(beforeCursor[:-1]+afterCursor, True, self.textColour)
                                self.cursorpos[0]-=1
                            else:
                                if self.cursorpos!=[0,0]:
                                    self.valuebeforecursor=self.values[self.cursorpos[1]-1]
                                    self.values.pop(self.cursorpos[1])
                                    self.texts.pop(self.cursorpos[1])
                                    
                                    self.values[self.cursorpos[1]-1]+=afterCursor
                                    self.texts[self.cursorpos[1]-1]=self.font.render(self.values[self.cursorpos[1]-1], True, self.textColour)
                                    self.cursorpos[0]=len(self.values[self.cursorpos[1]-1])-len(afterCursor)
                                    self.cursorpos[1]-=1
                                    
                            self.removeSelection()

                                   

                            redraw = True
                        elif event.key == pygame.K_TAB:
                            hasChanged = True
                            beforeCursor = self.values[self.cursorpos[1]][:self.cursorpos[0]]
                            afterCursor = self.values[self.cursorpos[1]][self.cursorpos[0]:]
                            self.cursorpos[0]+= 4
                            self.values[self.cursorpos[1]] = beforeCursor + "    " + afterCursor
                            self.texts[self.cursorpos[1]] = self.font.render(self.values[self.cursorpos[1]], True, self.textColour)
                            self.text=self.font.render(self.values[self.cursorpos[1]], True, self.textColour)
                            redraw = True
                        elif event.key!=pygame.K_LCTRL:
                            hasChanged = True
                            self.removeSelection()
                            beforeCursor = self.values[self.cursorpos[1]][:self.cursorpos[0]]
                            afterCursor = self.values[self.cursorpos[1]][self.cursorpos[0]:]
                            self.cursorpos[0]+= len(event.unicode)
                            self.values[self.cursorpos[1]] = beforeCursor + event.unicode + afterCursor
                            self.texts[self.cursorpos[1]] = self.font.render(self.values[self.cursorpos[1]], True, self.textColour)
                            self.text=self.font.render(self.values[self.cursorpos[1]], True, self.textColour)
                            
                            
                            
                            redraw = True

                        if redraw:
                            self.valuebeforecursor = self.values[self.cursorpos[1]][:self.cursorpos[0]]
                            self.textbeforecursor = self.font.render(self.valuebeforecursor, True, self.textColour)
            
                return hasChanged