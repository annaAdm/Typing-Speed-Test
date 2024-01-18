import tkinter as tk
from tkinter import Label, Canvas, Button, Text
from word_list import word_list as words
import random

GREY = "#F0F0F0"
PINK = "#FF52A2"
L_BLUE = "#38F6FC"
PURPLE = "#5F0F40"
class TypingSpeed_GUI:
    def __init__(self, master, *args, **kwargs):
        self.master = master
        master.title("Typing Speed Test")
        master.config(bg=GREY, padx=25, pady=25)

        self.errors = 0
        self.cpm = 0
        self.wpm = 0
        self.i = 0
        with open("data.txt", mode="w") as file:
            file.write("0")
        with open("data.txt") as file:
            self.high_score = int(file.read())
        self.right_words = []
        self.typed_words_list = []
        self.typed_word = ""
        self.number_of_words = 300
        self.words = random.sample(words, self.number_of_words)  # Add your word list

        self.create_widgets()
        self.countdown_seconds = 60
        self.countdown_running = False
        self.stop_countdown = False

    def create_widgets(self):
        self.title_label = Label(self.master, text="Typing Speed Test", font=("Courier New", 30, "bold"), fg=GREY, bg=PINK, padx=10, pady=10)
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10)
        self.canvas = Canvas(self.master, width=1500, height=200, bg=GREY, highlightthickness=0)
        self.time_canvas = self.canvas.create_text(250, 55, text="Time left: 60", fill=PINK, font=("Arial", 12, "bold"))
        self.error_canvas = self.canvas.create_text(50, 55, text=f"Errors: {self.errors}", fill=PINK, font=("Arial", 12, "bold"))
        self.wpm_canvas = self.canvas.create_text(500, 55, text=f"WPM: {""}", fill=PINK, font=("Arial", 12, "bold"))
        self.cpm_canvas = self.canvas.create_text(750, 55, text=f"Score: {""}", fill=PINK, font=("Arial", 12, "bold"))
        self.highscore_label = Label(self.master, text=f"Best score: {self.high_score} ", font=("Arial", 12, "bold"), fg=PURPLE, bg=L_BLUE, padx=5, pady=5)
        self.highscore_label.grid(row=0, column=1)

        self.end_game_canvas = Canvas(self.master, width=0, height=0, bg=L_BLUE, highlightthickness=0)
        self.end_game_canvas.grid(row=1, column=0, pady=5)

        self.canvas.grid(row=1, column=0, pady=5)

        self.restart_button = Button(self.master, text="Restart", font=("Arial", 12, "bold"), fg=GREY, bg=PINK, pady=5, padx=5, command=self.restart, highlightthickness=0, bd=0)
        self.restart_button.grid(row=1, column=1)

        self.words_box = Text(self.master, width=70, height=8, font=("Arial", 15), fg=PURPLE, wrap="word")
        # Enable the Text widget so that we can insert content into it
        self.words_box.config(state="normal")
        for word in self.words:
            self.words_box.insert("end", word + ", ")
        # Disable the Text widget so that the user can't edit it
        self.words_box.config(state="disabled")
        self.words_box.grid(row=2, column=0, columnspan=2, pady=5)

        self.typing_entry = Text(self.master, width=70, height=6, font=("Arial", 15), fg=PURPLE)
        self.typing_entry.config(fg=PINK)
        self.typing_entry.insert("end", "Start typing here...",)
        self.typing_entry.grid(row=3, column=0, columnspan=2, pady=5)

    # ---------------------------- RESTART ------------------------------- #
    def restart(self):
        # Add logic to restart the typing test
        self.stop_countdown = True
        self.countdown_running = False
        self.errors = 0
        self.right_words = []
        self.typed_words_list = []
        self.typed_word = ""
        self.i = 0
        self.cpm = 0
        self.wpm = 0
        self.countdown_seconds = 60
        self.words = random.sample(words, self.number_of_words)
        self.words_box.config(state="normal")
        self.words_box.delete("1.0", "end")
        for word in self.words:
            self.words_box.insert("end", word + ", ")
        self.words_box.config(state="disabled")
        self.canvas.itemconfig(self.error_canvas, text=f"Errors: {self.errors}")
        self.canvas.itemconfig(self.wpm_canvas, text=f"WPM: {self.wpm}")
        self.canvas.itemconfig(self.time_canvas, text=f"Time left: {self.countdown_seconds}")
        self.canvas.itemconfig(self.cpm_canvas, text=f"Score: {self.cpm}")
        self.typing_entry.config(fg=PINK)
        self.typing_entry.config(state="normal")
        self.typing_entry.delete("1.0", "end")  # Delete all the previous text"
        self.typing_entry.insert("end", "Start typing here...", )  # Add the text "Start typing here..."
        if hasattr(self, "end_game_canvas"):
            for widget in self.end_game_canvas.winfo_children():
                widget.destroy()
            self.end_game_canvas.grid_forget()

    # ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
    def countdown(self, seconds):
        """Counts down from the given seconds"""
        self.canvas.itemconfig(self.time_canvas, text=f"Time left: {self.countdown_seconds}")
        if self.countdown_seconds > 0 and not self.stop_countdown:
            self.countdown_seconds -= 1
            self.master.after(1000, self.countdown, self.countdown_seconds)

        if self.countdown_seconds == 0 and not self.stop_countdown:
            self.countdown_running = False
            self.stop_countdown = True
            self.master.after(1000, self.countdown, self.countdown_seconds)

            self.typing_entry.config(state="disabled")
            self.check_highscore()
            self.timesup()
    # ---------------------------- TIME'S UP ------------------------------- #

    def timesup(self):
        self.end_game_canvas.grid(row=1,column=0,columnspan=3,pady=5)
        Label(self.end_game_canvas, text="TIME's UP!", font=("Arial", 15, "bold"), fg=PURPLE, bg=L_BLUE, padx=2, pady=2).grid(row=2, column=0,columnspan=3, pady=5)
        Label(self.end_game_canvas, text=f"Your score: {self.cpm}\nYou can type {self.wpm} words per minute!\nYou did {self.errors} typing errors.",
              font=("Arial", 15, "bold"), fg=PURPLE, bg=L_BLUE, padx=10, pady=10).grid(row=3, column=0,columnspan=3, pady=5)
    # ---------------------------- CHECK HIGHSCORE ------------------------------- #

    def check_highscore(self):
        """ Checks if the current score is higher than the high score and updates the high score """
        if self.cpm > self.high_score:
            self.high_score = self.cpm
            with open("data.txt", mode="w") as file:
                file.write(str(self.high_score))
        self.highscore_label.config(text=f"Best score: {self.high_score} ")

    # ---------------------------- START COUNTDOWN ------------------------------- #
    def start_countdown(self):
        # Start countdown in a separate thread
        self.countdown(60)

    # ---------------------------- CLICK PRESS ------------------------------- #
    def click_press(self, event):
        if event and not self.countdown_running:
            self.typing_entry.delete("1.0", "end")  # Delete the text "Start typing here..."
            self.typing_entry.config(fg=PURPLE)

    # ---------------------------- KEY PRESS ------------------------------- #
    def key_press(self, event):
        if not self.countdown_running:
            # Start the countdown only if it's not already running
            self.countdown_running = True
            self.stop_countdown = False
            self.start_countdown()

    # ---------------------------- SPACE PRESS ------------------------------- #
    def space_press(self, event):
        if self.countdown_running:
            self.catch_word()

    def catch_word(self):
        current_typing = self.typing_entry.get("1.0", "end-1c").strip().lower().split()
        # Get the new word typed from the first char,to the last char before the space (the space is not included)
        # all the word is lowercase, without spaces, the space is the delimiter between words
        # Get the last word typed, from the length of the list of words typed.
        self.typed_word = current_typing[len(self.typed_words_list):]  # from the item[len(list)] to the end
        self.typed_words_list.extend(self.typed_word)  # Add the new word to the list of words typed
        # print("Typed words:", self.typed_words_list)
        # print("Word:", self.typed_word)
        self.check_word()
        # print("Words:", self.words)

    # ---------------------------- CHECK WORD ------------------------------- #
    def check_word(self):
        typed_words = self.typing_entry.get("1.0", "end-1c").strip().lower()
        self.typed_word = self.typing_entry.get("1.0", "end-1c").strip().lower().split()

        start_index = self.words_box.search(self.words[self.i], '1.0', stopindex="end")
        end_index = f"{start_index}+{len(self.words[self.i])}c"

        try:
            if self.words[self.i] == self.typed_words_list[self.i]:
                self.right_words.append(self.typed_word)
                print("Right words:", len(self.right_words))
                # underline the right word in words_box in turquoise
                # For correct words
                self.words_box.tag_add("correct", start_index, end_index)
                self.words_box.tag_config("correct", underline=1, foreground=L_BLUE)

            else:
                self.errors += 1
                print("Typed word:", self.typed_words_list[self.i], "Right word was:", self.words[self.i])
                self.canvas.itemconfig(self.error_canvas, text=f"Errors: {self.errors}")
                # underline the wrong word in words_box in pink
                self.words_box.tag_add("wrong", start_index, end_index)
                self.words_box.tag_config("wrong", underline=1, foreground=PINK)

            # move to the next word
            self.i += 1
        except IndexError:
            pass

        # Calculate CPM and WPM
        total_char = len(self.typing_entry.get("1.0", "end-1c").replace(" ", ""))
        self.cpm = round(((total_char / 60) * 60), 2)
        self.wpm = round(((self.cpm / 5) / 1), 2)

        # Update the display
        self.canvas.itemconfig(self.wpm_canvas, text=f"WPM: {self.wpm}")
        self.canvas.itemconfig(self.cpm_canvas, text=f"Score: {self.cpm}")

