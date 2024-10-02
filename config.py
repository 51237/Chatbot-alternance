import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    return {
        'AZURE_VISION_KEY': os.getenv('AZURE_VISION_KEY'),
        'AZURE_VISION_ENDPOINT': os.getenv('AZURE_VISION_ENDPOINT'),
        'MISTRAL_API_KEY': os.getenv('MISTRAL_API_KEY'),
        'JOOble_API_KEY': os.getenv('JOOble_API_KEY')
    }