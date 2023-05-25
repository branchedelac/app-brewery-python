import os

import pandas
from tkinter import *
from tkinter import messagebox
import random

words_to_learn_path = "data/words_to_learn.csv"
full_vocabulary_path = "data/french_words.csv"
from_lang = "French"
to_lang = "English"
current_card = {}
words = {}

# ---------------------------- PARSE DATA FROM FILE ------------------------------- #
def parse_vocabulary_files(full_vocabulary_path, words_to_learn_path):
    global words

    # Open file
    try:
        file = open(words_to_learn_path, encoding='utf-8')
    except FileNotFoundError:
        try:
            file = open(full_vocabulary_path, encoding='utf-8')
        except FileNotFoundError:
            sys.exit("No vocabulary data file found.")

    # Parse file
    try:
        data = pandas.read_csv(file)
        words = data.to_dict(orient="records")
        file.close()
    except pandas.errors.EmptyDataError:
        parse_vocabulary_files(full_vocabulary_path, "")

# ---------------------------- METHODS ------------------------------- #
def get_next_card(remove_current_from_list):
    global current_card, flip_timer
    window.after_cancel(flip_timer)

    if remove_current_from_list:
        update_word_list(current_card)

    if words:
        current_card = random.choice(words)
        canvas.itemconfig(card, image=front_img)
        canvas.itemconfig(title, text=from_lang,fill="black")
        canvas.itemconfig(word, text=current_card[from_lang], fill="black")
        flip_timer = window.after(3000, show_translation)
    else:
        if messagebox.askokcancel(title="Congratulations!", message="You have learned all the words! Do you want to start over?"):
            parse_vocabulary_files(full_vocabulary_path, "")
            get_next_card(remove_current_from_list=False)
        else:
            sys.exit()


def update_word_list(current_card):
    words.remove(current_card)
    data = pandas.DataFrame.from_dict(words)
    with open("data/words_to_learn.csv", "w", encoding='utf-8') as f:
        data.to_csv(f, index=False, lineterminator='\n')


def show_translation():
    canvas.itemconfig(card, image=back_img)
    canvas.itemconfig(title, text=to_lang, fill="white")
    canvas.itemconfig(word, text=current_card[to_lang], fill="white")
# ---------------------------- UI SETUP ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"

# Window
window = Tk()
window.title("Flashy")
window.config(bg="#B1DDC6", pady=50, padx=20)
flip_timer = window.after(3000, show_translation)

# Canvas
canvas = Canvas(width=1000, height=600, bg="#B1DDC6", highlightthickness=0)

# Cards
front_img = PhotoImage(file='images/card_front.png')
back_img = PhotoImage(file='images/card_back.png')

card = canvas.create_image(500, 300, image=front_img)
title = canvas.create_text(500, 150, text="Title", font=("Arial", 40, "italic"))
word = canvas.create_text(500, 300, text="Word", font=("Arial", 60, "bold"))

# Buttons
img_x = PhotoImage(file="images/wrong.png")
button_x = Button(
    image = img_x,
    highlightthickness = 0,
    command = lambda: get_next_card(remove_current_from_list= False))

img_check = PhotoImage(file="images/right.png")
button_check = Button(
    image = img_check,
    highlightthickness = 0,
    command = lambda: get_next_card(remove_current_from_list= True))

# Layout
canvas.grid(row=0, column=0, columnspan=2)

button_x.grid(row=1, column=0)
button_check.grid(row=1, column=1)

# Run
parse_vocabulary_files(full_vocabulary_path, words_to_learn_path)
get_next_card(remove_current_from_list= False)

window.mainloop()