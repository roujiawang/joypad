import tkinter as tk
from tkinter import scrolledtext
from parser import parse_intent
from executor import execute_intents

import tkinter as tk
from tkinter import scrolledtext

class JoyBotApp:
    def __init__(self, root):
        root.title("JoyBot AI")
        root.geometry("700x500")
        root.resizable(False, False)

        LEFT_WIDTH = 350  # Fixed width for left elements (input, button, dialogue)

        # Dialogue window (left half)
        self.dialogue = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, height=18, width=43, font=("Arial", 10)
        )
        self.dialogue.insert(tk.END, "JoyBot: Hi! How can I help you today?\n")
        self.dialogue.config(state='disabled')
        self.dialogue.place(x=20, y=10, width=LEFT_WIDTH)

        # Input field (matching width with dialogue and button)
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(
            root, textvariable=self.entry_var, width=43, font=("Arial", 12), fg="grey"
        )
        self.entry.insert(0, "Type your command here...")
        self.entry.place(x=20, y=370, width=LEFT_WIDTH)

        # Send button underneath input field (same width as input box)
        self.send_button = tk.Button(
            root, text="Send", width=43, font=("Arial", 10), command=self.handle_input,
            bg="#007BFF", fg="white", activebackground="#0056b3", activeforeground="white"
        )
        self.send_button.place(x=20, y=405, width=LEFT_WIDTH)

        # Action label (right top corner)
        self.action_label = tk.Label(root, text="Action Window", font=("Arial", 12, "bold"))
        self.action_label.place(x=420, y=10)

        # Action history window (right side, taking up 2/3 of right half)
        self.action_box = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, height=18, width=32, font=("Arial", 9)
        )
        self.action_box.insert(tk.END, "🔍 Action History:\nActions performed will appear here...\n")
        self.action_box.config(state='disabled')
        self.action_box.place(x=400, y=40)

        # Search-related keywords window (remaining 1/3 height of the right side)
        self.search_box = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, height=9, width=32, font=("Arial", 9)
        )
        self.search_box.insert(tk.END, "🔍 Search Keywords:\nEnter keywords to search...\n")
        self.search_box.config(state='disabled')
        self.search_box.place(x=400, y=290)  # Place it below the action box, taking the remaining space

        # Placeholder behavior
        self.entry.bind("<FocusIn>", self.clear_placeholder)
        self.entry.bind("<FocusOut>", self.restore_placeholder)

    def clear_placeholder(self, event):
        if self.entry_var.get() == "Type your command here...":
            self.entry_var.set("")  # Clear the placeholder when the input field is focused
            self.entry.config(fg="black")  # Change text color to black when typing

    def restore_placeholder(self, event):
        if self.entry_var.get().strip() == "":
            self.entry_var.set("Type your command here...")  # Restore placeholder if input is empty
            self.entry.config(fg="grey")  # Change text color back to grey for the placeholder

    def log_dialogue(self, text):
        self.dialogue.config(state='normal')
        self.dialogue.insert(tk.END, f"{text}\n")
        self.dialogue.config(state='disabled')

    def log_action(self, text):
        # Update the action history window
        self.action_box.config(state='normal')
        self.action_box.insert(tk.END, f"{text}\n")
        self.action_box.config(state='disabled')

        # Update the search-related window (can be modified for keywords if necessary)
        self.search_box.config(state='normal')
        self.search_box.insert(tk.END, f"{text}\n")
        self.search_box.config(state='disabled')

    def handle_input(self, event=None):
        user_input = self.entry.get().strip()
        if not user_input or user_input == "Type your command here...":
            return
        self.log_dialogue(f"You: {user_input}")
        self.entry.delete(0, tk.END)

        intents = parse_intent(user_input)
        if not intents:
            self.log_dialogue("JoyBot: Sorry, I couldn't parse that.")
        else:
            self.log_dialogue("JoyBot: Let me take care of that...")
            execute_intents(intents, self.log_action)

if __name__ == "__main__":
    root = tk.Tk()
    app = JoyBotApp(root)
    root.mainloop()
