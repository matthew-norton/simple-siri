# Simple Jarvis
What can you make with an LLM and a few hours of prompt engineering? A minimal LLM-based Siri-like assistant (for MacOS) is what I ended up with. Can interact with it over text or via voice commands (using OpenAI's Whisper API). It uses ChatGPT to auto-generate and execute Applescript (or a Bash script) for accomplishing tasks. NOTE: Executing code is dangerous, so I recommend you review the code before executing (you will be prompted with a y/n choice when code is generated) or only use this on a test machine.

The assistant can do a variety of simple tasks. Try to ask it to:
1) Send an email: "Send an email to X with the subject Y and the body Z. Also include a list of good home remedies for a cold."
2) Send a text message: "Send a text message to X saying blah blah blah."
3) Search the web: "Search the web for X."
4) Search Wikipedia: "Search Wikipedia for X."
5) Search YouTube: "Search YouTube for X."
6) Search Google Maps: "Search Google Maps for X."
7) Open a file
8) Open an application
9) Add events to your calendar
10) Set reminders
11) Display the time
12) Display someones phone number from your contacts

You can do some surprisingly complex things with this mini-assistant. For example, you can ask it to "Open up a new document in the numbers app. Then add a table with information about 10 countries with columns for name, official language, and continent."

## How to use it
1) Install the requirements: `pip install -r requirements.txt`
2) Run the assistant: `python main.py`
3) Choose whether you want to interact with it via text or voice commands when prompted.
4) Enter your OpenAI API key when prompted.
5) It will show you the code it generated and ask it it's ok to run it. You can turn this off by setting `trust_the_code=True` in `main.py`. But don't do this unless your on a test machine or in an isolated environment.

## Notes
A few notes from this experiment:
1) I actually didn't even know that Applescript existed before doing this project. I started by asking the LLM to write code to do certain tasks on MacOS and Applescript is what it generated. 

2) Few-shot examples are critical for the LLM to generate code that works. Without them, it will get close, but will struggle with syntax, especially with languages like Applescript that are not super common.

3) I had much better luck using ChatGPT and text-davinci-003 for code generation than Codex. Interestingly, it was recently announced that Codex was being discontinued, so I guess my experience was not an outlier.

4) The code could have been shorter, but I played with a self-correction loop and letting the LLM try both Applescript and Bash. I also set up the chat conversation 

5) ChatGPT's conversational API is annoying for this task, but it's cheaper than text-davinci-003 and better than text-davinci-002.

6) ChatGPT pays closer attention to few-shot examples if given as the first user query instead of the system prompt.

7) I wanted to play with code generation, but for making a good assistant, code generation and execution isn't the best strategy. It is much more realistic to create API's yourself that perform the tasks, and to teach the LLM to use the API as part of the few-shot prompt. This is how chatGPT plugins work. An example would be the Toolformer https://arxiv.org/abs/2302.04761 which actually uses a bit of fine-tuning, but follows this idea. 


