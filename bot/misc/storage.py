from aiogram.fsm.storage.base import BaseStorage, StorageKey, StateType
from typing import Optional, Dict, Any
from aiogram import Bot

from ..db.base import _client


class MongoStorage(BaseStorage):

    db = _client['AiogramFSMStorage']

    async def set_state(self, bot: Bot, key: StorageKey, state: StateType = None) -> None:
        if not await self.db.FSMStorage.find_one({'_id': key.user_id}):
            await self.db.FSMStorage.insert_one({'_id': key.user_id, 'state': state.state, 'data': {}})
        else:
            await self.db.FSMStorage.update_one({'_id': key.user_id}, {'$set': {'state': state.state}})

    async def get_state(self, bot: Bot, key: StorageKey) -> Optional[str]:
        res = await self.db.FSMStorage.find_one({'_id': key.user_id})
        return res.get('state', None) if res else None

    async def set_data(self, bot: Bot, key: StorageKey, data: Dict[str, Any]) -> None:
        if not await self.db.FSMStorage.find_one({'_id': key.user_id}):
            await self.db.FSMStorage.insert_one({'_id': key.user_id, 'state': None, 'data': data})
        else:
            await self.db.FSMStorage.update_one({'_id': key.user_id}, {'$set': {'data': data}})

    async def get_data(self, bot: Bot, key: StorageKey) -> Dict[str, Any]:
        res = await self.db.FSMStorage.find_one({'_id': key.user_id})
        return res.get('data', {}) if res else {}

    async def close(self) -> None:
        _client.close()
