# Simple Jarvis
A simple Jarvis or Siri-like assistant written in about 100 lines of Python. Can interact with it over text or via voice commands (using OpenAI's Whisper API). It uses ChatGPT to auto-generate and execute Applescript (or a Bash script) for accomplishing tasks. All of the few-shot examples in the main prompt were created by sampling the LLM to do a task until it generated a script that worked (I don't know anything about Applescript).

This is really just a personal experiment I wanted to do to test 2 things: 1) How much can you do with an LLM in like ~100 lines of Python over a few hours. 2) Code generation using LLM's. I wanted to get a feel for how reliably an LLM can generate runnable code that executes common tasks without manual intervention. Turns out, with just a handful few-shot examples and a single prompt, it's pretty great. And the number of tasks it can complete are surprising. A Note: I had much better luck using ChatGPT and text-davinci-003 for code generation than Codex. Interestingly, Codex was discontinued recently, so I guess my experience was not an outlier. 

The assistant can do a variety of simple tasks. Try to ask it to:
1) Send an email: "Send an email to <email> with the subject <subject> and the body <body>. Also include a list of good home remedies for a cold."
2) Send a text message: "Send a text message to <contact name> saying blah blah blah."
3) Search the web: "Search the web for <query>."
4) Search Wikipedia: "Search Wikipedia for <query>."
5) Search YouTube: "Search YouTube for <query>."
6) Search Google Maps: "Search Google Maps for <query>."
7) Open a file
8) Open an application
9) Add events to your calendar
10) Set reminders
11) Display the time
12) Display someones phone number from your contacts

You can do some surprisingly complex things with this mini-assistant. For example, you can ask it to "Open up a new document in the numbers app. Then add a table with information about 10 countries with columns for name, official language, and continent."


