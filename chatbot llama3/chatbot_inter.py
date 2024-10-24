import tkinter as tk
from threading import Thread
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = '''
Answer the question below.
Here is the conversation history: {context}
Question: {question}
Answer:
'''

model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI ChatBot")
        
        self.root.configure(bg='darkgray')

        self.context = ""
        self.is_generating = False
        self.font_size = 18

        self.text_area = tk.Text(root, wrap='word', state='disabled', height=20, font=("Arial", self.font_size), bg='lightgray')
        self.text_area.pack(padx=10, pady=10, expand=True, fill='both')

        self.text_area.tag_config("user", background="#83D883", font=("Arial", self.font_size))
        self.text_area.tag_config("bot", background="#ADD8E6", font=("Arial", self.font_size))

        self.entry = tk.Entry(root, font=("Arial", self.font_size), bg='white')
        self.entry.pack(padx=10, pady=10, fill='x')

        self.send_button = tk.Button(root, text="Enviar", command=self.handle_input, font=("Arial", self.font_size))
        self.send_button.pack(pady=5)

        self.entry.bind("<Return>", self.handle_input)

        self.root.bind("<Control-MouseWheel>", self.zoom)

        self.entry.focus()

    def handle_input(self, event=None):
        user_input = self.entry.get()
        if user_input.lower() == "exit":
            self.root.quit()

        if user_input.strip():
            self.entry.delete(0, tk.END)

            self.text_area.config(state='normal')
            self.text_area.insert(tk.END, f"You: {user_input}\n\n", "user")
            self.text_area.config(state='disabled')

            self.is_generating = True
            Thread(target=self.respond_to_user, args=(user_input,)).start()

    def respond_to_user(self, user_input):
        response = ""
        self.text_area.config(state='normal')
        
        for word in chain.stream({"context": self.context, "question": user_input}):
            if not self.is_generating:
                break
            response += word
            self.text_area.insert(tk.END, word, "bot")
            self.text_area.yview(tk.END)
            self.root.update_idletasks()

        self.text_area.insert(tk.END, "\n\n", "bot")
        self.text_area.config(state='disabled')

        self.context += f"\nUser: {user_input}\nAI: {response}\n"

    def stop_generation(self):
        self.is_generating = False

    def zoom(self, event):
        if event.delta > 0:
            self.font_size += 1
        elif event.delta < 0:
            self.font_size = max(8, self.font_size - 1)

        self.update_font()

    def update_font(self):
        self.text_area.config(font=("Arial", self.font_size))
        self.text_area.tag_config("user", font=("Arial", self.font_size))
        self.text_area.tag_config("bot", font=("Arial", self.font_size))
        self.entry.config(font=("Arial", self.font_size))
        self.send_button.config(font=("Arial", self.font_size))

if __name__ == '__main__':
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
