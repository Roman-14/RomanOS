import pygame
import cv2
import assets
import subprocess
import threading
import time
import os



class AudioPlayer:
    def __init__(self, mp4_file):
        self.mp4_file = mp4_file
        self.running = False
        self.ffmpeg_process = None
        self.ffplay_process = None
        self.thread = None

    def play_audio_from_mp4(self):
        command = [
            'ffmpeg',
            '-i', self.mp4_file,
            '-vn',
            '-acodec', 'pcm_s16le',
            '-ar', '44100',
            '-ac', '2',
            '-f', 'wav',
            '-'
        ]

        ffplay_command = ['ffplay', '-nodisp', '-']

        try:
            self.running = True
            self.ffmpeg_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            self.ffplay_process = subprocess.Popen(ffplay_command, stdin=self.ffmpeg_process.stdout, stderr=subprocess.DEVNULL)



            while self.running:
                time.sleep(0.1)  # Adjust the sleep time as needed

            self.ffmpeg_process.terminate()
            self.ffplay_process.terminate()
        except KeyboardInterrupt:
            self.ffmpeg_process.terminate()
            self.ffplay_process.terminate()

    def start_playback(self):
        self.thread = threading.Thread(target=self.play_audio_from_mp4)
        self.thread.start()

    def stop_playback(self):
        self.running = False
        self.thread.join()


class VideoPlayer:

    def __init__(self, videopath,screen):
            self.screen=screen
            self.videopath=videopath
            self.video = cv2.VideoCapture(videopath)
            self.video_fps = self.video.get(cv2.CAP_PROP_FPS)
            self.video_spf = 1 / self.video_fps
            self.current_frame_shown_for = 0
            self.clock = pygame.time.Clock()
            self.success, self.video_image = self.video.read()
            self.video_size = self.video_image.shape[1::-1]
            self.x=100
            self.y=100
            self.w=300
            self.h=200
            self.video_surf = None
            self.type="VideoPlayer"
            self.rect = pygame.Rect((self.x,self.y,self.w,self.h))
            self.bar=pygame.Rect(self.x,self.y-10,self.w,10)
            self.exitRect=pygame.Rect(self.x+self.w-8,self.y-7,5,5)

            self.audioplayer=AudioPlayer(self.videopath)
            
            threading.Thread(target=self.audioplayer.start_playback).start()
    def mbHeld(self,mousePos):
        self.x=mousePos[0]
        self.y=mousePos[1]

        if (self.x+self.w)>=self.screen.get_rect().w:
            self.x=self.screen.get_rect().w-self.w
        elif self.x<=0:
            self.x=0
        if (self.y+self.h)>=self.screen.get_rect().h:
            self.y=self.screen.get_rect().h-self.h
        elif self.y<=0:
            self.y=0
            
        self.rect=pygame.Rect(self.x,self.y,self.w,self.h)
        self.bar=pygame.Rect(self.x,self.y,self.w,10)
        self.exitRect=pygame.Rect(self.x+self.w-8,self.y+3,5,5)
    def draw(self, screen):
        self.current_frame_shown_for += self.clock.get_time() / 1000
        while self.success and self.current_frame_shown_for > self.video_spf:
            self.current_frame_shown_for -= self.video_spf
            self.success = self.video.grab()

        if self.success and self.current_frame_shown_for <= self.video_spf:
            self.success, self.video_image = self.video.retrieve()

            if self.success:
                self.video_surf = pygame.image.frombuffer(
                    self.video_image.tobytes(), self.video_image.shape[1::-1], "BGR")
                scaled_video_surf = pygame.transform.scale(self.video_surf, (300, 200))

        if self.success:
            screen.blit(scaled_video_surf, (self.x, self.y))
            pygame.draw.rect(screen,(0,0,0),self.bar)
            pygame.draw.rect(screen,(255,0,0),self.exitRect)
            #pygame.display.flip()

            self.clock.tick()
        if not self.success:

            windowstemp=[]
            for window in assets.windows:
                if window!=self:
                    windowstemp.append(window)
            assets.windows=windowstemp
            

    def close(self):
        pygame.quit()
        exit()
