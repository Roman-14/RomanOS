def collidePygameRect(pRect, mousePos):
    if mousePos[0]>pRect.x and mousePos[1]>pRect.y and mousePos[0]<(pRect.x+pRect.w) and mousePos[1]<(pRect.y+pRect.h):
        return True
    return False


import platform
import subprocess

def set_system_volume(volume_percentage):
    system_platform = platform.system()
    volume_percentage = max(0, min(100, volume_percentage))  # Ensure volume is within 0-100 range

    if system_platform == 'Windows':
        try:
            import ctypes
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(volume_percentage / 100, None)
            print(f"Volume set to {volume_percentage}% on Windows.")
        except FileNotFoundError:
            print("Please download and place 'nircmd.exe' in your system PATH.")

    elif system_platform == 'Darwin':
        try:
            # Set the volume on macOS using the 'osascript' command
            subprocess.run(["osascript", "-e", f'set volume output volume {volume_percentage}'])
            print(f"Volume set to {volume_percentage}% on macOS.")
        except FileNotFoundError:
            print("macOS volume control is not supported.")

    elif system_platform == 'Linux':
        try:
            # Set the volume on Linux using the 'amixer' command (adjust 'amixer' as per your system)
            subprocess.run(["amixer", "set", "Master", f"{volume_percentage}%"])
            print(f"Volume set to {volume_percentage}% on Linux.")
        except FileNotFoundError:
            print("Linux volume control is not supported.")

    else:
        print("Unsupported operating system.")

