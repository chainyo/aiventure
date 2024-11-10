# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "aiohttp",
#     "websockets",
# ]
# ///

import asyncio
import json

import aiohttp
import websockets
from websockets.client import WebSocketClientProtocol


class GameWebsocketClient:
    """Client for testing game websocket connections."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the client.

        Args:
            base_url: Base URL of the API server
        """
        self.base_url = base_url
        self.ws_url = base_url.replace("http", "ws")
        self.token: str | None = None
        self.ws: WebSocketClientProtocol | None = None

    async def login(self, email: str, password: str) -> bool:
        """Login to get authentication token.

        Args:
            email: User email
            password: User password

        Returns:
            bool: True if login successful
        """
        async with aiohttp.ClientSession() as session:
            try:
                data = {
                    "username": email,
                    "password": password,
                    "grant_type": "password",
                }

                async with session.post(
                    f"{self.base_url}/api/auth/authenticate",
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.token = data["access_token"]
                        return True
                    return False
            except aiohttp.ClientError as e:
                print(f"Login failed: {e}")
                return False

    async def connect_websocket(self) -> None:
        """Connect to the game websocket."""
        if not self.token:
            raise ValueError("Must login first")

        try:
            self.ws = await websockets.connect(
                f"{self.ws_url}/api/game/ws?token={self.token}",
            )
            print("Connected to websocket")
            await asyncio.sleep(1)  # Small delay to allow server to process connection

        except Exception as e:
            print(f"Failed to connect: {e}")
            raise

    async def send_command(self, command: str, **kwargs) -> None:
        """Send a command to the websocket.

        Args:
            command: Command name
            **kwargs: Additional command parameters
        """
        if not self.ws:
            raise ValueError("Websocket not connected")

        message = {"command": command, **kwargs}
        print(f"Sending: {message}")
        await self.ws.send(json.dumps(message))

    async def receive_message(self) -> dict:
        """Receive a message from the websocket.

        Returns:
            dict: Received message
        """
        if not self.ws:
            raise ValueError("Websocket not connected")

        message = await self.ws.recv()
        return json.loads(message)

    async def close(self) -> None:
        """Close the websocket connection."""
        if self.ws:
            await self.ws.close()


async def main():
    """Main test function."""
    client = GameWebsocketClient()

    # Login
    logged_in = await client.login("test@test.com", "test")
    if not logged_in:
        return

    # Connect to websocket
    await client.connect_websocket()

    # Send a test command
    await client.send_command("test", data="Hello, World!")

    # Receive response
    try:
        response = await client.receive_message()
        print(f"Received: {response}")
    except Exception as e:
        print(f"Error receiving message: {e}")

    # Close connection
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
