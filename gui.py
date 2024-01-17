import tkinter as tk
from tkinter import Label, Canvas, Button, Text
from word_list import word_list as words
import random
import time
import datetime

YELLOW = "#FFECAF"
ORANGE = "#FFB07F"
PINK = "#FF52A2"
PURPLE = "#5F0F40"
class TypingSpeed_GUI:
    def __init__(self, master):
        self.master = master
        master.title("Typing Speed Test")
        #master.geometry("1000x600")
        master.config(bg=YELLOW, padx=25, pady=25)

        self.errors = 0
        self.right_words = []
        self.typed_words_list = []
        self.typed_word = ""
        number_of_words = 50
        self.words = random.sample(words, number_of_words)  # Add your word list

        self.create_widgets()
        self.countdown_seconds = 60
        self.countdown_running = False
        self.stop_countdown = False
        self.space_pressed = False

    def create_widgets(self):
        self.title_label = Label(self.master, text="Typing Speed Test", font=("Courier", 30, "bold"), fg=PURPLE, bg=PINK, padx=10, pady=10)
        self.title_label.grid(row=0, column=0)
        self.canvas = Canvas(self.master, width=1000, height=90, bg=YELLOW, highlightthickness=0)
        #self.title_canvas = self.canvas.create_text(500, 20, text="Typing Speed Test", fill=PURPLE, font=("Arial", 30, "bold"))
        self.time_canvas = self.canvas.create_text(250, 55, text="Time left: 60", fill=PINK, font=("Arial", 10, "bold"))
        self.error_canvas = self.canvas.create_text(50, 55, text=f"Errors: {self.errors}", fill=PINK, font=("Arial", 10, "bold"))
        self.wpm_canvas= self.canvas.create_text(500, 55, text=f"WPM: {len(self.right_words)}", fill=PINK, font=("Arial", 10, "bold"))

        self.canvas.grid(row=1, column=0, pady=5)

        self.restart_button = Button(self.master, text="Restart", font=("Arial", 10, "bold"), fg=YELLOW, bg=PINK, pady=5, command=self.restart)
        self.restart_button.grid(row=1, column=1, pady=5)

        self.words_box = Text(self.master, width=70, height=8, font=("Arial", 12), fg=PURPLE, wrap="word", state="disabled")
        self.words_box
        self.words_box.grid(row=2, column=0, columnspan=2, pady=5)

        self.typing_entry = Text(self.master, width=60, height=8, font=("Arial", 15), fg=PURPLE)
        self.typing_entry.grid(row=3, column=0, columnspan=2, pady=10)

    # ---------------------------- RESTART ------------------------------- #
    def restart(self):
        # Add logic to restart the typing test
        self.stop_countdown = True
        self.countdown_running = False
        self.errors = 0
        self.right_words = []
        self.countdown_seconds = 60
        self.typing_entry.delete("1.0", "end")

    # ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
    def countdown(self, seconds):
        """Counts down from the given seconds"""
        self.canvas.itemconfig(self.time_canvas, text=f"Time left: {self.countdown_seconds}")
        if self.countdown_seconds > 0 and not self.stop_countdown:
            self.master.after(1000, self.countdown, self.countdown_seconds)
            self.countdown_seconds -= 1

    # ---------------------------- START COUNTDOWN ------------------------------- #
    def start_countdown(self):
        # Start countdown in a separate thread
        self.countdown(60)

    def key_press(self, event):
        if not self.countdown_running:
            # Start the countdown only if it's not already running
            self.countdown_running = True
            self.stop_countdown = False
            self.start_countdown()
        # char_typed = event.char.lower()
        # self.char_typed += char_typed
        self.space_pressed = False
        self.end_of_word = False


    def space_press(self, event):
        print("Space pressed")
        # Get the current word typed
        current_typing = self.typing_entry.get("1.0", "end-1c").strip().lower().split()
        # Get the new word typed from the first to the last
        self.typed_word = current_typing[len(self.typed_words_list):]
        self.typed_words_list.extend(self.typed_word)

        print("Typed words:", self.typed_words_list)
        print("Word:", self.typed_word)
        self.space_pressed = True


