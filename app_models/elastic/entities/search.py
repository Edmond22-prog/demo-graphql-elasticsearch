from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class FilterRelationType(str, Enum):
    INCLUDES = "includes"
    EXCLUDES = "excludes"
    IS = "is"
    IS_NOT = "is not"

    AFTER = "is after"
    BEFORE = "is before"
    EQUAL = "is equal"
    BETWEEN = "is between"


class FilterItem(BaseModel):
    key: str
    relation: FilterRelationType = FilterRelationType.INCLUDES
    value: List[str]


class SearchInput(BaseModel):
    page: int
    size: int
    query: Optional[str]
    regex_on: Optional[bool] = False
    exact_search_on: Optional[bool] = False
    filters: List[FilterItem] = []
