import asyncio
import os

import aiohttp.web

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))


async def testhandle(request):
    return aiohttp.web.Response(text='Test handle')


async def websocket_handler(request):
    print('Websocket connection starting')
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)
    print('Websocket connection ready')

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            print(msg.data)
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.BINARY:
            save_file(msg.data)

            await ws.send_str('recieved')

    print('Websocket connection closed')
    return ws

# Might have async problem with this function
frame_count = 0
def save_file(jpeg):
    global frame_count

    with open('data/output_{}.jpg'.format(frame_count), 'wb') as f:
        f.write(jpeg)

    frame_count += 1

loop = asyncio.get_event_loop()
app = aiohttp.web.Application(loop=loop)
app.router.add_route('GET', '/', testhandle)
app.router.add_route('GET', '/ws', websocket_handler)
aiohttp.web.run_app(app, host=HOST, port=PORT)
