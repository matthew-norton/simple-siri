from simple_siri.chat import Conversation

if __name__ == "__main__":
    how = input("How would you like to converse? (text or voice) ")
    OPEN_AI_API_KEY = input("Enter your OpenAI API key: ")
    conversation = Conversation(OPEN_AI_API_KEY)
    conversation.converse(how)
