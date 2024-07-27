import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import TELEGRAM_BOT_TOKEN, NGROK_TUNNEL_URL

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

print(f"NGROK_TUNNEL_URL: {NGROK_TUNNEL_URL}")


@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Перейти", web_app=WebAppInfo(url=NGROK_TUNNEL_URL))
    await message.reply(
        "Натисніть кнопку, щоб відкрити додаток:",
        reply_markup=keyboard_builder.as_markup(),
    )


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
