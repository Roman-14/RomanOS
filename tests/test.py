import musicalbeeps

import random

import math
sorting = [i for i in range(380)]
random.shuffle(sorting)
options = 189
notes = ["A","B","C","D","E","F","G"]
octaves=["0","1","2","3","4","5","6","7","8"]
options=["","b","#"]

player = musicalbeeps.Player(volume = 1,
                            mute_output = False)

# Examples:

# To play an A on default octave n°4 for 0.2 seconds
for i in sorting:
    player.play_note(notes[math.floor(i/len(sorting)*len(notes))]+octaves[math.floor(i/len(sorting)*len(octaves))]+options[math.floor(i/len(sorting)*len(options))], 0.01)
