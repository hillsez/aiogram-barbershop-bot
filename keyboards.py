from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message
from aiogram import Router
from aiogram import F
from aiogram.filters import CommandStart

router = Router(name="new rout")

@router.message(CommandStart())
async def show_keyboard(message: Message) -> None:
    builder = InlineKeyboardBuilder()
    builder.button(text="Услуги и цены", callback_data="price")
    builder.button(text="Адрес и часы", callback_data="address")
    builder.button(text="Записаться", callback_data="go")
    builder.button(text="Контакты", callback_data="contacts")
    builder.adjust(2,2)
    await message.reply(f"Привет, {message.from_user.full_name}, это барбершоп БОРОДА!", reply_markup=builder.as_markup())

@router.callback_query(F.data == "price")
async def on_set_chosen(callback):
    builder = InlineKeyboardBuilder()
    builder.button(text="Вернуться в меню", callback_data="back")
    await callback.message.answer(f"Стрижка - 1200 Руб.\n"
                                  f"Окрашивание - 7000 Руб.\n"
                                  f"Стрижка + борода - 1500 Руб.\n"
                                  f"Укладка - 300 Руб.\n"
                                  f"Био-завивка - 8000 Руб", reply_markup=builder.as_markup())

@router.callback_query(F.data == "address")
async def on_set_chosen(callback):
    builder = InlineKeyboardBuilder()
    builder.button(text="Вернуться в меню", callback_data="back")
    await callback.message.answer(f"Москва, ул. Красногвардейская д. 6\n"
                                  f"Будние дни 9:00 - 20:00\n"
                                  f"Выходные дни 10:00 - 19:00", reply_markup=builder.as_markup())

@router.callback_query(F.data == "go")
async def on_set_chosen(callback):
    builder = InlineKeyboardBuilder()
    builder.button(text="Вернуться в меню", callback_data="back")
    await callback.message.answer(f"Запись скоро будет доступна", reply_markup=builder.as_markup())

@router.callback_query(F.data == "contacts")
async def on_set_chosen(callback):
    builder = InlineKeyboardBuilder()
    builder.button(text="Вернуться в меню", callback_data="back")
    await callback.message.answer(f"Телеграм - @hillsez", reply_markup=builder.as_markup())

@router.callback_query(F.data == "back")
async def back(callback):
    builder = InlineKeyboardBuilder()
    builder.button(text="Услуги и цены", callback_data="price")
    builder.button(text="Адрес и часы", callback_data="address")
    builder.button(text="Записаться", callback_data="go")
    builder.button(text="Контакты", callback_data="contacts")
    builder.adjust(2, 2)
    await callback.message.answer("", reply_markup=builder.as_markup())
