from aiogram.types import Message
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from typing import Any
from config import ADMIN_ID
from database import save_booking
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

router = Router(name="booking router")


class Form(StatesGroup):
    name = State()
    service = State()
    time = State()
    confirm = State()

def get_time_keyboard():
    builder = InlineKeyboardBuilder()
    slots = ["9:00", "11:00", "13:00", "15:00", "17:00", "19:00"]
    for slot in slots:
        builder.button(text=slot, callback_data=f"time:{slot}")
    builder.adjust(2)
    return builder.as_markup()

def get_confirm_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Да", callback_data="yes")
    builder.button(text="Нет", callback_data="no")
    builder.adjust(2)
    return builder.as_markup()

@router.callback_query(F.data == "service")
async def start_booking(callback, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(Form.name)
    await callback.message.edit_text("Как вас зовут?")

@router.message(Form.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Form.service)
    await message.answer(f"{message.text}, на какую услугу Вы хотели бы записаться?\n\n"
                         f"Доступные услуги:\n\n"
                         f"1. Стрижка волос - 1200 Руб.\n"
                         f"2. Окрашивание - 7000 Руб.\n"
                         f"3. Стрижка + борода - 1500 Руб. \n"
                         f"4. Укладка волос - 500 Руб.\n"
                         f"5. Био-завивка - 8000 Руб.\n\n"
                         f"Для записи отправьте номер услуги в ответ.")

@router.message(Form.service, F.text.casefold() == "1")
async def process_service_1(message: Message, state: FSMContext) -> None:
    await state.update_data(service="Стрижка волос")
    await state.set_state(Form.time)
    await message.answer(f"Вы выбрали услугу Стрижка волос, на какую дату и время Вы хотите записаться?", reply_markup=get_time_keyboard())

@router.message(Form.service, F.text.casefold() == "2")
async def process_service_2(message: Message, state: FSMContext) -> None:
    await state.update_data(service="Окрашивание")
    await state.set_state(Form.time)
    await message.answer(f"Вы выбрали услугу Окрашивание, на какую дату и время Вы хотите записаться?", reply_markup=get_time_keyboard())

@router.message(Form.service, F.text.casefold() == "3")
async def process_service_3(message: Message, state: FSMContext) -> None:
    await state.update_data(service="Стрижка + борода")
    await state.set_state(Form.time)
    await message.answer(f"Вы выбрали услугу Стрижка + борода, на какую дату и время Вы хотите записаться?", reply_markup=get_time_keyboard())

@router.message(Form.service, F.text.casefold() == "4")
async def process_service_4(message: Message, state: FSMContext) -> None:
    await state.update_data(service="Укладка волос")
    await state.set_state(Form.time)
    await message.answer(f"Вы выбрали услугу Укладка волос, на какую дату и время Вы хотите записаться?", reply_markup=get_time_keyboard())

@router.message(Form.service, F.text.casefold() == "5")
async def process_service_5(message: Message, state: FSMContext) -> None:
    await state.update_data(service="Био-завивка")
    await state.set_state(Form.time)
    await message.answer(f"Вы выбрали услугу Био-завивка, на какую дату и время Вы хотите записаться?", reply_markup=get_time_keyboard())

@router.message(Form.service)
async def process_service_6(message: Message) -> None:
    await message.reply("Такую услугу мы не предоставляем, выберите существующую")

@router.callback_query(Form.time, F.data.startswith("time:"))
async def process_time(callback, state: FSMContext) -> None:
    await callback.answer()
    slot = callback.data.split(":", 1)[1]
    data = await state.update_data(time=slot)
    await state.set_state(Form.confirm)
    await callback.message.edit_text(text=f"Вы уверены, что привильно выбрали время - {slot}?", reply_markup=get_confirm_keyboard())

@router.callback_query(Form.confirm, F.data == "yes")
async def process_confirm(callback, state: FSMContext) -> None:
    await callback.answer()
    data = await state.get_data()
    await state.clear()
    await show_summary(callback, data=data)
    await text_for_admin(callback, data=data)

@router.callback_query(Form.confirm, F.data == "no")
async def process_confirm_2(callback, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(Form.time)
    await callback.message.edit_text(text="Выберите время:", reply_markup=get_time_keyboard())

async def show_summary(callback, data: dict[str, Any]) -> None:
    name = data['name']
    service = data['service']
    time = data['time']
    text = f"{name}, Вы записаны на {service} {time}. Ждем Вас!"
    await save_booking(name, service, time, callback.from_user.id)
    await callback.message.answer(text=text)

async def text_for_admin(callback, data: dict[str, Any]) -> None:
    text_admin = (
        f"Новая запись!\n\n"
        f"Имя: {data['name']}\n"
        f"Услуга: {data['service']}\n"
        f"Время: {data['time']}\n"
        f"От: @{callback.from_user.username}"
    )
    await callback.bot.send_message(ADMIN_ID, text_admin)



