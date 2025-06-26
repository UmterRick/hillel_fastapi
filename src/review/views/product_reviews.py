from typing import Annotated

from fastapi import APIRouter, status, Response
from fastapi.params import Depends

from src.common.exceptions.base import ObjectDoesNotExistException
from src.common.schemas.common import ErrorResponse
from src.review.models.mongo import BaseProductReview, ProductReview, Reply
from src.review.services import ProductReviewService

router = APIRouter(prefix="/product-reviews")


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=list[BaseProductReview]
)
async def product_review_list(product_review_service: Annotated[ProductReviewService, Depends()]) -> list[
    BaseProductReview]:
    """
    Get list of product reviews

    """
    return await product_review_service.list()


@router.get(
    path="/{pk}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": ProductReview},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}
    },
    response_model=ProductReview | ErrorResponse
)
async def product_review_detail(
        response: Response,
        pk: str,
        product_review_service: Annotated[ProductReviewService, Depends()]
) -> Response | ErrorResponse:
    """
    Get list of product reviews

    """
    try:
        response = await product_review_service.detail_with_replies(pk=pk)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return response


@router.post(
    "/",
    response_model=ProductReview
)
async def add_review(review: BaseProductReview, service: ProductReviewService = Depends()):
    new_review = await service.create(instance_data=review)
    return new_review


@router.post(
    "/{pk}/reply",
    responses={
        status.HTTP_200_OK: {"model": ProductReview},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}
    },
    response_model=ProductReview | ErrorResponse
)
async def add_reply(
response: Response,
        pk: str,
        reply: Reply,
        service: Annotated[ProductReviewService, Depends()]
):
    try:
        response = await service.add_reply(pk, reply)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)
    return  response
