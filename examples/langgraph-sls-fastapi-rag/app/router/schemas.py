from typing import Annotated, Sequence
from uuid import UUID

from langchain_core.documents import Document
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from pydantic import BaseModel as PydanticBaseModel
from pydantic import model_serializer, model_validator

from app.types import FiltersData


class BaseModel(PydanticBaseModel):
    __abstract__ = True


class BaseFilters(PydanticBaseModel):
    __abstract__ = True

    def is_any_filter_set(self) -> bool:
        return any(value is not None for value in self.__dict__.values())

    def __bool__(self) -> bool:
        return self.is_any_filter_set()

    @model_serializer()
    def serialize_model(
        self,
    ) -> dict[str, str | list[str] | int | float | bool | UUID | list[UUID]]:
        data = {}
        for key, value in self.__dict__.items():
            if value is not None:
                data[key] = value
        return data

    @staticmethod
    def comma_str_to_list(value: str) -> list[str]:
        return [elem.strip() for elem in value.split(",") if elem.strip()]

    @model_validator(mode="before")
    @staticmethod
    def convert_filters(filters: FiltersData) -> FiltersData:
        for key, value in filters.items():
            if "__in" in key and isinstance(value, str):
                filters[key] = BaseFilters.comma_str_to_list(value)
            if "__not_in" in key and isinstance(value, str):
                filters[key] = BaseFilters.comma_str_to_list(value)
        return filters




class StatusResponse(BaseModel):
    data: list[Document]

class WebSearchResult(BaseModel):
    title: str
    url: str
    content: str
    score: float

class RetrieveResponse(BaseModel):
    messages: Annotated[Sequence[AnyMessage], add_messages]
    retrieved_docs: list[Document]
    web_search_results: list[WebSearchResult]

class DocumentMetadata(BaseModel):
    source: str
    permalink: str | None = None
    issue: str | None = None


class IndexRequest(BaseModel):
    user_id: str


class RetrieveRequest(BaseModel):
    user_id: str
    thread_id: str
    messages: Annotated[Sequence[AnyMessage], add_messages]
