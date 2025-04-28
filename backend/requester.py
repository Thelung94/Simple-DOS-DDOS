import aiohttp
import asyncio

async def send_request(session, url, proxy_ip=None):
    try:
        proxy = None
        if proxy_ip:
            proxy = f"http://{proxy_ip}"

        async with session.get(url, proxy=proxy, timeout=120) as response:
            return response.status == 200
    except Exception as e:
        print(f"[!] Request failed: {e}")
        return False
