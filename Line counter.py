
filenames = ["shortcut.py","rightclick.py","window.py","imageviewer.py","threeDimensional.py","sorts.py","clock.py",
             "tictactoe.py","main.py","wrapper.py","texteditor.py","python3.py","audioplayer.py",
             "videoplayer.py","terminal.py","functions.py","assets.py","textbox.py"]

c=0
c2=0
for i in filenames:
    f=open(i,"r")
    for j in f.readlines():
        c+=1
        for x in j:
            c2+=1
    f.close()

print(f"The OS is {c} lines of code and {c2} characters.")