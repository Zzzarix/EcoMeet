from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore, create_engine

from ..config import config

engine = create_engine(config['db']['uri'])

jobstores = {
    'default': SQLAlchemyJobStore(engine=engine)
}

gconfig = {
    'max_instances': 10000,
    'misfire_grace_time': 10000
}

scheduler = AsyncIOScheduler(gconfig=gconfig, jobstores=jobstores)

async def start_scheduler():
    scheduler.start()
