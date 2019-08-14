import asyncio
import os

import aiohttp.web

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))


async def test_handler(request):
    return aiohttp.web.Response(text='Success')


async def websocket_handler(request):
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)

    print('Websocket connection ready')

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.BINARY:
            save_file(msg.data)
            
        await ws.close()

    print('Websocket connection closed')
    return ws

counter = 0
def save_file(jpeg):
    global counter

    with  open('data/output_{}.jpg'.format(counter), 'wb') as f:
        f.write(jpeg)


    counter += 1

loop = asyncio.get_event_loop()
app = aiohttp.web.Application(loop=loop)

app.router.add_route('GET', '/', test_handler)
app.router.add_route('GET', '/ws', websocket_handler)

aiohttp.web.run_app(app, host=HOST, port=PORT)

