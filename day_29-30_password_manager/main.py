import json
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip


# ---------------------------- GENERATE PASSWORD ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    pyperclip.copy(password)

    password_entry.delete(0, END)
    password_entry.insert(0, password)

# ---------------------------- LOAD SAVED DATA ------------------------------- #

def load_saved_data():
    try:
        with open("my_secret_passwords.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return

# ---------------------------- DISPLAY WEBSITE INFO ------------------------------- #

def display_website_info():
    website = website_entry.get()
    saved_data = load_saved_data()
    if not saved_data:
        messagebox.showwarning(title="No file", message="No file found.")
    else:
        website_info = look_up_entry(saved_data, website)
        if website_info:
            messagebox.showinfo(title=website, message=website_info)
        else:
            messagebox.showinfo(title=website, message="No information available.")


        

# ---------------------------- LOOK UP ENTRY ------------------------------- #
def look_up_entry(saved_data, website):
    try:
        if website in saved_data:
            existing_entry = f"\nUsername: {saved_data[website]['username']}" \
                            f"\nPassword: {saved_data[website]['password']}"
            return existing_entry
    except TypeError:
        return False

# ---------------------------- VALIDATE USER INPUT ------------------------------- #
def validate_user_input():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if not website and username and password:
        message = f"All fields must be filled in."
        messagebox.showwarning(title="Missing value(s)!", message=message)
    else:
        new_entry = {website: {"username": username, "password": password}}
        add_or_update(new_entry, website)


# ---------------------------- ADD NEW ENTRY ------------------------------- #

def add_or_update(new_entry, website):
    saved_data = load_saved_data()
    if not saved_data:
        save_to_file(new_entry)
    else:
        existing_entry = look_up_entry(saved_data, website)
        if not existing_entry:
            saved_data.update(new_entry)
            save_to_file(saved_data)
        else:
            if messagebox.askyesno(
                    title="Entry already exists!", message=f"An entry for {website} already exists."
                                                           f"Do you want to overwrite it?\n{existing_entry}"):
                saved_data.update(new_entry)
                save_to_file(saved_data)
            else:
                messagebox.showinfo(title="Cancelled!", message="Information was not updated.")

# ---------------------------- SAVE TO FILE ------------------------------- #

def save_to_file(entries_to_save):
    with open("my_secret_passwords.json", "w") as file:
        json.dump(entries_to_save, fp=file, indent=4)
        website_entry.delete(0, END)
        username_entry.delete(0, END)
        password_entry.delete(0, END)
        username_entry.insert(END, "myemail@mydomain.com")
        messagebox.showinfo(title="Success!", message="Information successfully saved!")

# ---------------------------- UI SETUP ------------------------------- #
# Window
window = Tk()
window.title("Password Manager")
window.config(bg="white", pady=20, padx=20)

# Canvas
canvas = Canvas(width=200, height=200, highlightthickness=0, bg="white")

# Image canvas
myimg = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=myimg)

# User input components
website_label = Label(text="Website:", bg="white")
website_entry = Entry(window, width="35")

username_label = Label(text="Email/Username:", bg="white")
username_entry = Entry(window, width="35")
username_entry.insert(END, "myemail@mydomain.com")

password_label = Label(text="Password:", bg="white")
password_entry = Entry(window, width="21")

# Buttons
button_search = Button(
    text="Search",
    fg="black",
    bg="white",
    command=display_website_info)

button_generate = Button(
    text="Generate password",
    fg="black",
    bg="white",
    command=generate_password
)
button_add = Button(
    text="Add",
    width="36",
    fg="black",
    bg="white",
    command=validate_user_input)

# Layout
canvas.grid(row=0, column=1)

website_label.grid(row=1, column=0)
website_entry.grid(row=1, column=1, sticky="EW", pady="4")
button_search.grid(row=1, column=2, padx=(4, 0))
website_entry.focus()

username_label.grid(row=2, column=0)
username_entry.grid(row=2, column=1, columnspan=2, sticky="EW", pady="4")

password_label.grid(row=3, column=0)
password_entry.grid(row=3, column=1, sticky="EW", pady="4")
button_generate.grid(row=3, column=2, padx=(4, 0))

button_add.grid(row=4, column=1, columnspan=2, sticky="EW", pady="4")

# Run
window.mainloop()
