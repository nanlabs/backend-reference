import strawberry

from .mutations import Mutations
from .queries import Query
from .subscriptions import Subscription

schema = strawberry.Schema(query=Query, mutation=Mutations, subscription=Subscription)
