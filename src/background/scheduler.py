from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.background.config import CLUSTERING_JOB_ID, CLUSTERING_JOB_INTERVAL, PARSING_JOB_ID, PARSING_JOB_INTERVAL
from src.background.jobs import clustering_job, parsing_job

bg_scheduler: AsyncIOScheduler = AsyncIOScheduler()
bg_scheduler.add_job(
    parsing_job,    
    'interval',
    seconds=PARSING_JOB_INTERVAL,
    id=PARSING_JOB_ID,
    replace_existing=True
)
bg_scheduler.add_job(
    clustering_job,
    'interval',
    seconds=CLUSTERING_JOB_INTERVAL,
    id=CLUSTERING_JOB_ID,
    replace_existing=True
)