import httpx
from io import BytesIO
from functools import lru_cache

@lru_cache(maxsize=None)
async def download_image(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        img = BytesIO(response.content)
    return img
