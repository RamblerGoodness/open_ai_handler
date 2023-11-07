import openai
import os
import json


class OpenAIHandler:
    
    conversation = []
    functions = []
    temp = 0.0
    model = "gpt-3.5-turbo"

    def __init__(self, key=None):
        if self.key is None:
            raise Exception("OPENAI_KEY environment variable is not set")
        else:
            openai.api_key = self.key
        
        for file in os.listdir("functions"):
            if file.endswith(".json"):
                with open("functions/" + file, "r") as f:
                    self.functions.append(json.load(f))

    def message(self, prompt):

        self.conversation.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.conversation,
            temperature=self.temp,
            functions=self.functions,
            function_call = "auto"
        )

        if "function_call" in response["choices"][0]["message"]:
            self.conversation.append({"role": "system", "content": response["choices"][0]["message"]["function_call"]})
            chosen_function = eval(response.choices[0].message.function_call.name)
            params = json.loads(response.choices[0].message.function_call.arguments)
            response = self.function_return(chosen_function, params)
            self.conversation.append({"role": "system", "content": response["choices"][0]["message"]["content"]}) 

        else:
            self.conversation.append({"role": "system", "content": response["choices"][0]["message"]["content"]})


        return response["choices"][0]["message"]["content"]
    
    def function_return(self, function, params):

        self.conversation.append( {"role": "function", "name": function, "content": function(**params)})

        response = openai.ChatCompletion.create(
            model=self.model,
            message={"function_return": function(params)},
            temperature=self.temp,
            max_tokens=2000,
            functions=self.functions,
            function_call = "auto"
        )

        if "function_call" in response["choices"][0]["message"]:
            self.conversation.append({"role": "system", "content": response["choices"][0]["message"]["function_call"]})
            chosen_function = eval(response.choices[0].message.function_call.name)
            params = json.loads(response.choices[0].message.function_call.arguments)
            response = self.function_return(chosen_function, params)

        else:
            return response
