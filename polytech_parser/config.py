import os
from typing import List

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.environ['API_TOKEN']
admin_usernames: List[str] = os.environ['admin_usernames'].split('&')
