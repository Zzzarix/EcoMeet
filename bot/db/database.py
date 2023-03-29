import datetime
from .base import _db
from .models import User, Category, Task
from typing import Optional

class Database:
    def __init__(self, _db) -> None:
        self._db = _db
    
    async def get_message(self, key: str) -> str:
        res = await self._db.messages.find_one({'_id': key})
        return res.get('text', key)

    async def create_user(self, id: int) -> User:
        user = User(_id=id)
        await self._db.users.insert_one(user.get_payload())
        return user
    
    async def get_user(self, id: int) -> Optional[User]:
        res = await self._db.users.find_one({'_id': id})
        return User(**res) if res else None
    
    async def update_user(self, user: User):
        await self._db.users.replace_one({'_id': user.id}, user.get_payload())
    
    async def add_points(self, id: int, points: int):
        self._db.users.update_one({'_id': id}, {'$inc': {'points': points}})
    
    async def delete_user(self, id: int):
        await self._db.users.delete_one({'_id': id})
    
    async def get_users(self) -> list[User]:
        res = []
        async for u in self._db.users.find():
            res.append(User(**u))
        return res
    
    async def get_category(self, id: int) -> Category:
        res = await self._db.categories.find_one({'_id': id})
        return Category(**res) if res else None

    async def get_categories(self) -> list[Category]:
        res = []
        async for c in self._db.categories.find():
            res.append(Category(**c))
        return res

    async def get_task(self, id: int) -> Task:
        res = await self._db.tasks.find_one({'_id': id})
        return Task(**res) if res else None

    async def get_tasks(self, category: int) -> list[Task]:
        res = []
        async for t in self._db.tasks.find({'category': category}):
            res.append(Task(**t))
        return res


db = Database(_db)
