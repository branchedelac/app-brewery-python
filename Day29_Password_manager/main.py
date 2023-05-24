from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip


# ---------------------------- GENERATE PASSWORD ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
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


# ---------------------------- SAVE ENTRY ------------------------------- #
def save():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if website and username and password:
        with open("my_secret_passwords.txt", "a") as file:
            file.write(f"{website} | {username} | {password}\n")
            website_entry.delete(0, END)
            username_entry.delete(0, END)
            password_entry.delete(0, END)
            username_entry.insert(END, "myemail@mydomain.com")
            messagebox.showinfo(title="Success!", message="Password successfully saved!")
    else:
        messagebox.showwarning(title="Missing value(s)!", message=f"All fields must be filled in.")




# ---------------------------- UI SETUP ------------------------------- #
# Window
window = Tk()
window.title("Password Manager")
window.config(bg="#d5ebf6", pady=20, padx=20)

# Canvas
canvas = Canvas(width=200, height=200, highlightthickness=0, bg="#d5ebf6")

# Image canvas
myimg = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=myimg)

# User input components
website_label = Label(text="Website:",  bg="#d5ebf6")
website_entry = Entry(window, width="35")

username_label = Label(text="Email/Username:",  bg="#d5ebf6")
username_entry = Entry(window, width="35")
username_entry.insert(END, "myemail@mydomain.com")


password_label = Label(text="Password:", bg="#d5ebf6")
password_entry = Entry(window, width="21")

# Buttons
button_generate = Button(
    text="Generate password",
    fg="black", bg="white", activeforeground="black",
    activebackground="#f6feff",
    command=generate_password
)
button_save = Button(
    text="Save",
    width="36",
    fg="black",
    bg="white",
    activeforeground="black",
    activebackground="#f6feff",
    command=save)

# Layout
canvas.grid(row=0, column=1)

website_label.grid(row=1, column=0)
website_entry.grid(row=1, column=1, columnspan=2, sticky="EW", pady="4")
website_entry.focus()

username_label.grid(row=2, column=0)
username_entry.grid(row=2, column=1, columnspan=2, sticky="EW", pady="4")

password_label.grid(row=3, column=0)
password_entry.grid(row=3, column=1, sticky="EW", pady="4")
button_generate.grid(row=3, column=2, padx=(4,0))

button_save.grid(row=4, column=1, columnspan=2, sticky="EW", pady="4")

# Run
window.mainloop()
