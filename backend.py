import openai
import pandas as pd
import numpy as np
import os
from openai.embeddings_utils import cosine_similarity

# set global variables
systemprompt = "You are a helpful assistant."
chatGPT_history = [{"role": "system", "content": systemprompt}]


# embedding model parameters
embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
max_tokens = 8000  # the maximum for text-embedding-ada-002 is 8191

# output dimensions: 1536


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
    chatGPT_history.append({"role": "user", "content": message})
    try:
        # Generate response using OpenAI's GPT-3 language model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chatGPT_history
        )
        return response['choices'][0]['message']['content']
    except openai.error.APIError as e:
        # Handle error communicating with OpenAI API
        print(f"Error communicating with OpenAI API: {e}")
        return "Sorry, I'm having trouble generating a response right now. Please try again later."


def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    embedding = openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']
    return embedding
 
def add_context_to_message(message):
    message_new =  "These are messages that I sent earlier. you can use them if needed to help me: \n " 
    context = find_relevent_messages(message)
    for i in context:
        message_new += i + "\n -------- \n"
    message = message_new + "My prompt: " + message
    return message

def find_relevent_messages(message, n=3):
    """

    Finds the most relevant messages in the chat history.

    Returns:
    - list: the most relevant messages in the chat history
    """
    # Find the most relevant messages in the chat history
    #load the chat history from history.csv file in the memory folder
    chat_history = load_csv("memory/history.csv")
    chat_history["embedding"] = chat_history.embedding.apply(eval).apply(np.array)
    # Get the embedding for the message
    message_embedding = get_embedding(message)

    chat_history['similarities'] = chat_history.embedding.apply(lambda x: cosine_similarity(x, message_embedding))
    res = chat_history.sort_values('similarities', ascending=False).head(n)
    return res["message"].tolist()


# Load CSV file containing messages and embeddings
def load_csv(filename):
    try:
        #check if file is empty
        if os.stat(filename).st_size == 0:
            return pd.DataFrame(columns=["message", "embedding"])
        else:
            return pd.read_csv(filename)
    except FileNotFoundError:
        # If the file doesn't exist yet, return an empty data frame
        return pd.DataFrame(columns=["message", "embedding"])


def save_message(message):
    """
    Saves the message to the chat history.

    Args:
    - message (str): the message to save to the chat history
    """
    # cut the message down to 8000 tokens and only take the first 8000 tokens
    message = message[:4000]

    embedding = get_embedding(message)

    # Create DataFrame with new message and embedding
    new_data = pd.DataFrame({
        "message": [message],
        "embedding": [embedding]
    })


    existing_data = load_csv("memory/history.csv")

    # Append new data to existing data and save to CSV file
    combined_data = existing_data.append(new_data)
    combined_data.to_csv("memory/history.csv", index=False)
