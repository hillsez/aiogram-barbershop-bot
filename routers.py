from aiogram import F
from aiogram import Router
from aiogram.types import Message
from aiogram.types import ErrorEvent

my_router = Router(name="main router")

@my_router.message(F.text)
async def handle_text(message):
    await message.answer("Вы отправили текст")

@my_router.message(F.sticker)
async def handle_sticker(message):
    await message.answer("Вы отправили стикер")

@my_router.message(F.photo)
async def handle_photo(message):
    await message.answer("Вы отправили фото")

@my_router.errors()
async def error_handler(event: ErrorEvent):
    print(f"Что-то не работает {event.exception}")

