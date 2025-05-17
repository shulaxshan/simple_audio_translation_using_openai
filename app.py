from dotenv import load_dotenv
import os
import openai
from flask import Flask, request, jsonify ,render_template


load_dotenv()
OPENAI_API_KEY = os.getenv("OPEN_API_KEY")
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        language = request.form["language"]
        file = request.files["file"]
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            audio_file = open("uploads/Recording.m4a", "rb")
            transcript = openai.Audio.translate("whisper-1", audio_file)

        # with open("uploads/Recording.m4a", "rb") as file:
        #     transcript = openai.Audio.translate(
        #         model="whisper-1",
        #         file=file,
        #         response_format="text",
        #         temperature=0,
        #     )

        response = openai.ChatCompletion.create(
        model="gpt-4.1-nano",
        messages = [{ "role": "system", "content": f"You will be provided with a sentence in English, and your task is to translate it into {language}" }, 
                    { "role": "user", "content": transcript.text }],
        temperature=0,
        max_tokens=50
        )    
        return jsonify({"response": response.choices[0].message['content']})
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)