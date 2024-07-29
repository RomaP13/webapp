import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Retrieve and assert environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
assert (
    TELEGRAM_BOT_TOKEN is not None
), "TELEGRAM_BOT_TOKEN environment variable is not set"
