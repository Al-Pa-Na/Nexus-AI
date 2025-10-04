from flask import Flask, render_template, request
from app.agent import run_conversation

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
async def index():
    result = None
    if request.method == 'POST':
        user_command = request.form['command']
        if user_command:
            result = await run_conversation(user_command)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)