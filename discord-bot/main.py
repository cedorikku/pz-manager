import discord
import os
import requests
import logging
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
BASE_URL = os.getenv('BASE_URL')

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode='w')
intents = discord.Intents.default()

class ServerManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def api_request(self, interaction: discord.Interaction, method: str, endpoint: str):
        """Helper to handle HTTP logic and status codes."""
        url = f"{BASE_URL.rstrip('/')}/{endpoint}"
        
        try:
            if method == "POST":
                response = requests.post(url, timeout=10)
            else:
                response = requests.get(url, timeout=10)

            if response.status_code == 200:
                await interaction.followup.send(f"Succesfully did {endpoint} command to server")
            elif response.status_code == 400:
                await interaction.followup.send(f"Bad request")
            elif response.status_code == 500:
                await interaction.followup.send(f"Something went wrong on the backend side. :p")
            else:
                await interaction.followup.send(f"Unexpected status received: {response.status_code}")

        except requests.exceptions.RequestException as e:
            await interaction.followup.send(f"Connection Error: Host is unalive. \n`{e}`")

    @app_commands.command(name="pz_start", description="Power on the server")
    async def start_server(self, interaction: discord.Interaction):
        await interaction.response.defer() # Gives the API time to respond
        await self.api_request(interaction, "POST", "start")

    @app_commands.command(name="pz_stop", description="Power off the server")
    async def stop_server(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.api_request(interaction, "POST", "stop")

    @app_commands.command(name="pz_status", description="Check server status")
    async def check_server(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.api_request(interaction, "GET", "status")

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
    async def setup_hook(self):
        await self.add_cog(ServerManager(self))
        await self.tree.sync()

bot = MyBot()
bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)