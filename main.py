"""
To do:
-when making an audio and video window and then restarting, the restart doesn't work
- multiple instances of tic tac toe window causes weird problems
- make restarting work during audio and video
- allow the moving, creation (for txt) and deletion of files
- add a horizontal scroll bar on text editor
- add ctrl a to notepads
- create one big class for textboxes
- when typing in files, allow basic auto complete functionality so that entering "python3 tes" gives "python3 test.py" 
- allow deleting of files

- make a flash cards app
- more games such as minesweeper
- plant growing app
- 3D spinning stuff
- completely erradicate errors when typing invalid commands
- text editor selection stuff and cursor doesnt have a focus system
"""

import os
import pygame
import functions
import terminal
import assets
import math
from clock import Clock
import rightclick

pygame.display.init()
pygame.mixer.init()

fps = 120

clock = pygame.time.Clock()

print(pygame.display.get_driver())

wallpaper = terminal.wallpaper
r = terminal.r
g = terminal.g
b = terminal.b

exitRect = pygame.Rect(assets.width-20, 0, 20, 20)

OSclock = Clock()




def autoStart():
    autostart = terminal.Terminal(assets.screen)
    autostartpath = "data/autostart.txt"
    if not os.path.exists(autostartpath):
        open(autostartpath,"x").close()
    autostartdata = open(autostartpath,"r")
    for i in autostartdata.readlines():
        for j in i.split(";"):
            autostart.command(values=[],autostart=j)

autoStart()

iconFont = pygame.font.Font(None, 20)

def blitandDraw():
    global rollingTextOffset

    if terminal.custom!="null":
        assets.screen.blit(terminal.custom,(0,0))
    else:
        if wallpaper!=str(wallpaper):
            assets.screen.blit(wallpaper, (0,0))
        else:
            global r, g, b
            r = terminal.r
            g = terminal.g
            b = terminal.b

    for tile in assets.tiles:
        assets.screen.blit(assets.icons[assets.tiles[tile][1]],(tile[0]*assets.width/assets.iconX,tile[1]*assets.height/assets.iconY))
        
        tiletext = iconFont.render(assets.tiles[tile][0], True, (OSclock.r, OSclock.g, OSclock.b))
        try:
            assets.screen.subsurface((tile[0]*assets.width/assets.iconX,(tile[1])*assets.height/assets.iconY,assets.width/30,assets.height/20)).blit(tiletext,(assets.tilesOffset[tile],assets.height/20-20))
        except ValueError:
            pass
        assets.tilesOffset[tile] += 1

        for offset in assets.tilesOffset:
            if (tile[0]*assets.width/assets.iconX+assets.tilesOffset[offset]) > (tiletext.get_rect().x+(tile[0]+1)*assets.width/assets.iconX):
                assets.tilesOffset[offset] = -1*tiletext.get_rect().w

    pygame.draw.rect(assets.screen, (255, 0, 0), exitRect)

    assets.screen.blit(assets.power_off, (assets.width-20,0))

    OSclock.draw(assets.screen)

    if rightclick.rightClickBox!=None:
        rightclick.rightClickBox.draw(assets.screen)
    for window in assets.windows[::-1]:
        window.draw(assets.screen)
    
markedWindow = None

while assets.running:
    assets.screen.fill((r, g, b))
    wallpaper = terminal.wallpaper
    assets.mousePos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        for window in assets.windows[:]:
            if event.type==pygame.KEYDOWN:
                if window.type == "terminal" and window.textInput.focused:
                    window.toggleResponse = False
                if event.key == pygame.K_RETURN:
                    window.onReturnPressed()
                elif window.onKeyDown(event):
                    break
                
            elif event.type == pygame.MOUSEMOTION:
                window.onMouseMotion(event, assets.mousePos)
            elif event.type==pygame.MOUSEBUTTONUP:
                window.onMouseButtonUp(event, assets.mousePos)
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if event.button == assets.leftClickCode:
                    if functions.collidePygameRect(window.exitRect,assets.mousePos):
                        window.onExitRectPressed()           
                        assets.windows.remove(window)
                    elif functions.collidePygameRect(window.bar,assets.mousePos) and not functions.collidePygameRect(window.exitRect,assets.mousePos):
                        assets.clicked_window=window
                        assets.heldtoggle=[True,window]
                    if window.onButtonPress(assets.mousePos):
                        break
                    if window.onResizeRectHeld(assets.mousePos):
                        break
                if window.onMouseButtonDown(event, assets.mousePos):
                    break
            elif event.type==pygame.MOUSEWHEEL:
                window.onScrollWheel(event, assets.mousePos)

        if event.type == pygame.QUIT:
            assets.running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if os.path.isfile("requested_action"):
                    os.remove("requested_action")
                assets.running = False

        if assets.clicked_window != None and assets.clicked_window in assets.windows:
            assets.windows.remove(assets.clicked_window) 
            assets.windows.insert(0, assets.clicked_window)

        if event.type == pygame.MOUSEBUTTONUP:
            assets.heldtoggle[0]=False
            assets.heldresize[0]=False


        if event.type == pygame.MOUSEBUTTONDOWN:
            rightclick.rightClickBox = rightclick.onRightClick(event, assets.mousePos, rightclick.rightClickBox)
            if event.button==assets.leftClickCode:
                if functions.collidePygameRect(exitRect,assets.mousePos):
                    if os.path.isfile("requested_action"):
                        os.remove("requested_action")
                    assets.running=False
                    print("Goodbye!")


    if assets.heldtoggle[0]==True:
        assets.heldtoggle[1].mbHeld(assets.mousePos)
    elif assets.heldresize[0]==True:
        assets.heldresize[1].resizeHeld(assets.mousePos)

    blitandDraw()

    pygame.display.flip()
    pygame.display.update()
    clock.tick(fps)

for window in assets.windows:
    if window.type=="VideoPlayer" or window.type=="AudioPlayer":
        window.audioplayer.stop_playback()
    elif window.type == "Sort":
        window.running=False

if not (os.path.exists("data/shortcuts.txt")):
    with open("data/shortcuts.txt","x") as file:
        ...

with open("data/shortcuts.txt","w") as file:
    for i in assets.tiles:
        file.write(str(i)+"|"+str(assets.tiles[i][0])+"|"+str(assets.tiles[i][1])+"|"+str(assets.tiles[i][2])+"\n")

pygame.quit()