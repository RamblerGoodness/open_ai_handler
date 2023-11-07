# OpenAIHandler

This Python script, `open_ai_handler.py`, is a handler for OpenAI's GPT-3 model. It is designed to facilitate the interaction with the model by managing the conversation history and the API key. This is meant to be a easy-start for your A.I. projects.

## Features

- **API Key Management**: The script requires an API key to interact with OpenAI's API. The key is passed during the initialization of the `OpenAIHandler` class. If no key is provided, an exception is raised.

- **Conversation Management**: The script maintains a list of conversation history. Each message from the user is appended to this list before making a request to the API.

- **Function Management**: The script loads JSON files from the `functions` directory and stores them in a list. These functions can be used in the conversation with the model.

- **Temperature Control**: The script allows for the control of the randomness of the model's responses through the `temp` attribute.

- **Model Selection**: The script uses the GPT-3 model by default, but this can be changed by modifying the `model` attribute.

## Usage

To use this script, initialize the `OpenAIHandler` class with your OpenAI API key. Then, use the `message` method to send prompts to the model. The method will append your message to the conversation history and send a request to the API. The response from the API is then returned by the method.

```python
handler = OpenAIHandler(key="your-api-key")
response = handler.message("Hello, world!")
```

## Example

Included is a helloworld.py example where you can prompt open_ai from your console.

```python

from open_ai_handler import OpenAIHandler as handler
from dotenv import load_dotenv
import os

load_dotenv()

api = os.getenv("OPENAI_KEY")
ai = handler(key=api)

while True:
    prompt = input("You: ")
    print("Bot: " + ai.message(prompt))

```
