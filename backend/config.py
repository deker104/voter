from os import getenv

from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = getenv('TELEGRAM_TOKEN')
OWNER_ID = int(getenv('OWNER_ID') or 439766454)
