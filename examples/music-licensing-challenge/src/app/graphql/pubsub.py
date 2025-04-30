import asyncio

from .types.song import Song

song_update_queue: asyncio.Queue[Song] = asyncio.Queue()


async def trigger_license_change_subscription(song_model):
    song = Song.from_model(song_model)
    await song_update_queue.put(song)
