"""
To do:
-when making an audio and video window and then restarting, the restart doesn't work
-shortcut window textboxes and terminal textbox can both be focused into at same time, must be fixed

- fix bug where one shortcut menu textbox and another textbox can both be focused on simultaneously

- make restarting work during audio and video
- allow the moving, creation (for txt) and deletion of files
- add a horizontal scroll bar on text editor
- add ctrl a to notepads
- create one big class for textboxes
- when typing in files, allow basic auto complete functionality so that entering "python3 tes" gives "python3 test.py" 
- allow deleting of files

- more games such as minesweeper
- plant growing app
- 3D spinning stuff
- custom icon commands
- completely erradicate errors when typing invalid commands
- find max refresh rate and make it the pygame fps
"""

import os
import sys
#if len(sys.argv)>1 and sys.argv[1] == '--cli': os.environ['SDL_VIDEODRIVER'] = 'KMSDRM' #VERY IMPORTANT LINE!!!
import pygame
import functions
import subprocess
import terminal
import assets
import math
import videoplayer
import texteditor
import python3
from clock import Clock
import rightclick

#subprocess.Popen(["python3", "sound.py"])


pygame.display.init()
pygame.mixer.init()


fps = 120

clock = pygame.time.Clock()

print(pygame.display.get_driver())

wallpaper = terminal.wallpaper
r = terminal.r
g = terminal.g
b = terminal.b

screen = pygame.display.set_mode((assets.width, assets.height),pygame.FULLSCREEN)

exitRect = pygame.Rect(assets.width-20, 0, 20, 20)

OSclock = Clock()

rightClickBox = "null"
rightClickCode = 3
leftClickCode = 1

invisterminal = terminal.Terminal(screen)

def autoStart():
    autostart = terminal.Terminal(screen)
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
        screen.blit(terminal.custom,(0,0))
    else:
        if wallpaper!=str(wallpaper):
            screen.blit(wallpaper, (0,0))
        else:
            global r, g, b
            r = terminal.r
            g = terminal.g
            b = terminal.b

    for tile in assets.tiles:
        screen.blit(assets.icons[assets.tiles[tile][1]],(tile[0]*assets.width/assets.iconX,tile[1]*assets.height/assets.iconY))
        
        tiletext = iconFont.render(assets.tiles[tile][0], True, (OSclock.r, OSclock.g, OSclock.b))
        try:
            screen.subsurface((tile[0]*assets.width/assets.iconX,(tile[1])*assets.height/assets.iconY,assets.width/30,assets.height/20)).blit(tiletext,(assets.tilesOffset[tile],assets.height/20-20))
        except ValueError:
            pass
        assets.tilesOffset[tile] += 1

        for offset in assets.tilesOffset:
            if (tile[0]*assets.width/assets.iconX+assets.tilesOffset[offset]) > (tiletext.get_rect().x+(tile[0]+1)*assets.width/assets.iconX):
                assets.tilesOffset[offset] = -1*tiletext.get_rect().w

    #for i in range(20):
    #    for j in range(30):
    #        pygame.draw.circle(screen,(255,0,0),(j*assets.width/30,i*assets.height/20),2)

    pygame.draw.rect(screen, (255, 0, 0), exitRect)

    screen.blit(assets.power_off, (assets.width-20,0))

    OSclock.draw(screen)

    if rightClickBox!="null":
        rightClickBox.draw(screen)
    for window in assets.windows[::-1]:
        window.draw(screen)
    
    

heldtoggle=[False,0]

heldresize=[False,0]

markedWindow = None

while assets.running:
    screen.fill((r, g, b))
    wallpaper = terminal.wallpaper
    for event in pygame.event.get():
        for window in assets.windows:
            if event.type==pygame.KEYDOWN:
                if window.type=="Python3" and window.textInput.focused:
                    window.keyPressed(event)
                if (window.type == "Python3" or window.type=="terminal" or window.type=="TextEditor") and window.textInput.focused:
                    window.textInput.update(event,pygame.mouse.get_pos())
                    break
                if window.type == "Shortcut" and window.nameInput.focused:
                    window.nameInput.update(event,pygame.mouse.get_pos())
                elif window.type == "Shortcut" and window.commandInput.focused:
                    window.commandInput.update(event,pygame.mouse.get_pos())
            elif window.type == "TextEditor" and window.textInput.focused and event.type == pygame.MOUSEMOTION:
                window.textInput.update(event,pygame.mouse.get_pos())
            elif event.type==pygame.MOUSEBUTTONUP:
                if window.type == "TextEditor":
                    window.textInput.update(event)
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if window.type == "Icons":
                    for key in window.iconLocs:
                        if functions.collidePygameRect(pygame.Rect(window.iconLocs[key][0],window.iconLocs[key][1],window.iconLocs[key][2],window.iconLocs[key][3]),pygame.mouse.get_pos()):
                            window.chosenIcon = key
                            markedWindow = window
                    break
                if window.type == "Python3" or window.type=="terminal" or window.type=="TextEditor":
                    window.textInput.update(event,pygame.mouse.get_pos())
                        
                    
                if window.type == "Shortcut":
                    window.nameInput.update(event,pygame.mouse.get_pos())    
                    window.commandInput.update(event,pygame.mouse.get_pos())
                    if window.iconMenu!=None and functions.collidePygameRect(window.iconMenu.exitRect,pygame.mouse.get_pos()):
                        window.iconMenu=None

                if window.type == "TicTacToe":
                    window.update(pygame.mouse.get_pos())
                if window.type == "Shortcut" and functions.collidePygameRect(window.submit_rect,pygame.mouse.get_pos()):
                    window.submitClicked()
                    break
                if window.type == "Shortcut" and functions.collidePygameRect(window.addRect,pygame.mouse.get_pos()):
                    window.addRectClicked()
                    break
                
            elif event.type==pygame.MOUSEWHEEL:
                #Scroll down is negative, scroll up is positive
                if window.type=="terminal" and functions.collidePygameRect(window.rect,pygame.mouse.get_pos()):
                    scroll_amount = event.y * 10  # Keep the original sign

                    # Calculate the maximum scroll offset based on content height and window height
                    max_scroll_offset = max(0, len(window.responses) * 15 - window.h + 15)

                    # Update the scroll offset within bounds
                    window.scrollOffset += scroll_amount
                    window.scrollOffset = min(0, max(window.scrollOffset, -max_scroll_offset))
                    break
                elif window.type == "TextEditor" and functions.collidePygameRect(window.rect, pygame.mouse.get_pos()):
                    scroll_amount = event.y * 10  # Keep the original sign

                    # Calculate the maximum scroll offset based on content height and window height
                    max_scroll_offset = max(0, len(window.textInput.values) * 25 - window.h + 10)

                    # Update the scroll offset within bounds
                    window.textInput.scrollOffset += scroll_amount
                    window.textInput.scrollOffset = min(0, max(window.textInput.scrollOffset, -max_scroll_offset))
                    break
                elif window.type == "Python3" and functions.collidePygameRect(window.rect, pygame.mouse.get_pos()):
                    scroll_amount = event.y * 10  # Keep the original sign

                    # Calculate the maximum scroll offset based on content height and window height
                    max_scroll_offset = max(0, sum(text.decode().count("\n")+1 for text in window.stdout_list) * 25 - window.stdout.h)

                    # Update the scroll offset within bounds
                    window.scrollOffset += scroll_amount
                    window.scrollOffset = min(0, max(window.scrollOffset, -max_scroll_offset))
                    break

        if markedWindow:
            tempwindowsMarking = []
            for twindow in assets.windows:
                if twindow != markedWindow:
                    tempwindowsMarking.append(twindow)
            assets.windows = tempwindowsMarking
            markedWindow = None

        if event.type == pygame.MOUSEBUTTONDOWN:
            for window in assets.windows:
                if functions.collidePygameRect(window.rect,pygame.mouse.get_pos()):
                    break
            else:
                if event.button == rightClickCode:
                    locX,locY = (math.floor(pygame.mouse.get_pos()[0]/assets.width*assets.iconX),math.floor(pygame.mouse.get_pos()[1]/assets.height*assets.iconY))
                    if (locX,locY) not in assets.tiles:
                        rightClickBox = rightclick.RightClickBox(x=pygame.mouse.get_pos()[0],y=pygame.mouse.get_pos()[1],clicked="empty slot",screen=screen)
                    else:
                        rightClickBox = rightclick.RightClickBox(x=pygame.mouse.get_pos()[0],y=pygame.mouse.get_pos()[1],clicked="filled slot",screen=screen)
                elif event.button == leftClickCode:
                    for tile in assets.tiles:
                        if functions.collidePygameRect(pygame.Rect(tile[0]*assets.width/assets.iconX,tile[1]*assets.height/assets.iconY,assets.width/assets.iconX, assets.height/assets.iconY),pygame.mouse.get_pos()):
                            invisterminal.command(values=[],autostart=assets.tiles[tile][2])
            if event.button == leftClickCode:
                if rightClickBox != "null":
                    rightClickBox.update(pygame.mouse.get_pos())
                rightClickBox="null"

        if event.type == pygame.QUIT:
            assets.running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                assets.running = False
            elif event.key == pygame.K_RETURN:
                for window in assets.windows:
                    if window.type=="terminal" and window.textInput.focused:
                        window.command(window.textInput.values)
                        wallpaper = terminal.wallpaper
                    elif window.type=="Python3" and window.textInput.focused:
                        window.returnPressed()
            else:
                for window in assets.windows:
                    if window.type=="terminal" and window.textInput.focused:
                        window.toggleResponse=False
        if pygame.mouse.get_pressed()[0] and event.type==pygame.MOUSEBUTTONDOWN:
            clicked_window=None
            for window in assets.windows:
                if functions.collidePygameRect(window.bar,pygame.mouse.get_pos()) and not functions.collidePygameRect(window.exitRect,pygame.mouse.get_pos()):
                    clicked_window=window
                    heldtoggle=[True,window]
                elif window.type == "Shortcut" and window.iconMenu != None and functions.collidePygameRect(window.iconMenu.bar,pygame.mouse.get_pos()):
                    clicked_window=window.iconMenu
                    heldtoggle=[True,window.iconMenu]
                elif window.type == "TextEditor" and functions.collidePygameRect(window.resizeRect,pygame.mouse.get_pos()):
                    clicked_window=window
                    heldresize = [True, window]
                    break
                elif functions.collidePygameRect(window.exitRect,pygame.mouse.get_pos()):
                    if window.type=="VideoPlayer" or window.type=="AudioPlayer":
                       window.audioplayer.stop_playback()
                    elif window.type=="Sort":
                        window.running=False
                    elif window.type == "Shortcut":
                        temporaryWindows = []
                        for potentialIconMenu in assets.windows:
                            if not potentialIconMenu == window.iconMenu:
                                temporaryWindows.append(potentialIconMenu)
                        assets.windows=temporaryWindows
                        window.iconMenu = None
                        
                        
                    tempwindows=[]
                    for window2 in assets.windows:
                        if window2!=window:
                            tempwindows.append(window2)
                    break
                    
                elif window.type == "AudioPlayer" and functions.collidePygameRect(window.playlistRect,pygame.mouse.get_pos()):
                    window.playlistToggled = not window.playlistToggled
                    break
            try:
                assets.windows=tempwindows
            except NameError as e:
                pass
            if clicked_window is not None and clicked_window in assets.windows:
                assets.windows.remove(clicked_window) 
                assets.windows.insert(0, clicked_window)

        if event.type == pygame.MOUSEBUTTONUP:
            heldtoggle[0]=False
            heldresize[0]=False

        for window in assets.windows:
            if assets.terminalImg.get_rect().colliderect(window.rect):
                break
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button==leftClickCode:
                    if functions.collidePygameRect(exitRect,pygame.mouse.get_pos()):
                        if os.path.isfile("requested_action"):
                            os.remove("requested_action")
                        assets.running=False
                        print("Goodbye!")


    if heldtoggle[0]==True:
        heldtoggle[1].mbHeld(pygame.mouse.get_pos())
    elif heldresize[0]==True:
        heldresize[1].resizeHeld(pygame.mouse.get_pos())

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
