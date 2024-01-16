import pygame
import subprocess
import threading
import time
import assets
import os
import window

class PlayAudio:
    def __init__(self, file):
        self.file = file
        self.running = True
        self.ffmpeg_process = None
        self.ffplay_process = None
        self.thread = None

    def play_audio_from_mp4(self):
        command = [
            'ffmpeg',
            '-i', self.file,
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
    def eventually_stop(self,duration):
        time.sleep(duration)
        print("Over!")
        self.running = False
        self.thread.join()
class AudioPlayer(window.Window):
    def __init__(self,file,screen,directory) -> None:
        super().__init__(100, 100, 300, 200, screen, "AudioPlayer", (137,8,22))
        self.file=file
        self.audioplayer=PlayAudio(self.file)
        self.audioplayer.start_playback()
        self.playlistToggled=False
        self.playlistRect = pygame.Rect(self.x+5,self.y+self.h-25,20,20)
        self.directory = directory

        self.font = assets.Defaultfont
        self.text = self.font.render(self.file.split("/")[-1], True, (0, 0, 0))

        self.rollOffset = -1*self.text.get_rect().w
        #print(*directory,sep="\n")
        delayed_thread = threading.Thread(target=self.audioplayer.eventually_stop, args=(self.getDuration(self.file),))
        delayed_thread.start()

    def getDuration(self,file):
        
        command = [
            'ffprobe',
            '-i', file,
            '-show_entries', 'format=duration',
            '-v', 'quiet',
            '-of', 'csv=p=0'
        ]

        try:
            
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
            
            
            duration = float(output.strip())
            
            return round(duration)
        except subprocess.CalledProcessError as e:
            print(f"Error running ffprobe: {e}")
        except ValueError:
            print("Error parsing duration.")

    def draw(self,screen):
        super().draw(screen)
        if self.playlistToggled:
            pygame.draw.circle(screen, (100,100,255), (self.x+15,self.y+self.h-15),14)
        screen.blit(assets.playlist, (self.x+5,self.y+self.h-25))
        screen.subsurface((self.x,self.y,self.w,self.h)).blit(self.text, (self.rollOffset,20))
        self.rollOffset += 1
        if self.rollOffset == self.w:
            self.rollOffset = -1*self.text.get_rect().w
        try:
            if not self.audioplayer.running and self.playlistToggled:
                print("if statement was fired")
                self.filenames = [i.split("/")[-1] for i in self.directory]
                self.file = "/".join(self.file.split("/")[:-1])+"/"+self.filenames[self.filenames.index(self.file.split("/")[-1])+1]

                self.audioplayer=PlayAudio(self.file)
                self.audioplayer.start_playback()
                self.text = self.font.render(self.file.split("/")[-1], True, (0, 0, 0))
                delayed_thread = threading.Thread(target=self.audioplayer.eventually_stop, args=(self.getDuration(self.file),))
                delayed_thread.start()
        except IndexError as e:
            pass
        except ValueError as e:
            pass
    def mbHeld(self,mousePos):
        super().mbHeld(mousePos)
        self.playlistRect = pygame.Rect(self.x+5,self.y+self.h-25,20,20)