import requests
import os
import streamlit as st
import json
from dotenv import load_dotenv

load_dotenv()
try:
    FIREWORKS_API_KEY = os.getenv('FIREWORKS_API_KEY')
except Exception as e:
    print(f'dotenv not working: {e} ')
    FIREWORKS_API_KEY = st.secrets("FIREWORKS_API_KEY")


def connect_for_response(prompt : str):

    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    payload = {
      "model": "accounts/fireworks/models/deepseek-v3p1-terminus",
      "max_tokens": 5000,
      "top_p": 1,
      "top_k": 40,
      "presence_penalty": 0,
      "frequency_penalty": 0,
      "temperature": 0.6,
      "messages": [
        {
          "role": "user",
          "content": prompt
        }
      ]
    }
    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json",
      "Authorization": FIREWORKS_API_KEY
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f'Error, {response.status_code} '

