import copy


USER_MIN_PROP = {
    "type": "object",
    "properties": {
        "uuid": {"type": "keyword"},
        "fullname": {"type": "keyword"},
        "email": {"type": "keyword"},
    },
}


CATEGORY_PROP = {
    "type": "nested",
    "properties": {
        "uuid": {"type": "keyword"},
        "name": {"type": "text"},
        "normalized_name": {"type": "keyword"},
        "created_at": {"type": "date"},
    },
}


ARTICLE_INDEX_SETTINGS = {
    "mappings": {
        "properties": {
            "uuid": {"type": "keyword"},
            "title": {"type": "text"},
            "content": {"type": "text"},
            "summary": {"type": "text"},
            "author": copy.deepcopy(USER_MIN_PROP),
            "categories": copy.deepcopy(CATEGORY_PROP),
            "tags": {"type": "keyword"},
            "published": {"type": "boolean"},
            "created_at": {"type": "date"},
            "updated_at": {"type": "date"},
        }
    }
}
