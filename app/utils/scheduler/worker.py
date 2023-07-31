from arq import cron

from app.core.config import settings
from app.utils.scheduler.cron import check_proxies, bot_online
from app.utils.scheduler.tasks import subscribers, views, tasks


class WorkerSettings:
    redis_settings = settings.redis
    cron_jobs = [
        # cron(check_proxies.run_check_proxies, second=0),
        cron(tasks.Tasks().run_tasks, second=0, run_at_startup=True),
        # cron(views.Views().run_tasks, second=5),
        # cron(subscribers.Subscribers().run_tasks, second=10),
        # cron(bot_online.BotOnline().run_set_online,
        #      minute={0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55})
    ]
