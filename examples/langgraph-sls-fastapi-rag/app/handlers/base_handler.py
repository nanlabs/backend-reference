from typing import Union

from app.schemas.context import ContextModel


class BaseHandler:
    def __init__(self) -> None:
        self.next_handler: "BaseHandler" | None = None

    def set_next(self, handler: "BaseHandler") -> None:
        self.next_handler = handler

    async def handle(self, context: ContextModel) -> Union[ContextModel, None]:
        if self.next_handler:
            return await self.next_handler.handle(context)
        return context
