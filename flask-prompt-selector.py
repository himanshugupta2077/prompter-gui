import os
from flask import Flask, render_template, request

app = Flask(__name__)

PROMPTS_DIR = 'prompts'

def get_prompt_files():
    return [f for f in os.listdir(PROMPTS_DIR) if f.endswith('.md')]

def read_prompt(filename):
    with open(os.path.join(PROMPTS_DIR, filename), 'r') as file:
        return file.read()

@app.route('/', methods=['GET', 'POST'])
def index():
    prompt_files = get_prompt_files()
    selected_prompt = ''

    if request.method == 'POST':
        selected_file = request.form.get('prompt_file')
        if selected_file:
            selected_prompt = read_prompt(selected_file)

    return render_template('index.html', prompt_files=prompt_files, selected_prompt=selected_prompt)

if __name__ == '__main__':
    app.run(debug=True)
