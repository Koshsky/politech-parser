import os
from typing import List

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.environ['API_TOKEN']
admin_IDs: List[int] = [int(i) for i in os.environ['admin_IDs'].split('&')]
