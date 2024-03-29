from typing import List, Optional

from fastapi import APIRouter, Depends

from src.market.models.auth import User
from src.market.models.orders import Order, OrderCreate, OrderStatus, OrderUpdate, GetOrders
from src.market.services.auth import get_current_user
from src.market.services.orders import OrdersService

router = APIRouter(
    prefix='/orders',
    tags=['orders']
)


@router.post('/list', response_model=List[Order])
def get_orders(
        request: GetOrders,
        service: OrdersService = Depends()
):
    """
    Получение списка заказов.

    - **status**: статус заказаа (см. схему OrderStatus)
    - **owner**: ID владельца заказа
    - **worker**: ID исполнителя заказа
    - **page**: страница заказов
    - **amount**: количество заказов
    - **categories**: массив ID необходимых категорий
    - **paybacks**: массив ID необходимых способов оплаты

    \f
    :param request:
    :param service:
    :return:
    """
    return service.get_orders(order_status=request.status,
                              owner_id=request.owner,
                              worker_id=request.worker,
                              page=request.page,
                              amount=request.amount,
                              categories=request.categories,
                              paybacks=request.paybacks)



@router.get('/{order_id}', response_model=Order, summary="Получение заказа")
def get_order(
        order_id: int,
        service: OrdersService = Depends(),
):
    """
    Получение заказа.

    - **order_id**: ID заказа.

    \f
    :param order_id:
    :param service:
    :return:
    """
    return service.get_order(order_id)


@router.post('/', response_model=Order, summary='Создание заказа')
def create_order(
        order_data: OrderCreate,
        user: User = Depends(get_current_user),
        service: OrdersService = Depends(),
):
    """
    Первичное создание заказа.

    - **title**: название заказа
    - **description**: длинное описание заказа
    - **reward**: сумма заказа

    \f
    :param order_data:
    :param user:
    :param service:
    :return:
    """
    return service.create_order(order_data, user)


@router.put('/{order_id}', response_model=Order, summary='Обновление заказа')
def update_order(
        order_id: int,
        update_data: OrderUpdate,
        user: User = Depends(get_current_user),
        service: OrdersService = Depends()
):
    """
    Обновление информации о заказе.


    :param order_id:
    :param update_data:
    :param user:
    :param service:
    :return:
    """
    return service.update_order(order_id, user, update_data)