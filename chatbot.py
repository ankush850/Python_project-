import re

def chatbot():
    print("Chatbot: Hello! I am a simple rule-based chatbot. Type 'bye' to exit.")

    while True:
        user_input = input("You: ").lower()

        if user_input in ["bye", "exit", "quit"]:
            print("Chatbot: Goodbye! Have a nice day 😊")
            break

        # Rule-based responses
        elif "hello" in user_input or "hi" in user_input:
            print("Chatbot: Hi there! How can I help you?")
        
        elif "how are you" in user_input:
            print("Chatbot: I'm just a program, but I'm doing great! Thanks for asking.")
        
        elif re.search(r"(your name|who are you)", user_input):
            print("Chatbot: I'm a simple chatbot created using Python!")
        
       
        else:
            print("Chatbot: Sorry, I don't understand that. Can you rephrase?")

# Run the chatbot
chatbot()
