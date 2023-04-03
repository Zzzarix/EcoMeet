from aiogram import types, Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from ..utils import check_user

from ..misc.keyboards import (
    rating_kb,
)

from ..db.database import db
from ..config import config

rating_router = Router()


@rating_router.message(Command(commands='rating', commands_ignore_case=True))
@rating_router.callback_query(text='rating')
async def rating(obj, state: FSMContext):
    await state.set_state(None)
    flag = await check_user(obj.from_user.id)
    if not flag:
        return

    users = await db.get_top_users(10)

    rating = ''

    for c, u in enumerate(users, 1):
        if u.id == obj.from_user.id:
            rating += f'<b>{c}. {u.name} {u.last_name} <i>{u.points}</i></b>\n'
        else:
            rating += f'{c}. {u.name} {u.last_name} <b>{u.points}</b>\n'
    
    if isinstance(obj, types.Message):
        await obj.answer(f'🔥<b>Топ-10 лучших:</b>🔥\n\n{rating}', reply_markup=rating_kb())
    elif isinstance(obj, types.CallbackQuery):
        await obj.message.edit_text(f'🔥<b>Топ-10 лучших:</b>🔥\n\n{rating}', reply_markup=rating_kb())
        await obj.answer()
