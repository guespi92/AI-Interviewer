import openai
import os
import time
import util

util.import_config()


# Set up OpenAI API client
openai.api_key = util.apiKey

# define the questions the bot will ask
questions = [
    "What is your name?",
    "What is your age?",
    "What is your occupation?",
    "What are your hobbies?",
    "What is your favorite book?",
]

# define a function to ask questions and wait for user input
def ask_question(question):
    # ask the question
    response = openai.Completion.create(
        engine="davinci", prompt=question, max_tokens=50, n=1, stop=None, temperature=0.5
    )
    print(response.choices[0].text.strip())

    # wait for user input
    while True:
        answer = input("> ").strip()
        if answer:
            break
        else:
            print("Please enter a valid answer.")

    return answer

# start the interview
print("Welcome to the interview!")
time.sleep(1)

for question in questions:
    answer = ask_question(question)
    print(f"Your answer: {answer}\n")
    time.sleep(1)

print("Thank you for participating in the interview!")