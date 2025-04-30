import tkinter as tk
from tkinter import scrolledtext
from parser import parse_intent
from executor import execute_intents
from data.accessibility_tree import accessibility_tree

class JoyBotApp:
    def __init__(self, root):
        self.tree = accessibility_tree

        # Window setup
        root.title("JoyBot AI")
        root.geometry("700x500")
        root.resizable(False, False)

        # === LEFT SIDE (50% width of window, ~350px) ===

        # Dialogue box
        self.dialogue = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, width=48, font=("Arial", 10))
        self.dialogue.insert(tk.END, "JoyBot: Hi! How can I help you today?\n")
        self.dialogue.config(state='disabled')
        self.dialogue.place(x=20, y=20)

        # Input field with placeholder
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(root, textvariable=self.entry_var, width=48, font=("Arial", 12), fg="grey")
        self.entry.insert(0, "Type your command here...")
        self.entry.place(x=20, y=400)

        # Placeholder behavior
        self.entry.bind("<FocusIn>", self.clear_placeholder)
        self.entry.bind("<FocusOut>", self.restore_placeholder)
        self.entry.bind("<Return>", self.handle_input)

        # Send button (below input)
        self.send_button = tk.Button(root, text="Send", width=46, font=("Arial", 10), command=self.handle_input)
        self.send_button.place(x=20, y=430)

        # === RIGHT SIDE ===

        # Action label (top-left of right half)
        self.action_label = tk.Label(root, text="Action Window", font=("Arial", 12, "bold"))
        self.action_label.place(x=390, y=10)

        # Top: Action log window (timestamped messages)
        self.action_log = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, width=35, font=("Arial", 9))
        self.action_log.insert(tk.END, "")
        self.action_log.config(state='disabled')
        self.action_log.place(x=390, y=40)

        # Bottom: Action summary/search window
        self.action_summary = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=8, width=35, font=("Arial", 9))
        self.action_summary.insert(tk.END, "🔍 Action History:\nActions performed will appear here...\n")
        self.action_summary.config(state='disabled')
        self.action_summary.place(x=390, y=310)

    def clear_placeholder(self, event):
        if self.entry_var.get() == "Type your command here...":
            self.entry_var.set("")
            self.entry.config(fg="black")

    def restore_placeholder(self, event):
        if self.entry_var.get().strip() == "":
            self.entry_var.set("Type your command here...")
            self.entry.config(fg="grey")

    def log_dialogue(self, text):
        self.dialogue.config(state='normal')
        self.dialogue.insert(tk.END, f"{text}\n")
        self.dialogue.config(state='disabled')

    def log_action(self, text):
        self.action_log.config(state='normal')
        self.action_log.insert(tk.END, f"{text}\n")
        self.action_log.config(state='disabled')

        self.action_summary.config(state='normal')
        self.action_summary.insert(tk.END, f"{text}\n")
        self.action_summary.config(state='disabled')

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
            execute_intents(self.tree, intents, self.log_action)

if __name__ == "__main__":
    root = tk.Tk()
    app = JoyBotApp(root)
    root.mainloop()
