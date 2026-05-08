import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from streamlit.errors import StreamlitSecretNotFoundError


load_dotenv()

DEFAULT_MODEL = "gpt-4.1-mini"


def get_openai_api_key():
    try:
        if "OPENAI_API_KEY" in st.secrets:
            return st.secrets["OPENAI_API_KEY"]
    except StreamlitSecretNotFoundError:
        pass

    return os.getenv("OPENAI_API_KEY")


def generate_resume_advice(prompt, model=DEFAULT_MODEL):
    api_key = get_openai_api_key()

    if not api_key:
        raise ValueError("未找到 OPENAI_API_KEY，请检查本地 .env 或 Streamlit Cloud Secrets。")

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model=model,
        input=prompt
    )

    return response.output_text