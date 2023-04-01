#sample requests
def get_sample_requests():
    requests = { 
        'calendar' : [
            """Add an event to my calendar for tomorrow at 9:15 AM for an appointment with Geetha for Emma.""",
        ],
        'organize' : [
            "make a to do list which includes buy groceries, call mom, and call dad.",
            "remind me to call mom tomorrow at 9:00 AM.",
        ],
        'texting' : [
            """Send a text to Sasha Norton saying I'm running late for our meeting. And will you also start dinner. Also, add a joke about hockey and let her know it was written by an AI.""",
        ],
        'email' : [
            "Send an email to mdnorto@gmail.com with subject tomorrows meetings and body saying I will be in the office at 9:00 AM and will be available for meetings until 5:00 PM. Also, add a joke about hockey and him her know it was written by an AI.",
            "Send an email to mdnorto at gmail.com with a list of five ideas for how to present technical content to CEOs and other c-suite executives in a presentation that is 10 minutes or less. And the presentation contents will be technical.",
        ],
        'google' : [
            "Search for the best restaurants in San Francisco.",
        ],
        'files' : [
            "Open the file called resume in the documents folder.",
            "create a new folder called my new folder in the documents folder.",
        ],
        'applications' : [
            "Open safari and go to google.com.",
        ],
        'contacts' : [
            "What is Luke Skywalker's phone number?",
        ],
        'time' : [
            "What time is it?",
            "when is father's day?",
        ],
        'weather' : [
            "What is the weather like in San Francisco?",
            "What is the low for tomorrow in San Francisco?",
        ]
    }
    return requests