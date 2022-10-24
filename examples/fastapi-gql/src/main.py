import strawberry
import uvicorn
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from models.queries import Query

schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(schema)


app = FastAPI(
    title='StrawberryGql',
    description='GraphQL Contact APIs',
    version='0.1'
)
app.include_router(graphql_app, prefix="/graphql")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
