import numpy as np
import sounddevice as sd
import random

print("Sound file read")

def generate_beep(frequency, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    beep_signal = 0.5 * np.sin(2 * np.pi * frequency * t)
    return beep_signal

base_frequency = 440  # A4 note (440 Hz)
major_third_ratio = 5/4
perfect_fifth_ratio = 3/2

harmony = [base_frequency, base_frequency * major_third_ratio, base_frequency * perfect_fifth_ratio]

for _ in range(random.randint(2, 10)):
    frequency = random.choice(harmony)
    duration = random.uniform(0.1, 1.0)
    
    beep_signal = generate_beep(frequency, duration)
    sd.play(beep_signal, 44100)
    sd.wait()



