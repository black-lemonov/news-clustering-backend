from celery import Celery
from celery.utils.log import get_task_logger

from src.bg.config import (
    CLUSTERING_TASK_INTERVAL,
    ENABLE_UTC,
    PARSING_TASK_INTERVAL,
    QUEUE_BACKEND,
    QUEUE_URL,
    TIMEZONE,
)

app = Celery("bg", broker=QUEUE_URL, backend=QUEUE_BACKEND)

app.conf.update(timezone=TIMEZONE, enable_utc=ENABLE_UTC)

logger = get_task_logger("bg")


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from src.bg.tasks import parsing_task, clustering_task

    sender.add_periodic_task(
        PARSING_TASK_INTERVAL,
        parsing_task.s(),
    )
    sender.add_periodic_task(
        CLUSTERING_TASK_INTERVAL,
        clustering_task.s(),
    )
