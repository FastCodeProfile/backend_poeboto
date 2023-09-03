import random

from loguru import logger
from datetime import timedelta
from datetime import datetime as dt

from pyrogram.errors import UsernameNotOccupied

from app.database import Database
from app.database.models import ReactionsTask
from app.utils.telegram.client import TgClient


async def reactions(db: Database, task: ReactionsTask, client: TgClient):
    targets = await db.reactions_target.get_for_working()
    if not targets:
        await db.reactions_task.update(task.id, completed=True)
        await db.session.commit()
        logger.success(f"Реакции: задача №{task.id} завершена!")
    else:
        for target in targets:
            if not target.error:
                if client.bot_id not in [used_bot.bot_fk for used_bot in target.used_bots]:
                    try:
                        await client.reaction(target.target, random.choice(task.reactions.split(",")))
                        target.count_done += 1
                        await db.reactions_target.update(target.id, count_done=target.count_done)
                        await db.reactions_used_bot.new(client.bot_id, target.id)
                        await db.session.commit()
                        logger.info(f"Реакции: задача №{task.id} "
                                    f"цель №{target.id} бот №{client.bot_id} - {target.count_done}/{target.count}")
                    except UsernameNotOccupied:
                        logger.info(f"Реакции: задача №{task.id} цель №{target.id} - недоступна.")
                        await db.reactions_task.update(task.id, pause=True)
                        await db.reactions_target.update(
                            target.id,
                            error="Ссылка на канал была изменена или канал стал непубличным.")
                        await db.session.commit()

                else:
                    continue
        next_start_date = dt.now()+timedelta(seconds=task.delay)
        await db.reactions_task.update(task.id, busy=False, next_start_date=next_start_date)
        await db.session.commit()
