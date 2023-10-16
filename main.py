"""
To do:
- auto start commands

- allow the moving, creation (for txt) and deletion of files
- add a horizontal scroll bar on text editor
- add ctrl a, ctrl v, ctrl c and highlighting text to notepads
- create one big class for textboxes
- when typing in files, allow basic auto complete functionality so that entering "python3 tes" gives "python3 test.py" 
- allow deleting of files

- more games such as minesweeper
- plant growing app
- cool sorting algorithms
- create an image viewer
- 3D spinning stuff
- custom icon commands
- make a centralised class for window code (maybe using inheritance if appropriate)

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
import videoplayer
import texteditor
import python3
from clock import Clock
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

def blitandDraw():
    
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

    pygame.draw.rect(screen, (255, 0, 0), exitRect)
    screen.blit(assets.power_off, (assets.width-20,0))
    screen.blit(assets.terminalImg, (0,0))

    OSclock.draw(screen)
    for window in assets.windows[::-1]:
        window.draw(screen)
    
    

heldtoggle=[False,0]

heldresize=[False,0]



while assets.running:
    screen.fill((r, g, b))
    
    for event in pygame.event.get():
        for window in assets.windows:
            if event.type==pygame.KEYDOWN:
                if window.type=="Python3" and window.textInput.focused:
                    window.keyPressed(event)
                if (window.type == "Python3" or window.type=="terminal" or window.type=="TextEditor") and window.textInput.focused:
                    window.textInput.update(event,pygame.mouse.get_pos())
                    break
            elif window.type == "TextEditor" and window.textInput.focused and event.type == pygame.MOUSEMOTION:
                window.textInput.update(event,pygame.mouse.get_pos())
            elif event.type==pygame.MOUSEBUTTONUP:
                if window.type == "TextEditor":
                    window.textInput.update(event)
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if window.type == "Python3" or window.type=="terminal" or window.type=="TextEditor":
                    window.textInput.update(event,pygame.mouse.get_pos())
                if window.type == "TicTacToe":
                    window.update(pygame.mouse.get_pos())

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
                elif window.type == "TextEditor" and functions.collidePygameRect(window.resizeRect,pygame.mouse.get_pos()):
                    clicked_window=window
                    heldresize = [True, window]
                    break
                elif functions.collidePygameRect(window.exitRect,pygame.mouse.get_pos()):
                    if window.type=="VideoPlayer" or window.type=="AudioPlayer":
                       window.audioplayer.stop_playback()
                    elif window.type=="Sort":
                        window.running=False
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
            if clicked_window is not None:
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
                if event.button==1:
                    if functions.collidePygameRect(exitRect,pygame.mouse.get_pos()):
                        if os.path.isfile("requested_action"):
                            os.remove("requested_action")
                        assets.running=False
                        print("Goodbye!")
                    elif functions.collidePygameRect(assets.terminalImg.get_rect(),pygame.mouse.get_pos()):
                        term=terminal.Terminal(screen)
                        assets.windows.append(term)

     
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
pygame.quit()
