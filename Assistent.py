import os
import asyncio
import threading

import tkinter as tk
import customtkinter
import tkinter as tk
from ttkthemes import ThemedStyle

import pinecone
import tiktoken
import openai

# Set the API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# set global variables
systemprompt = "You are a helpful assistant."
chatGPT_history = [{"role": "system", "content": systemprompt}]


class ChatWindow(customtkinter.CTkTextbox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag_config("user", foreground="#FFC107", justify="right")
        self.tag_config("bot", foreground="#8BC34A")
        self.configure(state="disabled", font=("Helvetica", 16))

    def add_message(self, message, sender):
        self.configure(state="normal")
        self.insert(tk.END, message + "\n", sender)
        self.see(tk.END)
        self.configure(state="disabled")


async def chat_gpt(message):
    """
    Uses OpenAI's GPT-3 language model to generate a response to a given message.

    Args:
    - message (str): the message to generate a response to

    Returns:
    - str: the generated response

    Raises:
    - ValueError: if the message is empty or None
    - openai.error.APIError: if there is an error communicating with the OpenAI API
    """
    # Check if message is empty or None
    if not message:
        raise ValueError("Message cannot be empty or None")

    # Append message to chat history
    chat_history = [] # assume chat history is a list of dictionaries
    chat_history.append({"role": "user", "content": message})

    try:
        # Generate response using OpenAI's GPT-3 language model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history
        )
        return response['choices'][0]['message']['content']
    except openai.error.APIError as e:
        # Handle error communicating with OpenAI API
        print(f"Error communicating with OpenAI API: {e}")
        return "Sorry, I'm having trouble generating a response right now. Please try again later."


async def send_message():
    message = input_field.get()

    # Clear the input field
    input_field.delete(0, tk.END)

    # Add the message to the chat history
    chat_history.add_message(message, "user")

    # Generate a response using OpenAI's chatGPT language model
    loop = asyncio.get_event_loop()
    answer = await loop.create_task(chat_gpt(message))
    
    chat_history.add_message(answer, "bot")

def send_message_callback():
    asyncio.run_coroutine_threadsafe(send_message(), loop)

root = customtkinter.CTk()
root.title("AI Assistant")

customtkinter.set_appearance_mode("dark")

# Creating Chat History
chat_history = ChatWindow(root, height=500, width=400) 
chat_history.pack(side=tk.TOP, padx=20, pady=20, fill=tk.BOTH, expand=True)

# Creating Input Field
input_frame = customtkinter.CTkFrame(root)
input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)

input_field = customtkinter.CTkEntry(input_frame, font=("Helvetica", 14))
input_field.pack(side=tk.LEFT, padx=10, pady=10, ipady=8, fill=tk.X, expand=True)

send_button = customtkinter.CTkButton(input_frame, text="Send", font=("Helvetica", 14), command=send_message_callback)
send_button.pack(side=tk.LEFT, padx=10, pady=10, ipady=7, ipadx=15)


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    thread = threading.Thread(target=start_loop, args=(loop,), daemon=True)
    thread.start()
    root.mainloop()
