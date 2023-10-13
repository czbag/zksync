import aiohttp


async def get_bungee_data():
    async with aiohttp.ClientSession() as session:
        url = "https://refuel.socket.tech/chains"
        response = await session.get(url)
        response_data = await response.json()
        if response.status == 200:
            data = response_data["result"]
            return data
        return False
