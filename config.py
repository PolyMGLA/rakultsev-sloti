import os
import dotenv

dotenv.load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMINS = list(map(int, os.environ["ADMINS"].split(",")))

print("admins:", ADMINS)
