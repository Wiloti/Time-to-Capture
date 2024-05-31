from discord import Embed, app_commands, Interaction
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
import json
import pytz
import os

load_dotenv()
config_location = os.getenv("config_file")
if config_location is not None:
    with open(config_location, "r", encoding="UTF-8") as f:
        config = json.load(f)
    bot_name = config["bot_name"]
    bot_logo_url = config["bot_logo_url"]
    color_setting = config["color_file_path"]
    with open(color_setting, "r") as c:
        colors = json.load(c)
else:
    config = {}

timezone = pytz.timezone("Europe/Paris")
embed_timestamp = datetime.now(timezone)

class help(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(name="help", description="Help command of Time-to-Capture")
    async def help(self, interaction: Interaction) -> None:
        embed = Embed(title="Help Command", description="List of available commands:", color=int(colors["help_color"],16), timestamp=embed_timestamp)
        embed.add_field(name="CTFtime commands", value="All CTFtime commands:", inline=False)
        embed.add_field(name="**/ctftime team** _{top}_ _{year}_", value="List of top teams up to top 25 by year", inline=False)
        embed.add_field(name="**/ctftime event**", value="List of all upcoming events over the next 7 days", inline=False)
        embed.add_field(name="**/ctftime reminder** _{event-name}_", value="Let you set an event for a CTF up to the next 25 events", inline=True)
        embed.set_footer(text=f"{bot_name}", icon_url=f"{bot_logo_url}")
        await interaction.response.send_message(embed=embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(help(client))
