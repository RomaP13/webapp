import asyncio
import logging
import os
import secrets

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from asgiref.sync import sync_to_async
import django
from django.contrib.auth import get_user_model

from config import TELEGRAM_BOT_TOKEN
from ngrok import get_ngrok_url

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "miniapp.settings")
django.setup()
User = get_user_model()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    if message.from_user is None:
        logging.warning("[WARNING] - message.from_user is None")
        return
    telegram_id = message.from_user.id
    username = message.from_user.username
    profile_photos = await bot.get_user_profile_photos(telegram_id)
    photo = (
        profile_photos.photos[0][-1].file_id
        if profile_photos.total_count > 0
        else None
    )

    # Check if user exists, otherwise create a new user
    user, created = await sync_to_async(User.objects.get_or_create)(
        telegram_id=telegram_id,
        defaults={
            "username": username,
            "silver": 1000,
            "photo": (
                f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{photo}"
                if photo
                else None
            ),
        },
    )

    if not created:
        user.username = username
        user.photo = (
            f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{photo}"
            if photo
            else user.photo
        )
        await sync_to_async(user.save)()

    # Generate token
    auth_token = secrets.token_urlsafe()
    user.auth_token = auth_token
    await sync_to_async(user.save)()

    NGROK_TUNNEL_URL = get_ngrok_url()

    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="Перейти",
        web_app=WebAppInfo(url=f"{NGROK_TUNNEL_URL}?auth_token={auth_token}"),
    )
    await message.reply(
        "Натисніть кнопку, щоб відкрити додаток:",
        reply_markup=keyboard_builder.as_markup(),
    )


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
