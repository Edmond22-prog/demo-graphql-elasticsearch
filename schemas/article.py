import graphene
from graphene_pydantic import PydanticObjectType

from app_models.elastic.entities import Article, PaginatedArticles
from schemas.category import CategoryEntitySchema
from schemas.user import UserMinSchema


class ArticleSchema(PydanticObjectType):
    author = graphene.Field(UserMinSchema)
    categories = graphene.List(CategoryEntitySchema)

    class Meta:
        model = Article


class PaginatedArticlesSchema(PydanticObjectType):
    articles = graphene.List(ArticleSchema)

    class Meta:
        model = PaginatedArticles
