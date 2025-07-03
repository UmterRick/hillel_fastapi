import datetime
import json
from typing import Self
from uuid import uuid4, UUID

from pydantic import BaseModel, Field

from src.base_settings import base_settings
from src.common.databases.redis import get_redis_client
from src.common.enums import TaskStatus

redis = get_redis_client()

class TaskStatusModel(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    status: TaskStatus = TaskStatus.IN_PROGRESS
    created_at: str = datetime.datetime.now(tz=datetime.timezone.utc).strftime(base_settings.date_time_format)
    done_at: str | None = None
    details: str | None = None

    @staticmethod
    def get_redis_key(uuid: str):
        return f"background_task__{uuid}"

    async def save_to_redis(self) -> Self: # return TaskStatusModel
        redis_key = self.get_redis_key(uuid=str(self.uuid))
        await redis.set(
            name=redis_key,
            value=self.model_dump_json()
        )

        return self

    @classmethod
    async def get_from_redis(cls, uuid: UUID) -> Self | None:
        redis_response = await redis.get(name=cls.get_redis_key(str(uuid)))
        if not redis_response:
            return None

        task_status_data = json.loads(redis_response)
        return TaskStatusModel.model_validate(task_status_data)