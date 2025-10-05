from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
try:
    HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')
except Exception as e:
    HUGGINGFACE_API_TOKEN = st.secrets('HUGGINGFACE_API_TOKEN')

def get_chatModel():
    llm = HuggingFaceEndpoint(repo_id='zai-org/GLM-4.6', temperature=0.3,
                              task='text-generation', verbose=False,
                              huggingfacehub_api_token=HUGGINGFACE_API_TOKEN)

    chat_model = ChatHuggingFace(llm=llm)
    return chat_model

