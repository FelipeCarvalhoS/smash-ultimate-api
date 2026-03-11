from fastapi_pagination import Page, paginate, set_page
from fastapi_pagination.bases import AbstractParams
from pydantic import BaseModel
from utils import load_json
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type


T = TypeVar('T', bound=BaseModel)


class Service(ABC, Generic[T]):
    def __init__(self, schema: Type[T], data_filename: str):
        self._schema = schema
        self._data = [self._schema.model_validate(stage) for stage in load_json(data_filename)]
        self._filter_strategies = self._get_filter_strategies()
    
    @abstractmethod
    def _get_filter_strategies(self):
        raise NotImplementedError("Subclasses must implement the _get_filter_strategies method")

    def get_all(self) -> list[T]:
        return self._data

    def filter_and_paginate(self, **filters) -> Page[T]:
        return paginate(self._filter(**filters))

    def _filter(self, **filters) -> list[T]:
        filtered = []

        for item in self._data:
            if self._item_matches_filters(item, **filters):
                filtered.append(item)

        return filtered
    
    def _item_matches_filters(self, item: T, **filters) -> bool:
        for key, value in filters.items():
            if value is None:
                continue

            attr = getattr(item, key)
            filter_strategy = self._filter_strategies[key]

            if not filter_strategy(attr, value):
                return False

        return True
