import asyncio
import aiohttp

async def test_websocket():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('http://localhost:3000/ws') as ws:
            print("Connected to WebSocket server")

            # Send a message to the server
            await ws.send_str("Hello from Python client!")

            # Receive messages for a short time
            try:
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        print(f"Received: {msg.data}")
                    elif msg.type == aiohttp.WSMsgType.CLOSED:
                        break
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        break
            except asyncio.TimeoutError:
                print("Timeout: No more messages received.")
            finally:
                await ws.close()
                print("WebSocket connection closed")

if __name__ == "__main__":
    asyncio.run(test_websocket())
