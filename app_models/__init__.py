from app_models.elastic.create_indexes import create_demo_indexes
from app_models.elastic.entities import IndexedEntities
from app_models.elastic.entities.common import build_index_name
from app_models.elastic.es_helper import ElasticsearchHelper
from app_models.memory import Memory
from demo import settings

memory = Memory.get_instance()

memory.es_helper = ElasticsearchHelper(
    es_host=settings.ES_HOST,
    es_port=settings.ES_PORT,
    es_username=settings.ES_USERNAME,
    es_password=settings.ES_PASSWORD,
)

# Create default index if not existing
for entity in IndexedEntities:
    memory.indexes[entity] = build_index_name(entity)

create_demo_indexes()
