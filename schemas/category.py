from graphene_django import DjangoObjectType
from graphene_pydantic import PydanticObjectType

from app_models.elastic.entities import Category as CategoryEntity
from app_models.models import Category


class CategorySchema(DjangoObjectType):

    class Meta:
        model = Category
        fields = "__all__"


class CategoryEntitySchema(PydanticObjectType):

    class Meta:
        model = CategoryEntity
