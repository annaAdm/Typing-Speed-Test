from tkinter import Tk
from gui import TypingSpeed_GUI

import random

if __name__ == "__main__":
    root = Tk()
    gui = TypingSpeed_GUI(root)

    root.bind('<Key>', gui.key_press)
    # root.bind('<space>', gui.space_press)
    # root.bind('<BackSpace>', gui.backspace_press)
    # root.bind('<Return>', gui.enter_press)
    root.bind('<space>', gui.space_press)
    root.mainloop()
