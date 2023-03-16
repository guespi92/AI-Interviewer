import openai
import os
import util

util.import_config()

# Set up OpenAI API client
openai.api_key = util.apiKey

# Load questions from file
with open("questions.txt", "r") as f:
    questions = f.readlines()

# Introduction
print("Hi, I'm a chatbot. I'm going to ask you some questions. Please type your answer and press enter.")

# Loop over questions
for question in questions:
    # Ask the question and wait for user input
    user_input = input(question.strip() + " ")

    # Generate response using GPT-3 API
    prompt = f"{question.strip()} {user_input}"
    response = openai.Completion.create(
        engine="curie",
        prompt=prompt,
        max_tokens=120,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Print response
    print(response.choices[0].text.strip())
