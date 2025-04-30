import tkinter as tk
from tkinter import scrolledtext
from parser import parse_intent
from executor import execute_intents
from data.accessibility_tree import accessibility_tree

class JoyBotApp:
    def __init__(self, root):
        self.tree = accessibility_tree 

        root.title("JoyBot AI")
        root.geometry("700x500")
        root.resizable(False, False)

        self.dialogue = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, width=80, font=("Arial", 10))
        self.dialogue.insert(tk.END, "JoyBot: Hi! How can I help you today?\n")
        self.dialogue.config(state='disabled')
        self.dialogue.place(x=20, y=20)

        self.entry = tk.Entry(root, width=70, font=("Arial", 12))
        self.entry.place(x=20, y=370)
        self.entry.bind("<Return>", self.handle_input)

        self.action_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=7, width=40, font=("Arial", 9))
        self.action_box.insert(tk.END, "🔍 Action History:\nActions performed will appear here...\n")
        self.action_box.config(state='disabled')
        self.action_box.place(x=380, y=260)

        self.action_label = tk.Label(root, text="Action Window", font=("Arial", 12, "bold"))
        self.action_label.place(x=520, y=230)

    def log_dialogue(self, text):
        self.dialogue.config(state='normal')
        self.dialogue.insert(tk.END, f"{text}\n")
        self.dialogue.config(state='disabled')

    def log_action(self, text):
        self.action_box.config(state='normal')
        self.action_box.insert(tk.END, f"{text}\n")
        self.action_box.config(state='disabled')

    def handle_input(self, event=None):
        user_input = self.entry.get().strip()
        if not user_input:
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
