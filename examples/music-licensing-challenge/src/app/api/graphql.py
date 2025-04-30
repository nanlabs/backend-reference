from strawberry.fastapi import GraphQLRouter
from ..graphql.schema import schema

router = GraphQLRouter(schema)
