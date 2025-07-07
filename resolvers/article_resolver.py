import copy
import logging

import graphene

from app_models.elastic.entities import Article, IndexedEntities, PaginatedArticles
from app_models.memory import Memory
from schemas import PaginatedArticlesSchema, SearchInputSchema

memory = Memory.get_instance()


class ArticleQuery(graphene.ObjectType):
    search_articles = graphene.Field(
        PaginatedArticlesSchema,
        search_in=SearchInputSchema(required=True),
        description="Search for articles in index matching provided inputs."
    )

    def resolve_search_articles(self, info, search_in: SearchInputSchema):
        # Extract search parameters
        page = search_in.page
        size = search_in.size
        filters = search_in.filters
        regex_on = search_in.regex_on
        exact_search_on = search_in.exact_search_on
        query = search_in.query.strip() if search_in.query else ""

        # Calculate pagination
        start = (page - 1) * size
        end = page * size

        # Build Elasticsearch query
        should_query = []
        filter_query = []

        if query:
            if exact_search_on:
                print("[*] Making exact match ...")
                should_query.extend(
                    [
                        {"match_phrase_prefix": {"title": query}},
                        {"match_phrase_prefix": {"content": query}},
                        {"match_phrase_prefix": {"summary": query}},
                    ]
                )

            elif regex_on:
                print("[*] Making regex match ...")
                should_query.extend(
                    [
                        {
                            "regexp": {
                                "title": {
                                    "value": f"""{query}""",
                                    "flags": "ALL",
                                    "case_insensitive": True,
                                    "max_determinized_states": 10000,
                                    "rewrite": "constant_score",
                                }
                            }
                        },
                        {
                            "regexp": {
                                "content": {
                                    "value": f"""{query}""",
                                    "flags": "ALL",
                                    "case_insensitive": True,
                                    "max_determinized_states": 10000,
                                    "rewrite": "constant_score",
                                }
                            }
                        },
                        {
                            "regexp": {
                                "summary": {
                                    "value": f"""{query}""",
                                    "flags": "ALL",
                                    "case_insensitive": True,
                                    "max_determinized_states": 10000,
                                    "rewrite": "constant_score",
                                }
                            }
                        },
                    ]
                )

            else:
                print("[*] Simple match ...")
                should_query.extend(
                    [
                        {"match": {"title": query}},
                        {"match": {"content": query}},
                        {"match": {"summary": query}},
                        {"match_phrase": {"title": query}},
                        {"match_phrase": {"content": query}},
                        {"match_phrase": {"summary": query}},
                    ]
                )

        if filters:
            print("[*] Filtering ...")
            for filter_item in filters:
                if filter_item.key == "categories":
                    filter_query.append(
                        {"terms": {"categories.normalized_name": filter_item.value}}
                    )

                if filter_item.key == "tags":
                    filter_query.append({"terms": {"tags": filter_item.value}})

                # TODO: Implement for created_at, updated_at, published

        bool_query = {
            "should": should_query,
            "filter": filter_query,
        }
        if len(should_query) > 1:
            bool_query["minimum_should_match"] = 1

        es_query = {"query": {"bool": bool_query}, "from": start, "size": size}

        # Retrieve from ES and parse results
        article_index_name = memory.indexes[IndexedEntities.ARTICLE]
        results = memory.es_helper.retrieve_docs(
            index_name=article_index_name, query=es_query
        )
        articles = [Article(**hit["_source"]) for hit in results]

        # Check if there are more articles for pagination
        es_more_query = copy.deepcopy(es_query)
        es_more_query["from"] = end
        more_articles = memory.es_helper.retrieve_docs(
            index_name=article_index_name, query=es_more_query
        )

        # Count total for pagination
        es_query = {"query": {"bool": bool_query}}
        total = memory.es_helper.count_docs(query=es_query, index_name=article_index_name)

        return PaginatedArticles(
            page=page,
            size=size,
            total=total,
            more=len(more_articles) > 0,
            articles=articles,
        )
