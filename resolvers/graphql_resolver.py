import graphene

from resolvers.article_resolver import ArticleQuery


class GraphQLQuery(ArticleQuery):
    pass


class GraphQLMutation(graphene.ObjectType):
    pass


demo_schema = graphene.Schema(query=ArticleQuery)
