import datetime
from abc import ABC
import enum

import bson
from ..config import config

class _Document(ABC):

    _id: bson.ObjectId  # id in mongo documents (we won't use it)
    _payload: dict  # payload

    def __init__(self, *args, **kwargs):
        self._payload = dict()

    # @abstractmethod
    # def get_payload(self):
    #     raise NotImplementedError("get_payload method not implemented yet.")

    def get_payload(self) -> dict:  # returns payload to insert in mongo collection
        return self._payload

    # @abstractstaticmethod
    # def from_payload(_payload: dict):  # returns class instance from mongo document payload
    #     raise NotImplementedError("from_payload method not implemented yet.")



class Category(_Document):
    id: int
    text: str

    def __init__(self, *, _id: int, text: str, **kwargs) -> None:
        super().__init__()
        self._payload['_id'] = _id
        self._payload['text'] = text

    @property
    def id(self):
        return self._payload['_id']
    
    @property
    def text(self):
        return self._payload['text']
    

class Task(_Document):
    id: int
    category: int
    text: str
    points: int

    def __init__(self, *, _id: int, category: int, text: str, points: int, **kwargs) -> None:
        super().__init__()
        self._payload['_id'] = _id
        self._payload['category'] = category
        self._payload['text'] = text
        self._payload['points'] = points

    @property
    def id(self):
        return self._payload['_id']
    
    @property
    def points(self):
        return self._payload['points']
    
    @property
    def category(self):
        return self._payload['category']
    
    @property
    def text(self):
        return self._payload['text']


class User(_Document):
    id: int
    name: str
    last_name: str
    patronymic: str
    email: str
    phone: str
    points: int
    task: int
    birth: datetime.datetime
    completed_tasks: list[int]

    __months = [
        '',
        'Января',
        'Февраля',
        'Марта',
        'Апреля',
        'Мая',
        'Июня',
        'Июля',
        'Августа',
        'Сентября',
        'Октября',
        'Ноября',
        'Декабря',
    ]

    def __init__(self, *, _id: int, name: str = '', phone: str = '', last_name: str = '', patronymic: str = '', email: str = None, points: int = 0, task: int = None, completed_tasks: list[int] = [], birth: int = None, **kwargs) -> None:
        super().__init__()
        self._payload['_id'] = _id
        self._payload['name'] = name
        self._payload['phone'] = phone
        self._payload['last_name'] = last_name
        self._payload['patronymic'] = patronymic
        self._payload['email'] = email
        self._payload['points'] = points
        self._payload['task'] = task

        if birth:
            self._birth = datetime.datetime.fromtimestamp(birth)

        self._payload['birth'] = birth

        self._payload['completed_tasks'] = completed_tasks
    
    @property
    def birth(self):
        return self._birth

    @birth.setter
    def birth(self, value: datetime.datetime):
        self._birth = value
        self._payload['birth'] = value.timestamp()

    def format_birth(self) -> str:
        return f'{self.birth.day} {self.__months[self.birth.month]} {self.birth.year} года'
    
    @property
    def completed_tasks(self):
        return self._payload['completed_tasks']
    
    def complete_task(self):
        self._payload['completed_tasks'].append(self.task)
        self.task = None

    @property
    def last_name(self):
        return self._payload['last_name']

    @last_name.setter
    def last_name(self, value):
        self._payload['last_name'] = value
    
    @property
    def task(self):
        return self._payload['task']

    @task.setter
    def task(self, value):
        self._payload['task'] = value
    
    @property
    def patronymic(self):
        return self._payload['patronymic']
    
    @patronymic.setter
    def patronymic(self, value):
        self._payload['patronymic'] = value

    @property
    def id(self):
        return self._payload['_id']

    @property
    def name(self):
        return self._payload['name']

    @name.setter
    def name(self, value: str):
        self._payload['name'] = value
    
    @property
    def phone(self) -> str:
        return self._payload['phone']

    @phone.setter
    def phone(self, value: str):
        self._payload['phone'] = value
    

    @property
    def email(self) -> str:
        return self._payload['email']

    @email.setter
    def email(self, value: str):
        self._payload['email'] = value
    
    @property
    def points(self):
        return self._payload['points']

    @points.setter
    def points(self, value: int):
        self._payload['points'] = value


class Payment(_Document):
    order_id: str
    payment_id: int
    payment_url: str
    id: int
    description: str
    amount: int
    date: datetime.datetime
    confirmed: bool
    rebill_id: int

    def __init__(self, *, _id: int, order_id: int = None, payment_id: int = None, payment_url: str = None, description: str = '',
                 amount: int = 0, date: int = 0, confirmed: bool = None, subscription: str = '', rebill_id: int = None, **kwargs) -> None:
        super().__init__()
        self._payload['id'] = _id
        self._payload['order_id'] = order_id
        self._payload['payment_id'] = payment_id
        self._payload['payment_url'] = payment_url
        self._payload['date'] = date
        self._date = datetime.datetime.fromtimestamp(date)
        self._payload['description'] = description
        self._payload['amount'] = amount
        self._payload['subscription'] = subscription
        self._payload['confirmed'] = confirmed
        self._payload['rebill_id'] = rebill_id

    @property
    def id(self):
        return self._payload['_id']
    
    @property
    def rebill_id(self):
        return self._payload['rebill_id']

    @property
    def order_id(self):
        return self._payload['order_id']

    @property
    def payment_id(self):
        return self._payload['payment_id']

    @property
    def payment_url(self):
        return self._payload['payment_url']

    @property
    def description(self):
        return self._payload['description']

    @property
    def amount(self):
        return self._payload['amount']

    @property
    def date(self):
        return self._date

    @property
    def confirmed(self):
        return self._payload['confirmed']
