from fastapi import APIRouter, Depends, HTTPException

from app.api import depends
from app.core.config import settings
from app.database import Database
from app.schemas import UserScheme, ViewsSchemeAdd, ViewsScheme

router = APIRouter(prefix="/views")


@router.post("/new", response_model=ViewsScheme)
async def new(
    task: ViewsSchemeAdd,
    db: Database = Depends(depends.get_db),
    current_user: UserScheme = Depends(depends.get_current_user),
):
    if "/+" in "".join(task.targets):
        raise HTTPException(status_code=404, detail="Ссылка на канал должна быть публичной.")
    price = task.count * settings.PRICE
    if current_user.balance >= price:
        await db.user.update(current_user.id, balance=current_user.balance-price)
        new_task = await db.views_task.new(current_user.id, task.count, task.start_date, task.end_date, task.limit)
        await db.session.flush()
        for target in task.targets:
            new_task.targets.append(await db.views_target.new(new_task.id, task.count, target))
        await db.session.commit()
        return ViewsScheme(**new_task.__dict__, task_type="views")
    else:
        raise HTTPException(status_code=404, detail="У вас не достаточно средств.")


@router.post("/pause")
async def pause(
    task_id: int,
    db: Database = Depends(depends.get_db),
    current_user: UserScheme = Depends(depends.get_current_user),
):
    task = await db.views_task.get(task_id)
    if task:
        if task.user_fk == current_user.id:
            is_pause = False if task.pause else True
            await db.views_task.update(task.id, pause=is_pause)
            await db.session.commit()
            return {"pause": is_pause}
        else:
            raise HTTPException(status_code=404, detail="Вы не создатель задачи.")
    else:
        raise HTTPException(status_code=404, detail="Такой задачи не существует.")
