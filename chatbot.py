import re
from datetime import datetime
import random

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
            print("Chatbot: I'm just a program, but I'm doing great! Thanks for asking. How about you?")
        
        elif re.search(r"(your name|who are you)", user_input):
            print("Chatbot: I'm a simple chatbot created using Python!")
        
        elif "time" in user_input:
            now = datetime.now().strftime("%H:%M:%S")
            print(f"Chatbot: The current time is {now}")
        
        elif "date" in user_input:
            today = datetime.now().strftime("%Y-%m-%d")
            print(f"Chatbot: Today's date is {today}")
        
        elif "weather" in user_input:
            print("Chatbot: Sorry, I cannot check the weather right now. 🌦️")
        
        elif "joke" in user_input:
            jokes = [
                "Why don’t scientists trust atoms? Because they make up everything!",
                "I told my computer I needed a break, and it said 'No problem — I’ll go to sleep.'",
                "Why was the math book sad? Because it had too many problems."
            ]
            print("Chatbot: " + random.choice(jokes))
        
        elif "thank you" in user_input or "thanks" in user_input:
            print("Chatbot: You're welcome! 😊")
        
        elif "help" in user_input:
            print("Chatbot: I can respond to greetings, tell you the time/date, crack a joke, or just chat with you!")
        
        elif "age" in user_input:
            print("Chatbot: I don’t have an age, but I was created recently in Python 🐍")
        
        elif "creator" in user_input or "made you" in user_input:
            print("Chatbot: I was created by a Python programmer just like you!")
        
        elif "food" in user_input:
            print("Chatbot: I don’t eat food, but I like the idea of pizza 🍕")
        
        elif "color" in user_input:
            print("Chatbot: My favorite color is blue 💙. What’s yours?")
        
        else:
            print("Chatbot: Sorry, I don't understand that. Can you rephrase?")

# Run the chatbot
chatbot()
