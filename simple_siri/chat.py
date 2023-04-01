import os
import sys
import openai
import subprocess
from collections import deque
import speech_recognition as sr

from .prompts import get_applescript_prompt


class Conversation:
    """A class to hold the conversation state and methods to interact with it.
    Args: OPENAI_API_KEY (str): The API key for OpenAI.
    Attributes: messages (deque): A deque of the messages in the conversation.
                system_prompt (list): An initial prompt with insturctions and few-shot examples.
                num_requests (int): The number of requests made to OpenAI. Used to rate limit.
                request_limit (int): The maximum number of requests allowed per session.
    Methods: rate_limit: Increments num_requests and exits if it exceeds request_limit.
                llm: Sends a request to OpenAI and returns the response.
                ask: Sends a request to OpenAI and appends the response to messages.
                execute: Executes the code in the last message.
                get_input: Gets input from the user for requested action.
                converse: Runs the conversation loop.
    """

    def __init__(self, OPENAI_API_KEY, trust_the_code=False):
        # Set the API key
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
        openai.api_key = os.getenv("OPENAI_API_KEY")
        # Set the trust the code flag. If True, the code will be executed without asking the user.
        self.trust_the_code = trust_the_code
        # Initialize the conversation state
        self.messages = deque(maxlen=5)
        self.system_prompt = [
            {"role": "user", "content": get_applescript_prompt()},
        ]
        # For now, let's only allow ten requests per session
        self.num_requests = 0
        self.request_limit = 10

    def rate_limit(self):
        self.num_requests += 1
        if self.num_requests > self.request_limit:
            sys.exit("Request limit exceeded")

    def llm(self):
        # Send a request to OpenAI and return the response
        response = dict(
            openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.system_prompt + list(self.messages),
                temperature=0.2,
                # stop=["```End-of-code."],
            )["choices"][0]["message"]
        )
        self.rate_limit()
        return response

    def ask(self, request, language="Applescript"):
        # Send a request to OpenAI and append the response to messages
        request = {
            "role": "user",
            "content": f"""X: {request}.
                Language: {language}.""",
        }
        self.messages.append(request)
        response = self.llm()
        self.messages.append(response)
        print(response["content"])

    def execute(self, language="Applescript"):
        # Execute the code in the last message
        code = self.messages[-1]["content"].split("```")[-2]
        if language == "Applescript":
            script_file = "code.scpt"
        elif language == "Bash":
            script_file = "code.sh"
        else:
            raise ValueError("Language not supported")

        with open(script_file, "w") as f:
            f.write(code)

        if language == "Applescript":
            output = subprocess.run(
                f"osascript {script_file}", shell=True, capture_output=True
            )
        elif language == "Bash":
            output = subprocess.run(
                f"/bin/bash {script_file}", shell=True, capture_output=True
            )
        else:
            raise ValueError("Language not supported")

        if output.returncode != 0:
            print(output.stdout.decode("utf-8"))
            output = self.try_correction(code, output, language)
        return output

    def get_input(self, how):
        # Get input from the user for requested action
        if how == "text":
            request = input("What would you like me to do?: ")
        elif how == "voice":
            # obtain audio from the microphone
            r = sr.Recognizer()
            r.pause_threshold = 0.5
            print("Listening...")
            with sr.Microphone() as source:
                print("What would you like me to do?")
                audio = r.listen(source)
            print("Done listening!")
            # write audio to a WAV file
            with open("recording.wav", "wb") as f:
                f.write(audio.get_wav_data())

            audio_file = open("recording.wav", "rb")
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            request = transcript.text
        return request

    def converse(self, how, request=None, language="Applescript"):
        # Run the conversation loop
        while True:
            request = request if request is not None else self.get_input(how)
            if request.lower() == "exit":
                break
            self.ask(request, language=language)
            # For safety, and since this is a toy, ask if the user wants to execute the code
            do_execute = "y" if self.trust_the_code else input("Execute? (y/n) ")
            if do_execute == "y":
                output = self.execute(language)
                if output.returncode != 0:
                    # If the Applescript didn't execute, try to do it in Bash instead
                    print("Error: ", output.stderr.decode("utf-8"))
                    if language != "Bash":
                        self.converse(how, request=request, language="Bash")
            request = None

    def try_correction(self, code, prev_output, language):
        """A correction loop that asks the LLM to correct the code. Asks for reasons why the code
        failed to provide context for the correction.
        """
        # Loading a new model to give the option to try a different one
        llm = lambda x: openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            # stop=["```End-of-code."],
            messages=[
                {"role": "user", "content": x},
            ],
        )["choices"][0]["message"]["content"]
        # Ask for reasons why the code failed
        get_reason = f"""The code below gives the error "{prev_output.stderr.decode("utf-8")}".
        ```
        {code}
        ```
        Provide 2 or more reasons why this error would occur.
        """
        reason = llm(get_reason)
        # Ask the LLM to correct the code
        get_correction = (
            get_reason
            + reason
            + f"Provide the corrected {language}. Code should start and end with triple backticks like this: ```<code>```End-of-code."
        )
        print(reason)
        fixed_code = llm(get_correction).split("```")[-2]
        print(fixed_code)
        # Write the corrected code to a file and ask if the user wants to execute it
        if language == "Applescript":
            script_name = "code_correction.scpt"
            command = "osascript code_correction.scpt"
        elif language == "Bash":
            script_name = "code_correction.sh"
            command = "/bin/bash code_correction.sh"
        else:
            raise ValueError("Language not supported")
        with open(script_name, "w") as file:
            file.write(fixed_code)
        do_execute = "y" if self.trust_the_code else input("Execute? (y/n) ")
        if do_execute == "y":
            return subprocess.run(command, shell=True, capture_output=True)
        else:
            return prev_output


if __name__ == "__main__":
    how = "text"
    conversation = Conversation()
    conversation.converse()
