from typing import Annotated

from fastapi.params import Depends

from src.common.service import BaseService
from src.review.models.mongo import Reply, ProductReview
from src.review.repository import ProductReviewRepository


class ProductReviewService(BaseService):
    def __init__(
            self,
            repository: Annotated[ProductReviewRepository, Depends()]
    ):
        super().__init__(repository=repository)

    async def add_reply(self, pk: str, reply: Reply) -> ProductReview:
        review = await self.repository.get(pk=pk)

        review.replies.append(reply.model_dump())

        return await review.save()

    def __build_reply_tree(self, parent_id, replies):
        tree = []
        for reply in replies:
            if reply.to_reply == parent_id:
                reply.replies = self.__build_reply_tree(reply.id, replies)
                tree.append(reply)
        return tree

    async def detail_with_replies(self, pk: str) -> ProductReview:
        review = await self.repository.get(pk=pk)
        replies = self.__build_reply_tree(parent_id=None, replies=review.replies)
        review.replies = replies
        return review


