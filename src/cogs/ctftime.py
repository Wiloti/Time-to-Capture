from discord import Embed, EntityType, PrivacyLevel, app_commands, Interaction
from src.functions.get_reminder_info import get_reminder_info
from datetime import datetime, timedelta
from discord.ext import commands
from dotenv import load_dotenv
from typing import Literal
import requests
import json
import pytz
import os

load_dotenv()
config_location = os.getenv("config_file")
if config_location is not None:
    with open(config_location, "r", encoding="UTF-8") as f:
        config = json.load(f)
    bot_logo_url = config["bot_logo_url"]
    color_setting = config["color_file_path"]
    ctftime_setting = config["ctftime_file_path"]

    with open(color_setting, "r") as c:
        colors = json.load(c)

    with open(ctftime_setting, "r") as s:
        setting = json.load(s)
    ctftime_logo = setting["logo"]
else:
    config = {}

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"}
timezone = pytz.timezone("Europe/Paris")
embed_timestamp = datetime.now(timezone)
schedule_manager = get_reminder_info()

class CTFtime(commands.GroupCog, group_name="ctftime"):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(name="team", description="List of top teams from 1 to 25 by year")
    @app_commands.describe(top="value between 1 to 25", year="from 2011 to this year")
    async def team(self, interaction: Interaction, top: Literal[1, 5, 10, 15, 20, 25], year: Literal[2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]) -> None:
        req = requests.get(f"https://ctftime.org/api/v1/top/{year}/?limit={top}", headers=headers)
        data = req.json()
        embed = Embed(title=f"Top team in {list(data.keys())[0]}", color=int(colors["ctftime_color"], 16), timestamp=embed_timestamp)
        embed.set_thumbnail(url=ctftime_logo)
        for i in range(0, top):
            team = f"{i + 1}. " + data[str(year)][i]["team_name"]
            points = "**points:** " + str(round(data[str(year)][i]["points"], 2))
            embed.add_field(name=team, value=points, inline=False)
        embed.set_footer(text="Powered by ctftime.org", icon_url=f"{bot_logo_url}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="event", description="Available CTF in the next 7 days")
    async def event(self, interaction: Interaction) -> None:
        start = round(datetime.now().timestamp())
        finish = round((datetime.now() + timedelta(7)).timestamp())
        req = requests.get(f"https://ctftime.org/api/v1/events/?limit=100&start={start}&finish={finish}", headers=headers)
        data = req.json()
        
        if data:
            await interaction.response.send_message("Here are the upcoming CTF events:")
            for event in range(len(data)):
                embed = Embed(title=data[event]["title"], description=data[event]["description"], color=int(colors["ctftime_color"], 16), timestamp=embed_timestamp, url=data[event]["url"])
                embed.set_thumbnail(url=data[event]["logo"])
                embed.add_field(name="Organizers", value=data[event]["organizers"][0]["name"], inline=False)
                embed.add_field(name="Format", value=data[event]["format"], inline=True)
                embed.add_field(name="Weight", value=data[event]["weight"], inline=True)
                embed.add_field(name="Restrictions", value=data[event]["restrictions"], inline=True)
                embed.add_field(name="Duration", value=f"{data[event]['duration']['days']} Day(s) {data[event]['duration']['hours']} Hour(s)", inline=False)
                # formating date properly
                embed.add_field(name="Event start", value=f"{data[event]['start'].replace('T', ' ').split('+', 1)[0]} UTC", inline=True)
                embed.add_field(name="Event end", value=f"{data[event]['finish'].replace('T', ' ').split('+', 1)[0]} UTC", inline=True)
                embed.set_footer(text="Powered by ctftime.org", icon_url=f"{bot_logo_url}")
                await interaction.followup.send(embed=embed)
        else:
            await interaction.response.send_message("No upcoming events found.")

    @app_commands.command(name="reminder", description="Add a Discord event on interested CTF")
    @app_commands.describe(event="Choose one of the next 25 CTF")
    @app_commands.choices(event=[app_commands.Choice(name=schedule_manager[i]["event"], value=schedule_manager[i]["event"]) for i in range(len(schedule_manager))])
    async def reminder(self, interaction: Interaction, event: str) -> None:
        event_details = next((e for e in schedule_manager if e["event"] == event), None)
        if event_details is not None:
            # formating dates iso 8601
            event_details["start_date"] = datetime.fromisoformat(event_details["start_date"])
            event_details["finish_date"] = datetime.fromisoformat(event_details["finish_date"])

            # checking length of description due to discord limitation
            if len(event_details["description"]) > 1000:
                event_details["description"] = f"CTF reminder for {event_details['event']}"

            embed = Embed(title=f"{event_details["event"]}", description="An event has just been created", color=int(colors["ctftime_color"], 16), timestamp=embed_timestamp)
            embed.set_footer(text="Powered by ctftime.org", icon_url=bot_logo_url)
            try:
                # creation of the event
                await interaction.guild.create_scheduled_event(name=event_details["event"],
                                                                description=event_details["description"],
                                                                start_time=event_details["start_date"],
                                                                end_time=event_details["finish_date"],
                                                                privacy_level=PrivacyLevel.guild_only,
                                                                entity_type=EntityType.external,
                                                                location=event_details["url"]
                                                               )
                await interaction.response.send_message(embed=embed)
            except Exception as e:
                print(e)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(CTFtime(client))

