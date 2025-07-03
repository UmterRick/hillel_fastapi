from uuid import UUID

from fastapi import APIRouter, status, Response
from src.common.schemas.common import DetailsResponse, ErrorResponse
from src.general.schemas.task_status import TaskStatusModel

router = APIRouter()

@router.get(
    path="/health-check",
    tags=['Status'],
    response_model=DetailsResponse,
    status_code=status.HTTP_200_OK
)
def health_check() -> DetailsResponse:
    """
    Health check endpoint.

    :return: Response is our app alive
    """
    return DetailsResponse(details="OK")


@router.get(
    path="/task-status",
    tags=['Status'],
    response_model=TaskStatusModel,
    status_code=status.HTTP_200_OK
)
async def get_status(uuid: UUID, response: Response):
    transfer_status = await TaskStatusModel.get_from_redis(uuid=uuid)

    if transfer_status is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=f"Task with UUID {uuid} does not exists")

    return transfer_status
