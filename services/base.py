from pydantic import BaseModel
from utils.loader import load_json
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type


T = TypeVar('T', bound=BaseModel)


class Service(ABC, Generic[T]):
    def __init__(self, schema: Type[T], data_filename: str):
        self._schema = schema
        self._data = [self._schema.model_validate(stage) for stage in load_json(data_filename)]
        self._indexes = self._get_indexes()
        self._filter_strategies = self._get_filter_strategies()

    @abstractmethod
    def _get_indexes(self):
        raise NotImplementedError("Subclasses must implement _get_indexes method")
    
    @abstractmethod
    def _get_filter_strategies(self):
        raise NotImplementedError("Subclasses must implement _get_filter_strategies method")

    def get_all(self) -> list[T]:
        return self._data
    
    def filter(self, **kwargs) -> list[T]:
        filtered = []

        for item in self._data:
            matches = True

            for key, value in kwargs.items():
                if value is None:
                    continue

                attr = getattr(item, key)
                filter_strategy = self._filter_strategies[key]

                if not filter_strategy(attr, value):
                    matches = False
                    break

            if matches:
                filtered.append(item)

        return filtered
