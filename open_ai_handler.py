import openai
import os
import json

#----------------------------------------#
# OpenAIHandler
# This class handles the OpenAI API.
#----------------------------------------#
class OpenAIHandler:
    key = None
    conversation = []
    functions = []
    temp = 0.0
    model = "gpt-3.5-turbo-1106"

    def __init__(self, key=None):
        if key == None:
            raise Exception("OPENAI_KEY environment variable is not set")
        else:
            self.key = key
            openai.api_key = self.key
        
        for file in os.listdir("functions"):
            if file.endswith(".json"):
                with open("functions/" + file, "r") as f:
                    try:
                        self.functions.append(json.load(f))
                    except: 
                        print("Error loading function " + file)
                        continue
        for fun in self.functions:
            print("Loaded function " + fun["function"]["name"])

    def message(self, prompt):
        
        self.conversation.append({
            "role": "user",
            "content": prompt
        })
        
        response = None

        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.conversation,
            temperature=self.temp,
            tools=self.functions,
            tool_choice= "auto"
        )

        self.conversation.append(response["choices"][0]["message"])

        if 'tool_calls' in response["choices"][0]["message"]:
            tool_call = response["choices"][0]["message"]["tool_calls"][0]
            function_name = eval(tool_call["function"]["name"])
            function_args = json.loads(tool_call["function"]["arguments"])
            content = function_name(**function_args)
            
            while "tool_calls" in response["choices"][0]["message"]:
                self.conversation.append({
                    "tool_call_id": tool_call["id"],
                    "role": "tool",
                    "name": tool_call["function"]["name"],
                    "content": content
                })

                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=self.conversation,
                    temperature=self.temp,
                    tools=self.functions,
                    tool_choice="auto"
                )
            
            return response["choices"][0]["message"]["content"]



        else:
            return response["choices"][0]["message"]["content"]
    
    


#----------------------------------------#
# Define functions here:
# after you define a function, add a 
# description of it to the functions folder
#----------------------------------------#

def hello_world():
    print("Hello World!")
    return "Hello World!"


#----------------------------------------#