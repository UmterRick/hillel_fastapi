from typing import Union, Annotated
from fastapi import APIRouter, status, Depends, Response
from src.orders.models.pydantic import (
    BasketLineModel,
    BasketModel,
    OrderLineModel,
    OrderModel,
    OrderCreateFromBasket,
    OrderUpdate,
)

from src.orders.services import (
    BasketLineService,
    get_basket_line_service,
    BasketService,
    get_basket_service,
    OrderLineService,
    get_order_line_service,
    OrderService,
    get_order_service,
)

from src.common.exceptions.base import ObjectDoesNotExistException
from src.common.schemas.common import ErrorResponse

orders_router = APIRouter(prefix="/orders", tags=["Orders"])



# ------------------------------------------------------------------------
# BasketLine CRUD endpoints
# ------------------------------------------------------------------------


@orders_router.get(
    path="/basket_lines",
    status_code=status.HTTP_200_OK,
    response_model=list[BasketLineModel]
)
async def get_basket_line_list(service: Annotated[BasketLineService, Depends(get_basket_line_service)]) -> list[BasketLineModel]:
    """
    Retrieve list of all basket lines.

    :return: List of BasketLineModel instances.
    """
    return await service.list()


@orders_router.get(
    path="/basket_lines/{basket_line_id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": BasketLineModel},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}
    },
    response_model=Union[BasketLineModel, ErrorResponse]
)
async def get_basket_line_details(
        response: Response,
        basket_line_id: int,
        service: Annotated[BasketLineService, Depends(get_basket_line_service)],
) -> Union[BasketLineModel, ErrorResponse]:
    """
    Retrieve details of a specific basket line by ID.

    :return: BasketLineModel if found, or ErrorResponse if it does not exist.
    """
    try:
        result = await service.detail(pk=basket_line_id)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return result


@orders_router.post(
    path="/basket_lines",
    status_code=status.HTTP_200_OK,
    response_model=BasketLineModel
)
async def basket_line_create(
        basket_line_data: BasketLineModel,
        response: Response,
        service: Annotated[BasketLineService, Depends(get_basket_line_service)],
) -> Union[BasketLineModel, ErrorResponse]:
    """
    Create a new basket line.

    :return: Created BasketLineModel instance.
    """
    try:
        result = await service.create(basket_line_data)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return result


@orders_router.put(
    path="/basket_lines/{basket_line_id}",
    status_code=status.HTTP_200_OK,
    response_model=BasketLineModel
)
async def basket_line_update(
        basket_line_data: BasketLineModel,
        response: Response,
        basket_line_id: int,
        service: Annotated[BasketLineService, Depends(get_basket_line_service)],
) -> Union[BasketLineModel, ErrorResponse]:
    """
    Update an existing basket line by ID.

    :return: Updated BasketLineModel instance.
    """
    try:
        result = await service.update(basket_line_id, basket_line_data)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return result


@orders_router.delete(
    path="/basket_lines/{basket_line_id}",
    status_code=status.HTTP_200_OK,

)
async def basket_line_delete(
        response: Response,
        basket_line_id: int,
        service: Annotated[BasketLineService, Depends(get_basket_line_service)],
) -> dict:
    """
    Delete a basket line by ID.

    :return: Dictionary with deletion confirmation message.
    """
    try:
        await service.delete(pk=basket_line_id)
        result = {"detail": "Basket_line deleted successfully"}
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return result



# ------------------------------------------------------------------------
# Basket CRUD endpoints
# ------------------------------------------------------------------------


@orders_router.get(
    path="/baskets",
    status_code=status.HTTP_200_OK,
    response_model=list[BasketModel]
)
async def get_basket_list(service: Annotated[BasketService, Depends(get_basket_service)]) -> list[BasketModel]:
    """
    Retrieve list of all baskets.

    :return: List of BasketModel instances.
    """
    return await service.list()


@orders_router.get(
    path="/baskets/{basket_id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": BasketModel},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}
    },
    response_model=Union[BasketModel, ErrorResponse]
)
async def get_basket_details(
        response: Response,
        basket_id: int,
        service: Annotated[BasketService, Depends(get_basket_service)],
) -> Union[BasketModel, ErrorResponse]:
    """
    Retrieve details of a specific basket by ID.

    :return: BasketModel if found, or ErrorResponse if it does not exist.
    """
    try:
        result = await service.detail(pk=basket_id)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return result


@orders_router.post(
    path="/baskets",
    status_code=status.HTTP_200_OK,
    response_model=BasketModel
)
async def basket_create(
        basket_data: BasketModel,
        response: Response,
        service: Annotated[BasketService, Depends(get_basket_service)],
) -> Union[BasketModel, ErrorResponse]:
    """
    Create a new basket.

    :return: Created BasketModel instance.
    """
    try:
        result = await service.create(basket_data)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return result


@orders_router.put(
    path="/baskets/{basket_id}",
    status_code=status.HTTP_200_OK,
    response_model=BasketModel
)
async def basket_update(
        basket_data: BasketModel,
        response: Response,
        basket_id: int,
        service: Annotated[BasketService, Depends(get_basket_service)],
) -> Union[BasketModel, ErrorResponse]:
    """
    Update an existing basket by ID.

    :return: Updated BasketModel instance.
    """
    try:
        result = await service.update(pk=basket_id, instance_data=basket_data)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return result


@orders_router.delete(
    path="/baskets/{basket_id}",
    status_code=status.HTTP_200_OK,

)
async def basket_delete(
        response: Response,
        basket_id: int,
        service: Annotated[BasketService, Depends(get_basket_service)],
) -> dict:
    """
    Delete a basket by ID.

    :return: Dictionary with deletion confirmation message.
    """
    try:
        await service.delete(pk=basket_id)
        result = {"detail": "Basket deleted successfully"}
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return result



# ------------------------------------------------------------------------
# OrderLine CRUD endpoints
# ------------------------------------------------------------------------


@orders_router.get(
    path="/order_lines",
    status_code=status.HTTP_200_OK,
    response_model=list[OrderLineModel]
)
async def get_order_line_list(service: Annotated[OrderLineService, Depends(get_order_line_service)]) -> list[OrderLineModel]:
    """
    Retrieve list of all order lines.

    :return: List of OrderLineModel instances.
    """
    return await service.list()


@orders_router.get(
    path="/order_lines/{order_line_id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": OrderLineModel},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}
    },
    response_model=Union[OrderLineModel, ErrorResponse]
)
async def get_order_line_details(
        response: Response,
        order_line_id: int,
        service: Annotated[OrderLineService, Depends(get_order_line_service)],
) -> Union[OrderLineModel, ErrorResponse]:
    """
    Retrieve details of a specific order line by ID.

    :return: OrderLineModel if found, or ErrorResponse if it does not exist.
    """
    try:
        result = await service.detail(pk=order_line_id)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return result

# views.py
"""
OrderLine endpoints:
--------------------
- GET /order-lines/            ✅ Allowed — get list of order lines
- GET /order-lines/{id}        ✅ Allowed — get detail of an order line
- POST /order-lines/           🚫 Not implemented — order lines are created automatically during order creation
- PUT /order-lines/{id}        🚫 Not implemented — order lines are immutable after creation
- DELETE /order-lines/{id}     🚫 Not implemented — order lines cannot be removed from confirmed orders

Reasoning:
OrderLine is a snapshot of the basket state at the moment of order creation. 
They must remain unchanged for consistency, accounting, and order integrity.
"""



# ------------------------------------------------------------------------
# Order CRUD endpoints
# ------------------------------------------------------------------------


@orders_router.get(
    path="/orders",
    status_code=status.HTTP_200_OK,
    response_model=list[OrderModel]
)
async def get_order_list(service: Annotated[OrderService, Depends(get_order_service)]) -> list[OrderModel]:
    """
    Retrieve list of all orders.

    :return: List of OrderModel instances.
    """
    return await service.list()


@orders_router.get(
    path="/orders/{order_id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": OrderModel},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}
    },
    response_model=Union[OrderModel, ErrorResponse]
)
async def get_order_details(
        response: Response,
        order_id: int,
        service: Annotated[OrderService, Depends(get_order_service)],
) -> Union[OrderModel, ErrorResponse]:
    """
    Retrieve details of a specific order by ID.

    :return: OrderModel if found, or ErrorResponse if it does not exist.
    """
    try:
        result = await service.detail(pk=order_id)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return result


@orders_router.post(
    path="/orders",
    status_code=status.HTTP_201_CREATED,
    response_model=OrderModel
)
async def order_create(
        order_data: OrderCreateFromBasket,
        response: Response,
        service: Annotated[OrderService, Depends(get_order_service)],
) -> Union[OrderModel, ErrorResponse]:
    """
    Create a new order from basket.

    :return: Created OrderModel instance.
    """
    try:
        result = await service.create_from_basket(order_data)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return result


@orders_router.put(
    path="/orders/{order_id}",
    status_code=status.HTTP_200_OK,
    response_model=OrderModel
)
async def order_update(
        order_data: OrderUpdate,
        response: Response,
        order_id: int,
        service: Annotated[OrderService, Depends(get_order_service)],
) -> Union[OrderModel, ErrorResponse]:
    """
    Update an existing order by ID.

    :return: Updated OrderModel instance.
    """
    try:
        result = await service.update_order(order_id=order_id, update_data=order_data)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return result


@orders_router.delete(
    path="/orders/{order_id}",
    status_code=status.HTTP_200_OK,

)
async def order_delete(
        response: Response,
        order_id: int,
        service: Annotated[OrderService, Depends(get_order_service)],
) -> dict:
    """
    Delete a order by ID.

    :return: Dictionary with deletion confirmation message.
    """
    try:
        await service.delete(pk=order_id)
        result = {"detail": "Order deleted successfully"}
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return result