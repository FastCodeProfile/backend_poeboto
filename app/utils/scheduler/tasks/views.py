from loguru import logger
from datetime import timedelta
from datetime import datetime as dt

from pyrogram.errors import UsernameNotOccupied

from app.database import Database
from app.database.models import ViewsTask
from app.utils.telegram.client import TgClient


async def views(db: Database, task: ViewsTask, client: TgClient):
    targets = await db.views_target.get_for_working()
    if not targets:
        await db.views_task.update(task.id, completed=True)
        await db.session.commit()
        logger.success(f"Просмотры: задача №{task.id} завершена!")
    else:
        for target in targets:
            if not target.error:
                if client.bot_id not in [used_bot.bot_fk for used_bot in target.used_bots]:
                    try:
                        await client.view(target.target, task.limit)
                        target.count_done += 1
                        await db.views_target.update(target.id, count_done=target.count_done)
                        await db.views_used_bot.new(client.bot_id, target.id)
                        await db.session.commit()
                        logger.info(f"Просмотры: задача №{task.id} "
                                    f"цель №{target.id} бот №{client.bot_id} - {target.count_done}/{target.count}")
                    except UsernameNotOccupied:
                        logger.info(f"Просмотры: задача №{task.id} цель №{target.id} - недоступна.")
                        await db.views_task.update(task.id, pause=True)
                        await db.views_target.update(target.id,
                                                     error="Ссылка на канал была изменена или канал стал непубличным.")
                        await db.session.commit()

                else:
                    continue
        next_start_date = dt.now()+timedelta(seconds=task.delay)
        await db.views_task.update(task.id, busy=False, next_start_date=next_start_date)
        await db.session.commit()
