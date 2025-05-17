from dotenv import load_dotenv
import os
import openai


load_dotenv()
OPENAI_API_KEY = os.getenv("OPEN_API_KEY")
openai.api_key = OPENAI_API_KEY

audio_file = open("Recording.m4a", "rb")
output = openai.Audio.translate(
    model="whisper-1",
    file=audio_file,
    response_format="text",
    temperature=0,
)

print(output)


