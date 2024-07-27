import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Retrieve and assert environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
assert (
    TELEGRAM_BOT_TOKEN is not None
), "TELEGRAM_BOT_TOKEN environment variable is not set"

NGROK_TUNNEL_URL = os.getenv("NGROK_TUNNEL_URL")
assert (
    NGROK_TUNNEL_URL is not None
), "NGROK_TUNNEL_URL environment variable is not set"

SECRET_KEY = os.getenv("SECRET_KEY")

HOSTS = os.getenv("ALLOWED_HOSTS")
ALLOWED_HOSTS = []

for HOST in HOSTS.split(","):
    ALLOWED_HOSTS.append(HOST)
ALLOWED_HOSTS.append(NGROK_TUNNEL_URL)
