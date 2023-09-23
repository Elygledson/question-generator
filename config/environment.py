from dotenv import load_dotenv
import os

load_dotenv()

CONFIG = {
    'OPENAI_API_TYPE': os.getenv('OPENAI_API_TYPE'),
    'OPENAI_API_VERSION': os.getenv('OPENAI_API_VERSION'),
    'OPENAI_API_BASE': os.getenv('OPEN_API_BASE'),
    'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
    'MONGODB_URI': os.getenv('MONGODB_URI'),
    'DB_NAME': os.getenv('DB_NAME'),
    'COLLECTION': os.getenv('COLLECTION')
}
