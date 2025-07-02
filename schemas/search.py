import graphene
from graphene_pydantic import PydanticInputObjectType

from app_models.elastic.entities import FilterItem, SearchInput


class FilterItemInSchema(PydanticInputObjectType):
    relation = graphene.String()

    class Meta:
        model = FilterItem


class SearchInputSchema(PydanticInputObjectType):
    page = graphene.Int(default_value=1)
    size = graphene.Int(default_value=30)
    filters = graphene.List(FilterItemInSchema, default_value=[])

    class Meta:
        model = SearchInput
