import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import threading
import time


# ==== Placeholder BitNet LLM backend ====
def bitnet_llm_respond(user_message: str) -> str:
    """
    Fake BitNet LLM response function.

    Replace this with real BitNet / other LLM integration.
    For now it just echoes and pretends to "think".
    """
    # Simulate thinking delay
    time.sleep(0.8)
    # Very simple dummy behavior
    if not user_message.strip():
        return "BitNet: Please type something so I can respond."
    return f"BitNet: I heard you say:\n{user_message}"


# ==== GUI app ====
class ChatApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window setup (600x400 as requested)
        self.title("BitNet Chat - deepseek style")
        self.geometry("600x400")
        self.minsize(600, 400)

        # Use a modern ttk theme if available
        try:
            self.style = ttk.Style(self)
            if "clam" in self.style.theme_names():
                self.style.theme_use("clam")
        except Exception:
            pass

        self.configure(bg="#0b1015")  # dark background similar to modern chat UIs

        self._build_layout()

    def _build_layout(self):
        # Top frame (title / header)
        header = tk.Frame(self, bg="#111827", height=40)
        header.pack(side=tk.TOP, fill=tk.X)

        header_label = tk.Label(
            header,
            text="chat.deepseek.com · BitNet LLM",
            fg="#e5e7eb",
            bg="#111827",
            font=("Segoe UI", 11, "bold"),
            padx=10,
        )
        header_label.pack(side=tk.LEFT, pady=8)

        # Main chat area
        main_frame = tk.Frame(self, bg="#0b1015")
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=(6, 4))

        self.chat_box = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg="#020617",
            fg="#e5e7eb",
            insertbackground="#e5e7eb",
            font=("Consolas", 10),
            relief=tk.FLAT,
        )
        self.chat_box.pack(fill=tk.BOTH, expand=True)

        # Input area
        input_frame = tk.Frame(self, bg="#020617")
        input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=8, pady=8)

        self.input_var = tk.StringVar()

        self.input_entry = tk.Entry(
            input_frame,
            textvariable=self.input_var,
            bg="#020617",
            fg="#e5e7eb",
            insertbackground="#e5e7eb",
            relief=tk.FLAT,
            font=("Segoe UI", 10),
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 4), pady=4)
        self.input_entry.bind("<Return>", self._on_send_event)

        send_button = tk.Button(
            input_frame,
            text="Send",
            command=self._on_send_click,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief=tk.FLAT,
            padx=12,
            pady=4,
        )
        send_button.pack(side=tk.RIGHT, padx=(4, 4), pady=4)

        # Initial system message
        self._append_message(
            "system",
            "Welcome to BitNet Chat.\nType a message below to talk to the BitNet LLM (placeholder).\n",
        )

        # Focus on input field initially
        self.after(200, lambda: self.input_entry.focus_set())

    # ==== Chat helpers ====
    def _append_message(self, sender: str, message: str):
        self.chat_box.config(state=tk.NORMAL)

        if sender == "user":
            tag = "user"
            prefix = "You: "
        elif sender == "assistant":
            tag = "assistant"
            prefix = "BitNet: "
        else:
            tag = "system"
            prefix = ""

        self.chat_box.insert(tk.END, prefix, (tag,))
        self.chat_box.insert(tk.END, message + "\n\n")

        # Styling for tags
        self.chat_box.tag_config("user", foreground="#a5b4fc")
        self.chat_box.tag_config("assistant", foreground="#6ee7b7")
        self.chat_box.tag_config("system", foreground="#9ca3af", font=("Segoe UI", 9, "italic"))

        self.chat_box.config(state=tk.DISABLED)
        self.chat_box.see(tk.END)

    def _on_send_event(self, event):
        self._on_send_click()

    def _on_send_click(self):
        user_text = self.input_var.get()
        if not user_text.strip():
            return

        self.input_var.set("")
        self._append_message("user", user_text)

        # Process the LLM response in another thread so GUI doesn't freeze
        threading.Thread(
            target=self._handle_llm_response,
            args=(user_text,),
            daemon=True,
        ).start()

    def _handle_llm_response(self, user_text: str):
        try:
            reply = bitnet_llm_respond(user_text)
        except Exception as e:
            reply = f"(Error from BitNet backend: {e})"

        self._append_message("assistant", reply)


if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()
