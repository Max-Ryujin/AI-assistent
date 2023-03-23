import os
import asyncio
import threading

import backend

import tkinter as tk
import customtkinter
import tkinter as tk
from ttkthemes import ThemedStyle

import openai

# Set the API key
openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatWindow(customtkinter.CTkTextbox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag_config("user", foreground="#FFC107", justify="right")
        self.tag_config("bot", foreground="#8BC34A")
        self.configure(state="disabled", font=("Helvetica", 16))

    def add_message(self, message, sender):
        self.configure(state="normal")
        #make sure words don't get cut off into a new line
        self.configure(width=1)
        self.configure(wrap=tk.WORD)
        self.insert(tk.END, message + "\n", sender)
        self.see(tk.END)
        self.configure(state="disabled")

def open_settings():
    # Create a new window for settings
    settings_window = customtkinter.CTkToplevel(root)
    settings_window.title("Settings")
    settings_window.minsize(300, 400)
    #set spawnn location
    settings_window.geometry("+%d+%d" % (root.winfo_rootx() + 100, root.winfo_rooty() + 100))
    #place settings window on top of main window
    settings_window.transient(root)

    close_button = customtkinter.CTkButton(settings_window, text="Close", command=settings_window.destroy)
    close_button.pack(side=tk.BOTTOM,pady=10)


    dropdown = customtkinter.CTkComboBox(settings_window, values=["gpt-3.5-turbo", "gpt-4 (not available yet)"])


    dropdown.pack(side=tk.TOP, pady=10)
   



async def send_message():
    message = input_field.get()

    # Clear the input field
    input_field.delete(0, tk.END)

    # Add the message to the chat history
    chat_history.add_message(message, "user")

    # Add the message to the chat history
    message_with_context = backend.add_context_to_message(message)
    # Save the message to the chat history
    backend.save_message(message)
    # Generate a response using OpenAI's chatGPT language model
    loop = asyncio.get_event_loop()
    answer = await loop.create_task(backend.chat_gpt(message_with_context))
    
    chat_history.add_message(answer, "bot")

    

def send_message_callback():
    asyncio.run_coroutine_threadsafe(send_message(), loop)

def handle_return_key(event):
    send_message_callback()

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

if __name__ == "__main__":
    root = customtkinter.CTk()
    root.title("AI Assistant")

    customtkinter.set_appearance_mode("dark")
    root.minsize(400, 700)


    # Creating Chat History
    chat_history = ChatWindow(root, height=500, width=400) 
    chat_history.pack(side=tk.TOP, padx=20, pady=20, fill=tk.BOTH, expand=True)

    # Creating Input Field
    input_frame = customtkinter.CTkFrame(root)
    input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)

    input_field = customtkinter.CTkEntry(input_frame, font=("Helvetica", 14))
    input_field.pack(side=tk.LEFT, padx=10, pady=10, ipady=8, fill=tk.X, expand=True)
    input_field.bind("<Return>", handle_return_key)

    # Creating Send Button
    send_button = customtkinter.CTkButton(input_frame,width=35, text="=>", font=("Helvetica", 24), command=send_message_callback)
    send_button.pack(side=tk.LEFT, padx=5, pady=10, ipady=6, ipadx=0)

    # Creating Settings Button
    settings_button = customtkinter.CTkButton(input_frame, text="...",width=20, fg_color="grey", font=("Helvetica", 20), command=open_settings)
    settings_button.pack(side=tk.LEFT, padx=5, pady=10, ipady=6, ipadx=0)

    loop = asyncio.get_event_loop()
    thread = threading.Thread(target=start_loop, args=(loop,), daemon=True)
    thread.start()
    root.mainloop()
