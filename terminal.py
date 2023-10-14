import pygame
import textbox
import assets
import os
import threading
import time
import random
import python3
import videoplayer
import functions
import audioplayer
import texteditor
import tictactoe
import sys
import sorts
import threeDimensional
import imageviewer
wallpaper = assets.background
wallpapers={
    "windows_grass" : assets.background,
    "windows10" : assets.windows10,
    "ubuntu" : assets.ubuntu,
    "moon" : assets.moon,
    "butterfly" : assets.butterfly,
    "mountain" : assets.mountain,
    "aquarium" : assets.aquarium,
    "bright" : assets.Bright,
    "car" : assets.car,
    "car2" : assets.car2,
    "castle" : assets.castle,
    "circuitry" : assets.circuitry,
    "cyberpunk" : assets.cyberpunk,
    "galaxy" : assets.Galaxy,
    "moon" : assets.moon,
    "moon2" : assets.moon2,
    "ocean" : assets.ocean,
    "rain" : assets.rain,
    "ship" : assets.ship,
    "space" : assets.space,
    "spike" : assets.Spike,
    "tokyo" : assets.tokyo,
    "village" : assets.village,
    "waterfall" : assets.Waterfall,
}
r=255
g=255
b=255
custom="null"



class Terminal:
    def __init__(self,screen) -> None:
        self.screen=screen
        self.type = "terminal"
        self.x=100
        self.y=100
        self.w=300
        self.h=200
        self.textInput = textbox.textInput(self.x,self.y,self.w,self.h,self.type)
        self.font = pygame.font.Font(None, 16)
        self.toggleResponse=False
        self.responses=[]
        self.rect=pygame.Rect(self.x,self.y,self.w,self.h)
        self.bar = pygame.Rect(self.x,self.y,self.w,10)
        self.directory = os.path.dirname(os.path.abspath(__file__))
        self.scrollOffset=0
        self.exitRect=pygame.Rect(self.x+self.w-8,self.y+3,5,5)
        self.history = []
        self.video_extensions = ['.avi', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.wmv', '.flv', '.webm']
        self.audiofiletypes = [".wav",".mp3",".aac",".flac",".ogg",".aiff",".wma",".midi",".amr",".ac3",".m4a",".opus","au"]
        self.textfiletypes=["txt","py","cpp","rb","html","css","js","json","xml","sql","csv","md","java","php","c","h","sh","log","yml","yaml","ini","cfg","bat","tex","svg","scss"]
    def draw(self, screen):
        pygame.draw.rect(screen,(70,70,70),self.rect)
        pygame.draw.rect(screen,(10,10,10),self.bar)
        pygame.draw.rect(screen,(255,0,0),self.exitRect)
        try:
            c=0
            for text in self.textInput.texts:
                screen.blit(text,(self.x,self.y+10+c))
                c+=25
            if len(self.textInput.values)==1 and len(self.textInput.value)==0 and self.toggleResponse:
                c=0
                for response in self.responses:
                    screen.subsurface((self.x,self.y+10,self.w,self.h-10)).blit(response,(0,c+10+self.scrollOffset))
                    c+=15
        except AttributeError as e:
            self.mbHeld((100,100))

    def mbHeld(self,mousePos):
        self.x=mousePos[0]
        self.y=mousePos[1]

        try:
            if (self.x+self.w)>=self.screen.get_rect().w:
                self.x=self.screen.get_rect().w-self.w
            elif self.x<=0:
                self.x=0
            if (self.y+self.h)>=self.screen.get_rect().h:
                self.y=self.screen.get_rect().h-self.h
            elif self.y<=0:
                self.y=0
        except AttributeError as e:
            #self.screen doesn't exist
            pass

        self.rect=pygame.Rect(self.x,self.y,self.w,self.h)
        self.bar=pygame.Rect(self.x,self.y,self.w,10)
        self.textInput.textbox=pygame.Rect(self.x,self.y,self.w,self.h)
        self.exitRect=pygame.Rect(self.x+self.w-8,self.y+3,5,5)
    
    def audio_get_files(self,args):
       # try:
            
            items = os.listdir(os.path.join(self.directory,"/".join(args.split("/")[:-1])))
           
            files = [item for item in items if os.path.isfile(os.path.join(os.path.join(self.directory,"/".join(args.split("/")[:-1])),item))]
            dm = []
            for file in files:
                dm.append(file)
            

            return sorted(dm)

    def list_files_and_folders(self):
        try:

            items = os.listdir(self.directory)
            files = [item for item in items if os.path.isfile(os.path.join(self.directory, item))]
            folders = [item for item in items if os.path.isdir(os.path.join(self.directory, item))]
            fi=[*sorted(files)]
            fo=[*sorted(folders)]
            if len(fi)==0:
                fi=["None in this directory"]
            elif len(fo)==0:
                fo=["None in this directory"]
            dm = ["Current directory:","",self.directory,"","Files:","",*fi,"","Folders:","",*fo]
            return dm
        except OSError as e:
            dm.append(f"Error: {e}")

    def command(self,values):
        self.scrollOffset=0
        global wallpaper
        global wallpapers
        global custom

        self.toggleResponse=True
        self.textInput.value=""
        self.textInput.values=[self.textInput.value]
        self.textInput.text=self.textInput.font.render(self.textInput.value, True, (255, 255, 255))
        self.textInput.texts=[self.textInput.text]
        self.cmd=""
        for i in "\n".join(values):
            if i != "\n":
                self.cmd+=i
        
        self.history.append(values)
        self.textInput.history=self.history
        self.response=["Command not found. Type 'help' for commands."]

        if self.cmd == "help":
            self.response=["help - Shows commands.",
                           "exit - Exits the program.",
                           "wallpapers - shows your wallpapers",
                           "screen <r> <g> <b> - changes screen colour",
                           "ls - lists the current directory you're in.",
                           "cd <directory/folder> - changes the folder you're in.",
                           "cd ../ - takes you one step back in your directory",
                           "video <filename> - lets you play video files",
                           "volume <1-100> - Change the volume",
                           "audio <filename> - play an audio file",
                           "text <filename> - open and edit a .txt or a .py file",
                           "python3 <filename> - runs python code",
                           "text types - view supported file types",
                           "text new <filename> - creates a new text file",
                           "text <filename> - edits supported text files",
                           "games - shows a list of commands that launch games",
                           "sorts - shows a list of sorting algorithm commands",
                           "3d - shows some rotating 3d shape commands",
                           "image <filename> - displays images."
                           ]
            
        elif self.cmd == "exit":
            if os.path.isfile("requested_action"):
                os.remove("requested_action")
            assets.running=False
        elif self.cmd == "restart" or self.cmd == "reboot" or self.cmd == "r":
            with open('requested_action', 'w') as f: f.write('restart')
            assets.running=False
            self.response=["Restarting..."]
        elif os.path.exists(os.path.join(self.directory, " ".join(self.cmd.split()[1:]))) and os.path.exists(os.path.join(os.getcwd(),"main.py")) and os.path.samefile(os.path.join(self.directory, " ".join(self.cmd.split()[1:])),os.path.join(os.getcwd(),"main.py")):
            with open('requested_action', 'w') as f: f.write('restart')
            assets.running=False
            self.response=["Restarting..."]
        elif os.path.exists(os.path.join(self.directory, " ".join(self.cmd.split()[1:]))) and os.path.exists(os.path.join(os.getcwd(),"wrapper.py")) and os.path.samefile(os.path.join(self.directory, " ".join(self.cmd.split()[1:])),os.path.join(os.getcwd(),"wrapper.py")):
            with open('requested_action', 'w') as f: f.write('restart')
            assets.running=False
            self.response=["Restarting..."]

        elif self.cmd =="wallpapers":
            self.response=["To change your wallpaper, type 'wallpaper'","with one of the following options:",
                           "windows_grass",
                            "windows10", 
                            "ubuntu",
                           "moon",
                           "butterfly",
                           "mountain",
                           "aquarium",
                           "bright",
                           "car",
                           "car2",
                           "castle",
                           "circuitry",
                           "cyberpunk",
                           "galaxy",
                           "moon2",
                           "ocean",
                           "rain",
                           "ship",
                           "space",
                           "spike",
                           "tokyo",
                           "village",
                           "waterfall",
                           "To add a custom wallpaper, add an image", "to your assets folder and type:","wallpaper custom <filename>"
                           ]

        elif len(self.cmd)>15 and self.cmd[0:16]=="wallpaper custom":
            if len(self.cmd.split())==3:
                try:
                    custom = pygame.image.load(f'assets/{self.cmd.split()[2]}')
                    custom = pygame.transform.scale(custom, (1920, 1080))
                    wallpaper="null"
                    self.response=["Completed successfully."]
                except:
                    self.response=["Invalid file name."]
        elif len(self.cmd.split())>1 and self.cmd.split()[0]=="wallpaper" and self.cmd.split()[1] in list(wallpapers):
            kw=self.cmd.split()[1]

            wallpaper=wallpapers[self.cmd.split()[1]]
            custom="null"
            self.response=["Completed successfully."]
            print(wallpaper)
        elif len(self.cmd.split())==4 and self.cmd.split()[0]=="screen":
            try:
                global r, g, b
                if 0<=int(self.cmd.split()[1])<=255 and 0<=int(self.cmd.split()[2])<=255 and 0<=int(self.cmd.split()[3])<=255:
                    r=int(self.cmd.split()[1])
                    g=int(self.cmd.split()[2])
                    b=int(self.cmd.split()[3])
                    wallpaper = "null"
                    custom = "null"
                    self.response=["Completed successfully."]
                else:
                    self.response=["r g b values must be numbers between 0 and 255."]
            except:
                self.response=["Error - r g b values must be", "space separated values from 0-255"]
        elif self.cmd == "ls":
            self.response=self.list_files_and_folders()
        elif len(self.cmd.split())>0 and self.cmd.split()[0] == "cd":
            if len(self.cmd.split()) > 1:
                new_directory = os.path.join(self.directory, " ".join(self.cmd.split()[1:]))
                if os.path.exists(new_directory) and os.path.isdir(new_directory):
                    self.directory = new_directory
                    self.directory = os.path.normpath(self.directory)
                    self.response=["Directory changed successfully!","Current directory:",self.directory]
                else:
                    self.response=["Invalid directory."]
            else:
                self.response=["Usage: cd <directory>"]
        elif len(self.cmd.split())>1 and self.cmd[0:5]=="video":
            if os.path.isfile(os.path.join(self.directory, " ".join(self.cmd.split()[1:]))):
                
                if os.path.splitext(os.path.join(self.directory, " ".join(self.cmd.split()[1:])))[1].lower() in self.video_extensions:
                    self.response=["Completed successfully."]
                    video_dir = os.path.join(self.directory, " ".join(self.cmd.split()[1:]))
                    newplayer=videoplayer.VideoPlayer(video_dir,self.screen)
                    assets.windows.append(newplayer)
                else:
                    self.response=["Error. You must be in the directory of the video","or the command must specify the location of the", "video in relation to the terminal's location."]
         
            else:
                self.response=["Error. You must be in the directory of the video","or the command must specify the location of the", "video in relation to the terminal's location."]
        elif len(self.cmd.split())>=2 and self.cmd.split()[0]=="image":
            if os.path.isfile(os.path.join(self.directory, " ".join(self.cmd.split()[1:]))):
                assets.windows.append(imageviewer.ImageViewer(os.path.join(self.directory, " ".join(self.cmd.split()[1:])),self.screen))
                self.response=["Completed successfully."]
        elif len(self.cmd.split())==2 and self.cmd.split()[0]=="volume":
            functions.set_system_volume(int(self.cmd.split()[1]))
            self.response=["Completed successfully."]
        elif len(self.cmd.split())>1 and self.cmd[0:5]=="audio" and os.path.exists(self.directory+"/"+" ".join(self.cmd.split()[1:])):
            temp_playlist = self.audio_get_files(self.cmd[6:])
            
            if temp_playlist != None:
                filtered_dir = []
                for i in temp_playlist:
                    for j in self.video_extensions+self.audiofiletypes:
                        if i.endswith(j):
                            break
                    else:
                        continue
                    filtered_dir.append(os.path.abspath(os.path.join(os.path.join(self.directory,self.cmd[6:]),i)))
                
                assets.windows.append(audioplayer.AudioPlayer(os.path.abspath(os.path.join(self.directory, " ".join(self.cmd.split()[1:]))),self.screen,filtered_dir))
                self.response=["Completed successfully."]
            else:
                self.response=["Error. Invalid file."]
        elif self.cmd=="text types":
            self.response=["The following text types are supported"]+self.textfiletypes
        elif len(self.cmd.split())>=3 and self.cmd.split()[0]=="text" and self.cmd.split()[1]=="new" and "." in self.cmd and self.cmd.split(".")[-1] in self.textfiletypes:
            try:
                open(self.directory+"/"+self.cmd.split()[2],"x").close()
                self.response=["Completed successfully."]
            except:
                self.response=["Error. Invalid file type or file already exists."]
        elif len(self.cmd.split())>=2 and self.cmd[0:4]=="text":
            if "." in self.cmd and self.cmd.split(".")[-1] in self.textfiletypes and os.path.isfile(self.directory+"/"+" ".join(self.cmd.split()[1:])):
                assets.windows.append(texteditor.TextEditor(self.directory+"/"+" ".join(self.cmd.split()[1:]),self.screen))
                self.response=["File opened successfully."]
            else:
                self.response=["Invalid file or usage of command.","Type 'help' for commands."]
        elif len(self.cmd.split())==2 and self.cmd[0:7]=="python3":
            if os.path.isfile(self.directory+"/"+self.cmd.split()[1]) and self.cmd[-3:]==".py": 
                assets.windows.append(python3.Python3(self.directory+"/"+self.cmd.split()[1],self.directory,self.screen))
                self.response=["Completed successfully."]
            else:
                self.response=["Invalid file."]
        elif self.cmd == "games":
            self.response=["The following game commands are:","Tic Tac Toe (or ttt)"]
        elif self.cmd == "ttt" or self.cmd.lower() == "tic tac toe":
            assets.windows.append(tictactoe.TicTacToe(self.screen))
            self.response=["Completed successfully."]
        elif self.cmd=="sorts":
            self.response=["The following sorts are:","bubble sort <size> <delay>","insertion sort <size> <delay>",
                           "merge sort <size> <delay>","quick sort <size> <delay>","bogo sort <size> <delay>","cocktail shaker sort <size> <delay>",
                           "comb sort <size> <delay>",]
        elif " ".join(self.cmd.split()[0:2]).lower() == "bubble sort":
            try:
                sort = sorts.Sort("bubble",self.screen,int(self.cmd.split()[2]),float(self.cmd.split()[3]))
                if sort.type!="None":
                    assets.windows.append(sort)
                    self.response=["Completed successfully."]
                else:
                    self.response=["Error.", "Make sure you entered the size as a whole number","and the size is smaller than 380."]
                
            except:
                self.response=["Error.", "Make sure you entered the size as a whole number","and the size is smaller than 380."]
            
        elif " ".join(self.cmd.split()[0:2]).lower() == "insertion sort":
            try:
                sort = sorts.Sort("insertion",self.screen,int(self.cmd.split()[2]),float(self.cmd.split()[3]))
                if sort.type!="None":
                    assets.windows.append(sort)
                    self.response=["Completed successfully."]
                else:
                    self.response=["Error.", "Make sure you entered the size as a whole number","and the size is smaller than 380."]
                
            except:
                self.response=["Error.", "Make sure you entered the size as a whole number","and the size is smaller than 380."]
        elif " ".join(self.cmd.split()[0:2]).lower() == "merge sort":
            try:
                sort = sorts.Sort("merge",self.screen,int(self.cmd.split()[2]),float(self.cmd.split()[3]))
                if sort.type!="None":
                    assets.windows.append(sort)
                    self.response=["Completed successfully."]
                else:
                    self.response=["Error.", "Make sure you entered the size as a whole number","and the size is smaller than 380."]
                
            except:
                self.response=["Error.", "Make sure you entered the size as a whole number","and the size is smaller than 380."]
        elif " ".join(self.cmd.split()[0:2]).lower() == "quick sort":
            try:
                sort = sorts.Sort("quick",self.screen,int(self.cmd.split()[2]),float(self.cmd.split()[3]))
                if sort.type!="None":
                    assets.windows.append(sort)
                    self.response=["Completed successfully."]
                else:
                    self.response=["Error.", "Make sure you entered the size as a whole number","and the size is smaller than 380."]
                
            except:
                self.response=["Error.", "Make sure you entered the size as a whole number","and the size is smaller than 380."]
        elif " ".join(self.cmd.split()[0:2]).lower() == "bogo sort":
            try:
                sort = sorts.Sort("bogo",self.screen,int(self.cmd.split()[2]),float(self.cmd.split()[3]))
                if sort.type!="None":
                    assets.windows.append(sort)
                    self.response=["Completed successfully."]
                else:
                    self.response=["Error.", "Make sure you entered the size as a whole number","and the size is smaller than 380."]
                
            except:
                self.response=["Error.", "Make sure you entered the size as a whole number","and the size is smaller than 380."]
        elif " ".join(self.cmd.split()[0:2]).lower() == "comb sort":
            try:
                sort = sorts.Sort("comb",self.screen,int(self.cmd.split()[2]),float(self.cmd.split()[3]))
                if sort.type!="None":
                    assets.windows.append(sort)
                    self.response=["Completed successfully."]
                else:
                    self.response=["Error.", "Make sure you entered the size as a whole number","and the size is smaller than 380."]
                
            except:
                self.response=["Error.", "Make sure you entered the size as a whole number","and the size is smaller than 380."]
        elif " ".join(self.cmd.split()[0:3]).lower() == "cocktail shaker sort":
            try:
                sort = sorts.Sort("cocktail",self.screen,int(self.cmd.split()[3]),float(self.cmd.split()[4]))
                if sort.type!="None":
                    assets.windows.append(sort)
                    self.response=["Completed successfully."]
                else:
                    self.response=["Error.", "Make sure you entered the size as a whole number","and the size is smaller than 380."]
                
            except:
                self.response=["Error.", "Make sure you entered the size as a whole number","and the size is smaller than 380."] 
        elif " ".join(self.cmd.split()[0:2]).lower() == "radix sort":
            try:
                sort = sorts.Sort("radix",self.screen,int(self.cmd.split()[2]),float(self.cmd.split()[3]))
                if sort.type!="None":
                    assets.windows.append(sort)
                    self.response=["Completed successfully."]
                else:
                    self.response=["Error.", "Make sure you entered the size as a whole number","and the size is smaller than 380."]
                
            except:
                self.response=["Error.", "Make sure you entered the size as a whole number","and the size is smaller than 380."]
        elif self.cmd.lower()=="3d":
            self.response=["Here are the following commands for 3D experiments:","cube","triangular prism"]
        elif self.cmd.lower() == "cube":
            assets.windows.append(threeDimensional.ThreeDimensional("cube",self.screen))
            self.response=["Completed successfully."]
        elif self.cmd.lower()=="pyramid":
            assets.windows.append(threeDimensional.ThreeDimensional("pyramid",self.screen))
            self.response=["Completed successfully."]   
        self.responses=[]
        for response in self.response:
            self.responses.append(self.font.render(response, True, (255, 255, 255)))

    