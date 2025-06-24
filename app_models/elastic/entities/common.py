from enum import Enum


class IndexedEntities(str, Enum):
    """
    Entities indexed in Elasticsearch
    """

    ARTICLE = "article"


def build_index_name(entity: str) -> str:
    """
    Build the final index name from the entity name

    :type entity: str
    :param entity: The entity from which we generate the name

    :rtype: str
    :return: The index name of the entity
    """
    return f"demo_{entity}_index"
