import openai
import requests
import util

util.import_config()


openai.api_key = util.apiKey
CHAT_API_URL = "https://api.openai.com/v1/chat/completions"

def generate_text(conversation, is_follow_up=False):
    if is_follow_up:
        prompt = f"Please ask a follow-up question related to the previous answer."
    else:
        prompt = f"Please ask the next question from the list."

    message = {
        "role": "assistant",
        "content": prompt,
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": conversation + [message],
        "max_tokens": 100,
        "temperature": 0.9,
        "top_p": 1,
    }
    response = requests.post(CHAT_API_URL, headers={"Authorization": f"Bearer {openai.api_key}"}, json=data)
    response_json = response.json()

    if "choices" in response_json:
        ai_response = response_json["choices"][0]["message"]["content"].strip()
        if ai_response.lower() == "next question":
            return ""
        else:
            return ai_response
    else:
        return "Error: Could not generate a response."





interview_goal = "The goal of this interview is to find out if you would want to use our marketplace for second hand phones."

questions = [
    "Have you ever bought or sold a second-hand phone before? If so, can you describe your experience?",
    "What factors are most important to you when purchasing a used phone, such as price, condition, or warranty?",
    "What concerns or reservations do you have about purchasing a second-hand phone, and how do you typically address those concerns?",
    "Have you used any other online marketplaces or services for buying or selling used phones, and how would you compare those experiences to what you would want from a new marketplace?",
    "What features or tools would you find most helpful when buying or selling a used phone through an online marketplace, such as a secure payment system, verified seller ratings, or detailed product descriptions?",
]

def main():
    print("Welcome to the AI Interview!")
    print("Interview goal:", interview_goal)
    print("-------------------------------------------------------------")

    conversation = []

    max_follow_ups = 3  # Adjust this value to control the depth of follow-up questions

    # Append the interview_goal to the conversation only once
    message = {
        "role": "system",
        "content": interview_goal,
    }
    conversation.append(message)

    for question in questions:
        user_answer = ""
        while user_answer.strip() == "":
            message = {
                "role": "assistant",
                "content": question,
            }
            conversation.append(message)

            user_answer = input(f"{question}\nYou: ").strip()

            message = {
                "role": "user",
                "content": user_answer,
            }
            conversation.append(message)

        follow_up_counter = 0

        while follow_up_counter < max_follow_ups:
            message = {
                "role": "assistant",
                "content": f"Please ask a follow-up question related to {user_answer} that extracts more information from the user.",
            }
            conversation.append(message)

            ai_response = generate_text(conversation)

            if ai_response.lower() == "next question":
                break
            else:
                print("AI:", ai_response)
                user_answer = input("You: ").strip()

                message = {
                    "role": "user",
                    "content": user_answer,
                }
                conversation.append(message)
                follow_up_counter += 1

    print("-------------------------------------------------------------")
    print("Thank you for participating in the interview! Goodbye!")


if __name__ == "__main__":
    main()
