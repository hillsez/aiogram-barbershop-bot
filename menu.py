from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message
from aiogram import Router
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from database import get_all_books
from os import getenv
from dotenv import load_dotenv

load_dotenv()
ADMIN_ID = int(getenv("ADMIN_ID"))

router = Router(name="new rout")
class Form(StatesGroup):
    name = State()
    service = State()
    time = State()

@router.message(CommandStart())
async def show_keyboard(message: Message) -> None:
    builder = InlineKeyboardBuilder()
    builder.button(text="Услуги и цены", callback_data="price")
    builder.button(text="Адрес и часы", callback_data="address")
    builder.button(text="Записаться", callback_data="service")
    builder.button(text="Контакты", callback_data="contacts")
    builder.adjust(2,2)
    await message.reply(f"Привет, {message.from_user.full_name}, это барбершоп БОРОДА!", reply_markup=builder.as_markup())



@router.callback_query(F.data == "price")
async def show_price(callback):
    await callback.answer()
    builder = InlineKeyboardBuilder()
    builder.button(text="Вернуться в меню", callback_data="back")
    await callback.message.edit_text(f"Стрижка волос - 1200 Руб.\n"
                                  f"Окрашивание - 7000 Руб.\n"
                                  f"Стрижка + борода - 1500 Руб.\n"
                                  f"Укладка волос - 500 Руб.\n"
                                  f"Био-завивка - 8000 Руб", reply_markup=builder.as_markup())

@router.callback_query(F.data == "address")
async def show_address(callback):
    await callback.answer()
    builder = InlineKeyboardBuilder()
    builder.button(text="Вернуться в меню", callback_data="back")
    await callback.message.edit_text(f"Москва, ул. Красногвардейская д. 6\n"
                                  f"Будние дни 9:00 - 20:00\n"
                                  f"Выходные дни 10:00 - 19:00", reply_markup=builder.as_markup())

@router.callback_query(F.data == "contacts")
async def show_contacts(callback):
    await callback.answer()
    builder = InlineKeyboardBuilder()
    builder.button(text="Вернуться в меню", callback_data="back")
    await callback.message.edit_text(f"Телеграм - @hillsez", reply_markup=builder.as_markup())

@router.callback_query(F.data == "back")
async def back(callback):
    await callback.answer()
    builder = InlineKeyboardBuilder()
    builder.button(text="Услуги и цены", callback_data="price")
    builder.button(text="Адрес и часы", callback_data="address")
    builder.button(text="Записаться", callback_data="service")
    builder.button(text="Контакты", callback_data="contacts")
    builder.adjust(2, 2)
    await callback.message.edit_text("Выберите действие", reply_markup=builder.as_markup())

@router.message(Command("bookings"))
async def show_all_books(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("У вас нет прав для этой команды")
        return

    rows = await get_all_books()
    if not rows:
        await message.answer("Записей пока нет")
        return

    text = "Список всех записей:\n\n"
    for row in rows:
        text += f"{row['name']} - {row['service']}, {row['time']}\n"
    await message.answer(text)





