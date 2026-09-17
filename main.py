import ollama
import requests
import datetime

#model data
usedModel = "qwen3.5:9b"
currentDatetime = datetime.datetime.now()
systemPromptSetup = f'''You are Astrid, a local desktop assistant on a Windows 11 PC.
                    Current date/time: {currentDatetime}. 
                    User: Paul.
                    Rules:
                    - Be concise: 1-3 sentences. Plain text only, no markdown.
                    - Use tools for system actions. If no tool fits, say so — never pretend.
                    - Never invent tool results. Report only what tools actually returned.
                    - Ask one short question if a request is ambiguous.
                    - Confirm before anything destructive (deleting, overwriting, closing apps).
                    '''
# {memory_section} TODO add memory at some point


class Message:
    def __init__(self, role, content):
        self.role = role
        self.content = content

    def to_dictionary(self):
        return {"role": self.role, "content": self.content}

    # factory methods
    @classmethod
    def system(cls, content):
        return cls("system", content)

    @classmethod
    def user(cls, content):
        return cls("user", content)

    @classmethod
    def assistant(cls, content):
        return cls("assistant", content)

    @classmethod
    def tool(cls, content):
        return cls("tool", str(content))

    def __repr__(self):
        return f"Message({self.role!r}, {self.content!r})"


class MessageStack:
    def __init__(self, system_prompt=systemPromptSetup):
        self.messages = []
        if system_prompt:
            self.messages.append(Message.system(system_prompt))

    def add(self, message: Message):
        self.messages.append(message)
        return self  # lets you chain .add().add()

    def add_user(self, content):
        return self.add(Message.user(content))

    def add_assistant(self, content):
        return self.add(Message.assistant(content))

    def to_ollama_format(self):
        return [m.to_dictionary() for m in self.messages]


#Variables
runningModels = requests.get("http://localhost:11434/api/ps")
msgStack = MessageStack()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print(runningModels.content)
    # print(datetime.datetime.now())

    #Running Chat loop
    while True:
        inputMessage = input("Nachricht: ")
        msgStack.add_user(inputMessage)
        chat = ollama.chat(
            model=usedModel,
            messages=msgStack.to_ollama_format(),
            stream=True,
            think=False,
            options={
                "temperature": 0.6,   # creativity: 0.0 = deterministic, 1.0+ = loose
                "num_predict": 256,   # max tokens the model may generate per reply
                "num_ctx": 8192,      # context window size (how much it can "see")
            }
        )
        print()
        print("Astrid: ")
        response = ""

        for chunk in chat:
            token = chunk["message"]["content"]
            print(token, end="", flush=True)
            response += token
        msgStack.add_assistant(response)
        print("\n")

        # for chunk in chat:
        #     print(chunk['message']['content'], end='', flush=True)

    #response = ollama.chat(model=usedModel, messages=stack.to_ollama_format())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
