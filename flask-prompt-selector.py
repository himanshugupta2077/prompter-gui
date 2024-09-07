import os
from flask import Flask, render_template, request, jsonify
from anthropic import Anthropic
import anthropic

app = Flask(__name__)

PROMPTS_DIR = 'prompts'

def get_prompt_files():
    return [f for f in os.listdir(PROMPTS_DIR) if f.endswith('.md')]

def read_prompt(filename):
    with open(os.path.join(PROMPTS_DIR, filename), 'r') as file:
        return file.read()

def process_with_anthropic(content, selected_prompt):
    try:
        client = Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
        prompt = f"""
        {selected_prompt}
        {content}
        """
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=2000,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        processed_content = message.content[0].text
        return processed_content
    except Exception as e:
        print(f"Error processing with Anthropic API: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    prompt_files = get_prompt_files()
    selected_prompt = ''
    llm_output = ''
    if request.method == 'POST':
        selected_file = request.form.get('prompt_file')
        user_input = request.form.get('user_input')
        if selected_file:
            selected_prompt = read_prompt(selected_file)
            if user_input:
                llm_output = process_with_anthropic(user_input, selected_prompt)
    return render_template('index.html', prompt_files=prompt_files, selected_prompt=selected_prompt, llm_output=llm_output)

if __name__ == '__main__':
    app.run(debug=True)
