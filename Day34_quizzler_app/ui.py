from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"

class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain

        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(bg=THEME_COLOR, pady=20, padx=20)
        self.score = Label(text="Score: 0", fg="white", bg=THEME_COLOR)

        self.canvas = Canvas(width=300, height=250)
        self.question = self.canvas.create_text(
            150,
            125,
            text="Question will be here!",
            font=("Arial", 14, "italic"),
            width=280
        )

        true_image = PhotoImage(file="images/true.png")
        false_image = PhotoImage(file="images/false.png")

        self.button_true = Button(
            image=true_image,
            command = self.true_pressed
        )
        self.button_false = Button(
            image=false_image,
            command= self.false_pressed
        )

        # Layout
        self.score.grid(row=0, column=1)
        self.canvas.grid(row=1, column=0,columnspan=2, pady=50)
        self.button_true.grid(row=2, column=0)
        self.button_false.grid(row=2, column=1)

        # Run
        self.get_next_question()
        self.window.mainloop()

    def get_next_question(self):
        self.canvas.configure(bg="white")
        self.score.configure(text= f"Score: {self.quiz.score}/{self.quiz.question_number}")
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question, text=q_text)
        else:
            self.canvas.itemconfig(
                self.question,
                text="Congratulations! You've reached the end of the quiz!"
            )
            self.button_true.config(state="disabled")
            self.button_false.config(state="disabled")


    def true_pressed(self):
        is_right = self.quiz.check_answer("True")
        self.give_feedback(is_right)

    def false_pressed(self):
        is_right = self.quiz.check_answer("False")
        self.give_feedback(is_right)

    def give_feedback(self, is_right):
        if is_right:
            self.canvas.configure(bg="green")
        else:
            self.canvas.configure(bg="red")
        self.window.after(1000, self.get_next_question)
