from enum import Enum
from typing import Optional, List

from pydantic import BaseModel
from datetime import date


class OrderStatus(str, Enum):
    OPEN = 'open'
    IN_PROCESS = 'in_process'
    DECLINED = 'declined'
    CLOSED = 'closed'


class OrderBase(BaseModel):
    title: str
    description: str
    reward: int
    category_id: int


class Order(OrderBase):
    id: int
    owner_id: int
    status: OrderStatus
    worker_id: Optional[int]
    created_at: Optional[date]
    assigned_at: Optional[date]
    closed_at: Optional[date]

    class Config:
        from_attributes = True

class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    status: OrderStatus
    worker_id: Optional[int]

class GetOrders(BaseModel):
    status: Optional[OrderStatus] = OrderStatus.OPEN
    owner: Optional[int] = None
    worker: Optional[int] = None
    page: Optional[int] = None
    amount: Optional[int] = None
    categories: List[int] = None
    paybacks: List[int] = None