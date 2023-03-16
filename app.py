from flask import Flask, render_template, request, redirect, url_for
from Chatbot import generate_text, interview_goal, questions

app = Flask(__name__)

question_index = 0


conversation = [
    {
        "role": "system",
        "content": interview_goal
    },
    {
        "role": "assistant",
        "content": questions[0]
    }
]

@app.route('/', methods=['GET', 'POST'])
def index():
    global conversation, question_index
    if request.method == 'POST':
        user_input = request.form['user_input']
        conversation.append({"role": "user", "content": user_input})
        ai_response = generate_text(conversation, is_follow_up=True)
        if not ai_response:
            if question_index < len(questions) - 1:
                question_index += 1
                ai_response = questions[question_index]
            else:
                ai_response = "That's all the questions we have! Thank you for participating."
        conversation.append({"role": "assistant", "content": ai_response})
    return render_template('index.html', conversation=conversation)



@app.route('/restart', methods=['POST'])
def restart():
    global conversation, question_index
    conversation = [
        {
            "role": "system",
            "content": interview_goal
        },
        {
            "role": "assistant",
            "content": questions[0]
        }
    ]
    question_index = 0
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
