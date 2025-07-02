from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app_models.elastic.entities.category import Category
from app_models.elastic.entities.user import UserMin


class Article(BaseModel):
    uuid: str
    title: str
    content: str
    summary: Optional[str] = ""
    author: UserMin
    categories: List[Category]
    tags: List[str] = None
    published: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class PaginatedArticles(BaseModel):
    page: int
    size: int
    total: int
    more: bool
    articles: List[Article] = []
