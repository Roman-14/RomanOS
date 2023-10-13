import pygame

windows=[]
running=True

pygame.init()

screen_info = pygame.display.Info()
width,height = (screen_info.current_w, screen_info.current_h)


Defaultfont = pygame.font.Font(None, 32)

background = pygame.image.load('assets/Background')
background = pygame.transform.scale(background, (width, height))

power_off = pygame.image.load('assets/off.png')
power_off = pygame.transform.scale(power_off, (20, 19))

terminalImg = pygame.image.load('assets/Terminal')
terminalImg = pygame.transform.scale(terminalImg, (100, 100))

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

car2 = pygame.image.load('assets/Car')
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