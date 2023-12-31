from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException

from app.api import depends
from app.core.config import settings
from app.database import Database
from app.schemas import UserScheme, SubscribersScheme, SubscribersSchemeAdd

router = APIRouter(prefix="/subscribers")


@router.post("/new")
async def new(
    task: SubscribersSchemeAdd,
    db: Database = Depends(depends.get_db),
    current_user: UserScheme = Depends(depends.get_current_user),
):
    if "/+" in "".join(task.targets):
        raise HTTPException(status_code=404, detail="Ссылка на канал должна быть публичной.")
    price = task.count * settings.PRICE
    if current_user.balance >= price:
        await db.user.update(current_user.id, balance=current_user.balance-price)
        new_task = await db.subscribers_task.new(current_user.id, task.count, task.start_date, task.end_date)
        await db.session.flush()
        for target in task.targets:
            new_task.targets.append(await db.subscribers_target.new(new_task.id, task.count, target))
        await db.session.commit()

        before_execution: timedelta = new_task.end_date - new_task.next_start_date
        speed = f"1 подписчик в {f'{new_task.delay / 60} мин' if new_task.delay >= 60 else f'{new_task.delay} сек'}"
        last_bot = new_task.next_start_date-timedelta(seconds=new_task.delay)
        return SubscribersScheme(**new_task.__dict__, before_execution=int(before_execution.total_seconds()),
                                 last_bot=last_bot,
                                 count=new_task.targets[0].count, count_done=0,
                                 speed=speed, task_type="subscribers")
    else:
        raise HTTPException(status_code=404, detail="У вас не достаточно средств.")


@router.post("/pause")
async def pause(
    task_id: int,
    db: Database = Depends(depends.get_db),
    current_user: UserScheme = Depends(depends.get_current_user),
):
    task = await db.subscribers_task.get(task_id)
    if task:
        if task.user_fk == current_user.id:
            is_pause = False if task.pause else True
            await db.subscribers_task.update(task.id, pause=is_pause)
            await db.session.commit()
            return {"pause": is_pause}
        else:
            raise HTTPException(status_code=404, detail="Вы не создатель задачи.")
    else:
        raise HTTPException(status_code=404, detail="Такой задачи не существует.")
