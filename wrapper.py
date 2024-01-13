#wrapper.py

import subprocess
import os
import sys
if len(sys.argv)>1 and sys.argv[1] == '--KMSDRM': 
    os.environ['SDL_VIDEODRIVER'] = 'KMSDRM'
elif len(sys.argv)>1 and sys.argv[1] == "--wayland": 
    os.environ['SDL_VIDEODRIVER'] = 'wayland'
    
while True:

    result = subprocess.Popen(["python3", "main.py"])
    result.communicate()

    if os.path.isfile("requested_action"):
        with open('requested_action', 'r') as f: 
            if f.readline() != 'restart':
                break
    else:
        exit()