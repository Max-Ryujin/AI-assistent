# Personal AI Assistant

This is a Python-based personal AI assistant that uses the chatGPT API for natural language processing and generation. It is designed to provide helpful responses to users' questions or commands, and will store a memory of previous conversations using embedding vectors for improved responses in the future. The program also utilizes CustomTkinter for a simple chat GUI.

## Setup

Before running the program, you will need to set up your environment variables with your OpenAI API key.

To do this:

1. Sign up for OpenAI [here](https://platform.openai.com/signup/).
2. Once you have created an account, navigate to your [dashboard](https://platform.openai.com/account/usage).
3. Click on the "API Keys" tab on the left-hand side of the page.
4. Create a new API key by clicking on the "Create New API Key" button.
5. Copy the API key that is generated.
6. Search for "Environment Variables" in the Windows search bar and select "Edit the system environment variables".
7. Click on the "Environment Variables" button in the bottom right corner.
8. Under "System Variables", click "New".
9. Set the variable name to "OPENAI_API_KEY".
10. Set the variable value to your OpenAI API key.
11. Click "OK" to save.

## Running the Program

To run the personal AI assistant program, simply execute the following command in your terminal:

```python Assistant.py```

This will launch the CustomTkinter chat GUI, where you can start interacting with the personal AI assistant.

## Dependencies

The following Python packages are required to run the program:

    OpenAI
    CustomTkinter

You can install these dependencies using pip:

```pip install openai```
```pip install CustomTkinter```

## Future Development

In the future, I plan to implement memory for the personal AI assistant using embedding vectors for older messages. This will allow the assistant to provide even more helpful responses to user queries over time.