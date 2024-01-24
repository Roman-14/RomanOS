import pygame
import os


windows=[]
running=True

pygame.init()

heldresize = [False,0]
heldtoggle=[False,0]

clicked_window = None

rightClickCode = 3
leftClickCode = 1

screen_info = pygame.display.Info()
width,height = (screen_info.current_w, screen_info.current_h)
screen = pygame.display.set_mode((width, height),pygame.FULLSCREEN)
mousePos = pygame.mouse.get_pos()
if width >=1920:
    iconX=30
    iconY=20
elif width >=700:
    iconX=20
    iconY=15
elif width >= 400:
    iconX=15
    iconY=10
else:
    iconX=10
    iconY=5

tiles = {}

if not (os.path.exists("data/shortcuts.txt")):
    with open("data/shortcuts.txt","x") as file:
        ...
else:
    with open("data/shortcuts.txt","r") as file:
        for i in file.readlines():
            tiles[(int(i.split(")")[0][1:].split(", ")[0]),int(i.split(")")[0][1:].split(", ")[1]))]=[i.split("|")[1],i.split("|")[2],i.split("|")[3][:-1]]

tilesOffset = {}
for i in tiles:
    tilesOffset[i]=0

Defaultfont = pygame.font.Font(None, 32)

background = pygame.image.load('assets/Background')
background = pygame.transform.scale(background, (width, height))

power_off = pygame.image.load('assets/off.png')
power_off = pygame.transform.scale(power_off, (20, 19))

terminalImg = pygame.image.load('assets/terminal')
terminalImg = pygame.transform.scale(terminalImg, (width/iconX, height/iconY))

playlist = pygame.image.load('assets/playlist')
playlist = pygame.transform.scale(playlist, (20, 20))

ubuntu = pygame.image.load('assets/ubuntu')
ubuntu = pygame.transform.scale(ubuntu, (width, height))

windows10 = pygame.image.load('assets/windows10')
windows10 = pygame.transform.scale(windows10, (width, height))

moon = pygame.image.load('assets/moon')
moon = pygame.transform.scale(moon, (width, height))

butterfly = pygame.image.load('assets/Butterfly')
butterfly = pygame.transform.scale(butterfly, (width, height))

mountain = pygame.image.load('assets/Mountain')
mountain = pygame.transform.scale(mountain, (width, height))

aquarium = pygame.image.load('assets/aquarium')
aquarium = pygame.transform.scale(aquarium, (width, height))

Bright = pygame.image.load('assets/Bright')
Bright = pygame.transform.scale(Bright, (width, height))

car = pygame.image.load('assets/car')
car = pygame.transform.scale(car, (width, height))

car2 = pygame.image.load('assets/car2')
car2 = pygame.transform.scale(car2, (width, height))

castle = pygame.image.load('assets/castle')
castle = pygame.transform.scale(castle, (width, height))

circuitry = pygame.image.load('assets/circuitry')
circuitry = pygame.transform.scale(circuitry, (width, height))

cyberpunk = pygame.image.load('assets/cyberpunk')
cyberpunk = pygame.transform.scale(cyberpunk, (width, height))

Galaxy = pygame.image.load('assets/Galaxy')
Galaxy = pygame.transform.scale(Galaxy, (width, height))

rain = pygame.image.load('assets/rain')
rain = pygame.transform.scale(rain, (width, height))

moon2 = pygame.image.load('assets/moon2')
moon2 = pygame.transform.scale(moon2, (width, height))

ocean = pygame.image.load('assets/ocean')
ocean = pygame.transform.scale(ocean, (width, height))

ship = pygame.image.load('assets/ship')
ship = pygame.transform.scale(ship, (width, height))

space = pygame.image.load('assets/space')
space = pygame.transform.scale(space, (width, height))

Spike = pygame.image.load('assets/Spike')
Spike = pygame.transform.scale(Spike, (width, height))

tokyo = pygame.image.load('assets/tokyo')
tokyo = pygame.transform.scale(tokyo, (width, height))

village = pygame.image.load('assets/village')
village = pygame.transform.scale(village, (width, height))

Waterfall = pygame.image.load('assets/Waterfall')
Waterfall = pygame.transform.scale(Waterfall, (width, height))

returncode = 0

shapeImg = pygame.image.load('assets/shape')
shapeImg = pygame.transform.scale(shapeImg, (width/iconX, height/iconY))

warningImg = pygame.image.load('assets/warning')
warningImg = pygame.transform.scale(warningImg, (width/iconX, height/iconY))

gearImg = pygame.image.load('assets/gear')
gearImg = pygame.transform.scale(gearImg, (width/iconX, height/iconY))

barchartImg = pygame.image.load('assets/barchart')
barchartImg = pygame.transform.scale(barchartImg, (width/iconX, height/iconY))

codeImg = pygame.image.load('assets/code')
codeImg = pygame.transform.scale(codeImg, (width/iconX, height/iconY))

musicImg = pygame.image.load('assets/music')
musicImg = pygame.transform.scale(musicImg, (width/iconX, height/iconY))

gameImg = pygame.image.load('assets/game')
gameImg = pygame.transform.scale(gameImg, (width/iconX, height/iconY))

videoImg = pygame.image.load('assets/video')
videoImg = pygame.transform.scale(videoImg, (width/iconX, height/iconY))

restartImg = pygame.image.load('assets/restart')
restartImg = pygame.transform.scale(restartImg, (width/iconX, height/iconY))

icons = {"terminal" : terminalImg, "shape" : shapeImg, "warning" : warningImg, "gear" : gearImg, "barchart" : barchartImg, "code" : codeImg, "music" : musicImg, "game" : gameImg, "video" : videoImg, "restart" : restartImg}