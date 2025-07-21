from typing import Union, Annotated

from fastapi import APIRouter, status, Depends, Response, BackgroundTasks

from src.catalogue.models.pydantic import ProductModel, ProductCreate
from src.catalogue.services import get_product_service
from src.common.enums import TaskStatus
from src.common.exceptions.base import ObjectDoesNotExistException
from src.common.schemas.common import ErrorResponse
from src.general.schemas.task_status import TaskStatusModel

product_router = APIRouter(prefix="/products")


@product_router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=list[ProductModel]
)
async def get_products_list(product_service=Depends(get_product_service)) -> list[ProductModel]:
    """
    Get list of products

    :param product_service:
    :return: Response with list of ProductModels
    """
    return await product_service.list()


@product_router.get(
    path="/details/{pk}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": ProductModel},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}
    },
    response_model=Union[ProductModel, ErrorResponse]
)
async def get_product_details(
        response: Response,
        pk: int,
        service: Annotated[get_product_service, Depends()],
) -> Union[ProductModel, ErrorResponse]:
    """
    Get list of products

    :return: Response with list of ProductModels
    """
    try:
        response = await service.detail(pk=pk)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return response

@product_router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
async def create_product(
        product_data: ProductCreate,
        service: Annotated[get_product_service, Depends()]
):
    created_product = await service.create(instance_data=product_data)
    return created_product

@product_router.get(
    "/search",
    status_code=status.HTTP_200_OK
)
async def search(
        keyword: str,
        service: Annotated[get_product_service, Depends()]
):
    response = await service.search(keyword=keyword)
    return response


@product_router.post(
    "/update-index",
    status_code=status.HTTP_200_OK

)
async def update_elastic(
        background_tasks: BackgroundTasks,
        service: Annotated[get_product_service, Depends()]
):
    status_model = await TaskStatusModel(status=TaskStatus.IN_PROGRESS).save_to_redis()
    background_tasks.add_task(service.update_search_index, status_model.uuid)

    return await TaskStatusModel().get_from_redis(uuid=status_model.uuid)
