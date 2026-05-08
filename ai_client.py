import os
from dotenv import load_dotenv
from openai import  OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DEFAULT_MODEL = "gpt-4.1-mini"


def generate_resume_advice(prompt, model=DEFAULT_MODEL):
    response = client.responses.create(
        model=model,
        input=prompt
    )

    return response.output_text