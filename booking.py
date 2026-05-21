from aiogram.types import Message
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from typing import Any
from config import ADMIN_ID

router = Router(name="booking router")

class Form(StatesGroup):
    name = State()
    service = State()
    time = State()

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
    await message.answer(f"Вы выбрали услугу Стрижка волос, на какую дату и время Вы хотите записаться?", reply_markup=ReplyKeyboardRemove())

@router.message(Form.service, F.text.casefold() == "2")
async def process_service_2(message: Message, state: FSMContext) -> None:
    await state.update_data(service="Окрашивание")
    await state.set_state(Form.time)
    await message.answer(f"Вы выбрали услугу Окрашивание, на какую дату и время Вы хотите записаться?", reply_markup=ReplyKeyboardRemove())

@router.message(Form.service, F.text.casefold() == "3")
async def process_service_3(message: Message, state: FSMContext) -> None:
    await state.update_data(service="Стрижка + борода")
    await state.set_state(Form.time)
    await message.answer(f"Вы выбрали услугу Стрижка + борода, на какую дату и время Вы хотите записаться?", reply_markup=ReplyKeyboardRemove())

@router.message(Form.service, F.text.casefold() == "4")
async def process_service_4(message: Message, state: FSMContext) -> None:
    await state.update_data(service="Укладка волос")
    await state.set_state(Form.time)
    await message.answer(f"Вы выбрали услугу Укладка волос, на какую дату и время Вы хотите записаться?", reply_markup=ReplyKeyboardRemove())

@router.message(Form.service, F.text.casefold() == "5")
async def process_service_5(message: Message, state: FSMContext) -> None:
    await state.update_data(service="Био-завивка")
    await state.set_state(Form.time)
    await message.answer(f"Вы выбрали услугу Био-завивка, на какую дату и время Вы хотите записаться?", reply_markup=ReplyKeyboardRemove())

@router.message(Form.service)
async def process_service_6(message: Message) -> None:
    await message.reply("Такую услугу мы не предоставляем, выберите существующую")

@router.message(Form.time)
async def process_time(message: Message, state: FSMContext) -> None:
    data = await state.update_data(time=message.text)
    await state.clear()
    print(f"DEBUG ADMIN_ID = {ADMIN_ID!r}")
    await show_summary(message=message, data=data)
    await text_for_admin(message=message, data=data)

async def show_summary(message: Message, data: dict[str, Any]) -> None:
    name = data['name']
    service = data['service']
    time = data['time']
    text = f"{name}, Вы записаны на {service} {time}. Ждем Вас!"
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())

async def text_for_admin(message: Message, data: dict[str, Any]) -> None:
    text_admin = (
        f"Новая запись!\n\n"
        f"Имя: {data['name']}\n"
        f"Услуга: {data['service']}\n"
        f"Время: {data['time']}\n"
        f"От: @{message.from_user.username}"
    )
    await message.bot.send_message(ADMIN_ID, text_admin)

