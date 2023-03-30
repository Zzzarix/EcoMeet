import datetime, time, random
from aiogram import types, Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from ..utils import check_user

from ..misc.keyboards import (
    menu_kb,
    categories_kb,
    task_chose_kb,
    task_not_chose_kb,
    answer_kb,
    current_task_kb,
)

from ..db.database import db
from ..config import config
from ..misc.states import TaskState

tasks_router = Router()


@tasks_router.message(Command(commands='tasks', commands_ignore_case=True))
@tasks_router.callback_query(text='tasks')
async def menu(obj, state: FSMContext):
    await state.set_state(None)
    flag = await check_user(obj.from_user.id)
    if not flag:
        return

    user = await db.get_user(obj.from_user.id)
    
    if isinstance(obj, types.Message):
        await obj.answer((await db.get_message('menu')).format(name=user.name), reply_markup=menu_kb(user.task))
    elif isinstance(obj, types.CallbackQuery):
        await obj.message.edit_text((await db.get_message('menu')).format(name=user.name), reply_markup=menu_kb(user.task))
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
async def categories(obj, state: FSMContext):
    await state.set_state(None)
    flag = await check_user(obj.from_user.id)
    if not flag:
        return

    user = await db.get_user(obj.from_user.id)
    cats = await db.get_categories()

    if isinstance(obj, types.Message):
        if user.task:
            await obj.answer('Вы уже получили задание, сначала выполните его')
            await obj.answer((await db.get_message('menu')).format(name=user.name), reply_markup=menu_kb(user.task))
        else:
            await obj.answer(await db.get_message('choose_category'), reply_markup=categories_kb(cats))
    elif isinstance(obj, types.CallbackQuery):
        if user.task:
            await obj.message.edit_text((await db.get_message('menu')).format(name=user.name), reply_markup=menu_kb(user.task))
            await obj.answer(text='Вы уже получили задание, сначала выполните его', show_alert=True)
        else:
            await obj.message.edit_text(await db.get_message('choose_category'), reply_markup=categories_kb(cats))
            await obj.answer()


@tasks_router.callback_query(text_startswith='tasks:new:')
async def tasks(call: types.CallbackQuery):
    flag = await check_user(call.from_user.id)
    if not flag:
        return

    user = await db.get_user(call.from_user.id)
    
    cat = call.data.split(':')[2]

    tasks = await db.get_tasks(int(cat))


    random.shuffle(tasks)
    for t in tasks:
        if not t.id in user.completed_tasks:

            user.task = t.id
            await db.update_user(user)
            
            await call.message.edit_text(f"Ваше новое задание:\n\n<i>{t.text}</i>\n\nЗа него вы получите {t.points} баллов", reply_markup=task_chose_kb())
            await call.answer()
            return

    await call.message.edit_text(f"В этой категории пока нет заданий для выполнения :(\nПриходите позже, либо возьмите задание из другой номинации", reply_markup=task_not_chose_kb())
    await call.answer()


@tasks_router.message(Command(commands='mytask', commands_ignore_case=True))
@tasks_router.callback_query(text='tasks:current')
async def current_task(obj, state: FSMContext):
    await state.set_state(None)
    flag = await check_user(obj.from_user.id)
    if not flag:
        return

    user = await db.get_user(obj.from_user.id)
    task = await db.get_task(user.task)
    if not task:
        cats = await db.get_categories()

    if isinstance(obj, types.Message):
        if task:
            await obj.answer(f"Ваше текущее задание:\n\n<i>{task.text}</i>\n\nЗа него вы получите {task.points} баллов", reply_markup=current_task_kb())
        else:
            await obj.answer('У вас пока нет заданий!')
            await obj.answer(await db.get_message('choose_category'), reply_markup=categories_kb(cats))
    elif isinstance(obj, types.CallbackQuery):
        if task:
            await obj.message.edit_text(f"Ваше текущее задание:\n\n<i>{task.text}</i>\n\nЗа него вы получите {task.points} баллов", reply_markup=current_task_kb())
            await obj.answer()
        else:
            await obj.message.edit_text('У вас пока нет заданий!', reply_markup=None)
            await obj.answer(await db.get_message('choose_category'), reply_markup=categories_kb(cats))


@tasks_router.message(Command(commands='answer', commands_ignore_case=True))
@tasks_router.callback_query(text='tasks:answer')
async def answer_task(obj, state: FSMContext):
    await state.set_state(None)
    flag = await check_user(obj.from_user.id)
    if not flag:
        return

    user = await db.get_user(obj.from_user.id)
    task = await db.get_task(user.task)

    if not task:
        cats = await db.get_categories()

    if isinstance(obj, types.Message):
        if task:
            await obj.answer(f"Ваше текущее задание:\n\n{task.text}\n\nДля подтверждения выполнения задания отправьте медиа/документы/текстовое описание <b>Одним Сообщением</b>", reply_markup=answer_kb())
        else:
            await obj.message.edit_text('У вас пока нет заданий!', reply_markup=None)
            await obj.answer(await db.get_message('choose_category'), reply_markup=categories_kb(cats))
    elif isinstance(obj, types.CallbackQuery):
        if task:
            await obj.message.edit_text(f"Ваше текущее задание:\n\n{task.text}\n\nДля подтверждения выполнения задания отправьте медиа/документы/текстовое описание <b>Одним Сообщением</b>", reply_markup=answer_kb())
            await obj.answer()
        else:
            await obj.message.edit_text('У вас пока нет заданий!', reply_markup=None)
            await obj.answer(await db.get_message('choose_category'), reply_markup=categories_kb(cats))
    
    if task:
        await state.set_state(TaskState.answer)


@tasks_router.message(state=TaskState.answer)
async def answer_task(m: types.Message, state: FSMContext, bot: Bot):
    flag = await check_user(m.from_user.id)
    if not flag:
        return
    
    user = await db.get_user(m.from_user.id)
    task = await db.get_task(user.task)

    for admin in config['bot']['admins']:
        try:
            text = f'Результат выполнения задания\n\n<i>{task.text}</i>\n\n'
            text += f'id {user.id}\nusername @{m.from_user.username}\nФИО {user.name} {user.last_name} {user.patronymic}\n'
            
            birth = user.birth.strftime('%Y.%m.%d')
            
            text += f'Дата рождения {birth}\nEmail {user.email}'

            await bot.send_message(admin, text)
            await bot.forward_message(admin, user.id, m.message_id)
        except Exception:
            pass

    user.complete_task()
    user.points += task.points
    await db.update_user(user)

    await state.set_state(None)

    await m.answer(f"Выполнение успешно отправлено! Спасибо!\nТеперь вы можете взять новое задание", reply_markup=answer_kb())
