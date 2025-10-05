from langchain_fireworks import Fireworks, ChatFireworks
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

try:
    FIREWORKS_API_KEY = os.getenv('FIREWORKS_API_KEY')
except Exception as e:
    FIREWORKS_API_KEY = st.secrets('FIREWORKS_API_KEY')

def get_chatModel():
    llm = ChatFireworks( model = "accounts/fireworks/models/deepseek-v3p1-terminus",
      max_tokens = 5000, temperature = 0.6, api_key = FIREWORKS_API_KEY )
    return llm