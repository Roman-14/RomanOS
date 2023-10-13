from datetime import datetime
import assets



class Clock:
    def __init__(self) -> None:
        self.r=0
        self.g=0
        self.b=0

        self.rSpeed=1
        self.gSpeed=2
        self.bSpeed=3

        self.current_time =  datetime.now().strftime("%H:%M:%S")
        self.date_now = str(datetime.now())[:10]

        self.time = assets.Defaultfont.render(self.current_time, True, (self.r, self.g, self.b))
        self.date = assets.Defaultfont.render(self.date_now, True, (self.r, self.g, self.b))
    def draw(self,screen):
        self.r+=self.rSpeed
        self.g+=self.gSpeed
        self.b+=self.bSpeed
        if self.r//255==1:
            self.rSpeed*=-1
            self.r=254
        if self.g//255==1:
            self.gSpeed*=-1
            self.g=254
        if self.b//255==1:
            self.bSpeed*=-1
            self.b=254

        if self.r<=50:
            self.rSpeed*=-1
            self.r=51
        if self.g<=50:
            self.gSpeed*=-1
            self.g=51
        if self.b<=50:
            self.bSpeed*=-1
            self.b=51

        self.current_time =  datetime.now().strftime("%H:%M:%S")
        self.date_now = str(datetime.now())[:10]

        self.time = assets.Defaultfont.render(self.current_time, True, (self.r, self.g, self.b))
        self.date = assets.Defaultfont.render(self.date_now, True, (self.r, self.g, self.b))

        #screen.blit(self.time,(assets.width/2-self.time.get_rect().w,assets.height-self.time.get_rect().h))
        screen.blit(self.time,(assets.width/2-self.time.get_rect().w,0))