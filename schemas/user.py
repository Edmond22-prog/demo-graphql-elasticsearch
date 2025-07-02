from graphene_pydantic import PydanticObjectType

from app_models.elastic.entities import UserMin


class UserMinSchema(PydanticObjectType):
    class Meta:
        model = UserMin
