import tkinter as tk
from tkinter import filedialog
from pynput.keyboard import Listener as KeyboardListener, Key
import pyautogui
import csv
import time
import os
from datetime import datetime

recordedActions = []
keyboardListener = None
isRecording = False
macrosDir = "Macros"
lastActionTime = None

def macroDir():
    if not os.path.exists(macrosDir):
        os.makedirs(macrosDir)

def toggleRecording():
    global isRecording, keyboardListener, lastActionTime
    if not isRecording:
        # Reset lastActionTime when starting
        lastActionTime = datetime.now()
        keyboardListener = KeyboardListener(on_press=onPress)
        keyboardListener.start()
        toggleButton.config(text="Stop Recording")
        statusLabel.config(text="Recording...")
        isRecording = True
    else:
        if keyboardListener:
            keyboardListener.stop()
        macroDir()
        filePath = os.path.join(macrosDir, 'macro_' + time.strftime("%Y%m%d-%H%M%S") + '.csv')
        writeCSV(filePath, recordedActions)
        toggleButton.config(text="Start Recording")
        statusLabel.config(text="Recording stopped. Actions saved.")
        isRecording = False
        recordedActions.clear()  # Clear recorded actions after saving

def onPress(key):
    global lastActionTime
    current_time = datetime.now()
    x, y = pyautogui.position()
    delay = 0

    if lastActionTime is not None:
        delay = (current_time - lastActionTime).total_seconds()

    if hasattr(key, 'char') and key.char == 'g': # No click
        recordedActions.append((x, y, 0, delay))  
    elif hasattr(key, 'char') and key.char == 'f':  # Click
        recordedActions.append((x, y, 1, delay))  

    lastActionTime = current_time
     def readCSV(filePath):
        with open(filePath, 'r') as file:
            reader = csv.reader(file)
            return [(int(x), int(y), int(click), float(delay)) for x, y, click, delay in reader]
    
    def playMacro():
        filePath = filedialog.askopenfilename(initialdir=macrosFolder, title="Select Macro File", filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))
        if filePath:
            actions = readCSV(filePath)
            for x, y, click, delay in actions:
                pyautogui.moveTo(x, y, duration=delay)  # Use 'delay' for the duration of the move
                if click:
                    pyautogui.click()
    
    root = tk.Tk()
    root.title("Macro Recorder")
    root.geometry("300x200")
    root.configure(bg="#151515")
    
    toggleButton = tk.Button(root, text="Start Recording", command=toggleRecording)
    toggleButton.pack()
    
    playButton = tk.Button(root, text="Play Macro", command=playMacro)
    playButton.pack()
    
    statusLabel = tk.Label(root, text="Press 'Start Recording' to begin")
    statusLabel.pack()
    
    root.mainloop()
