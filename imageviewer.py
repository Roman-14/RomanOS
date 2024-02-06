import pygame
import window

class ImageViewer(window.Window):
    def __init__(self,image,screen) -> None:
        super().__init__(100, 100, 360, 240, screen, "ImageViewer")
        self.scrollOffset=0
        self.image=image
        self.loadedImg = pygame.image.load(self.image)
        self.loadedImg = pygame.transform.scale(self.loadedImg, (self.w, self.h-10))
        
    def draw(self,screen):
        super().draw(screen)
        screen.blit(self.loadedImg,(self.x,self.y+10))