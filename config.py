import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'urls.db')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    SHORT_CODE_LENGTH = int(os.getenv('SHORT_CODE_LENGTH', 6))
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')
