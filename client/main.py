import asyncio
import socketio

# @sio.event
# async def connect():
#     print("Connected to Socket.IO server")
#     await sio.emit("get-player-data")

# @sio.event
# async def disconnect():
#     print("Disconnected from Socket.IO server")

# @sio.event
# async def player_data(data):
#     print(f"Received player data: {data}")

async def main():
    async with socketio.AsyncSimpleClient() as sio:
        await sio.connect('http://localhost:5150/', transports=['websocket'])
        await sio.wait()
        await sio.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
