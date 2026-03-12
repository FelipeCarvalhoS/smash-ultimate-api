from fastapi_pagination import Page, paginate
from pydantic import BaseModel
from utils import load_json
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type


TBaseModel = TypeVar('TBaseModel', bound=BaseModel)


class Service(ABC, Generic[TBaseModel]):
    def __init__(self, schema: Type[TBaseModel], data_filename: str):
        self._schema = schema
        self._data = [self._schema.model_validate(stage) for stage in load_json(data_filename)]
        self._filter_strategies = self._get_filter_strategies()
    
    @abstractmethod
    def _get_filter_strategies(self):
        raise NotImplementedError("Subclasses must implement the _get_filter_strategies method")

    def get_all(self) -> list[TBaseModel]:
        return self._data

    def filter_and_paginate(self, query_params: BaseModel) -> Page[TBaseModel]:
        return paginate(self._filter(query_params))

    def _filter(self, query_params: BaseModel) -> list[TBaseModel]:
        filtered = []

        for item in self._data:
            if self._item_matches_filters(item, query_params):
                filtered.append(item)

        return filtered
    
    def _item_matches_filters(self, item: TBaseModel, query_params: BaseModel) -> bool:
        for key, value in query_params.model_dump().items():
            if value is None:
                continue

            attr = getattr(item, key)
            filter_strategy = self._filter_strategies[key]

            if not filter_strategy(attr, value):
                return False

        return True
