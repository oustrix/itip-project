from pydantic import BaseModel


class WorkerBase(BaseModel):
    pass


class Worker(WorkerBase):
    id: int
    user_id: int
    main_category: int