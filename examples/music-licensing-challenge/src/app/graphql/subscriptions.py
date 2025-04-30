from typing import AsyncGenerator

import strawberry

from .pubsub import song_update_queue
from .types.song import Song


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def license_changed(self) -> AsyncGenerator[Song, None]:
        while True:
            song = await song_update_queue.get()
            yield song
