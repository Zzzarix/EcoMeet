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


@start_router.message(state=SignUpState.phone)
async def signup(m: types.Message, state: FSMContext):
    user = await db.get_user(m.from_user.id)
    if not user:
        await m.answer("Пожалуйста, начните работу с ботом с команды /start :)")
        return
    if m.contact:
        user.phone = m.contact.phone_number
        await db.update_user(user)
        await m.answer(await db.get_message('enter_name'), reply_markup=clear_kb())
        await state.set_state(SignUpState.name)
    else:
        await m.answer('Нажмите, пожалуйста на кнопку отправить контакт под клавиатурой, чтобы продолжить')

@start_router.message(state=SignUpState.name)
async def name(m: types.Message, state: FSMContext):
    user = await db.get_user(m.from_user.id)
    if not user:
        await m.answer("Пожалуйста, начните работу с ботом с команды /start :)")
        return
    
    if m.text.startswith('/'):
        await m.answer("Пожалуйста, закончите регистрацию перед дальнейшим использованием бота")
        return
    
    if not m.text:
        await m.answer("Пожалуйста, вводите данные текстом")
        return
    
    user.name = m.text.title()
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
        return
    
    if not m.text:
        await m.answer("Пожалуйста, вводите данные текстом")
        return
    
    user.last_name = m.text.title()
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
        return
    
    if not m.text:
        await m.answer("Пожалуйста, вводите данные текстом")
        return
    
    user.patronymic = m.text.title()
    await db.update_user(user)
    await m.answer(await db.get_message('enter_birth'))
    await state.set_state(SignUpState.birth_date)

@start_router.message(state=SignUpState.birth_date)
async def birth_date(m: types.Message, state: FSMContext):
    user = await db.get_user(m.from_user.id)
    if not user:
        await m.answer("Пожалуйста, начните работу с ботом с команды /start :)")
        return
    
    if m.text.startswith('/'):
        await m.answer("Пожалуйста, закончите регистрацию перед дальнейшим использованием бота")
        return
    
    if not m.text:
        await m.answer("Пожалуйста, вводите данные текстом")
        return
    
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
        return
    
    if not m.text:
        await m.answer("Пожалуйста, вводите данные текстом")
        return
        
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", m.text):
        await m.answer("Некорректный адрес электронной почты, попробуйте ещё раз")
        return
    
    user.email = m.text.lower()
    await db.update_user(user)
    await m.answer(await db.get_message('menu').format(name=user.name), reply_markup=menu_kb(user.task))
    await state.set_state(None)

@start_router.message(CommandStart())
async def start_command(m: types.Message, state: FSMContext, bot: Bot) -> None:
    user = await db.get_user(m.from_user.id)
    await state.set_state(None)
    if user:
        await m.answer((await db.get_message('menu')).format(name=user.name), reply_markup=menu_kb(user.task))
        await state.clear()
    else:
        await m.answer(await db.get_message('greeting'))
        user = await db.create_user(m.from_user.id)

        await m.answer(await db.get_message('signup'), reply_markup=signup_kb())
        await state.set_state(SignUpState.phone)
