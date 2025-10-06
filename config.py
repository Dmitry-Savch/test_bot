import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN", "your_token_here")
TEMPLATE_PATH = "templates/sat_form.png"
OUTPUT_DIR = "output"
FONTS_DIR = "fonts"
