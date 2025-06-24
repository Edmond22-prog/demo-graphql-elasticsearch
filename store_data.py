import json
import os

import django

from app_models.elastic.entities import IndexedEntities
from app_models.elastic.mappings.article_mappings import ARTICLE_INDEX_SETTINGS
from app_models.memory import Memory

# --- Insert categories into Django DB ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")
django.setup()

from app_models.models import Category

with open("data/categories_unique.json") as f:
    categories = json.load(f)

for cat in categories:
    Category.objects.get_or_create(
        uuid=cat["uuid"],
        defaults={
            "name": cat["name"],
            "normalized_name": cat["normalized_name"],
            "created_at": cat["created_at"],
        }
    )

print(f"[*] Inserted/verified {len(categories)} categories in the database.")


# --- Index articles into Elasticsearch ---
memory = Memory.get_instance()

article_index_name = memory.indexes[IndexedEntities.ARTICLE]

with open("data/articles_long.json") as f:
    articles_dict = json.load(f)

to_index = []
if articles_dict:
    for article_dict in articles_dict:
        article_dict["_index"] = article_index_name
        to_index.append(article_dict)

    if not memory.es_helper.index_exists(article_index_name):
        memory.es_helper.create_index(article_index_name, ARTICLE_INDEX_SETTINGS)

    memory.es_helper.insert_doc_in_index(index_name=article_index_name, docs=to_index)

print(f"[*] Indexed {len(to_index)} articles.")
