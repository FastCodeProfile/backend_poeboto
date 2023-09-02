from arq import cron

from app.core.config import settings
from app.utils.scheduler.cron import execution_tasks


class WorkerSettings:
    redis_settings = settings.redis
    cron_jobs = [
        cron(execution_tasks, second={0, 10, 20, 30, 40, 50}),
    ]
