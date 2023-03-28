import datetime
import time
from aiogram import types, Bot, Router
from aiogram.filters.command import Command
from ..utils import check_user

from ..misc.keyboards import (
    menu_kb,
    categories_kb,
    tasks_kb,
    answer_kb,
    current_task_kb,
)

from ..db.database import db
from ..config import config

tasks_router = Router()


@tasks_router.message(Command(commands='tasks', commands_ignore_case=True))
@tasks_router.callback_query(text='tasks')
async def menu(obj):
    flag = await check_user(obj.from_user.id)
    if not flag:
        return

    user = await db.get_user(obj.from_user.id)
    
    if isinstance(obj, types.Message):
        await obj.answer((await db.get_message('menu')).format(user.name), reply_markup=menu_kb(user.task))
    elif isinstance(obj, types.CallbackQuery):
        await obj.message.edit_text((await db.get_message('menu')).format(user.name), reply_markup=menu_kb(user.task))
        await obj.answer()


@tasks_router.message(Command(commands='takepoints', commands_ignore_case=True))
async def takepoints(m: types.Message):
    flag = await check_user(m.from_user.id)
    if not flag:
        return
    
    if not m.from_user.id in config['bot']['admins']:
        await m.answer('Я не знаю такой команды, попробуйте ещё раз')
        return
    
    try:
        params = m.text.split(' ')[1:]
        await db.add_points(int(params[0]), -int(params[1]))
    except Exception:
        await m.answer('Не успешно!')
        return

    await m.answer('Успешно!')


@tasks_router.message(Command(commands='addpoints', commands_ignore_case=True))
async def addpoints(m: types.Message):
    flag = await check_user(m.from_user.id)
    if not flag:
        return
    
    if not m.from_user.id in config['bot']['admins']:
        await m.answer('Я не знаю такой команды, попробуйте ещё раз')
        return
    
    try:
        params = m.text.split(' ')[1:]
        await db.add_points(int(params[0]), int(params[1]))
    except Exception:
        await m.answer('Не успешно!')
        return

    await m.answer('Успешно!')


@tasks_router.message(Command(commands='tasks', commands_ignore_case=True))
@tasks_router.callback_query(text='tasks:new')
async def tasks(obj):
    flag = await check_user(obj.from_user.id)
    if not flag:
        return

    user = await db.get_user(obj.from_user.id)
    
    if isinstance(obj, types.Message):
        cats = await db.get_categories()
        await obj.answer(await db.get_message('menu').format(user.name), reply_markup=menu_kb(user.task))
    elif isinstance(obj, types.CallbackQuery):
        await obj.message.edit_text(await db.get_message('menu').format(user.name), reply_markup=menu_kb(user.task))
        await obj.answer()
