from arq import cron

from app.core.config import settings
from app.utils.scheduler.cron import start_tasks


class WorkerSettings:
    redis_settings = settings.redis
    cron_jobs = [
        # cron(check_proxies.run_check_proxies, minute=0, run_at_startup=True),
        cron(start_tasks.RunTasks().run_tasks, second={0, 10, 20, 30, 40, 50}, run_at_startup=True),
    ]
