import logging
from typing import Any, List, Optional

from elasticsearch import ConflictError, Elasticsearch
from elasticsearch.helpers import bulk


class ElasticsearchHelper:
    """Helper for elasticsearch operations"""

    def __init__(
        self,
        es_host: str,
        es_port: str,
        es_username: str,
        es_password: str,
        es_timeout: int = 300,
        es_insert_batch_size: int = 5000,
        es_retrieve_batch_size: int = 10000,
    ):
        self.client = Elasticsearch(
            hosts=[es_host], port=es_port, http_auth=(es_username, es_password)
        )
        self.es_timeout = es_timeout
        self.es_insert_batch_size = es_insert_batch_size
        self.es_retrieve_batch_size = es_retrieve_batch_size

    def index_exists(self, index_name: str) -> bool:
        """
        Check whether an index exists or not

        :type index_name: str
        :param index_name: Index name to check

        :rtype: bool
        :return: True if index exists, False if not.
        """
        if not self.client:
            return False

        return self.client.indices.exists(index=index_name)

    def refresh_index(self, index_name: str) -> None:
        """
        Refresh a given index.

        :type index_name: str
        :param index_name: The index to refresh
        """
        self.client.indices.refresh(index=index_name)

    def create_index(self, index_name: str, index_settings: Optional[dict]) -> bool:
        """
        Create an index with the name and settings.

        :type index_name: str
        :param index_name: The name of the index to create

        :type index_settings: Optional[dict]
        :param index_settings: Settings and mappings of the index to create

        :rtype: bool
        :return: True if index created, False if not
        """
        if not self.client:
            return False

        try:
            if not self.client.indices.exists(index=index_name):
                if index_settings:
                    self.client.indices.create(index=index_name, body=index_settings)
                else:
                    self.client.indices.create(index=index_name)
            return True

        except Exception as e:
            logging.exception(
                f"Problem while creating ElasticSearch Index : {index_name}\n{e}"
            )
            return False

    def update_by_query(self, index_name: str, query: dict) -> bool:
        """
        Update docs matching a query in index.

        :type index_name: str
        :param index_name: The name of the index where to update

        :type query: str
        :param query: The update query

        :rtype: bool
        :return: True if the object updated, False if not
        """
        if not self.client:
            return False

        try:
            self.client.update_by_query(index=index_name, body=query)
            return True

        except ConflictError:
            self.client.indices.refresh(index=index_name)
            try:
                self.client.update_by_query(index=index_name, body=query)
                return True

            except Exception as e:
                logging.exception(
                    f"And error Occurs during the updating of docs in {index_name}\n{e}"
                )
                return False

    def update_entity_prop(
        self, index_name: str, uuid: str, prop: str, value: Any
    ) -> None:
        """
        Update a property value of an entity in the index.

        :type index_name: str
        :param index_name: The name of the index where to update

        :type uuid: str
        :param uuid: The uuid of the entity document to update

        :type prop: str
        :param prop: The property of entity document to update

        :type value: Any
        :param value: New value to set for the property
        """
        update_query = {
            "query": {"term": {"uuid": uuid}},
            "script": {
                "inline": f"ctx._source.{prop}=params.value",
                "lang": "painless",
                "params": {"value": value},
            },
        }

        try:
            self.update_by_query(query=update_query, index_name=index_name)

        except Exception as e:
            logging.exception(
                f"Error while querying index {index_name} with query {update_query}\n{e}"
            )

    def insert_doc_in_index(self, index_name: str, docs: List[dict]) -> bool:
        """
        Insert a list of well-formed documents in an index.

        :type index_name: str
        :param index_name: The name of the index where to insert

        :type docs: List[dict]
        :param docs: Documents to insert in index

        :rtype: bool
        :return: True if documents indexed successfully, False if not
        """
        if not self.client:
            return False

        try:
            # Insert elements by batch
            start = 0
            successful = True
            while start <= len(docs):
                end = min(len(docs), start + self.es_insert_batch_size)
                success, failed = bulk(
                    self.client,
                    docs[start:end],
                    request_timeout=self.es_timeout,
                    index=index_name,
                )
                added = end - start
                successful = added == success
                start = start + self.es_insert_batch_size

            self.client.indices.refresh(index=index_name)
            return successful

        except Exception as e:
            logging.exception(f"Error while trying to insert docs in index!\n{e}")
            return False

    def retrieve_docs(self, index_name: str, query: dict) -> List[dict]:
        """
        Retrieve all documents mapping a query give as parameter.
        The size is in the query body.

        :type index_name: str
        :param index_name: The index where to retrieve docs

        :type query: dict
        :param query: The query from which we retrieve the docs

        :rtype: List[dict]
        :return: List of retrieved documents
        """
        if not self.client or not self.client.indices.exists(index=index_name):
            return []

        try:
            results = self.client.search(
                index=index_name, body=query, request_timeout=self.es_timeout
            )
            return results["hits"]["hits"]

        except Exception as e:
            logging.exception(f"Error while retrieving documents from index.\n{e}")
            return []

    def count_docs(self, index_name: str, query: dict) -> int:
        """
        Count total number of documents in an index matching a given query.

        :type index_name: str
        :param index_name: The index where to count docs

        :type query: dict
        :param query: The query from which we count the docs

        :rtype: int
        :return: Number of documents
        """
        if not self.client or not self.client.indices.exists(index=index_name):
            return 0

        count = self.client.count(body=query, index=index_name)
        if not count or "count" not in count:
            return 0

        return count["count"]
