import aiohttp
import asyncio
import os

from capture import CompressedCaptureManager

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))

URL = f'http://{HOST}:{PORT}/ws'

async def main():
    camera = CompressedCaptureManager()

    session = aiohttp.ClientSession()
    async with session.ws_connect(URL) as ws:
        for i in range(200):
            print(i)
            await capture_and_send(ws, camera)

        await session.close()
    
async def capture_and_send(ws, camera):
    jpeg = camera.encode()
    await ws.send_bytes(jpeg)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())