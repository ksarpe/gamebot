import tkinter as tk
import tkinter.messagebox
from pytesseract import pytesseract
import constans
from logger import Logger
import random
from PIL import Image
import time
import pyautogui
import pydirectinput

SECONDS_TO_START = 3


class Fishbot:
    def __init__(self):
        pytesseract.tesseract_cmd = constans.PATH_TO_TESSARACT
        self.Logger = Logger()
        self.root = tk.Tk()
        self.initiate_tkwindow()
        self.online = False
        self.cast_amount = 0
        self.fishing = False
        self.win = self.get_win()

    def get_win(self):
        return pyautogui.getWindowsWithTitle("Podgląd w oknie (źródło) - game")[0]

    def initiate_tkwindow(self):
        self.root.title('Vezuna Fishbot by haxper v1.0')
        self.root.geometry("400x200+300+300")
        frm = tk.Frame(self.root, padx=10, pady=10)
        frm.grid()
        tk.Label(frm, text="Welcome hacker!").grid(column=0, row=0)
        tk.Button(frm, text="Start", command=self.set_online).grid(column=2, row=0)
        tk.Button(frm, text="Quit", command=self.quit).grid(column=3, row=0)

    def quit(self):
        self.root.destroy()
        self.Logger.log("[LOG] EXIT")
        exit(0)

    def set_online(self):
        tkinter.messagebox.showinfo(f"Let's start", f"Click okay, and then you have {SECONDS_TO_START} second to focus game window. "
                                                   "\nThis window will be destroyed\n")
        self.Logger.log("[LOG] Bot has been started")
        time.sleep(SECONDS_TO_START)
        self.online = True
        self.root.destroy()

    def is_fish(self, text):  # return boolean if its fish on the line
        print(text)
        for letter in text:
             if letter == '[' or letter == ']' or letter == 'W' or letter == 'V':
                return False
        return True

    def give_spaces(self, text):  # returns number of spaces to click
        if text == "":
            print("dont know")
            self.Logger.log("[LOG] " + str(self.cast_amount) + " went wrong, AI failed to read image")
            return 5
        for letter in text:
            if letter.isdigit():
                print("clicking " + letter)
                self.Logger.log('[AI] I guess I need to click ' + letter + ' times')
                return int(letter)

    def start(self):
        self.root.mainloop()

        while True:
            if self.online:
                start_time = time.time()
                self.cast_amount += 1
                self.Logger.log('[LOG] Cast number ' + str(self.cast_amount))
                pydirectinput.press('space')
                self.fishing = True
                time.sleep(5)
                self.Logger.log("[LOG] Waiting for fish")

                while self.fishing:
                    time.sleep(0.4)
                    pyautogui.screenshot("screen1.png", region=(self.win.left + constans.LEFT_OFFSET,
                                                                self.win.top + constans.TOP_OFFSET,
                                                                constans.WIDTH + 20, constans.HEIGHT))
                    img = Image.open("screen1.png")
                    text = pytesseract.image_to_string(img)

                    if self.is_fish(text):
                        clicks = self.give_spaces(text)
                        if clicks is None:
                            time.sleep(10)
                            self.fishing = False
                        self.Logger.log("Performing " + str(clicks) + " clicks")
                        random.uniform(2, 3.5)
                        for i in range(0, clicks):
                            pydirectinput.press("space")
                            random.uniform(0.1, 0.3)
                        self.fishing = False
                        self.Logger.log('[LOG] Fishing successful')
                        self.Logger.log('[LOG] Adding random delay...')
                        time.sleep(random.uniform(10, 12))

                    if time.time() - start_time > 45:
                        self.Logger.log('[LOG] Something went wrong, reseting bot...')
                        break



