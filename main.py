from tkinter import Tk
from gui import TypingSpeed_GUI

import random

if __name__ == "__main__":
    root = Tk()
    gui = TypingSpeed_GUI(root)

    print(len(gui.words))
    root.bind('<Key>', gui.key_press)
    root.mainloop()
