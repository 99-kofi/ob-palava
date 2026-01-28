import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-obala-palava'
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    YARNGPT_API_KEY = os.environ.get('YARNGPT_API_KEY')
