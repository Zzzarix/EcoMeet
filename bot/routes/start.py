from aiogram import types, Router, Bot
from aiogram.filters.command import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType
import datetime, re

from ..utils import check_user
from ..db.database import db
from ..misc.states import SignUpState

from ..misc.keyboards import (
    menu_kb,
    clear_kb,
    signup_kb
)


start_router = Router()


@start_router.message(content_types=[ContentType.CONTACT])
async def signup(m: types.Message, state: FSMContext):
    user = await db.get_user(m.from_user.id)
    if not user:
        await m.answer("Пожалуйста, начните работу с ботом с команды /start :)")
        return
    if not user.phone:
        user.phone = m.contact.phone_number
        await db.update_user(user)
        await m.answer(await db.get_message('enter_name'), reply_markup=clear_kb())
        await state.set_state(SignUpState.name)

@start_router.message(state=SignUpState.name)
async def name(m: types.Message, state: FSMContext):
    user = await db.get_user(m.from_user.id)
    if not user:
        await m.answer("Пожалуйста, начните работу с ботом с команды /start :)")
        return
    
    if m.text.startswith('/'):
        await m.answer("Пожалуйста, закончите регистрацию перед дальнейшим использованием бота")
    
    user.name = m.text
    await db.update_user(user)
    await m.answer(await db.get_message('enter_last_name'))
    await state.set_state(SignUpState.last_name)

@start_router.message(state=SignUpState.last_name)
async def last_name(m: types.Message, state: FSMContext):
    user = await db.get_user(m.from_user.id)
    if not user:
        await m.answer("Пожалуйста, начните работу с ботом с команды /start :)")
        return
    
    if m.text.startswith('/'):
        await m.answer("Пожалуйста, закончите регистрацию перед дальнейшим использованием бота")
    
    user.last_name = m.text
    await db.update_user(user)
    await m.answer(await db.get_message('enter_patronymic'))
    await state.set_state(SignUpState.patronymic)

@start_router.message(state=SignUpState.patronymic)
async def patronymic(m: types.Message, state: FSMContext):
    user = await db.get_user(m.from_user.id)
    if not user:
        await m.answer("Пожалуйста, начните работу с ботом с команды /start :)")
        return
    
    if m.text.startswith('/'):
        await m.answer("Пожалуйста, закончите регистрацию перед дальнейшим использованием бота")
    
    user.patronymic = m.text
    await db.update_user(user)
    # await m.answer(await db.get_message('enter_birth'))
    await m.answer(await db.get_message('Введите дату рождения в формате год.месяц.день'))
    await state.set_state(SignUpState.birth_date)

@start_router.message(state=SignUpState.birth_date)
async def birth_date(m: types.Message, state: FSMContext):
    user = await db.get_user(m.from_user.id)
    if not user:
        await m.answer("Пожалуйста, начните работу с ботом с команды /start :)")
        return
    
    if m.text.startswith('/'):
        await m.answer("Пожалуйста, закончите регистрацию перед дальнейшим использованием бота")
    
    try:
        date = datetime.datetime.strptime(m.text, '%Y.%m.%d')
    except Exception:
        await m.answer(await db.get_message('enter_birth_error'))
    else:
        user = await db.get_user(m.from_user.id)
        user.birth = date
        await db.update_user(user)
        await m.answer(await db.get_message('enter_email'))
        await state.set_state(SignUpState.email)

@start_router.message(state=SignUpState.email)
async def email(m: types.Message, state: FSMContext):
    user = await db.get_user(m.from_user.id)
    if not user:
        await m.answer("Пожалуйста, начните работу с ботом с команды /start :)")
        return
    
    if m.text.startswith('/'):
        await m.answer("Пожалуйста, закончите регистрацию перед дальнейшим использованием бота")
        
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", m.text):
        await m.answer("Некорректный адрес электронной почты, попробуйте ещё раз")
        return
    
    user.email = m.text
    await db.update_user(user)
    await m.answer(await db.get_message('menu'))
    await state.set_state(SignUpState.patronymic)

@start_router.message(CommandStart())
async def start_command(m: types.Message, state: FSMContext, bot: Bot) -> None:
    user = await db.get_user(m.from_user.id)
    if user:
        await m.answer((await db.get_message('menu')).format(user.name), reply_markup=menu_kb(user.task))
        await state.clear()
    else:
        await m.answer(await db.get_message('greeting'))
        user = await db.create_user(m.from_user.id)

        await m.answer(await db.get_message('signup'), reply_markup=signup_kb())

@start_router.message()
async def cap(m: types.Message):
    await m.answer('Я не знаю такой команды, попробуйте ещё раз')
