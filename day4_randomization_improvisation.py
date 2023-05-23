import tkinter
import random

with open("source_text.txt", errors="ignore") as st:
    source_text = st.read()
    words = source_text.lower().split(" ")

def button_clicked():
    text.delete("1.0", "end")
    poem, title = write_poem(words)
    text.insert(tkinter.END, poem)
    my_label.config(text=title)

def write_poem(words):
    poem = []
    for s in range(3):
        for r in range(4):
            row = []
            for i in range(6):
                row.append(words[random.randint(0, len(words))])
                row_string = " ".join(row).capitalize()
            poem.append(row_string)
            if r == 3:
                poem.append("")
                if s == 1:
                    title = " ".join(row[2:5]).title()

    return "\n".join(poem), title

window = tkinter.Tk()
window.title("Poetry generator")
window.minsize(width=500, height=500)

my_label = tkinter.Label(text="My Poem", font=("Arial", 24, "bold"))
my_label.pack()

button = tkinter.Button(text="Click to generate poem", command=button_clicked)
button.pack(pady = (20, 20))

text = tkinter.Text(window, height=20, width=50)
text.pack()

window.mainloop()