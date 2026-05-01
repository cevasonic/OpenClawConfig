import discord
import asyncio
import os

token = "YOUR_DISCORD_BOT_TOKEN"

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        # Stop after connecting
        await self.close()
        os._exit(0)

intents = discord.Intents.default()
intents.message_content = True
client = Client(intents=intents)

try:
    client.run(token)
except Exception as e:
    print(f"Failed: {e}")
    os._exit(1)
