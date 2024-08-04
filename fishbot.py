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
from inputs import press_key, release_key

SECONDS_TO_START = 3

class Fishbot:
    def __init__(self):
        pytesseract.tesseract_cmd = constans.PATH_TO_TESSARACT  # path to tessaract used by pytessaract
        self.Logger = Logger()  # initiate logger for errors
        self.root = tk.Tk()  # initialize TK
        self.initiate_tkwindow()  # Start fishbot by showing tk window
        self.online = False  # Whole casting loop
        self.fishing = False  # Loop for waiting for fishies
        self.win = self.get_win()  # get OBS window to read text from

    def get_win(self):
        return pyautogui.getWindowsWithTitle("XenoxMt2.com")[0]  # get OBS window name

    def initiate_tkwindow(self):
        self.root.title('Xenox Fishbot by haxper v1.0')
        self.root.geometry("400x200+300+300")
        frm = tk.Frame(self.root, padx=10, pady=10)
        frm.grid()
        tk.Label(frm, text="Welcome hacker!").grid(column=0, row=0)
        tk.Button(frm, text="Start", command=self.set_online).grid(column=2, row=0)
        tk.Button(frm, text="Quit", command=self.quit).grid(column=3, row=0)

    def quit(self):
        # While click quit on TK window
        self.root.destroy()
        exit(0)

    def set_online(self):
        # While click start on TK window
        tkinter.messagebox.showinfo(f"Let's start", f"Click okay, and then you have {SECONDS_TO_START} second to focus game window. "
                                                   "\nThis window will be destroyed\n")
        time.sleep(SECONDS_TO_START)  # Add delay for user to focus game window
        self.online = True  # set bot loop to true
        self.root.destroy()  # destroy TK window

    def is_fish(self, text):
        # if read text contains one of these chars, just return False because its not correct sentence, else TRUE
        for letter in text:
             if letter == '[' or letter == ']' or letter == 'W' or letter == 'V' or letter == '|':
                return False
        return True

    def give_spaces(self, text):  # returns number of spaces to click
        if text == "":
            # If text is recognized as empty, return random 1-5 int?
            self.Logger.log("Text not recognized")
            return random.randint(1, 5)
        for letter in text:
            #if text is recognized as correct one, try to find digit and return it.
            if letter.isdigit():
                print("Clicking " + letter + " times.")
                return int(letter)

    def start(self):
        # Loop for tkinter
        self.root.mainloop()

        while True:
            # Fishing while bot is started
            if self.online:
                start_time = time.time()  # start time of the initial cast
                pydirectinput.press('1')
                time.sleep(random.uniform(0.2, 0.4))
                pydirectinput.press('space')  # Space for cast
                self.Logger.log("Clicking 1 and space")
                self.fishing = True  # since now fishing is started
                time.sleep(5)  # Sleep 5 second because anyway fishing takes longer

                while self.fishing:
                    time.sleep(0.4)  # Sleep 0.4s between each screenshot
                    pyautogui.screenshot("screen1.png", region=(self.win.left + constans.LEFT_OFFSET,
                                                                self.win.top + constans.TOP_OFFSET,  # Take screenshot of window set in the constants file
                                                                constans.WIDTH + 20, constans.HEIGHT))
                    img = Image.open("screen1.png")  # Open image that was taken
                    text = pytesseract.image_to_string(img)  # try to read text from it

                    if self.is_fish(text):  # if text is recognized as correct
                        self.Logger.log(f"Text has been found: {text}")
                        clicks = self.give_spaces(text)  # Try to get how many times we need to click
                        if clicks is None:  # if we couldn't get integer value from text
                            self.Logger.log("Couldn't get clicks, empty text.")
                            time.sleep(10)  # Wait for player to reset himself
                            self.fishing = False  # Set fishing to false and prevent loop going
                            continue  # break below code, continuing will start from the initial cast
                        time.sleep(random.uniform(2, 3.5))  # if all is ok, wait some second before getting fish
                        for i in range(0, clicks):
                            pydirectinput.press('space')  # Space for cast
                            self.Logger.log(f"{i+1} space for catching a fish")
                            time.sleep(random.uniform(0.1, 0.2))
                        self.fishing = False  # self next iteration to false
                        time.sleep(random.uniform(7, 9))  # add some sleep after getting a fish.

                    if time.time() - start_time > 50:  # if we didn't get any good screen till start
                        break  # break loop and wish that player is ready to cast again
