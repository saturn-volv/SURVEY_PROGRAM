"""
    WARNING: THIS PROGRAM ONLY WORKS WITH WINDOWS.

    IF YOU WANT TO TURN OFF THE PROGRAM, ENTER INTO TASK MANAGER, 
    FIND BACKGROUND PROCESSES, AND FIND THE "program.exe" WITH A PYTHON LOGO. 
    
    KILL PROCESS WILL TURN IT OFF.

    IF YOU WISH FOR THIS PROGRAM TO EMBED ITSELF INTO YOUR STARTUP,
    INCLUDE A FILE CALLED "yesplease.txt".

    THIS WILL ALLOW THIS PROGRAM TO EXIST IN YOUR PC WITHOUT NEEDING TO BE TURNED ON EVERYTIME.
"""

import os
import sys
import shutil
import keyboard
from nava import play
from nava import stop
from nava import stop_all
from nava import Engine
from tkinter import *
from PIL import Image
from PIL import ImageSequence
from PIL import ImageTk

file_name = os.path.basename(sys.executable)
cwd = os.getcwd()


# TRANSLATES TO THE LOCAL DIRECTORY OF THE EXECUTABLE
def local_dir(rel_dir):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, rel_dir)

# LOOKS FOR THE YESPLEASE.TXT AND CHECKS THAT THE CURRENT PROGRAM IS RUNNING FROM AN EXECUTABLE
if os.path.exists(f'{cwd}/yesplease.txt') and file_name != 'python.exe':
    # GETS THE USERNAME FOR THE PC
    username = os.getlogin()
    # FINDS THE "LOAD PROGRAMS ON STARTUP" FOLDER
    startup_folder = f'C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
    if cwd != startup_folder:
        print('Adding file to startup')
        # ADDS THE PROGRAM TO STARTUP.
        shutil.copy(f'{cwd}/{file_name}', startup_folder)
    pass


KEY_WORD = "GASTER"
token = ""

timeElapsed = 0
frame_index = 0
# CALLBACK WHEN THE KEY WORD IS TYPED.
def on_keyword_typed():
    global timeElapsed
    global frame_index
    global update_animation
    keyboard.press_and_release('F5')
    keyboard.press_and_release('Ctrl+R')
    play(local_dir('assets\\snd_mysterygo.wav'), engine=Engine.WINSOUND, async_mode=False)
    timeElapsed = 0
    frame_index = 0
    update_animation()


# CALLBACK ON WHEN A KEY IS PRESSED.
def on_press(e):
    key_pressed = e.name
    global token
    if key_pressed == 'backspace':
        token = token[:len(token)-1]
    if len(key_pressed) > 1: return
    token = token + key_pressed
    if len(token) > 6:
        token = token[1:]
    if len(token) == 6:
        global on_keyword_typed
        if token.upper() == KEY_WORD:
            on_keyword_typed()
            token = ""
def on_exit():
    global root
    global quitting
    quitting = True
    root.destroy()
    stop_all()
    exit()

# ADDS THE CALLBACK FOR KEYSTROKES
keyboard.on_press(on_press)
keyboard.add_hotkey('Ctrl+Shift+6', on_exit)
image = Image.open(local_dir('assets\\caption.gif'))

root = Tk()
root.title("WHEN I")

root.overrideredirect(True)

root.wm_attributes('-transparentcolor', 'green')
root.wm_attributes('-topmost', 1)

screen_size = (root.winfo_screenwidth(), root.winfo_screenheight())

canvas = Canvas(root, offset="200,200", width=screen_size[0], height=screen_size[1], bg="green", highlightthickness=0)
canvas.pack()

img_frames = [ImageTk.PhotoImage(frame.convert('RGBA')) for frame in ImageSequence.Iterator(image)]

quitting = False
sound = None
def update_animation():
    global sound
    global timeElapsed
    global frame_index
    canvas.delete('all')
    if quitting or timeElapsed >= 9000:
        stop(sound)
        return

    canvas.create_image(screen_size[0]/2 - image.width/2,screen_size[1]/2-image.height/2, anchor=NW, image=img_frames[frame_index])
    if frame_index == 0 and timeElapsed == 0:
        sound = play(local_dir('assets\\mus_st_him.wav'), engine=Engine.WINSOUND, async_mode=True, loop=True)
    timeElapsed += 30
    frame_index = (frame_index+1)%len(img_frames)
    root.after(30, update_animation)

root.mainloop()

# MAKES SURE THE PROGRAM STAYS RUNNING
# input()