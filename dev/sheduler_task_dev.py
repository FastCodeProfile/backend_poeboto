from datetime import datetime, timedelta

from pydantic import BaseModel, AwareDatetime


class Task(BaseModel):
    task: str = "Задача"
    count: int = 10
    count_done: int = 0
    limit_in_hour: int = 0
    start_date: AwareDatetime = datetime.now()
    end_date: AwareDatetime = datetime.now()

    class Config:
        from_attributes = True


task = Task()

print(task.end)