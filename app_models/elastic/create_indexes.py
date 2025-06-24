import logging

from app_models.elastic.entities import IndexedEntities
from app_models.elastic.mappings.article_mappings import ARTICLE_INDEX_SETTINGS
from app_models.memory import Memory

# Set logging level for elasticsearch to ERROR to suppress warnings
logging.getLogger("elasticsearch").setLevel(logging.ERROR)

memory = Memory.get_instance()


def create_demo_indexes():
    """
    Create Demo Indexes for the different indexed entities.
    """
    index_mappings = {IndexedEntities.ARTICLE: ARTICLE_INDEX_SETTINGS}

    for entity in index_mappings:
        if memory.es_helper.index_exists(memory.indexes[entity]):
            continue

        # index doest not exists
        memory.es_helper.create_index(
            index_name=memory.indexes[entity], index_settings=index_mappings[entity]
        )
