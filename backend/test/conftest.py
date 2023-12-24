# conftest.py
import os
from dotenv import load_dotenv

# Load the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..',  '.env')
load_dotenv(dotenv_path)
