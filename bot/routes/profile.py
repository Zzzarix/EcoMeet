from aiogram import types, Bot, Router
from aiogram.filters.command import Command
from ..utils import check_user

from ..misc.keyboards import (
    profile_kb,
    
)
from ..db.database import db

profile_router = Router()


@profile_router.message(Command(commands='profile', commands_ignore_case=True))
@profile_router.callback_query(text='profile')
async def profile(obj):
    flag = await check_user(obj.from_user.id)
    if not flag:
        return

    user = await db.get_user(obj.from_user.id)

    text = 'Ваш профиль\n\n'

    text += f'id {user.id}\nusername @{obj.from_user.username}\n\nФИО {user.name} {user.last_name} {user.patronymic}\n'
            
    birth = user.birth.strftime('%Y.%m.%d')
    
    text += f'Дата рождения {birth}\nEmail {user.email}\n\n'

    text += f'Выполнено заданий {len(user.completed_tasks)}\n' if user.completed_tasks else 'Вы пока не выполнили ни одного задания\n'

    text += f'Ваши быллы: <i>{user.points}</i>' if user.completed_tasks else 'У вас пока нет ни одного балла, но не расстраивайтесь! Вы получите их, выполнив парочку <b>несложных, но полезных для окружающей среды</b> заданий😁!'

    if isinstance(obj, types.Message):
        await obj.answer(text, reply_markup=profile_kb())
    elif isinstance(obj, types.CallbackQuery):
        await obj.message.edit_text(text, reply_markup=profile_kb())
        await obj.answer()
