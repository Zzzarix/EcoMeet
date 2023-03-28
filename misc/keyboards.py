from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from ..db.models import Category, Task

def clear_kb() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()

def signup_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.add(KeyboardButton(text='Отправить контакт', request_contact=True))
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

def menu_kb(can_choose_task: bool) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if can_choose_task:
        kb.row(InlineKeyboardButton(text='Выбрать задание', callback_data='tasks:new'))
    else:
        kb.row(InlineKeyboardButton(text='Выбранное задание', callback_data='tasks:current'))
        kb.row(InlineKeyboardButton(text='Завершить задание', callback_data='tasks:answer'))
    kb.row(InlineKeyboardButton(text='Ваш профиль', callback_data='profile'))
    return kb.as_markup()


def categories_kb(categories: list[Category]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for c in categories:
        kb.add(InlineKeyboardButton(text=c.text, callback_data=f'tasks:new:{c.id}'))
    kb.add(InlineKeyboardButton(text='Вернуться в меню', callback_data='tasks'))
    kb.adjust(1)
    return kb.as_markup()

# def tasks_kb(tasks: list[Task]) -> InlineKeyboardMarkup:
#     kb = InlineKeyboardBuilder()
#     for t in tasks:
#         kb.add(InlineKeyboardButton(text=t.text, callback_data=f'tasks:new:{t.category}:{t.id}'))
#     kb.add(InlineKeyboardButton(text='Вернуться в меню', callback_data='tasks'))
#     kb.adjust(1)
#     return kb.as_markup()

def task_choosed_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Вернуться в меню', callback_data='tasks'))
    kb.adjust(1)
    return kb.as_markup()

def profile_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Ваши забронированные сеансы', callback_data='booking:list'))
    kb.add(InlineKeyboardButton(text='Вернуться в меню', callback_data='tasks'))
    kb.adjust(1)
    return kb.as_markup()

def answer_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Вернуться в меню', callback_data='tasks'))
    kb.adjust(1)
    return kb.as_markup()

def current_task_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Вернуться в меню', callback_data='tasks'))
    kb.adjust(1)
    return kb.as_markup()
