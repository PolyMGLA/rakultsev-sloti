import os
import dotenv

dotenv.load_dotenv(override=True)

BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMINS = list(map(int, os.environ["BOT_ADMINS"].split(",")))
