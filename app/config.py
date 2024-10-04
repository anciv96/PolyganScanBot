from os import getenv
from dotenv import load_dotenv

load_dotenv()

POLYGON_SCAN_KEY = getenv('POLYGON_KEY')
TOKENS = getenv('ADDRESSES').split(',')
BOT_TOKEN = getenv("BOT_TOKEN")
