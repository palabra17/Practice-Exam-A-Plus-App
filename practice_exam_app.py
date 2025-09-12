import tkinter as tk
from tkinter import messagebox
import csv
import random
import datetime

class ExamApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Palabra's 1101 A+ Practice Exam")
        self.master.configure(bg="#f0f8ff")
        self.questions = []
        self.current_question = 0
        self.score = 0
        self.user_answers = [None] * 90
        self.results = []

        self.header_label = tk.Label(master, text="Palabra's 1101 A+ Practice Exam", font=("Helvetica", 18, "bold"), bg="#f0f8ff", fg="#003366")
        self.header_label.pack(pady=10)

        self.question_counter_label = tk.Label(master, text="", font=("Helvetica", 12), bg="#f0f8ff", fg="#333333")
        self.question_counter_label.pack()

        self.question_label = tk.Label(master, wraplength=700, justify="left", font=("Helvetica", 14), bg="#f0f8ff", fg="#000000")
        self.question_label.pack(pady=20, padx=20)

        self.answer_var = tk.StringVar()
        self.radio_buttons = []

        for i in range(4):
            rb = tk.Radiobutton(master, text="", variable=self.answer_var, value="", anchor="w", justify="left",
                                bg="#f0f8ff", font=("Helvetica", 13), fg="#000000", selectcolor="#e6f2ff", activebackground="#d9eaff",
                                wraplength=700, padx=10, pady=10)
            rb.pack(fill="x", padx=40, pady=6)
            self.radio_buttons.append(rb)

        self.button_frame = tk.Frame(master, bg="#f0f8ff")
        self.button_frame.pack(pady=10)

        self.back_button = tk.Button(self.button_frame, text="Back", command=self.go_back,
                                     font=("Helvetica", 12), bg="#cccccc", fg="#000000")
        self.back_button.grid(row=0, column=0, padx=10)

        self.submit_button = tk.Button(self.button_frame, text="Submit", command=self.check_answer,
                                       font=("Helvetica", 12, "bold"), bg="#004080", fg="white",
                                       activebackground="#0059b3", activeforeground="white")
        self.submit_button.grid(row=0, column=1, padx=10)

        self.load_questions()
        self.display_question()

    def load_questions(self):
        try:
            with open("exam_questions.csv", newline='', encoding='utf-8-sig', errors='replace') as f:
                reader = csv.DictReader(f)
                all_questions = list(reader)
                random.shuffle(all_questions)
                self.questions = all_questions[:90]
                print(f"✅ Loaded {len(self.questions)} questions.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load questions: {e}")
            self.master.destroy()

    def display_question(self):
        self.answer_var.set(None)
        question_data = self.questions[self.current_question]

        self.question_counter_label.config(
            text=f"Question {self.current_question + 1} of {len(self.questions)}")

        self.question_label.config(text=f"{question_data['Question']}")

        choices = [question_data['OptionA'], question_data['OptionB'], question_data['OptionC'], question_data['OptionD']]
        for i, choice in enumerate(choices):
            self.radio_buttons[i].config(text=choice, value=choice)

        # Restore previous selection if any
        previous_answer = self.user_answers[self.current_question]
        if previous_answer:
            self.answer_var.set(previous_answer)

    def check_answer(self):
        selected = self.answer_var.get()
        if not selected:
            messagebox.showwarning("No Answer", "Please select an answer before submitting.")
            return

        question_data = self.questions[self.current_question]
        correct_letter = question_data['CorrectAnswer'].strip().upper()
        options = {
            'A': question_data['OptionA'],
            'B': question_data['OptionB'],
            'C': question_data['OptionC'],
            'D': question_data['OptionD']
        }
        correct_answer = options.get(correct_letter, "")
        explanation = question_data.get('Explanation', '')

        previously_correct = self.user_answers[self.current_question] == correct_answer
        self.user_answers[self.current_question] = selected

        if selected == correct_answer:
            if not previously_correct:
                self.score += 1
            messagebox.showinfo("Correct", f"✅ Correct!\n\nExplanation: {explanation}")
        else:
            if previously_correct:
                self.score -= 1
            messagebox.showerror("Incorrect", f"❌ Incorrect.\n\nCorrect Answer: {correct_answer}\n\nExplanation: {explanation}")

        self.results.append({
            'Question': question_data['Question'],
            'Selected': selected,
            'Correct Answer': correct_answer,
            'Explanation': explanation
        })

        self.current_question += 1
        if self.current_question < len(self.questions):
            self.display_question()
        else:
            self.show_result()

    def go_back(self):
        if self.current_question > 0:
            self.current_question -= 1
            self.display_question()

    def show_result(self):
        score_msg = f"✅ Exam complete!\n\nYour score: {self.score} out of {len(self.questions)}"
        messagebox.showinfo("Exam Finished", score_msg)
        self.save_results()
        self.master.quit()

    def save_results(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"exam_results_{now}.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Question', 'Your Answer', 'Correct Answer', 'Explanation'])
            for entry in self.results:
                writer.writerow([entry['Question'], entry['Selected'], entry['Correct Answer'], entry['Explanation']])
            writer.writerow([])
            writer.writerow([f"Final Score: {self.score} out of {len(self.questions)}"])

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("850x650")
    app = ExamApp(root)
    root.mainloop()
