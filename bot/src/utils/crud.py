import aiohttp

async def get_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()

async def post_data(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            response.raise_for_status()
            return await response.json()

async def put_data(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.put(url, json=data) as response:
            response.raise_for_status()
            return await response.json()

async def delete_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.delete(url) as response:
            response.raise_for_status()
            return await response.json()
